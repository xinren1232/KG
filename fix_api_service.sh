#!/bin/bash

# 阿里云服务器API服务修复脚本
# 用于修复502错误和API服务问题

set -e

SERVER_IP="47.108.152.16"
SERVER_USER="root"
SERVER_PATH="/opt/kg"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================="
echo "API服务修复脚本"
echo "服务器: $SERVER_IP"
echo "========================================="

# 检查SSH连接
echo -e "\n${BLUE}检查SSH连接...${NC}"
if ssh -o ConnectTimeout=5 $SERVER_USER@$SERVER_IP "echo 'SSH连接成功'" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ SSH连接正常${NC}"
else
    echo -e "${RED}✗ SSH连接失败${NC}"
    echo "请检查:"
    echo "  1. 服务器IP是否正确"
    echo "  2. SSH密钥是否配置"
    echo "  3. 网络连接是否正常"
    exit 1
fi

# 在服务器上执行修复
echo -e "\n${BLUE}开始修复API服务...${NC}"

ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
set -e

cd /opt/kg

echo "========================================="
echo "1. 检查当前容器状态"
echo "========================================="
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "========================================="
echo "2. 检查API容器日志"
echo "========================================="
docker-compose -f docker-compose.prod.yml logs api --tail=20

echo ""
echo "========================================="
echo "3. 重启Redis服务"
echo "========================================="
docker-compose -f docker-compose.prod.yml restart redis
sleep 3
echo "✓ Redis已重启"

echo ""
echo "========================================="
echo "4. 重启API服务"
echo "========================================="
docker-compose -f docker-compose.prod.yml restart api
sleep 5
echo "✓ API已重启"

echo ""
echo "========================================="
echo "5. 检查服务状态"
echo "========================================="
docker-compose -f docker-compose.prod.yml ps

echo ""
echo "========================================="
echo "6. 测试API健康检查"
echo "========================================="
sleep 3
if docker exec kg_api_prod curl -f http://localhost:8000/health 2>/dev/null; then
    echo "✓ API健康检查通过"
else
    echo "✗ API健康检查失败"
    echo "查看详细日志:"
    docker-compose -f docker-compose.prod.yml logs api --tail=50
fi

echo ""
echo "========================================="
echo "7. 测试/kg/real-stats端点"
echo "========================================="
if docker exec kg_api_prod curl -f http://localhost:8000/kg/real-stats 2>/dev/null | head -c 200; then
    echo ""
    echo "✓ /kg/real-stats端点正常"
else
    echo "✗ /kg/real-stats端点失败"
fi

echo ""
echo "========================================="
echo "修复完成"
echo "========================================="
echo "访问地址: http://47.108.152.16/"
echo "API地址: http://47.108.152.16/api/kg/real-stats"
echo ""
echo "如果问题仍然存在，请运行:"
echo "  docker-compose -f docker-compose.prod.yml logs -f api"
echo "查看实时日志"

ENDSSH

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}修复脚本执行完成${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "请在浏览器中测试: http://$SERVER_IP/"
echo ""

