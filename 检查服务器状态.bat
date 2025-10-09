@echo off
chcp 65001 >nul
echo =========================================
echo 阿里云服务器状态检查
echo =========================================
echo.

echo [1/6] 检查容器状态...
echo ----------------------------------------
ssh root@47.108.152.16 "cd /opt/kg && docker-compose -f docker-compose.prod.yml ps"

echo.
echo [2/6] 检查API日志（最近30行）...
echo ----------------------------------------
ssh root@47.108.152.16 "cd /opt/kg && docker-compose -f docker-compose.prod.yml logs api --tail=30"

echo.
echo [3/6] 检查Nginx日志（最近20行）...
echo ----------------------------------------
ssh root@47.108.152.16 "cd /opt/kg && docker-compose -f docker-compose.prod.yml logs nginx --tail=20"

echo.
echo [4/6] 检查文件结构...
echo ----------------------------------------
ssh root@47.108.152.16 "ls -lh /opt/kg/dist/ 2>/dev/null || echo 'dist目录不存在'"

echo.
echo [5/6] 测试API健康检查...
echo ----------------------------------------
ssh root@47.108.152.16 "docker exec kg_api_prod curl -s http://localhost:8000/health 2>/dev/null || echo 'API健康检查失败'"

echo.
echo [6/6] 测试/kg/real-stats端点...
echo ----------------------------------------
ssh root@47.108.152.16 "docker exec kg_api_prod curl -s http://localhost:8000/kg/real-stats 2>/dev/null | head -c 300 || echo '/kg/real-stats端点失败'"

echo.
echo =========================================
echo 检查完成
echo =========================================
echo.
echo 如需修复，请运行: 一键修复服务器.bat
echo.
pause

