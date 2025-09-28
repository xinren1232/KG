@echo off
echo ========================================
echo Neo4j Desktop 重启工具
echo ========================================
echo.

echo 步骤 1: 检查当前状态
echo ----------------------------------------
powershell -Command "Get-Process -Name '*Neo4j*' -ErrorAction SilentlyContinue | Select-Object ProcessName, Id"

echo.
echo 步骤 2: 停止Neo4j Desktop进程
echo ----------------------------------------
powershell -Command "Get-Process -Name '*Neo4j*' -ErrorAction SilentlyContinue | Stop-Process -Force"
echo Neo4j Desktop进程已停止

echo.
echo 步骤 3: 等待进程完全停止
echo ----------------------------------------
timeout /t 3 /nobreak

echo.
echo 步骤 4: 启动Neo4j Desktop
echo ----------------------------------------
start "" "%LOCALAPPDATA%\Programs\neo4j-desktop\Neo4j Desktop 2.exe"
echo Neo4j Desktop启动命令已执行

echo.
echo 步骤 5: 等待应用启动
echo ----------------------------------------
timeout /t 5 /nobreak

echo.
echo 步骤 6: 检查启动状态
echo ----------------------------------------
powershell -Command "Get-Process -Name '*Neo4j*' -ErrorAction SilentlyContinue | Select-Object ProcessName, Id"

echo.
echo ========================================
echo 重启完成！
echo ========================================
echo.
echo 请在Neo4j Desktop中手动启动数据库实例：
echo 1. 打开Neo4j Desktop应用
echo 2. 选择或创建一个数据库项目
echo 3. 点击"Start"按钮启动数据库
echo 4. 等待数据库状态变为"Active"
echo.
echo 数据库启动后可访问：
echo - Web界面: http://localhost:7474
echo - Bolt连接: bolt://localhost:7687
echo.
pause
