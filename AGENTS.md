# AGENTS.md

本文档为 AI 编码助手提供本项目的关键信息，帮助理解项目架构、开发规范和注意事项。

---

## 项目概述

**TinyPNG图片压缩工具** 是一个基于 PyQt5 开发的桌面 GUI 应用程序，用于通过 TinyPNG API 批量压缩 PNG/JPG 图片。

**核心功能：**
- 支持拖拽导入文件/文件夹进行批量压缩
- 基于 MD5 的 SQLite 缓存机制，避免重复压缩
- 多 API Key 自动轮换，应对单个 Key 额度耗尽
- 支持 SOCKS5 代理配置
- 覆盖源文件模式（原始文件重命名为 `@source` 后缀备份）
- 清理工具用于批量删除 `@source` 备份文件
- 进度条和日志实时显示

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3 | 编程语言 |
| PyQt5 | GUI 框架 |
| requests | HTTP 请求 |
| PySocks | SOCKS5 代理支持 |
| SQLite3 | 本地缓存数据库 |

---

## 项目结构

```
pyqtTest/
├── main.py              # 程序入口，主窗口、工作线程、辅助窗口
├── TinyPngTool.py       # 业务逻辑层：压缩调度、缓存、API Key 轮换
├── tinyHttp.py          # API 层：TinyPNG API 调用封装
├── monkey_event.py      # 事件系统：同步/异步事件分发器
├── common.py            # 公共常量、事件类型定义、工具函数
├── errors.py            # 错误处理：HTTP 状态码映射到具体异常类
│
├── *.ui 文件             # Qt Designer 设计的 UI 文件（源文件）
│   ├── mainGUI2.ui      # 主窗口界面
│   ├── cleanGUI.ui      # 清理工具界面
│   └── aboutGUI.ui      # 关于窗口界面
│
├── *GUI.py 文件          # 由 .ui 文件自动生成的 Python 代码
│   ├── mainGUI2.py
│   ├── cleanGUI.py
│   └── aboutGUI.py
│
├── res.qrc              # Qt 资源文件定义
├── res_rc.py            # 由 res.qrc 生成的资源文件
├── icon.ico             # 应用程序图标
├── img/                 # 图片资源目录
│
└── config.json          # 应用配置文件（运行时读取）
```

---

## 运行与打包

### 依赖安装

```bash
pip install PyQt5 requests PySocks
```

### 运行应用

```bash
python main.py
```

### 打包为独立可执行文件

```bash
pyinstaller -F -w --icon=icon.ico main.py
```

---

## 配置文件

应用启动时读取 `./config.json`，格式如下：

```json
{
  "keys": ["api_key_1", "api_key_2"],
  "sourcePath": "./source",
  "outputPath": "./compress",
  "proxy": "",
  "override": false
}
```

| 字段 | 说明 |
|------|------|
| `keys` | TinyPNG API Key 列表，支持多个 Key 自动轮换 |
| `sourcePath` | 默认源文件目录 |
| `outputPath` | 默认输出目录 |
| `proxy` | 代理设置（如使用 SOCKS5 代理） |
| `override` | 是否覆盖源文件 |

---

## 架构说明

### 分层结构

```
┌─────────────────────────────────────┐
│           GUI 层 (main.py)          │
│  - MyQMainWindow: 主窗口            │
│  - MyThead: QThread 工作线程        │
│  - CleanView: 清理工具窗口          │
│  - AboutView: 关于窗口              │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│      业务逻辑层 (TinyPngTool.py)     │
│  - 压缩调度                          │
│  - MD5 缓存 (SQLite map.db)         │
│  - 多 API Key 轮换                   │
│  - 覆盖/清理文件逻辑                  │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│       API 层 (tinyHttp.py)          │
│  - TinyPNG API 两步流程              │
│  - POST 上传图片                     │
│  - GET 下载压缩结果                  │
│  - Base64 鉴权                       │
└─────────────────────────────────────┘
```

### 事件系统 (monkey_event.py + common.py)

自定义事件分发器实现组件解耦：

| 事件名称 | 说明 |
|----------|------|
| `EVENT_SHOW_LOG` | 显示日志消息 |
| `EVENT_MAIN_INIT` | 主窗口初始化完成 |
| `EVENT_FILE_COMPLETE` | 单个文件处理完成 |

- `EventCenterSync`: 同步事件中心，用于 UI 更新
- `EventCenterAsync`: 异步事件中心（当前未使用）

### 线程模型

- **主线程**: UI 渲染和交互
- **工作线程**: `MyThead` (QThread 子类) 执行压缩任务
- **通信**: 通过 `Queue` 传递文件列表，通过事件系统更新进度条

### 错误处理 (errors.py)

工厂模式将 HTTP 状态码映射为具体异常类：

| 异常类 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `AccountError` | 401, 429 | API Key 无效或额度耗尽 |
| `ClientError` | 400-499 | 客户端请求错误 |
| `ServerError` | 500-599 | 服务器错误 |
| `ConnectError` | - | 网络连接错误 |

---

## 开发规范

### 文件生成规则（重要）

**`*GUI*.py` 文件和 `res_rc.py` 均为自动生成，不要手动编辑。**

修改 `.ui` 或 `.qrc` 文件后，按以下命令重新生成：

```bash
# 生成 UI 文件
pyuic5 mainGUI2.ui -o mainGUI2.py
pyuic5 cleanGUI.ui -o cleanGUI.py
pyuic5 aboutGUI.ui -o aboutGUI.py

# 生成资源文件
pyrcc5 res.qrc -o res_rc.py
```

### 缓存机制

- 缓存数据库: `map.db` (SQLite)
- 缓存表结构: `md5(id TEXT PRIMARY KEY, md5_value TEXT)`
- 缓存目录: `./cache/`
- 逻辑:
  1. 计算源文件 MD5 作为 key
  2. 查询数据库判断是否已压缩
  3. 已压缩则从缓存复制，未压缩则调用 API
  4. 压缩成功后更新数据库和缓存

### 覆盖源文件逻辑

当 `override` 为 `true` 时：
1. 将源文件重命名为带 `@source` 后缀的备份
2. 将压缩后的文件移动到源文件位置
3. 使用清理工具可批量删除 `@source` 备份文件

---

## 注意事项

### 安全事项

1. **API Key 管理**: `config.json` 中的 API Key 是敏感信息，不要提交到版本控制
2. **代理配置**: SOCKS5 代理默认配置为 `127.0.0.1:1080`，如需修改请编辑 `TinyPngTool.py`

### 已知限制

1. 项目无 `requirements.txt`，依赖需手动安装
2. 无自动化测试套件
3. 无 CI/CD 配置

### 调试技巧

- 查看 `map.db` 可了解缓存状态
- 检查 `./cache/` 目录查看实际缓存文件
- 日志输出同时显示在 GUI 和控制台

---

## 相关链接

- [PyQt5 官方 API 文档](https://www.riverbankcomputing.com/static/Docs/PyQt5/module_index.html)
- [TinyPNG API 文档](https://tinypng.com/developers)
