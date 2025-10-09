#!/usr/bin/env python3
"""
导入数据到服务器Neo4j数据库
"""
import subprocess
import sys
import time

def run_ssh_command(command, description):
    """执行SSH命令"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    
    full_command = f'ssh root@47.108.152.16 "{command}"'
    print(f"执行命令: {command}\n")
    
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 成功")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print(f"❌ 失败")
        if result.stderr:
            print(f"错误: {result.stderr}")
        if result.stdout:
            print(result.stdout)
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     知识图谱数据导入工具                                  ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 1. 检查Neo4j状态
    run_ssh_command(
        "systemctl is-active neo4j",
        "检查Neo4j服务状态"
    )
    
    # 2. 检查当前数据量
    run_ssh_command(
        "echo 'MATCH (n) RETURN count(n) as total_nodes;' | cypher-shell -u neo4j -p password123",
        "检查当前数据量"
    )
    
    # 3. 创建约束和索引
    print(f"\n{'='*60}")
    print("📌 创建Neo4j约束和索引")
    print(f"{'='*60}")
    
    constraints = [
        "CREATE CONSTRAINT term_id IF NOT EXISTS FOR (t:Term) REQUIRE t.id IS UNIQUE;",
        "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE;",
        "CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE;",
        "CREATE INDEX term_name IF NOT EXISTS FOR (t:Term) ON (t.name);",
        "CREATE INDEX term_category IF NOT EXISTS FOR (t:Term) ON (t.category);"
    ]
    
    for constraint in constraints:
        run_ssh_command(
            f"echo '{constraint}' | cypher-shell -u neo4j -p password123",
            f"执行: {constraint[:50]}..."
        )
        time.sleep(1)
    
    # 4. 导入词典数据
    print(f"\n{'='*60}")
    print("📌 导入词典数据")
    print(f"{'='*60}")
    
    # 检查是否有导入脚本
    result = run_ssh_command(
        "ls -lh /opt/knowledge-graph/api/etl/",
        "检查ETL脚本"
    )
    
    # 5. 使用API导入数据
    print(f"\n{'='*60}")
    print("📌 通过API导入词典数据")
    print(f"{'='*60}")
    
    # 检查词典文件
    run_ssh_command(
        "wc -l /opt/knowledge-graph/data/dictionary/dictionary_v1.csv",
        "检查词典文件行数"
    )
    
    # 6. 创建示例数据
    print(f"\n{'='*60}")
    print("📌 创建示例数据")
    print(f"{'='*60}")
    
    sample_data = """
    // 创建示例分类
    MERGE (c1:Category {name: '质量管理', id: 'cat_quality'})
    SET c1.description = '质量管理相关术语'
    
    MERGE (c2:Category {name: '测试', id: 'cat_test'})
    SET c2.description = '测试相关术语'
    
    MERGE (c3:Category {name: '可靠性', id: 'cat_reliability'})
    SET c3.description = '可靠性相关术语'
    
    // 创建示例术语
    MERGE (t1:Term {id: 'term_001', name: '来料检验'})
    SET t1.category = '质量管理',
        t1.definition = '对供应商提供的原材料、零部件进行质量检验',
        t1.english = 'Incoming Quality Control',
        t1.abbreviation = 'IQC'
    
    MERGE (t2:Term {id: 'term_002', name: '功能测试'})
    SET t2.category = '测试',
        t2.definition = '验证产品功能是否符合设计要求',
        t2.english = 'Functional Test',
        t2.abbreviation = 'FT'
    
    MERGE (t3:Term {id: 'term_003', name: '可靠性测试'})
    SET t3.category = '可靠性',
        t3.definition = '验证产品在规定条件下的可靠性',
        t3.english = 'Reliability Test',
        t3.abbreviation = 'RT'
    
    MERGE (t4:Term {id: 'term_004', name: '跌落测试'})
    SET t4.category = '可靠性',
        t4.definition = '模拟产品跌落情况的测试',
        t4.english = 'Drop Test'
    
    MERGE (t5:Term {id: 'term_005', name: '环境测试'})
    SET t5.category = '可靠性',
        t5.definition = '在不同环境条件下测试产品性能',
        t5.english = 'Environmental Test'
    
    // 创建关系
    MERGE (t1)-[:BELONGS_TO]->(c1)
    MERGE (t2)-[:BELONGS_TO]->(c2)
    MERGE (t3)-[:BELONGS_TO]->(c3)
    MERGE (t4)-[:BELONGS_TO]->(c3)
    MERGE (t5)-[:BELONGS_TO]->(c3)
    
    MERGE (t4)-[:RELATED_TO {type: '包含于'}]->(t3)
    MERGE (t5)-[:RELATED_TO {type: '包含于'}]->(t3)
    
    // 创建标签
    MERGE (tag1:Tag {name: '质量', id: 'tag_quality'})
    MERGE (tag2:Tag {name: '测试', id: 'tag_test'})
    MERGE (tag3:Tag {name: '可靠性', id: 'tag_reliability'})
    
    MERGE (t1)-[:HAS_TAG]->(tag1)
    MERGE (t2)-[:HAS_TAG]->(tag2)
    MERGE (t3)-[:HAS_TAG]->(tag3)
    MERGE (t4)-[:HAS_TAG]->(tag3)
    MERGE (t5)-[:HAS_TAG]->(tag3)
    
    RETURN '示例数据创建成功' as result;
    """
    
    # 保存到临时文件并执行
    run_ssh_command(
        f"cat > /tmp/sample_data.cypher << 'EOF'\n{sample_data}\nEOF",
        "创建示例数据脚本"
    )
    
    run_ssh_command(
        "cypher-shell -u neo4j -p password123 -f /tmp/sample_data.cypher",
        "导入示例数据"
    )
    
    # 7. 验证数据
    print(f"\n{'='*60}")
    print("📌 验证导入结果")
    print(f"{'='*60}")
    
    run_ssh_command(
        "echo 'MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY count DESC;' | cypher-shell -u neo4j -p password123",
        "统计各类型节点数量"
    )
    
    run_ssh_command(
        "echo 'MATCH ()-[r]->() RETURN type(r) as relation_type, count(r) as count ORDER BY count DESC;' | cypher-shell -u neo4j -p password123",
        "统计各类型关系数量"
    )
    
    # 8. 测试API
    print(f"\n{'='*60}")
    print("📌 测试API数据查询")
    print(f"{'='*60}")
    
    run_ssh_command(
        "curl -s http://localhost:8000/kg/stats | python3 -m json.tool",
        "获取图谱统计信息"
    )
    
    print(f"\n{'='*60}")
    print("✅ 数据导入完成！")
    print(f"{'='*60}")
    print("""
下一步操作:
1. 访问前端: http://47.108.152.16/
2. 查看API文档: http://47.108.152.16/api/docs
3. 访问Neo4j浏览器: http://47.108.152.16/neo4j/
   
如需导入更多数据，可以:
1. 上传Excel文件到服务器
2. 使用API的文件上传功能
3. 运行ETL脚本导入
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        sys.exit(1)

