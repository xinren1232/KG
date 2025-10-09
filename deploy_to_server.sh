#!/bin/bash
# 部署词典和图谱更新到服务器
# 服务器: 47.108.152.16

SERVER="root@47.108.152.16"
REMOTE_PATH="/opt/knowledge-graph"

echo "================================================================================"
echo "📦 开始部署词典和图谱更新到服务器"
echo "================================================================================"

# 1. 备份服务器现有数据
echo ""
echo "1️⃣ 备份服务器现有数据..."
ssh $SERVER "cd $REMOTE_PATH && \
    mkdir -p backups && \
    cp api/data/dictionary.json backups/dictionary_backup_\$(date +%Y%m%d_%H%M%S).json && \
    echo '✅ 备份完成'"

# 2. 上传更新后的词典文件
echo ""
echo "2️⃣ 上传更新后的词典文件..."
scp api/data/dictionary.json $SERVER:$REMOTE_PATH/api/data/
echo "✅ 词典文件上传完成"

# 3. 上传同步脚本
echo ""
echo "3️⃣ 上传Neo4j同步脚本..."
scp sync_to_neo4j.py $SERVER:$REMOTE_PATH/
echo "✅ 同步脚本上传完成"

# 4. 在服务器上同步到Neo4j
echo ""
echo "4️⃣ 在服务器上同步到Neo4j图谱..."
ssh $SERVER "cd $REMOTE_PATH && \
    echo '开始同步到Neo4j...' && \
    python3 sync_to_neo4j.py && \
    echo '✅ Neo4j同步完成'"

# 5. 重启后端API服务
echo ""
echo "5️⃣ 重启后端API服务..."
ssh $SERVER "systemctl restart kg-api && \
    sleep 3 && \
    systemctl status kg-api | head -10"

# 6. 验证部署
echo ""
echo "6️⃣ 验证部署..."
echo "检查API状态..."
curl -s http://47.108.152.16/kg/stats | python3 -m json.tool

echo ""
echo "================================================================================"
echo "✅ 部署完成！"
echo "================================================================================"
echo ""
echo "📊 验证步骤:"
echo "  1. 访问: http://47.108.152.16"
echo "  2. 检查词典数量是否为 1326 条"
echo "  3. 检查图谱节点数量"
echo "  4. 测试搜索功能"
echo ""
echo "📝 回滚方法（如有问题）:"
echo "  ssh $SERVER"
echo "  cd $REMOTE_PATH"
echo "  cp backups/dictionary_backup_*.json api/data/dictionary.json"
echo "  systemctl restart kg-api"
echo ""
