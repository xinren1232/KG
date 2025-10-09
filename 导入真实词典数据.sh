#!/bin/bash
# 导入真实的词典数据到服务器Neo4j

echo "🚀 开始导入真实词典数据到服务器"
echo "================================"

# 1. 上传导入脚本
echo "📤 上传导入脚本..."
scp services/etl/load_dictionary_batch.py root@47.108.152.16:/tmp/

# 2. 执行导入
echo ""
echo "📥 执行数据导入..."
ssh root@47.108.152.16 "cd /opt/knowledge-graph && python3 /tmp/load_dictionary_batch.py"

# 3. 验证导入结果
echo ""
echo "🔍 验证导入结果..."
ssh root@47.108.152.16 "echo 'MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY count DESC;' | cypher-shell -u neo4j -p password123"

echo ""
echo "📊 检查API统计..."
ssh root@47.108.152.16 "curl -s http://localhost:8000/kg/stats | python3 -m json.tool"

echo ""
echo "✅ 导入完成！"

