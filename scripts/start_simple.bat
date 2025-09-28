@echo off
echo ========================================
echo 启动后端服务
echo ========================================
echo.

echo 步骤 1: 启动Neo4j数据库
echo ----------------------------------------
call scripts\neo4j_manager.bat start

echo.
echo 步骤 2: 等待Neo4j启动 (30秒)
echo ----------------------------------------
timeout /t 30 /nobreak

echo.
echo 步骤 3: 检查Python环境
echo ----------------------------------------
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装
    pause
    exit /b 1
)

echo.
echo 步骤 4: 启动API服务
echo ----------------------------------------
echo 进入API目录...
cd services\api

echo 安装依赖...
pip install -r requirements.txt

echo 启动API服务...
echo 服务地址: http://localhost:8000
echo 按 Ctrl+C 停止服务
echo.

python main.py

echo.
echo 服务已停止
cd ..\..
pause
