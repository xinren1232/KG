#!/usr/bin/env python3
"""
为系统管理页面添加Schema相关的API端点
"""

import paramiko
import time

# 服务器配置
SERVER_IP = "47.108.152.16"
USERNAME = "root"
PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def execute_ssh_command(ssh, command, description=""):
    """执行SSH命令并返回结果"""
    if description:
        print(f"\n{'='*60}")
        print(f"📌 {description}")
        print(f"{'='*60}")
    
    print(f"💻 执行命令: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    
    if output:
        print(f"✅ 输出:\n{output}")
    if error and "warning" not in error.lower():
        print(f"⚠️ 错误:\n{error}")
    
    return output, error

def add_schema_endpoints():
    """添加Schema相关的API端点"""
    
    print("🚀 开始添加Schema API端点...")
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n🔗 连接服务器 {SERVER_IP}...")
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        print("✅ 连接成功！")
        
        # 1. 备份main.py
        execute_ssh_command(
            ssh,
            f"cd {PROJECT_DIR}/api && cp main.py main.py.backup.schema_$(date +%Y%m%d_%H%M%S)",
            "备份main.py"
        )
        
        # 2. 添加词典Schema统计端点
        schema_endpoints_code = '''
# ==================== Schema管理端点 ====================

@app.get("/kg/dictionary/stats")
async def get_dictionary_stats():
    """获取词典统计信息"""
    try:
        with driver.session() as session:
            # 获取术语总数
            term_count = session.run("MATCH (t:Term) RETURN count(t) as count").single()["count"]
            
            # 获取分类总数
            category_count = session.run("MATCH (c:Category) RETURN count(c) as count").single()["count"]
            
            # 获取标签总数
            tag_count = session.run("MATCH (t:Tag) RETURN count(t) as count").single()["count"]
            
            # 获取别名总数
            alias_count = session.run("MATCH (a:Alias) RETURN count(a) as count").single()["count"]
            
            return {
                "ok": True,
                "data": {
                    "totalTerms": term_count,
                    "totalCategories": category_count,
                    "totalTags": tag_count,
                    "totalAliases": alias_count
                }
            }
    except Exception as e:
        logger.error(f"获取词典统计失败: {str(e)}")
        return {"ok": False, "error": str(e)}

@app.get("/kg/dictionary/categories")
async def get_dictionary_categories():
    """获取词典分类详情"""
    try:
        with driver.session() as session:
            query = """
            MATCH (c:Category)
            OPTIONAL MATCH (t:Term)-[:BELONGS_TO]->(c)
            OPTIONAL MATCH (t)-[:HAS_TAG]->(tag:Tag)
            OPTIONAL MATCH (a:Alias)-[:ALIAS_OF]->(t)
            WITH c, 
                 count(DISTINCT t) as termCount,
                 count(DISTINCT tag) as tagCount,
                 count(DISTINCT a) as aliasCount
            RETURN c.name as name, 
                   termCount, 
                   tagCount, 
                   aliasCount
            ORDER BY termCount DESC
            """
            result = session.run(query)
            
            categories = []
            for record in result:
                categories.append({
                    "name": record["name"],
                    "termCount": record["termCount"],
                    "tagCount": record["tagCount"],
                    "aliasCount": record["aliasCount"]
                })
            
            return {"ok": True, "data": categories}
    except Exception as e:
        logger.error(f"获取分类详情失败: {str(e)}")
        return {"ok": False, "error": str(e)}

@app.get("/kg/entities")
async def get_entity_statistics():
    """获取所有实体类型的统计"""
    try:
        with driver.session() as session:
            query = """
            CALL db.labels() YIELD label
            CALL {
                WITH label
                MATCH (n)
                WHERE label IN labels(n)
                RETURN count(n) as count
            }
            RETURN label, count
            ORDER BY count DESC
            """
            result = session.run(query)
            
            entities = []
            for record in result:
                entities.append({
                    "label": record["label"],
                    "count": record["count"]
                })
            
            return {"ok": True, "data": entities}
    except Exception as e:
        logger.error(f"获取实体统计失败: {str(e)}")
        return {"ok": False, "error": str(e)}

@app.get("/kg/relations")
async def get_relationship_statistics():
    """获取所有关系类型的统计"""
    try:
        with driver.session() as session:
            query = """
            CALL db.relationshipTypes() YIELD relationshipType
            CALL {
                WITH relationshipType
                MATCH ()-[r]->()
                WHERE type(r) = relationshipType
                RETURN count(r) as count
            }
            RETURN relationshipType as type, count
            ORDER BY count DESC
            """
            result = session.run(query)
            
            relationships = []
            for record in result:
                relationships.append({
                    "type": record["type"],
                    "count": record["count"]
                })
            
            return {"ok": True, "data": relationships}
    except Exception as e:
        logger.error(f"获取关系统计失败: {str(e)}")
        return {"ok": False, "error": str(e)}
'''
        
        # 3. 将代码写入临时文件
        temp_file = "/tmp/schema_endpoints.py"
        execute_ssh_command(
            ssh,
            f"cat > {temp_file} << 'SCHEMA_EOF'\n{schema_endpoints_code}\nSCHEMA_EOF",
            "创建Schema端点代码"
        )
        
        # 4. 在main.py中添加这些端点（在文件末尾，app.run()之前）
        execute_ssh_command(
            ssh,
            f"""cd {PROJECT_DIR}/api && python3 << 'PYTHON_EOF'
import re

# 读取main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 读取新端点代码
with open('{temp_file}', 'r', encoding='utf-8') as f:
    new_endpoints = f.read()

# 检查是否已经添加过
if 'get_dictionary_stats' not in content:
    # 找到文件末尾的if __name__ == "__main__"之前插入
    if 'if __name__ == "__main__":' in content:
        content = content.replace(
            'if __name__ == "__main__":',
            new_endpoints + '\\n\\nif __name__ == "__main__":'
        )
    else:
        # 如果没有main块，直接追加到文件末尾
        content += '\\n\\n' + new_endpoints
    
    # 写回文件
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Schema端点已添加到main.py")
else:
    print("ℹ️ Schema端点已存在，跳过添加")
PYTHON_EOF
""",
            "添加Schema端点到main.py"
        )
        
        # 5. 重启API服务
        execute_ssh_command(
            ssh,
            "systemctl restart kg-api",
            "重启API服务"
        )
        
        # 等待服务启动
        print("\n⏳ 等待服务启动...")
        time.sleep(5)
        
        # 6. 测试新端点
        test_commands = [
            ("curl -s http://localhost:8000/kg/dictionary/stats | python3 -m json.tool", "测试词典统计端点"),
            ("curl -s http://localhost:8000/kg/dictionary/categories | python3 -m json.tool | head -30", "测试分类详情端点"),
            ("curl -s http://localhost:8000/kg/entities | python3 -m json.tool | head -30", "测试实体统计端点"),
            ("curl -s http://localhost:8000/kg/relations | python3 -m json.tool | head -30", "测试关系统计端点"),
        ]
        
        for cmd, desc in test_commands:
            execute_ssh_command(ssh, cmd, desc)
            time.sleep(1)
        
        # 7. 检查服务状态
        execute_ssh_command(
            ssh,
            "systemctl status kg-api --no-pager | head -20",
            "检查API服务状态"
        )
        
        print("\n" + "="*60)
        print("🎉 Schema API端点添加完成！")
        print("="*60)
        print("\n📋 已添加的端点:")
        print("  ✅ GET /kg/dictionary/stats - 词典统计")
        print("  ✅ GET /kg/dictionary/categories - 分类详情")
        print("  ✅ GET /kg/entities - 实体统计")
        print("  ✅ GET /kg/relations - 关系统计")
        print("\n🌐 访问地址:")
        print(f"  http://{SERVER_IP}/kg/dictionary/stats")
        print(f"  http://{SERVER_IP}/kg/dictionary/categories")
        print(f"  http://{SERVER_IP}/kg/entities")
        print(f"  http://{SERVER_IP}/kg/relations")
        print("\n💡 提示:")
        print("  - 前端页面已更新，访问系统管理页面查看新的Schema标签")
        print("  - 如有问题，查看日志: tail -f /var/log/kg-api.log")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        ssh.close()
        print("\n🔌 SSH连接已关闭")

if __name__ == "__main__":
    add_schema_endpoints()

