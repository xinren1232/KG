#!/bin/bash
# 阿里云服务器修复脚本 - 在服务器上执行

echo "========================================="
echo "阿里云服务器API服务修复"
echo "========================================="

cd /opt/kg

echo ""
echo "[1/7] 检查当前容器状态..."
echo "-----------------------------------------"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "[2/7] 查看API日志（最近30行）..."
echo "-----------------------------------------"
docker-compose -f docker-compose.prod.yml logs api --tail=30

echo ""
echo "[3/7] 重启Redis服务..."
echo "-----------------------------------------"
docker-compose -f docker-compose.prod.yml restart redis
echo "✓ Redis重启完成，等待3秒..."
sleep 3

echo ""
echo "[4/7] 重启API服务..."
echo "-----------------------------------------"
docker-compose -f docker-compose.prod.yml restart api
echo "✓ API重启完成，等待5秒..."
sleep 5

echo ""
echo "[5/7] 检查修复后的容器状态..."
echo "-----------------------------------------"
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "[6/7] 测试API健康检查..."
echo "-----------------------------------------"
if docker exec kg_api_prod curl -f -s http://localhost:8000/health 2>/dev/null; then
    echo "✓ API健康检查通过"
else
    echo "✗ API健康检查失败"
fi

echo ""
echo "[7/7] 测试/kg/real-stats端点..."
echo "-----------------------------------------"
if docker exec kg_api_prod curl -f -s http://localhost:8000/kg/real-stats 2>/dev/null | head -c 200; then
    echo ""
    echo "✓ /kg/real-stats端点正常"
else
    echo "✗ /kg/real-stats端点失败"
fi

echo ""
echo "========================================="
echo "修复完成！"
echo "========================================="
echo ""
echo "请在浏览器中访问: http://47.108.152.16/"
echo ""
echo "如果问题仍然存在，请查看详细日志:"
echo "  docker-compose -f docker-compose.prod.yml logs api --tail=100"
echo ""

