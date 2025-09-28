@echo off
REM 后端服务启动脚本
REM 按正确顺序启动所有后端服务

echo ========================================
echo 🚀 启动后端服务
echo ========================================
echo.

REM 设置颜色
set GREEN=[92m
set RED=[91m
set YELLOW=[93m
set BLUE=[94m
set NC=[0m

echo %BLUE%步骤 1: 检查Neo4j状态%NC%
echo ----------------------------------------

REM 检查Neo4j是否已经运行
echo 检查Neo4j状态...

REM 启动Neo4j
echo.
echo %YELLOW%正在启动Neo4j数据库...%NC%
call scripts\neo4j_manager.bat start

echo.
echo %BLUE%步骤 2: 等待Neo4j完全启动%NC%
echo ----------------------------------------
echo %YELLOW%等待Neo4j启动完成 (最多60秒)...%NC%

REM 等待Neo4j启动
set /a counter=0
:wait_neo4j
set /a counter+=1
if %counter% gtr 20 (
    echo %RED%❌ Neo4j启动超时%NC%
    goto :error
)

curl -s http://localhost:7474 >nul 2>&1
if %errorlevel%==0 (
    echo %GREEN%✅ Neo4j启动成功%NC%
    goto :neo4j_ready
)

echo %YELLOW%等待中... (%counter%/20)%NC%
timeout /t 3 /nobreak >nul
goto :wait_neo4j

:neo4j_ready
echo.
echo %BLUE%步骤 3: 检查Python环境%NC%
echo ----------------------------------------

REM 检查Python
python --version >nul 2>&1
if %errorlevel%==0 (
    echo %GREEN%✅ Python环境可用%NC%
    python --version
) else (
    echo %RED%❌ Python未安装或不在PATH中%NC%
    echo 请安装Python 3.8+并添加到PATH
    goto :error
)

echo.
echo %BLUE%步骤 4: 检查API服务依赖%NC%
echo ----------------------------------------

REM 检查是否在正确目录
if not exist "services\api\main.py" (
    echo %RED%❌ 未找到API服务文件%NC%
    echo 请确保在项目根目录运行此脚本
    goto :error
)

REM 检查requirements.txt
if not exist "services\api\requirements.txt" (
    echo %RED%❌ 未找到requirements.txt%NC%
    goto :error
)

echo %GREEN%✅ API服务文件存在%NC%

echo.
echo %BLUE%步骤 5: 安装Python依赖%NC%
echo ----------------------------------------
echo %YELLOW%正在安装依赖...%NC%

cd services\api
pip install -r requirements.txt
if %errorlevel%==0 (
    echo %GREEN%✅ 依赖安装成功%NC%
) else (
    echo %RED%❌ 依赖安装失败%NC%
    cd ..\..
    goto :error
)

echo.
echo %BLUE%步骤 6: 启动API服务%NC%
echo ----------------------------------------
echo %YELLOW%正在启动知识图谱API服务...%NC%
echo 服务将运行在: http://localhost:8000
echo API文档地址: http://localhost:8000/docs
echo.

REM 启动API服务
python main.py

REM 如果上面失败，尝试uvicorn
if %errorlevel% neq 0 (
    echo %YELLOW%尝试使用uvicorn启动...%NC%
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
)

cd ..\..
goto :end

:error
echo.
echo %RED%========================================%NC%
echo %RED%❌ 启动失败%NC%
echo %RED%========================================%NC%
echo.
echo 请检查以下项目:
echo 1. Neo4j是否正确安装
echo 2. Python是否正确安装 (3.8+)
echo 3. 是否在项目根目录运行脚本
echo 4. 网络连接是否正常
echo.
echo 手动启动步骤:
echo 1. scripts\neo4j_manager.bat start
echo 2. cd services\api
echo 3. pip install -r requirements.txt
echo 4. python main.py
echo.
pause
exit /b 1

:end
echo.
echo %GREEN%========================================%NC%
echo %GREEN%🎉 后端服务启动完成%NC%
echo %GREEN%========================================%NC%
echo.
echo 服务地址:
echo - Neo4j Web界面: http://localhost:7474
echo - API服务: http://localhost:8000
echo - API文档: http://localhost:8000/docs
echo - 前端应用: http://localhost:5173
echo.
echo 按任意键退出...
pause >nul
