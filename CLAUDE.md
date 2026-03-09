# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 语言规则

**始终使用中文**与用户交流，所有文档、注释、提交信息也应使用中文编写。

## 项目简介

基于 PyQt5 的桌面 GUI 工具，通过 TinyPNG API 批量压缩 PNG/JPG 图片。支持拖拽导入、进度条显示、基于 MD5 的 SQLite 缓存、覆盖源文件模式，以及清理源文件备份的清理工具。

## 运行与打包

```bash
# 运行应用
python main.py

# 打包为独立可执行文件
pyinstaller -F -w --icon=icon.ico main.py
```

## 依赖安装

项目无 requirements.txt，需手动安装：

```bash
pip install PyQt5 requests PySocks
```

## 重新生成 UI 和资源文件

`*GUI*.py` 文件和 `res_rc.py` 均为自动生成，**不要手动编辑**。修改 `.ui` 或 `.qrc` 文件后需重新生成：

```bash
pyuic5 mainGUI2.ui -o mainGUI2.py
pyuic5 cleanGUI.ui -o cleanGUI.py
pyuic5 aboutGUI.ui -o aboutGUI.py
pyrcc5 res.qrc -o res_rc.py
```

## 配置文件

应用启动时读取 `./config.json`：

```json
{
  "keys": ["api_key_1", "api_key_2"],
  "sourcePath": "./source",
  "outputPath": "./compress",
  "proxy": "",
  "override": false
}
```

## 架构说明

**分层结构：**

- **GUI 层**（`main.py`）：主窗口，支持拖拽、进度条、日志显示。`MyThead`（QThread 子类）在后台执行压缩任务。`CleanView` 和 `AboutView` 为辅助窗口。
- **业务逻辑层**（`TinyPngTool.py`）：压缩调度、MD5 缓存（SQLite `map.db`）、多 API Key 轮换、覆盖/清理文件。
- **API 层**（`tinyHttp.py`）：调用 TinyPNG API 的两步流程——POST 上传，GET 下载压缩结果，Base64 鉴权。
- **事件系统**（`monkey_event.py`、`common.py`）：自定义同步/异步事件分发器（`EventCenterSync`、`EventCenterAsync`），各组件通过事件（`EVENT_SHOW_LOG`、`EVENT_MAIN_INIT`、`EVENT_FILE_COMPLETE`）解耦通信。
- **错误处理**（`errors.py`）：工厂模式，将 HTTP 状态码映射为具体异常类（`AccountError`、`ClientError`、`ServerError`、`ConnectError`）。

**线程模型：** UI 运行在主线程，压缩任务运行在 `MyThead`（QThread）中，通过 `Queue` 传递文件列表。进度条更新通过事件系统发送，避免跨线程直接操作 Qt 控件。

**覆盖功能：** 开启后，原始文件会被重命名为带 `@source` 后缀的备份，再用压缩后的文件替换。清理工具用于批量删除这些 `@source` 备份文件。
