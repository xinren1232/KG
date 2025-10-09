#!/bin/bash
# 部署图谱可视化优化

set -e

SERVER="root@47.108.152.16"
PASSWORD="Zxylsy.99"
REMOTE_DIR="/opt/knowledge-graph"

echo "========================================="
echo "🚀 部署图谱可视化优化"
echo "========================================="

# 1. 上传前端文件
echo ""
echo "📤 上传前端文件..."
sshpass -p "$PASSWORD" scp apps/web/src/views/GraphVisualization.vue $SERVER:$REMOTE_DIR/apps/web/src/views/

# 2. 上传后端路由文件
echo ""
echo "📤 上传后端路由文件..."
sshpass -p "$PASSWORD" scp services/api/routers/kg_router.py $SERVER:$REMOTE_DIR/services/api/routers/

# 3. 上传Neo4j客户端文件
echo ""
echo "📤 上传Neo4j客户端文件..."
sshpass -p "$PASSWORD" scp services/api/database/neo4j_client.py $SERVER:$REMOTE_DIR/services/api/database/

# 4. 重启服务
echo ""
echo "🔄 重启服务..."
sshpass -p "$PASSWORD" ssh $SERVER << 'ENDSSH'
cd /opt/knowledge-graph

# 重启前端
echo "重启前端服务..."
systemctl restart kg-frontend

# 重启后端
echo "重启后端服务..."
systemctl restart kg-api

# 等待服务启动
sleep 5

# 检查服务状态
echo ""
echo "检查服务状态..."
systemctl status kg-frontend --no-pager | head -10
echo ""
systemctl status kg-api --no-pager | head -10

ENDSSH

echo ""
echo "========================================="
echo "✅ 部署完成！"
echo "========================================="
echo ""
echo "📊 访问地址: http://47.108.152.16/"
echo ""
echo "🧪 测试建议:"
echo "  1. 刷新浏览器页面"
echo "  2. 检查节点大小是否有差异"
echo "  3. 检查颜色是否更鲜明"
echo "  4. 检查是否显示图例"
echo "  5. 检查Tooltip是否显示连接数"
echo ""

