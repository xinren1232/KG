@echo off
REM Neo4j 数据库管理脚本 (Windows)
REM 用于启动、停止、重启Neo4j数据库

setlocal enabledelayedexpansion

REM 设置Neo4j可能的安装路径
set NEO4J_PATHS=^
"C:\neo4j\bin\neo4j.bat" ^
"C:\Program Files\Neo4j CE 4.4.0\bin\neo4j.bat" ^
"C:\Program Files\Neo4j CE 5.0.0\bin\neo4j.bat" ^
"C:\Program Files (x86)\Neo4j CE 4.4.0\bin\neo4j.bat" ^
"%NEO4J_HOME%\bin\neo4j.bat"

REM 检查参数
if "%1"=="" (
    echo Neo4j 管理脚本
    echo 用法:
    echo   neo4j_manager.bat status   - 检查状态
    echo   neo4j_manager.bat start    - 启动Neo4j
    echo   neo4j_manager.bat stop     - 停止Neo4j
    echo   neo4j_manager.bat restart  - 重启Neo4j
    echo   neo4j_manager.bat info     - 显示信息
    goto :end
)

set COMMAND=%1

REM 查找Neo4j可执行文件
set NEO4J_CMD=
for %%p in (%NEO4J_PATHS%) do (
    if exist %%p (
        set NEO4J_CMD=%%p
        goto :found
    )
)

REM 尝试直接使用neo4j命令（如果在PATH中）
where neo4j >nul 2>&1
if %errorlevel%==0 (
    set NEO4J_CMD=neo4j
    goto :found
)

echo ❌ 未找到Neo4j安装，请检查以下路径：
for %%p in (%NEO4J_PATHS%) do (
    echo   %%p
)
echo 或确保neo4j命令在PATH环境变量中
goto :end

:found
echo ✅ 找到Neo4j: %NEO4J_CMD%

REM 执行相应命令
if /i "%COMMAND%"=="status" goto :status
if /i "%COMMAND%"=="start" goto :start
if /i "%COMMAND%"=="stop" goto :stop
if /i "%COMMAND%"=="restart" goto :restart
if /i "%COMMAND%"=="info" goto :info

echo ❌ 未知命令: %COMMAND%
goto :end

:status
echo 🔍 检查Neo4j状态...
curl -s http://localhost:7474/db/data/ >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Neo4j正在运行
    echo 🌐 Web界面: http://localhost:7474
    echo 🔌 Bolt连接: bolt://localhost:7687
) else (
    echo ❌ Neo4j未运行或无法连接
)
goto :end

:start
echo 🚀 启动Neo4j...
%NEO4J_CMD% start
if %errorlevel%==0 (
    echo ✅ Neo4j启动命令执行成功
    echo ⏳ 等待服务启动...
    timeout /t 10 /nobreak >nul
    goto :status
) else (
    echo ❌ Neo4j启动失败
)
goto :end

:stop
echo 🛑 停止Neo4j...
%NEO4J_CMD% stop
if %errorlevel%==0 (
    echo ✅ Neo4j停止成功
) else (
    echo ❌ Neo4j停止失败
)
goto :end

:restart
echo 🔄 重启Neo4j...
echo 🛑 正在停止...
%NEO4J_CMD% stop
timeout /t 5 /nobreak >nul
echo 🚀 正在启动...
%NEO4J_CMD% start
if %errorlevel%==0 (
    echo ✅ Neo4j重启命令执行成功
    echo ⏳ 等待服务启动...
    timeout /t 10 /nobreak >nul
    goto :status
) else (
    echo ❌ Neo4j重启失败
)
goto :end

:info
echo ℹ️ Neo4j信息:
echo   HTTP URL: http://localhost:7474
echo   Bolt URL: bolt://localhost:7687
echo   可执行文件: %NEO4J_CMD%
echo   操作系统: Windows
echo.
goto :status

:end
pause
