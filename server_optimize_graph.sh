#!/bin/bash
# 服务器端图谱优化脚本

echo "================================================================================"
echo "🚀 知识图谱优化执行（服务器端）"
echo "================================================================================"

cd /opt/knowledge-graph

# 步骤1: 备份当前数据
echo ""
echo "================================================================================"
echo "步骤1: 备份当前数据"
echo "================================================================================"

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp api/data/dictionary.json "$BACKUP_DIR/dictionary.json"
echo "✅ 已备份词典数据到 $BACKUP_DIR"

# 步骤2: 同步词典到Neo4j
echo ""
echo "================================================================================"
echo "步骤2: 同步词典到Neo4j"
echo "================================================================================"

python3 sync_to_neo4j.py

# 步骤3: 发现语义关系
echo ""
echo "================================================================================"
echo "步骤3: 发现语义关系"
echo "================================================================================"

python3 build_semantic_relationships.py

# 步骤4: 导入语义关系到Neo4j
echo ""
echo "================================================================================"
echo "步骤4: 导入语义关系到Neo4j"
echo "================================================================================"

python3 import_relationships_to_neo4j.py

# 步骤5: 验证图谱状态
echo ""
echo "================================================================================"
echo "步骤5: 验证图谱状态"
echo "================================================================================"

python3 -c "
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))

with driver.session() as session:
    # 统计节点
    result = session.run('MATCH (n) RETURN labels(n)[0] AS label, count(n) AS count ORDER BY count DESC')
    print('节点统计:')
    total_nodes = 0
    for record in result:
        label = record['label']
        count = record['count']
        total_nodes += count
        print(f'  {label:20s}: {count:5d} 个')
    print(f'\\n总节点数: {total_nodes}')
    
    # 统计关系
    result = session.run('MATCH ()-[r]->() RETURN type(r) AS rel_type, count(r) AS count ORDER BY count DESC')
    print('\\n关系统计:')
    total_rels = 0
    for record in result:
        rel_type = record['rel_type']
        count = record['count']
        total_rels += count
        print(f'  {rel_type:20s}: {count:5d} 条')
    print(f'\\n总关系数: {total_rels}')

driver.close()
"

echo ""
echo "================================================================================"
echo "✅ 图谱优化完成！"
echo "================================================================================"

echo ""
echo "📊 优化总结:"
echo "  ✅ 数据已备份到 $BACKUP_DIR"
echo "  ✅ 词典已同步到Neo4j"
echo "  ✅ 语义关系已建立"
echo "  ✅ 图谱状态已验证"

echo ""
echo "📁 生成的文件:"
echo "  - semantic_relationships.json (语义关系数据)"
echo "  - $BACKUP_DIR/dictionary.json (备份文件)"

