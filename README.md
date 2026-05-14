# PassForge

密码学安全随机密码生成器，支持 Web UI 一键生成。

## 功能

### 密码类型

- **标准密码** - 自定义长度（4-128位）、字符集（大小写/数字/特殊符号）
- **短语密码** - Diceware 风格，好记又安全，适合 Wi-Fi/主密码
- **JWT 密钥** - HS256/HS512 标准格式，支持 Base64url/Hex/PEM 三种格式

### 核心特性

- 使用 `crypto.getRandomValues()` 前端生成，密码不出现在网络传输中
- 密码策略模板（标准/仅字母/纯数字 PIN）
- 排除易混淆字符（0O1lI）
- 实时强度可视化（熵值 + 进度条）
- 批量生成（最多 500 个）
- 一键复制全部 / 导出 TXT
- 暗色主题 Web UI
- Windows 系统托盘图标（右键打开/退出）

## 快速开始

### 环境要求

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 安装

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install flask pystray pillow
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

双击 `build.bat`，完成后在 `dist/PassForge.exe`。

独立可执行文件，无需 Python 环境。

## 项目结构

```
PassForge/
├── generator.py              # 后端生成逻辑（fallback）
├── app.py                    # Flask Web 服务 + 系统托盘
├── start.bat                 # 双击启动
├── build.bat                 # 打包 exe
├── pyproject.toml            # 项目配置
├── logo/
│   └── passforge.png         # 应用图标（托盘 + exe）
├── templates/
│   └── index.html            # Web UI
└── static/
    ├── password-generator.js # 前端密码生成模块
    ├── wordlist.js           # 短语密码词表（约2000词）
    └── style.css             # 样式
```

## 许可证

[MIT License](LICENSE)
