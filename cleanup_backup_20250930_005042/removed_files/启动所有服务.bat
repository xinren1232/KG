@echo off
chcp 65001
echo 🚀 启动知识图谱系统所有服务
echo ================================

echo.
echo 📋 检查当前目录...
cd /d "%~dp0"
echo 当前目录: %CD%

echo.
echo 🔍 检查Neo4j服务状态...
netstat -an | findstr :7687 >nul
if %errorlevel% equ 0 (
    echo ✅ Neo4j服务已运行 (端口7687)
) else (
    echo ❌ Neo4j服务未运行，请先启动Neo4j
    echo    可以通过Neo4j Desktop或命令行启动
    pause
    exit /b 1
)

echo.
echo 🌐 启动API服务...
start "API服务" cmd /k "cd /d %CD% && python api/main.py"
echo ✅ API服务启动中... (http://localhost:8000)

echo.
echo ⏳ 等待API服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 🎨 启动前端服务...
start "前端服务" cmd /k "cd /d %CD%\apps\web && npm run dev"
echo ✅ 前端服务启动中... (http://localhost:5173)

echo.
echo 📊 服务状态检查...
timeout /t 3 /nobreak >nul

echo.
echo 🎯 所有服务启动完成！
echo ================================
echo 📱 访问地址:
echo   - 前端界面: http://localhost:5173
echo   - API文档:  http://localhost:8000/docs
echo   - Neo4j浏览器: http://localhost:7474
echo.
echo 💡 提示:
echo   - 前端服务需要几秒钟完成编译
echo   - 如果端口被占用，请检查是否有其他服务在运行
echo   - 按Ctrl+C可以停止对应的服务
echo.
echo 🔧 如果遇到问题，请检查:
echo   1. Neo4j服务是否正常运行
echo   2. Python环境是否正确安装依赖
echo   3. Node.js环境是否正确安装依赖
echo.

pause
