# 食刻AI - 智能私厨助手

> 基于本地大模型的智能菜谱生成与饮食计划助手，完全离线可用，数据安全隐私保护

## 项目简介

食刻AI是一款面向个人用户的智能私厨助手应用，帮助用户根据现有食材、口味偏好和饮食目标生成个性化菜谱和多日饮食计划。项目采用全本地化部署方案，AI推理在本地完成，用户数据不出本机，兼顾实用性与隐私安全。

**核心功能：**
- 🥬 智能菜谱生成：根据食材、忌口、口味生成2-3道适合的菜谱
- 📅 多日饮食计划：生成连续2天一日三餐完整饮食规划
- 💬 AI对话调整：支持多轮对话，理解用户修改需求
- ❤️ 收藏管理：本地收藏喜爱的菜谱，离线可查
- 📋 历史记录：自动保存生成记录，最多保留50条

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 前端框架 | UniApp + Vue2 | - |
| 后端框架 | FastAPI | 0.115.0 |
| ORM | SQLAlchemy | 2.0.35 |
| 数据库 | SQLite | - |
| 本地大模型 | Ollama + Qwen2.5:7b | - |
| 语言 | Python 3.11+ / JavaScript | - |

## 目录结构

```
食刻AI-智能私厨助手/
├── backend/                          # FastAPI后端服务
│   ├── app/
│   │   ├── api/                      # API路由模块
│   │   │   └── routes.py             # 核心路由定义（chat/favorites/history）
│   │   ├── services/                 # 业务逻辑层
│   │   │   ├── ai_service.py         # AI服务（Ollama调用/Prompt模板）
│   │   │   └── storage_service.py    # 数据存储服务（ORM操作）
│   │   ├── utils/                    # 工具模块
│   │   │   └── prompts.py            # Prompt模板定义
│   │   ├── database.py               # 数据库连接配置
│   │   ├── main.py                   # 后端启动入口
│   │   ├── models.py                 # SQLAlchemy数据模型
│   │   └── schemas.py                # Pydantic请求/响应模型
│   ├── data/                         # SQLite数据库文件
│   ├── .env                          # 环境变量配置
│   └── requirements.txt              # Python依赖清单
├── frontend/                         # UniApp前端应用
│   ├── pages/                        # 页面组件
│   │   ├── index/                    # 首页（食材录入+生成菜谱）
│   │   ├── chat/                     # AI对话页面
│   │   ├── recipe-detail/            # 菜谱详情页
│   │   ├── diet-plan-detail/         # 饮食计划详情页
│   │   ├── favorites/                # 收藏页面
│   │   └── history/                  # 历史记录页面
│   ├── utils/                        # 工具函数
│   │   ├── api.js                    # API请求封装
│   │   └── storage.js                # 本地存储封装
│   ├── static/                       # 静态资源（图标）
│   ├── App.vue                       # 根组件
│   ├── main.js                       # 入口文件
│   ├── manifest.json                 # 应用配置
│   └── pages.json                    # 页面路由配置
└── README.md                         # 项目说明文档
```

## 本地启动步骤

### 前置条件

1. **安装 Ollama**：从 [ollama.com](https://ollama.com) 下载安装
2. **下载 Qwen2.5:7b 模型**：
   ```bash
   ollama pull qwen2.5:7b
   ```
3. **安装 Python 3.11+**：确保已安装并配置环境变量

### 启动流程

#### 步骤1：启动 Ollama 服务
```bash
ollama serve
```
- 默认端口：`11434`
- 验证：访问 `http://localhost:11434/api/tags` 应返回模型列表

#### 步骤2：启动后端服务
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```
- 默认端口：`8000`
- 验证：访问 `http://localhost:8000/` 应返回欢迎消息
- API文档：访问 `http://localhost:8000/docs` 查看 Swagger文档

#### 步骤3：启动前端（H5模式）
**方式一：使用 HBuilderX（推荐）**
1. 打开 HBuilderX
2. 导入项目：文件 → 导入 → 从本地目录导入
3. 选择 `frontend` 目录
4. 运行到浏览器：运行 → 运行到浏览器 → Chrome

**方式二：使用 uni-cli**
```bash
cd frontend
npm install
npm run dev:h5
```
- 默认端口：`5173`
- 代理配置：已在 `manifest.json` 中配置 `/api` 代理到 `http://localhost:8000`

### 运行验证

1. 打开前端首页 `http://localhost:5173`
2. 输入食材（如：番茄、鸡蛋）
3. 选择忌口/口味/目标
4. 点击"生成菜谱"按钮
5. 等待约20-25秒，应看到生成的菜谱列表

## 项目亮点

### 1. 全本地化部署，隐私安全
- AI推理完全在本地完成，不依赖云端API
- 数据不出本机，保护用户隐私
- 断网环境下可正常使用

### 2. 智能菜谱生成与多轮对话
- 基于 Qwen2.5:7b 大模型，理解自然语言需求
- 支持食材、忌口、口味、目标多维度约束
- 多轮对话理解上下文，支持修改调整

### 3. 分层存储设计
- 对话数据后端SQLite持久化，支持多轮上下文
- 收藏/历史前端本地存储，离线可用
- 历史记录自动限流50条，防止存储溢出

### 4. 健壮的错误处理
- JSON格式自动修复，应对模型输出截断
- 双重超时保护（前端3分钟/后端120秒）
- 饮食计划生成失败自动降级回退

### 5. 跨端适配
- UniApp一套代码编译到H5、微信小程序、App
- CSS安全区域适配，支持iPhone全面屏

## 待优化点

1. **性能优化**：本地7B模型推理耗时较长（单菜谱20-25秒），可考虑GPU加速或模型量化优化
2. **并发处理**：当前无并发控制，同时多次请求可能导致性能下降
3. **权限控制**：未实现用户认证，所有接口公开访问
4. **图片生成**：菜谱无配图，可接入AI图像生成
5. **移动端适配**：H5模式在部分移动端浏览器兼容性需优化
6. **错误提示**：部分错误提示不够友好，需细化

## API接口列表

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/chat` | POST | 生成菜谱/饮食计划/多轮对话 |
| `/api/history` | GET | 获取历史记录列表 |
| `/api/history/{id}` | DELETE | 删除历史记录 |
| `/api/favorites` | GET | 获取收藏列表 |
| `/api/favorites` | POST | 添加收藏 |
| `/api/favorites/{id}` | DELETE | 删除收藏 |
| `/api/conversations` | GET | 获取对话列表 |
| `/api/conversations/{id}/messages` | GET | 获取对话消息 |
| `/api/conversations/{id}` | DELETE | 删除对话 |

## 许可证

MIT License