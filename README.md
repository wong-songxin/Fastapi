# FastAPI OA

一个基于 **FastAPI + Vue** 开发的 OA（办公自动化）管理系统学习项目。

本项目主要用于学习前后端分离项目的开发方式，以及 FastAPI、Vue、JWT、数据库操作等技术。

## 技术栈

### 后端

- Python
- FastAPI
- Tortoise ORM
- MySQL
- JWT
- Pydantic
- python-dotenv

### 前端

- Vue 3
- Vite
- Element Plus
- Axios
- Pinia

## 项目结构

```text id="e3f8qp"
Fastapi/
├── Kong_OA_Backend/          # FastAPI 后端
│   ├── src/                  # 后端核心代码
│   ├── migrations/           # 数据库迁移
│   ├── media/                # 媒体/上传文件
│   ├── logs/                 # 日志文件
│   └── script/               # 项目脚本
│
├── Kong_OA_Front/            # Vue 前端
│   ├── src/                  # 前端核心代码
│   └── public/               # 静态资源
│
├── .gitignore                # Git 忽略文件配置
└── README.md                 # 项目说明文档
```
## 主要功能

目前项目包含以下功能：

- 用户登录
- JWT 身份认证
- 用户管理
- 用户信息修改
- 密码修改
- 密码重置
- 权限相关功能
- 前后端分离
- 数据库操作
- 动态路由

## 环境要求

建议使用以下环境：

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Git

## 后端运行

进入后端目录：

```bash
cd Kong_OA_Backend
```

创建并激活 Python 虚拟环境：

```bash
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

安装依赖：

```bash
pip install -r requirements.txt
```

### 配置环境变量

项目使用 `.env` 保存数据库等敏感配置。

请在后端项目中创建自己的 `.env` 文件，不要将真实密码提交到 GitHub。

例如：

```env
DB_USER=root
DB_PASSWORD=你的数据库密码
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=你的数据库名称
```

然后根据项目实际配置启动后端。

```bash
uvicorn src.main:app --reload
```

后端启动后，可以访问：

```text
http://127.0.0.1:8080
```

FastAPI 接口文档：

```text
http://127.0.0.1:8080/docs
```

## 前端运行

进入前端目录：

```bash
cd Kong_OA_Front
```

安装依赖：

```bash
npm install
```

启动开发服务器：

```bash
npm run dev
```

启动后根据终端提示访问前端地址。

## 配置说明

项目中的数据库密码等敏感信息通过 `.env` 管理。

`.env` 已加入 `.gitignore`，不会提交到 GitHub。

如果第一次运行项目，请根据自己的本地 MySQL 环境配置 `.env`。

## Git 使用

项目使用 Git 进行版本管理。

常用操作：

```bash
git add .
git commit -m "描述本次修改"
git push
```

## 项目说明

这是一个个人学习项目，主要用于学习：

- FastAPI 后端开发
- Vue 前端开发
- 前后端分离
- JWT 登录认证
- 数据库操作
- Git / GitHub 项目管理

项目中的部分设计和代码仍有进一步优化空间。

## License

This project is for learning purposes only.