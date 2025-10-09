#!/bin/bash
# 统一词典更新脚本

set -e  # 遇到错误立即退出

echo "================================"
echo "词典数据统一更新脚本"
echo "================================"

# 主数据文件
MAIN_DATA="/opt/knowledge-graph/api/data/dictionary.json"
FRONTEND_DATA="/opt/knowledge-graph/apps/web/src/data/dictionary.json"

# 检查主数据文件是否存在
if [ ! -f "$MAIN_DATA" ]; then
    echo "❌ 错误: 主数据文件不存在: $MAIN_DATA"
    exit 1
fi

# 显示主数据文件信息
ENTRY_COUNT=$(python3 -c "import json; print(len(json.load(open('$MAIN_DATA'))))")
echo "📊 主数据文件: $ENTRY_COUNT 条"

# 1. 备份现有数据
echo ""
echo "1️⃣ 备份现有数据..."
BACKUP_DIR="/opt/knowledge-graph/backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp "$MAIN_DATA" "$BACKUP_DIR/dictionary_backup_$TIMESTAMP.json"
echo "✅ 备份完成: $BACKUP_DIR/dictionary_backup_$TIMESTAMP.json"

# 2. 同步到前端源码目录
echo ""
echo "2️⃣ 同步到前端源码目录..."
cp "$MAIN_DATA" "$FRONTEND_DATA"
echo "✅ 同步完成: $FRONTEND_DATA"

# 3. 同步到Neo4j
echo ""
echo "3️⃣ 同步到Neo4j图谱..."
cd /opt/knowledge-graph
python3 sync_to_neo4j.py
echo "✅ Neo4j同步完成"

# 4. 重新构建前端
echo ""
echo "4️⃣ 重新构建前端..."
cd /opt/knowledge-graph/apps/web
npm run build > /dev/null 2>&1
echo "✅ 前端构建完成"

# 5. 重启服务
echo ""
echo "5️⃣ 重启服务..."
systemctl restart nginx
systemctl restart kg-api
sleep 2
echo "✅ 服务重启完成"

# 6. 验证
echo ""
echo "6️⃣ 验证更新..."
API_COUNT=$(curl -s http://localhost:8000/kg/dictionary | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))")
echo "✅ API返回: $API_COUNT 条"

echo ""
echo "================================"
echo "✅ 更新完成！"
echo "================================"
echo "主数据: $ENTRY_COUNT 条"
echo "API返回: $API_COUNT 条"
echo ""
echo "请在浏览器中按 Ctrl+Shift+R 强制刷新页面"

