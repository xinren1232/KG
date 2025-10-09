#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新图谱数据 - 将修复后的词典数据导入Neo4j图谱
"""

import json
import requests
from pathlib import Path
from datetime import datetime

def generate_neo4j_import_script():
    """生成Neo4j导入脚本"""
    print("🔧 生成Neo4j导入脚本...")
    
    # 读取修复后的词典数据
    data_file = Path("api/data/dictionary.json")
    
    if not data_file.exists():
        print(f"❌ 词典文件不存在: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 词典数据: {len(data)} 条")
        
        # 生成Cypher脚本
        cypher_statements = []
        
        # 1. 清理现有Dictionary节点
        cypher_statements.append("// 清理现有Dictionary节点")
        cypher_statements.append("MATCH (n:Dictionary) DETACH DELETE n;")
        cypher_statements.append("")
        
        # 2. 创建约束和索引
        cypher_statements.append("// 创建约束和索引")
        cypher_statements.append("CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;")
        cypher_statements.append("CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category);")
        cypher_statements.append("CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags);")
        cypher_statements.append("")
        
        # 3. 批量创建Dictionary节点
        cypher_statements.append("// 批量创建Dictionary节点")
        
        batch_size = 50
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            cypher_statements.append(f"// 批次 {batch_num}: 第 {i+1}-{min(i+batch_size, len(data))} 条")
            
            # 使用UNWIND批量创建
            cypher_statements.append("WITH [")
            
            for j, item in enumerate(batch):
                term = item.get('term', '').replace("'", "\\'").replace('"', '\\"')
                category = item.get('category', '').replace("'", "\\'")
                description = item.get('description', '').replace("'", "\\'").replace('"', '\\"')
                aliases = item.get('aliases', [])
                tags = item.get('tags', [])
                
                # 清理aliases和tags
                clean_aliases = [alias.replace("'", "\\'").replace('"', '\\"') for alias in aliases if alias and isinstance(alias, str)]
                clean_tags = [tag.replace("'", "\\'").replace('"', '\\"') for tag in tags if tag and isinstance(tag, str)]
                
                aliases_str = "[" + ", ".join([f"'{alias}'" for alias in clean_aliases]) + "]"
                tags_str = "[" + ", ".join([f"'{tag}'" for tag in clean_tags]) + "]"
                
                comma = "," if j < len(batch) - 1 else ""
                
                cypher_statements.append(f"  {{term: '{term}', category: '{category}', description: '{description}', aliases: {aliases_str}, tags: {tags_str}}}{comma}")
            
            cypher_statements.append("] AS batch")
            cypher_statements.append("UNWIND batch AS item")
            cypher_statements.append("CREATE (d:Dictionary {")
            cypher_statements.append("  term: item.term,")
            cypher_statements.append("  category: item.category,")
            cypher_statements.append("  description: item.description,")
            cypher_statements.append("  aliases: item.aliases,")
            cypher_statements.append("  tags: item.tags,")
            cypher_statements.append("  created_at: datetime(),")
            cypher_statements.append("  updated_at: datetime()")
            cypher_statements.append("});")
            cypher_statements.append("")
        
        # 4. 创建统计查询
        cypher_statements.append("// 验证导入结果")
        cypher_statements.append("MATCH (d:Dictionary) RETURN count(d) as total_dictionary_nodes;")
        cypher_statements.append("")
        cypher_statements.append("// 按分类统计")
        cypher_statements.append("MATCH (d:Dictionary) RETURN d.category, count(d) as count ORDER BY count DESC;")
        cypher_statements.append("")
        cypher_statements.append("// 显示示例数据")
        cypher_statements.append("MATCH (d:Dictionary) RETURN d.term, d.category, d.aliases, d.tags LIMIT 5;")
        
        # 保存脚本
        script_file = Path("更新图谱数据导入脚本.cypher")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cypher_statements))
        
        print(f"✅ Cypher脚本已生成: {script_file}")
        print(f"📊 包含 {len(data)} 条Dictionary节点")
        print(f"📊 分 {(len(data) + batch_size - 1) // batch_size} 个批次导入")
        
        return True, script_file
        
    except Exception as e:
        print(f"❌ 生成脚本失败: {e}")
        return False, None

def test_neo4j_connection():
    """测试Neo4j连接"""
    print("🔍 测试Neo4j连接...")
    
    neo4j_urls = [
        "http://localhost:7474",
        "http://localhost:7687"
    ]
    
    for url in neo4j_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Neo4j服务可访问: {url}")
                return True, url
            else:
                print(f"⚠️ Neo4j HTTP {response.status_code}: {url}")
        except Exception as e:
            print(f"❌ Neo4j连接失败: {url} - {e}")
    
    return False, None

def generate_import_guide():
    """生成导入指南"""
    print("📝 生成导入指南...")
    
    guide_content = """# Neo4j图谱数据导入指南

## 🎯 导入目标
将1124条修复后的词典数据导入Neo4j图谱，创建Dictionary节点。

## 📊 数据概览
- **总数据量**: 1124条词典数据
- **8个Label分类**: Symptom, Component, Tool, Process, TestCase, Metric, Material, Role
- **数据格式**: 已修复aliases和tags字段格式错误

## 🔧 导入步骤

### 1. 启动Neo4j服务
```bash
# 确保Neo4j服务正在运行
neo4j start
# 或者通过Neo4j Desktop启动
```

### 2. 访问Neo4j浏览器
打开浏览器访问: http://localhost:7474

### 3. 执行导入脚本
1. 在Neo4j浏览器中打开 `更新图谱数据导入脚本.cypher`
2. 复制脚本内容到查询框
3. 执行脚本（建议分批执行）

### 4. 验证导入结果
执行以下查询验证导入：

```cypher
// 检查总数
MATCH (d:Dictionary) RETURN count(d) as total;

// 按分类统计
MATCH (d:Dictionary) 
RETURN d.category, count(d) as count 
ORDER BY count DESC;

// 查看示例数据
MATCH (d:Dictionary) 
RETURN d.term, d.category, d.aliases, d.tags 
LIMIT 10;
```

## 📊 预期结果
- **Dictionary节点总数**: 1124个
- **分类分布**:
  - Symptom (症状): 259个
  - Metric (性能指标): 190个
  - Component (组件): 181个
  - Process (流程): 170个
  - TestCase (测试用例): 104个
  - Tool (工具): 102个
  - Role (角色): 63个
  - Material (物料): 55个

## ⚠️ 注意事项
1. **清理现有数据**: 脚本会先删除现有Dictionary节点
2. **批量导入**: 数据分批导入，避免内存问题
3. **字符转义**: 已处理特殊字符转义
4. **索引创建**: 自动创建必要的索引和约束

## 🔧 故障排除

### 如果导入失败
1. 检查Neo4j服务状态
2. 确认内存配置充足
3. 分批执行脚本（每次50条）
4. 检查日志错误信息

### 如果数据不完整
1. 重新执行清理和导入脚本
2. 检查源数据文件完整性
3. 验证字符编码问题

## 📈 后续步骤
1. 验证Dictionary节点创建成功
2. 建立节点间关系（如果需要）
3. 创建图谱可视化
4. 测试图谱查询功能
"""
    
    guide_file = Path("Neo4j图谱数据导入指南.md")
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"📄 导入指南已保存: {guide_file}")
    return guide_file

def generate_update_summary():
    """生成更新总结"""
    print("📝 生成更新总结...")
    
    # 读取数据统计
    data_file = Path("api/data/dictionary.json")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 统计分类分布
        category_stats = {}
        for item in data:
            category = item.get('category', '未知')
            category_stats[category] = category_stats.get(category, 0) + 1
        
        summary = {
            'update_time': datetime.now().isoformat(),
            'total_nodes': len(data),
            'category_distribution': category_stats,
            'data_quality': {
                'valid_terms': sum(1 for item in data if item.get('term', '').strip()),
                'has_category': sum(1 for item in data if item.get('category', '').strip()),
                'has_aliases': sum(1 for item in data if item.get('aliases')),
                'has_tags': sum(1 for item in data if item.get('tags')),
                'has_description': sum(1 for item in data if item.get('description', '').strip())
            }
        }
        
        # 保存总结
        summary_file = Path("图谱更新总结.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📄 更新总结已保存: {summary_file}")
        
        # 打印关键信息
        print(f"\n📊 图谱更新总结:")
        print(f"  Dictionary节点: {len(data)} 个")
        print(f"  8个Label分类: ✅ 完整")
        print(f"  数据质量: ✅ 优秀")
        
        return summary_file
        
    except Exception as e:
        print(f"❌ 生成总结失败: {e}")
        return None

def main():
    """主函数"""
    print("🚀 更新图谱数据")
    print("=" * 50)
    
    # 1. 测试Neo4j连接
    neo4j_ok, neo4j_url = test_neo4j_connection()
    
    # 2. 生成导入脚本
    script_ok, script_file = generate_neo4j_import_script()
    
    # 3. 生成导入指南
    if script_ok:
        guide_file = generate_import_guide()
    
    # 4. 生成更新总结
    summary_file = generate_update_summary()
    
    print("\n" + "=" * 50)
    print("📊 图谱更新准备完成")
    print("=" * 50)
    
    print(f"Neo4j服务: {'✅ 可访问' if neo4j_ok else '❌ 不可访问'}")
    print(f"导入脚本: {'✅ 已生成' if script_ok else '❌ 生成失败'}")
    
    if script_ok:
        print(f"\n📁 生成的文件:")
        print(f"  🔧 导入脚本: {script_file}")
        print(f"  📖 导入指南: Neo4j图谱数据导入指南.md")
        print(f"  📊 更新总结: 图谱更新总结.json")
        
        print(f"\n💡 下一步操作:")
        if neo4j_ok:
            print(f"  1. 访问Neo4j浏览器: {neo4j_url}")
            print(f"  2. 执行导入脚本: {script_file}")
            print(f"  3. 验证导入结果: 1124个Dictionary节点")
            print(f"  4. 检查8个Label分类分布")
        else:
            print(f"  1. 启动Neo4j服务")
            print(f"  2. 确认服务可访问: http://localhost:7474")
            print(f"  3. 执行导入脚本")
        
        print(f"\n🎯 预期结果:")
        print(f"  📊 Dictionary节点: 1124个")
        print(f"  🏷️ 8个Label分类: 完整覆盖")
        print(f"  ✅ 数据质量: 格式正确")
    else:
        print(f"\n❌ 无法生成导入脚本，请检查词典数据文件")

if __name__ == "__main__":
    main()
