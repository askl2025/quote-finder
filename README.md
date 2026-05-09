# Quote Finder 名句匹配

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

输入句子或关键词，从海量名句库中找到最契合的名句。

## 功能特点

- **语义匹配**: 基于深度学习模型（m3e-base），理解句子含义而非简单关键词匹配
- **同义词匹配**: 支持现代语句到古诗词意境的映射
- **海量名句**: 包含唐诗宋词、元曲、诗经、人民日报金句等13,500+条数据
- **多种输入**: 支持完整句子、关键词、情感描述等多种输入方式
- **跨平台**: 支持Windows桌面端和网页端

## 使用示例

| 输入 | 匹配结果 |
|------|----------|
| 思念家乡 | 举头望明月，低头思故乡 |
| 在消沉时也不要放弃自己 | 长风破浪会有时，直挂云帆济沧海 |
| 花 雨天 灯火 | 蓦然回首，那人却在，灯火阑珊处 |
| 心 迷茫 希望 | 山重水复疑无路，柳暗花明又一村 |

## 快速开始

### 在线体验

访问 [名句匹配在线版](https://askl2025.github.io/quote-finder/) 体验。

### 下载 EXE

从 [Releases](https://github.com/askl2025/quote-finder/releases) 下载 Windows 版本。

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/askl2025/quote-finder.git
cd quote-finder

# 安装客户端依赖
cd client
pip install -r requirements.txt

# 运行客户端
python main_tkinter.py
```

## 项目结构

```
quote-finder/
├── client/                          # tkinter客户端
│   ├── main_tkinter.py              # 应用入口
│   ├── api/client.py                # API调用封装
│   └── requirements.txt
│
├── server/                          # 后端服务（HF Spaces）
│   ├── app.py                       # FastAPI应用
│   ├── core/
│   │   ├── matcher.py               # 匹配逻辑（语义+关键词+同义词）
│   │   └── embedding.py             # 模型封装
│   ├── data/
│   │   ├── quotes.json              # 名句数据库（13,500+条）
│   │   ├── synonym_dict.json        # 同义词词典
│   │   └── phrase_dict.json         # 短语词典
│   └── requirements.txt
│
├── docs/                            # GitHub Pages
│   └── index.html                   # 网页版前端
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
| 客户端 | tkinter (Python) |
| 网页前端 | HTML/CSS/JavaScript |
| 后端 | FastAPI |
| 嵌入模型 | moka-ai/m3e-base |
| 向量检索 | FAISS |
| 部署 | HuggingFace Spaces |

## 数据来源

| 来源 | 条数 | 说明 |
|------|------|------|
| chinese-poetry | ~6,000 | 唐诗宋词元曲诗经 |
| hitokoto | ~4,600 | 一言社区（文学/诗词/哲学/动画/影视）|
| Wikiquote | ~1,900 | 名人名言 |
| 人民日报 | ~750 | 日报金句 |
| 米人语录 | ~300 | 经典/爱情/伤感语录 |

## 隐私说明

用户输入的查询内容会发送至服务器进行语义匹配，不会被存储或用于任何其他用途。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

- [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base) - 嵌入模型
- [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) - 古诗词数据
- [hitokoto-osc/sentences-bundle](https://github.com/hitokoto-osc/sentences-bundle) - 一言数据
- [FAISS](https://github.com/facebookresearch/faiss) - 向量检索
