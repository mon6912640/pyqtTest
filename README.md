# TinyPNG 图片压缩工具

基于 PyQt5 开发的桌面 GUI 应用程序，通过 TinyPNG API 批量压缩 PNG/JPG 图片，支持拖拽操作、缓存机制和智能备份。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能特性

- 🖱️ **拖拽操作** - 支持拖拽文件/文件夹到界面进行批量压缩
- 💾 **智能缓存** - 基于 MD5 的 SQLite 缓存机制，避免重复压缩相同图片
- 🔑 **多 Key 轮换** - 支持配置多个 API Key，自动轮换应对单个 Key 额度耗尽
- 🌐 **代理支持** - 支持 SOCKS5 代理配置
- 📁 **覆盖模式** - 可选覆盖源文件，支持生成 `@source` 备份
- 🧹 **清理工具** - 内置清理工具，一键删除所有 `@source` 备份文件
- 📊 **进度显示** - 实时显示压缩进度和处理日志

## 📸 界面预览

```
┌─────────────────────────────────────────┐
│  图片压缩工具                    [关于]  │
├─────────────────────────────────────────┤
│                                         │
│  [日志显示区域]                          │
│  C:\pics\photo.jpg √ -45%               │
│  C:\pics\banner.png 从缓存取出            │
│                                         │
├─────────────────────────────────────────┤
│  [==========>        ] 50/100           │
├─────────────────────────────────────────┤
│  [清理工具]  [✓]覆盖原文件  [✓]备份原文件 │
└─────────────────────────────────────────┘
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows / macOS / Linux

### 安装依赖

```bash
pip install PyQt5 requests PySocks
```

### 配置 API Key

1. 访问 [TinyPNG Developers](https://tinypng.com/developers) 申请免费 API Key
2. 编辑 `config.json` 文件，填入你的 Key：

```json
{
  "keys": ["你的_api_key_here"],
  "sourcePath": "./source",
  "outputPath": "./compress",
  "proxy": "",
  "override": false,
  "backup": false
}
```

> 💡 支持配置多个 Key，格式：`"keys": ["key1", "key2", "key3"]`

### 运行程序

```bash
python main.py
```

## 📖 使用说明

### 基本操作

1. **拖拽压缩** - 将图片或文件夹拖拽到程序窗口，自动开始压缩
2. **查看进度** - 底部进度条显示当前处理进度
3. **查看日志** - 文本区域显示详细处理信息（缓存命中、压缩率等）

### 模式说明

| 覆盖原文件 | 备份原文件 | 行为说明 |
|:---------:|:---------:|---------|
| ❌ | - | 压缩结果保存到 `./compress`，原文件不变 |
| ✅ | ❌ | 直接覆盖原文件，**不保留备份** |
| ✅ | ✅ | 覆盖原文件，原文件重命名为 `xxx@source.jpg` 备份 |

### 清理工具

点击【清理工具】按钮，拖拽包含 `@source` 备份文件的文件夹，一键删除所有备份。

## 📦 打包为 EXE

### 方法一：使用提供的脚本

```bash
compile.cmd
```

### 方法二：手动打包

```bash
pip install pyinstaller
pyinstaller -F -w --icon=icon.ico --distpath . main.py
```

打包完成后，项目根目录会生成 `main.exe` 文件。

## ⚙️ 配置文件说明

`config.json` 各字段含义：

| 字段 | 类型 | 说明 |
|-----|------|------|
| `keys` | 数组 | TinyPNG API Key 列表，支持多个 |
| `sourcePath` | 字符串 | 默认源文件目录 |
| `outputPath` | 字符串 | 默认输出目录（非覆盖模式下）|
| `proxy` | 字符串 | SOCKS5 代理地址，如 `127.0.0.1:1080` |
| `override` | 布尔 | 是否覆盖原文件 |
| `backup` | 布尔 | 覆盖时是否生成 `@source` 备份 |

## 🛠️ 技术栈

- **Python 3** - 编程语言
- **PyQt5** - GUI 框架
- **requests** - HTTP 请求
- **PySocks** - SOCKS5 代理支持
- **SQLite3** - 本地缓存数据库

## 📁 项目结构

```
pyqtTest/
├── main.py              # 程序入口，主窗口
├── TinyPngTool.py       # 业务逻辑：压缩、缓存、API 轮换
├── tinyHttp.py          # TinyPNG API 调用封装
├── monkey_event.py      # 事件系统
├── common.py            # 公共常量、工具函数
├── errors.py            # 错误处理
├── mainGUI2.py          # 主窗口 UI（自动生成）
├── cleanGUI.py          # 清理工具 UI
├── aboutGUI.py          # 关于窗口 UI
├── res_rc.py            # 资源文件
├── icon.ico             # 应用图标
├── config.json          # 配置文件
├── compile.cmd          # 打包脚本
└── README.md            # 本文件
```

## 📝 注意事项

1. **API 额度** - TinyPNG 免费账户每月 500 张图片额度，超出需要等待下月或购买付费套餐
2. **缓存机制** - 程序会在 `./cache/` 目录保存压缩后的图片缓存，删除后相同图片需要重新压缩
3. **备份文件** - 开启备份后生成的 `@source` 文件可以用清理工具批量删除
4. **配置文件** - `config.json` 中的 API Key 是敏感信息，请勿提交到公共仓库

## 🔧 常见问题

**Q: 压缩失败提示 "key 值无效"？**
> A: 你的 API Key 额度已用完，请等待下月重置或申请新的 Key。

**Q: 如何添加多个 API Key？**
> A: 在 `config.json` 中 `keys` 数组添加多个 Key，程序会自动轮换使用。

**Q: 压缩过的图片还能再压缩吗？**
> A: 程序会通过 MD5 缓存判断，已压缩过的图片会直接从缓存复制，不会重复调用 API。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [TinyPNG](https://tinypng.com/) - 提供图片压缩 API
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI 框架

---

⭐ 如果这个项目对你有帮助，欢迎 Star 支持！
