@echo off
chcp 65001 >nul
echo ==========================================
echo   TinyPNG 图片压缩工具 - 打包脚本
echo ==========================================
echo.

:: 检查 pyinstaller 是否安装
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 pyinstaller，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] pyinstaller 安装失败，请手动运行: pip install pyinstaller
        pause
        exit /b 1
    )
    echo [成功] pyinstaller 安装完成
    echo.
)

echo [信息] 开始打包...
echo.

:: 执行打包命令（输出到项目根目录）
pyinstaller -F -w --icon=icon.ico --distpath . main.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [成功] 打包完成！
echo 输出文件: main.exe
echo ==========================================
pause
