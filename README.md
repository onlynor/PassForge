# PassForge

密码学安全随机密码生成器，支持 Web UI 一键生成。

## 功能

- 支持 8 / 16 / 32 / 64 位密码长度
- 使用 `secrets` 模块，密码学安全 CSPRNG
- 强制包含大小写字母、数字、特殊字符
- 密码强度评估（熵值计算）
- 暗色主题 Web UI，点击即复制
- 批量生成（最多 50 个）

## 快速开始

### 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 安装

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install flask
```

### 启动

```bash
# 命令行启动
uv run python app.py

# 或双击
start.bat
```

浏览器自动打开 `http://127.0.0.1:18080`。

## 打包 exe

双击 `build.bat`，完成后在 `dist/WeakPass.exe`。

独立可执行文件，无需 Python 环境。

## 项目结构

```
PassForge/
├── generator.py      # 核心生成逻辑
├── app.py            # Flask Web 服务
├── start.bat         # 双击启动
├── build.bat         # 打包 exe
├── pyproject.toml    # 项目配置
├── templates/
│   └── index.html    # Web UI
└── static/
    └── style.css     # 样式
```

## 许可证

[MIT License](LICENSE)
