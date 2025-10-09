@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set SERVER_IP=47.108.152.16
set SERVER_USER=root
set SERVER_PATH=/opt/kg

echo =========================================
echo API服务修复脚本
echo 服务器: %SERVER_IP%
echo =========================================

echo.
echo 检查SSH连接...
ssh -o ConnectTimeout=5 %SERVER_USER%@%SERVER_IP% "echo SSH连接成功" >nul 2>&1
if errorlevel 1 (
    echo ✗ SSH连接失败
    echo 请检查:
    echo   1. 服务器IP是否正确
    echo   2. SSH密钥是否配置
    echo   3. 网络连接是否正常
    pause
    exit /b 1
)
echo ✓ SSH连接正常

echo.
echo 开始修复API服务...
echo.

ssh %SERVER_USER%@%SERVER_IP% "cd %SERVER_PATH% && docker-compose -f docker-compose.prod.yml restart redis && sleep 3 && docker-compose -f docker-compose.prod.yml restart api && sleep 5 && docker-compose -f docker-compose.prod.yml ps"

echo.
echo =========================================
echo 修复完成
echo =========================================
echo.
echo 请在浏览器中测试: http://%SERVER_IP%/
echo.
echo 如需查看日志，请运行:
echo   ssh %SERVER_USER%@%SERVER_IP%
echo   cd %SERVER_PATH%
echo   docker-compose -f docker-compose.prod.yml logs -f api
echo.
pause

