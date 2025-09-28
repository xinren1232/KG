@echo off
chcp 65001
echo 🚀 启动API服务
echo ==================

cd /d "%~dp0"
echo 当前目录: %CD%

echo.
echo 📋 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 📋 检查依赖包...
python -c "import fastapi, uvicorn, neo4j; print('✅ 依赖包正常')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ 缺少依赖包，正在安装...
    pip install fastapi uvicorn neo4j
)

echo.
echo 🚀 启动API服务...
echo 访问地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务
echo ==================

python api/main.py

pause
