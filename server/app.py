import asyncio
import aiohttp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from core.matcher import PoetryMatcher

app = FastAPI(
    title="名句匹配API",
    version="1.0.0",
    description="输入句子或关键词，从海量名句库中找到最契合的名句"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

matcher = None

class MatchRequest(BaseModel):
    query: str
    top_k: int = 5

class QuoteResponse(BaseModel):
    id: str
    text: str
    author: Optional[str] = None
    source: Optional[str] = None
    dynasty: Optional[str] = None
    type: Optional[str] = None
    score: float
    semantic_score: Optional[float] = None
    keyword_score: Optional[float] = None

class MatchResponse(BaseModel):
    query: str
    results: List[QuoteResponse]

async def self_ping():
    await asyncio.sleep(60)
    port = os.getenv("PORT", "7860")
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{port}/health"):
                    pass
        except:
            pass
        await asyncio.sleep(240)

@app.on_event("startup")
async def startup_event():
    global matcher
    print("Loading matcher...")
    matcher = PoetryMatcher()
    print(f"Matcher loaded with {matcher.get_quotes_count()} quotes")
    asyncio.create_task(self_ping())

@app.get("/")
async def root():
    return {
        "name": "quote-finder",
        "version": "1.0.0",
        "description": "名句匹配API",
        "endpoints": {
            "POST /match": "匹配名句",
            "GET /health": "健康检查"
        }
    }

@app.post("/match", response_model=MatchResponse)
async def match_quotes(request: MatchRequest):
    if matcher is None:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    try:
        results = matcher.match(request.query, request.top_k)
        return MatchResponse(
            query=request.query,
            results=[QuoteResponse(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "quotes_count": matcher.get_quotes_count() if matcher else 0,
        "model": "BAAI/bge-small-zh-v1.5"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
