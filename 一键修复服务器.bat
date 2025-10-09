@echo off
chcp 65001 >nul
echo =========================================
echo 阿里云服务器一键修复工具
echo =========================================
echo.
echo 正在连接服务器并修复API服务...
echo.

ssh root@47.108.152.16 "cd /opt/kg && echo '=== 当前容器状态 ===' && docker-compose -f docker-compose.prod.yml ps && echo '' && echo '=== 重启Redis ===' && docker-compose -f docker-compose.prod.yml restart redis && sleep 3 && echo '=== 重启API ===' && docker-compose -f docker-compose.prod.yml restart api && sleep 5 && echo '' && echo '=== 修复后容器状态 ===' && docker-compose -f docker-compose.prod.yml ps && echo '' && echo '=== 测试API ===' && docker exec kg_api_prod curl -s http://localhost:8000/health"

echo.
echo =========================================
echo 修复完成！
echo =========================================
echo.
echo 请在浏览器中测试: http://47.108.152.16/
echo.
pause

