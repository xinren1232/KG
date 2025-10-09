@echo off
chcp 65001
echo 🔄 全面重启知识图谱系统所有服务
echo ========================================

echo.
echo 📋 检查当前目录...
cd /d "%~dp0"
echo 当前目录: %CD%

echo.
echo 🛑 停止所有现有服务...
echo ========================================

echo 🔍 查找并停止现有进程...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "python.exe"') do (
    echo 停止Python进程: %%i
    taskkill /pid %%i /f >nul 2>&1
)

for /f "tokens=2" %%i in ('tasklist /fi "imagename eq node.exe" /fo csv ^| find "node.exe"') do (
    echo 停止Node.js进程: %%i
    taskkill /pid %%i /f >nul 2>&1
)

echo 🔌 释放端口占用...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do taskkill /pid %%a /f >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173"') do taskkill /pid %%a /f >nul 2>&1

echo ✅ 现有服务已停止

echo.
echo 🔍 检查Neo4j服务状态...
echo ========================================
netstat -an | findstr :7687 >nul
if %errorlevel% equ 0 (
    echo ✅ Neo4j服务正在运行 (端口7687)
) else (
    echo ❌ Neo4j服务未运行
    echo 🚀 尝试启动Neo4j服务...
    
    REM 尝试通过Neo4j Desktop启动
    if exist "%USERPROFILE%\AppData\Local\Neo4j\Relate\Data\dbmss" (
        echo 检测到Neo4j Desktop安装
        echo 请手动启动Neo4j Desktop并启动数据库
    )
    
    REM 尝试通过服务启动
    sc query neo4j >nul 2>&1
    if %errorlevel% equ 0 (
        echo 启动Neo4j Windows服务...
        net start neo4j
    )
    
    echo ⏳ 等待Neo4j启动...
    timeout /t 10 /nobreak >nul
    
    netstat -an | findstr :7687 >nul
    if %errorlevel% equ 0 (
        echo ✅ Neo4j服务启动成功
    ) else (
        echo ❌ Neo4j服务启动失败
        echo 💡 请手动启动Neo4j Desktop或检查安装
        echo    - Neo4j Desktop: 启动应用并点击Start按钮
        echo    - 命令行: neo4j console
        pause
        exit /b 1
    )
)

echo.
echo 🔧 检查Python环境和依赖...
echo ========================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或不在PATH中
    pause
    exit /b 1
) else (
    echo ✅ Python环境正常
)

echo 📦 检查API依赖...
cd api
if not exist "requirements.txt" (
    echo ❌ requirements.txt不存在
    cd ..
    pause
    exit /b 1
)

pip list | findstr fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔄 安装API依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        cd ..
        pause
        exit /b 1
    )
) else (
    echo ✅ API依赖已安装
)
cd ..

echo.
echo 🔧 检查Node.js环境和依赖...
echo ========================================
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js未安装或不在PATH中
    pause
    exit /b 1
) else (
    echo ✅ Node.js环境正常
)

echo 📦 检查前端依赖...
cd apps\web
if not exist "package.json" (
    echo ❌ package.json不存在
    cd ..\..
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo 🔄 安装前端依赖...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败
        cd ..\..
        pause
        exit /b 1
    )
) else (
    echo ✅ 前端依赖已安装
)
cd ..\..

echo.
echo 🚀 启动所有服务...
echo ========================================

echo 🌐 启动API服务...
start "API服务 - 知识图谱后端" cmd /k "cd /d %CD% && python api\main.py"
echo ✅ API服务启动中... (http://localhost:8000)

echo ⏳ 等待API服务启动...
timeout /t 8 /nobreak >nul

echo 🎨 启动前端服务...
start "前端服务 - 知识图谱界面" cmd /k "cd /d %CD%\apps\web && npm run dev"
echo ✅ 前端服务启动中... (http://localhost:5173)

echo.
echo 📊 验证服务状态...
echo ========================================
timeout /t 5 /nobreak >nul

echo 🔍 检查端口占用...
netstat -an | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ API服务 (端口8000): 正常运行
) else (
    echo ❌ API服务 (端口8000): 未启动
)

netstat -an | findstr :5173 >nul
if %errorlevel% equ 0 (
    echo ✅ 前端服务 (端口5173): 正常运行
) else (
    echo ❌ 前端服务 (端口5173): 未启动
)

netstat -an | findstr :7687 >nul
if %errorlevel% equ 0 (
    echo ✅ Neo4j数据库 (端口7687): 正常运行
) else (
    echo ❌ Neo4j数据库 (端口7687): 未运行
)

echo.
echo 🎯 服务重启完成！
echo ========================================
echo 📱 访问地址:
echo   - 🌐 前端界面: http://localhost:5173
echo   - 📊 图谱可视化: http://localhost:5173/graph-viz
echo   - 🔧 系统管理: http://localhost:5173/system
echo   - 📚 词典管理: http://localhost:5173/dictionary
echo   - 🔍 API文档: http://localhost:8000/docs
echo   - 🗄️ Neo4j浏览器: http://localhost:7474
echo.
echo 💡 使用提示:
echo   - 前端服务需要1-2分钟完成编译
echo   - 如果页面显示异常，请等待编译完成后刷新
echo   - API服务启动后会自动连接Neo4j数据库
echo   - 按Ctrl+C可以停止对应的服务窗口
echo.
echo 🔧 故障排除:
echo   1. 如果API无法连接Neo4j，请检查Neo4j是否正常启动
echo   2. 如果前端编译失败，请检查Node.js版本是否兼容
echo   3. 如果端口被占用，请关闭其他占用端口的程序
echo   4. 查看服务窗口的详细错误信息进行诊断
echo.

pause
