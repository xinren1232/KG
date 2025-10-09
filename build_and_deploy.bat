@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo =========================================
echo 质量知识图谱系统 - 构建和部署
echo =========================================

:: 步骤1: 构建前端
echo.
echo 步骤1: 构建前端应用
cd apps\web

:: 检查node_modules
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        exit /b 1
    )
)

:: 构建前端
echo 构建前端...
call npm run build
if errorlevel 1 (
    echo 错误: 前端构建失败
    exit /b 1
)

:: 检查构建结果
if not exist "dist" (
    echo 错误: 前端构建失败，dist目录不存在
    exit /b 1
)

echo ✓ 前端构建成功

:: 返回项目根目录
cd ..\..

:: 步骤2: 复制构建文件到项目根目录
echo.
echo 步骤2: 准备部署文件
if exist "dist" (
    rmdir /s /q dist
)
xcopy /E /I /Y apps\web\dist dist
echo ✓ 构建文件已复制到 .\dist

:: 步骤3: 使用HTTP配置替换nginx配置
echo.
echo 步骤3: 更新Nginx配置
if exist "nginx\nginx.http.conf" (
    copy /Y nginx\nginx.http.conf nginx\nginx.conf
    echo ✓ Nginx配置已更新为HTTP模式
) else (
    echo 警告: nginx.http.conf不存在，跳过配置更新
)

echo.
echo =========================================
echo 本地构建完成！
echo =========================================
echo.
echo 下一步: 将以下文件上传到服务器
echo   1. dist/ 目录
echo   2. nginx/nginx.conf 文件
echo   3. docker-compose.prod.yml 文件
echo.
echo 然后在服务器上执行:
echo   docker-compose -f docker-compose.prod.yml down
echo   docker-compose -f docker-compose.prod.yml up -d --build
echo.
pause

