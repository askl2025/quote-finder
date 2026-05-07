# Quote Finder 名句匹配

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

输入句子或关键词，从海量名句库中找到最契合的名句。

## 功能特点

- **语义匹配**: 基于深度学习模型（BGE-small-zh），理解句子含义而非简单关键词匹配
- **海量名句**: 包含唐诗宋词、成语俗语、经典名句等10万+条数据
- **多种输入**: 支持完整句子、关键词、情感描述等多种输入方式
- **跨平台**: 支持Windows桌面端和Android移动端

## 使用示例

| 输入 | 匹配结果 |
|------|----------|
| 思念家乡 | 举头望明月，低头思故乡 |
| 在消沉时也不要放弃自己 | 长风破浪会有时，直挂云帆济沧海 |
| 花 雨天 灯火 | 蓦然回首，那人却在，灯火阑珊处 |
| 心 迷茫 希望 | 山重水复疑无路，柳暗花明又一村 |

## 快速开始

### 在线体验

访问 [名句匹配在线版](https://your-username-quote-finder.hf.space) 体验。

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/your-username/quote-finder.git
cd quote-finder

# 安装客户端依赖
cd client
pip install -r requirements.txt

# 运行客户端
python main.py
```

## 项目结构

```
quote-finder/
├── client/                          # Kivy客户端
│   ├── main.py                      # 应用入口
│   ├── api/client.py                # API调用封装
│   ├── buildozer.spec               # Android打包配置
│   └── requirements.txt
│
├── server/                          # 后端服务
│   ├── app.py                       # FastAPI应用
│   ├── core/
│   │   ├── matcher.py               # 匹配逻辑
│   │   └── embedding.py             # 模型封装
│   ├── scripts/
│   │   ├── collect_data.py          # 数据收集
│   │   └── build_index.py           # 构建索引
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests/                           # 测试文件
│   ├── test_cases.json
│   └── test_api.py
│
├── .github/workflows/               # GitHub Actions
│   ├── release.yml                  # 自动打包发布
│   └── keep-alive.yml               # 防止服务休眠
│
├── LICENSE                          # MIT协议
└── README.md
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 客户端 | Kivy (Python) |
| 后端 | FastAPI |
| 嵌入模型 | BAAI/bge-small-zh-v1.5 |
| 向量检索 | FAISS |
| 数据库 | SQLite |
| 部署 | HuggingFace Spaces |

## 开发指南

### 1. 收集数据

```bash
cd server
pip install -r requirements.txt

# 收集名句数据
python scripts/collect_data.py

# 构建FAISS索引
python scripts/build_index.py
```

### 2. 启动后端服务

```bash
cd server
uvicorn app:app --reload --port 7860
```

### 3. 运行测试

```bash
python tests/test_api.py http://localhost:7860
```

### 4. 打包Android APK

```bash
cd client
buildozer android debug
```

### 5. 打包Windows EXE

```bash
cd client
pip install pyinstaller
pyinstaller --onefile --windowed --name quote-finder main.py
```

## 部署指南

### HuggingFace Spaces 部署

1. 注册 [HuggingFace](https://huggingface.co) 账号
2. 创建新的 Space，选择 Docker SDK
3. 将 `server/` 目录内容推送到 Space
4. 等待构建完成

### 防止休眠

Space 在不活跃时会休眠。使用以下方式保持活跃：

- **UptimeRobot**: 注册 [UptimeRobot](https://uptimerobot.com)，添加监控 `https://your-space.hf.space/health`
- **GitHub Actions**: 项目已配置 `keep-alive.yml`，每4分钟自动ping

## 隐私说明

用户输入的查询内容会发送至服务器进行语义匹配，不会被存储或用于任何其他用途。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

- [BAAI/bge-small-zh-v1.5](https://huggingface.co/BAAI/bge-small-zh-v1.5) - 嵌入模型
- [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) - 古诗词数据
- [chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua) - 成语数据
- [FAISS](https://github.com/facebookresearch/faiss) - 向量检索
- [Kivy](https://kivy.org) - 跨平台UI框架
