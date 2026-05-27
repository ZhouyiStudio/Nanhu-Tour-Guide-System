@echo off
chcp 65001 >nul
title 南湖导游系统 — 安装依赖库

echo ============================================
echo   嘉兴南湖导游系统 — 依赖库安装
echo   使用清华镜像源加速下载
echo ============================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo        下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] 升级 pip 到最新版本...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

echo [2/2] 安装项目依赖库...
echo.
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

if %errorlevel% equ 0 (
    echo ============================================
    echo   ✅ 全部依赖安装成功！
    echo.
    echo   运行控制台版：python nanhu_guide.py
    echo   运行 GUI 版：  python nhguide.py
    echo ============================================
) else (
    echo [错误] 部分依赖安装失败，请检查网络连接后重试。
)

echo.
pause
