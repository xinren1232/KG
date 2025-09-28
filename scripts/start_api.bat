@echo off
REM 快速启动API服务脚本

echo 🚀 启动知识图谱API服务...
echo.

REM 检查是否在正确目录
if not exist "services\api\main.py" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    echo 当前目录: %CD%
    pause
    exit /b 1
)

REM 进入API目录
cd services\api

echo 📍 当前目录: %CD%
echo 🔍 检查文件...

if exist "main.py" (
    echo ✅ 找到 main.py
) else (
    echo ❌ 未找到 main.py
    pause
    exit /b 1
)

if exist "requirements.txt" (
    echo ✅ 找到 requirements.txt
) else (
    echo ❌ 未找到 requirements.txt
    pause
    exit /b 1
)

echo.
echo 🐍 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    echo 请安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo 📦 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 🌐 启动API服务...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务
echo.

REM 尝试启动服务
python main.py

REM 如果失败，尝试uvicorn
if %errorlevel% neq 0 (
    echo.
    echo 🔄 尝试使用uvicorn启动...
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
)

echo.
echo 服务已停止
cd ..\..
pause
