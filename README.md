# 面向企业的 RAG 智库系统

**Enterprise RAG Knowledge System** —— 基于 RAG (Retrieval-Augmented Generation) 的企业级智能文档问答平台，支持多知识库管理、PDF 解析、向量检索、Agent 对话、自动化质量评测。

## 技术栈

| 层次 | 技术 |
|------|------|
| **后端框架** | FastAPI + Uvicorn |
| **前端** | Vue 3 + Element Plus + Vite |
| **LLM & Embedding** | DashScope (Qwen-Max) / OpenAI 兼容 API |
| **向量数据库** | Milvus |
| **关系数据库** | SQLite (SQLAlchemy ORM) |
| **异步任务** | Celery + Redis |
| **对象存储** | MinIO |
| **Agent 框架** | LangGraph + LangChain |
| **文档解析** | PyMuPDF / pdfplumber / Unstructured |
| **OCR** | PaddleOCR |
| **评测** | RAGAS + 自定义 LLM 评测 |

## 项目结构

```
ragPdfSystem/
├── config/                  # 配置管理
│   ├── settings.py          # Pydantic Settings
│   ├── database.py          # SQLAlchemy 引擎
│   └── embedding.py         # Embedding 模型配置
├── src/
│   ├── main.py              # FastAPI 入口
│   ├── api/routers/         # API 路由
│   │   ├── auth.py          # JWT 认证
│   │   ├── knowledge_base.py # 知识库管理
│   │   ├── chat.py          # RAG 对话
│   │   ├── evaluation.py    # 质量评测
│   │   ├── agent.py         # AI Agent
│   │   ├── assistant.py     # 助手管理
│   │   ├── monitor.py       # 监控面板
│   │   ├── storage.py       # MinIO 文件管理
│   │   ├── loadfile.py      # 文件上传 (Legacy)
│   │   └── health.py        # 健康检查
│   ├── database/            # 数据持久层
│   │   ├── models.py        # SQLAlchemy 模型定义
│   │   ├── sql_session.py   # Session 管理
│   │   └── vector_db.py     # Milvus 客户端
│   ├── embedding/           # Embedding 实现
│   │   ├── base.py
│   │   └── dashscope_embedding.py
│   ├── processors/          # 文档处理
│   │   ├── pdf_parser.py    # PDF 解析
│   │   ├── text_chunker.py  # 文本切片
│   │   ├── text_cleaner.py  # 文本清洗
│   │   └── metadata_extractor.py
│   ├── retrieval/           # 检索模块
│   │   ├── vector_retriever.py
│   │   └── reranker.py      # 重排序
│   ├── services/            # 业务逻辑
│   │   ├── rag_service.py   # RAG 问答
│   │   ├── qa_generator.py  # LLM 自动生成 QA
│   │   ├── evaluator.py     # 评测引擎
│   │   └── memory_service.py # 对话记忆
│   ├── worker/              # Celery 异步任务
│   │   ├── celery_app.py
│   │   └── tasks.py         # 文档处理任务
│   └── utils/               # 工具模块
├── frontend/                # Vue 3 前端
│   └── src/views/           # 页面组件
├── scripts/                 # 脚本
│   └── evaluate_rag.py      # RAG 评测脚本
├── docs/                    # 文档
│   └── api.md               # API 接口文档
├── data/                    # 数据目录
├── requirements.txt
└── .env.example
```

## 快速开始

### 环境要求

- Python >= 3.10
- Node.js >= 18
- Milvus (Docker)
- Redis (Docker)

### 1. 安装依赖

```bash
# Python 后端
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 前端
cd frontend && npm install
```

### 2. 启动基础设施

```bash
# 启动 Milvus
docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:latest

# 启动 Redis
docker run -d --name redis -p 6379:6379 redis:latest
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DashScope API Key 等配置
```

### 4. 启动服务

```bash
# 后端
python src/main.py

# Celery Worker
celery -A src.worker.celery_app worker --loglevel=info

# 前端
cd frontend && npm run dev
```

访问 `http://localhost:8000/docs` 查看 API 文档。

## 核心功能

### 多知识库管理
- 创建/删除知识库，支持多知识库隔离
- 上传 PDF 文档自动解析、切片、入库
- 支持查看文档处理状态

### RAG 对话
- 基于 Milvus 向量检索 + LLM 生成回答
- 多轮对话记忆 (Memory System)
- 自动保存对话历史
- 支持多知识库选择

### LLM 自动生成 QA
- 从文档中自动提取问答对
- 支持批量生成，可人工审核

### 质量评测
- 基于 RAGAS 和自定义 LLM 指标
- 评测维度：Faithfulness、Relevancy、Context Precision
- 自动生成 Markdown 评测报告

### AI Agent
- LangGraph 驱动的 Agent 对话
- 支持工具调用和反思链

## API 概览

| 模块 | 端点 | 说明 |
|------|------|------|
| Auth | `/api/v1/auth/*` | 注册、登录、Token |
| Knowledge Base | `/api/v1/knowledge-bases/*` | CRUD + 文件上传 |
| Chat | `/api/v1/chat/*` | RAG 问答 + 会话管理 |
| Evaluation | `/api/v1/evaluations/*` | 启动评测 + 报告 |
| Agent | `/api/v1/agents/*` | Agent 对话 |
| Monitor | `/api/v1/monitor/*` | 系统监控 |
| Storage | `/api/v1/storage/*` | MinIO 文件管理 |

详细 API 文档见 [docs/api.md](docs/api.md)
