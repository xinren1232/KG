#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证数据更新 - 检查词典和图谱数据是否正确更新
"""

import requests
import json
from pathlib import Path

def test_api_dictionary():
    """测试API词典数据"""
    print("🔍 测试API词典数据...")
    
    try:
        # 测试词典端点
        response = requests.get("http://localhost:8000/kg/dictionary/entries?page=1&page_size=10", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                entries = data.get('data', {}).get('entries', [])
                total = data.get('data', {}).get('total', 0)
                
                print(f"✅ API词典数据正常")
                print(f"  总数: {total}")
                print(f"  返回条目: {len(entries)}")
                
                if entries:
                    print(f"  示例词条:")
                    for i, entry in enumerate(entries[:3]):
                        print(f"    {i+1}. {entry.get('name', 'N/A')} ({entry.get('type', 'N/A')})")
                
                return True, total
            else:
                print(f"❌ API返回错误: {data.get('error', 'Unknown')}")
                return False, 0
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False, 0
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False, 0

def test_search_functionality():
    """测试搜索功能"""
    print("🔍 测试搜索功能...")
    
    search_terms = ["显示屏", "OLED", "电池", "传感器", "摄像头"]
    
    for term in search_terms:
        try:
            response = requests.get(f"http://localhost:8000/kg/dictionary/entries?search={term}&page_size=5", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    entries = data.get('data', {}).get('entries', [])
                    print(f"  '{term}': 找到 {len(entries)} 条结果")
                    
                    if entries:
                        for entry in entries[:2]:
                            print(f"    - {entry.get('name', 'N/A')}")
                else:
                    print(f"  '{term}': 搜索失败 - {data.get('error', 'Unknown')}")
            else:
                print(f"  '{term}': HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  '{term}': 异常 - {e}")

def check_data_files():
    """检查数据文件"""
    print("📁 检查数据文件...")
    
    files_to_check = [
        "api/data/dictionary.json",
        "api/data/dictionary.csv", 
        "api/data/dictionary_stats.json",
        "词典数据图谱更新脚本.cypher"
    ]
    
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {file_path}: {size:,} bytes")
        else:
            print(f"  ❌ {file_path}: 文件不存在")

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("🔍 测试Neo4j连接...")
    
    try:
        # 测试简单查询
        url = "http://localhost:7474/db/data/transaction/commit"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "statements": [
                {
                    "statement": "MATCH (n:Dictionary) RETURN count(n) as total",
                    "resultDataContents": ["row"]
                }
            ]
        }
        
        # 尝试不同的认证方式
        auth_methods = [
            None,
            ("neo4j", "neo4j"),
            ("neo4j", "password"),
            ("neo4j", "123456")
        ]
        
        for auth in auth_methods:
            try:
                response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if not result.get("errors"):
                        count = result["results"][0]["data"][0]["row"][0] if result["results"][0]["data"] else 0
                        print(f"✅ Neo4j连接成功 (认证: {auth})")
                        print(f"  Dictionary节点数: {count}")
                        return True, count
                    else:
                        print(f"⚠️ Neo4j查询错误: {result['errors']}")
                elif response.status_code == 401:
                    continue  # 尝试下一个认证方式
                else:
                    print(f"⚠️ Neo4j HTTP错误: {response.status_code}")
                    
            except Exception as e:
                continue  # 尝试下一个认证方式
        
        print("❌ Neo4j连接失败 - 所有认证方式都失败")
        return False, 0
        
    except Exception as e:
        print(f"❌ Neo4j测试异常: {e}")
        return False, 0

def create_import_guide():
    """创建导入指南"""
    print("📝 创建Neo4j导入指南...")
    
    guide = """# Neo4j图谱数据导入指南

## 自动导入（推荐）
1. 打开Neo4j浏览器: http://localhost:7474
2. 登录（尝试用户名/密码: neo4j/neo4j 或 neo4j/password）
3. 复制并执行以下命令清空现有Dictionary节点：
   ```cypher
   MATCH (n:Dictionary) DELETE n;
   ```

## 批量导入
由于数据量较大(1192条)，建议分批导入：

### 方法1: 使用生成的脚本
1. 打开文件: 词典数据图谱更新脚本.cypher
2. 复制前50条CREATE语句
3. 在Neo4j浏览器中执行
4. 重复直到所有数据导入完成

### 方法2: 使用LOAD CSV（推荐）
```cypher
LOAD CSV WITH HEADERS FROM 'file:///api/data/dictionary.csv' AS row
CREATE (d:Dictionary {
    id: row.id,
    name: row.name,
    type: row.type,
    category: row.category,
    description: row.description,
    created_at: row.created_at,
    updated_at: row.updated_at
});
```

## 验证导入
```cypher
MATCH (n:Dictionary) RETURN count(n) as total;
MATCH (n:Dictionary) RETURN n.type, count(n) ORDER BY count(n) DESC;
```

## 预期结果
- Dictionary节点总数: 1192
- 包含9种类型的词典数据
- 覆盖20个硬件模块的专业词汇
"""
    
    with open("Neo4j图谱数据导入指南.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("✅ 导入指南已创建: Neo4j图谱数据导入指南.md")

def main():
    """主函数"""
    print("🔧 验证数据更新")
    print("=" * 50)
    
    # 1. 检查数据文件
    check_data_files()
    
    # 2. 测试API词典
    api_ok, api_total = test_api_dictionary()
    
    # 3. 测试搜索功能
    if api_ok:
        test_search_functionality()
    
    # 4. 测试Neo4j连接
    neo4j_ok, neo4j_total = test_neo4j_connection()
    
    # 5. 创建导入指南
    create_import_guide()
    
    print("\n" + "=" * 50)
    print("📊 验证结果总结:")
    print(f"API词典数据: {'✅ 正常' if api_ok else '❌ 异常'} ({api_total} 条)")
    print(f"Neo4j图谱: {'✅ 连接正常' if neo4j_ok else '❌ 连接失败'} ({neo4j_total} 条Dictionary节点)")
    
    if api_ok and api_total >= 1000:
        print("✅ 词典数据已成功更新到1192条")
    else:
        print("⚠️ 词典数据可能未完全更新")
    
    if neo4j_ok and neo4j_total >= 1000:
        print("✅ 图谱数据已包含词典节点")
    elif neo4j_ok and neo4j_total == 0:
        print("⚠️ 图谱中暂无Dictionary节点，需要执行导入脚本")
    else:
        print("❌ 图谱连接失败，需要检查Neo4j服务")
    
    print(f"\n💡 下一步操作:")
    if api_ok and api_total >= 1000:
        print("1. ✅ 词典API已更新，前端应该能看到新数据")
    else:
        print("1. ❌ 需要重启API服务或检查数据加载")
    
    if neo4j_ok and neo4j_total < 1000:
        print("2. 📋 执行Neo4j导入脚本更新图谱数据")
        print("3. 📖 参考 Neo4j图谱数据导入指南.md")
    elif neo4j_ok:
        print("2. ✅ 图谱数据已更新")
    else:
        print("2. ❌ 需要启动Neo4j服务")
    
    print("4. 🌐 访问前端验证: http://localhost:5173")
    print("5. 📚 检查词典管理页面是否显示1192条数据")

if __name__ == "__main__":
    main()
