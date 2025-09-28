#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成分批导入命令 - 为Neo4j浏览器生成可执行的分批Cypher命令
"""

import json
from pathlib import Path

def generate_batch_import_commands():
    """生成分批导入命令"""
    print("🔧 生成分批导入命令...")
    
    # 读取词典数据
    data_file = Path("api/data/dictionary.json")
    
    if not data_file.exists():
        print(f"❌ 词典文件不存在: {data_file}")
        return False
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 词典数据: {len(data)} 条")
        
        # 生成分批命令文件
        batch_size = 20  # 每批20条，便于在Neo4j浏览器中执行
        total_batches = (len(data) + batch_size - 1) // batch_size
        
        # 创建命令文件
        commands = []
        
        # 1. 清理和准备命令
        commands.append("// ========================================")
        commands.append("// 步骤1: 清理现有数据")
        commands.append("// ========================================")
        commands.append("MATCH (n:Dictionary) DETACH DELETE n;")
        commands.append("")
        
        commands.append("// ========================================")
        commands.append("// 步骤2: 创建约束和索引")
        commands.append("// ========================================")
        commands.append("CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;")
        commands.append("CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category);")
        commands.append("CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags);")
        commands.append("")
        
        # 2. 分批导入命令
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(data))
            batch_data = data[start_idx:end_idx]
            
            commands.append(f"// ========================================")
            commands.append(f"// 步骤{batch_num + 3}: 导入批次 {batch_num + 1}/{total_batches}")
            commands.append(f"// 第 {start_idx + 1}-{end_idx} 条数据")
            commands.append(f"// ========================================")
            
            # 生成UNWIND批量插入
            commands.append("WITH [")
            
            for i, item in enumerate(batch_data):
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
                
                comma = "," if i < len(batch_data) - 1 else ""
                
                commands.append(f"  {{term: '{term}', category: '{category}', description: '{description}', aliases: {aliases_str}, tags: {tags_str}}}{comma}")
            
            commands.append("] AS batch")
            commands.append("UNWIND batch AS item")
            commands.append("CREATE (d:Dictionary {")
            commands.append("  term: item.term,")
            commands.append("  category: item.category,")
            commands.append("  description: item.description,")
            commands.append("  aliases: item.aliases,")
            commands.append("  tags: item.tags,")
            commands.append("  created_at: datetime(),")
            commands.append("  updated_at: datetime()")
            commands.append("});")
            commands.append("")
            
            # 添加验证命令
            commands.append(f"// 验证批次 {batch_num + 1} 导入结果")
            commands.append("MATCH (d:Dictionary) RETURN count(d) as current_total;")
            commands.append("")
        
        # 3. 最终验证命令
        commands.append("// ========================================")
        commands.append("// 最终验证")
        commands.append("// ========================================")
        commands.append("MATCH (d:Dictionary) RETURN count(d) as total_nodes;")
        commands.append("")
        commands.append("MATCH (d:Dictionary) RETURN d.category, count(d) as count ORDER BY count DESC;")
        commands.append("")
        commands.append("MATCH (d:Dictionary) RETURN d.term, d.category, d.aliases LIMIT 5;")
        
        # 保存完整命令文件
        full_commands_file = Path("完整分批导入命令.cypher")
        with open(full_commands_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(commands))
        
        print(f"✅ 完整命令文件已生成: {full_commands_file}")
        print(f"📊 总批次数: {total_batches}")
        print(f"📊 每批数量: {batch_size}")
        
        # 生成简化的执行指南
        generate_execution_guide(total_batches, batch_size, len(data))
        
        return True
        
    except Exception as e:
        print(f"❌ 生成命令失败: {e}")
        return False

def generate_execution_guide(total_batches, batch_size, total_data):
    """生成执行指南"""
    guide_content = f"""# Neo4j分批导入执行指南

## 🎯 导入目标
- **总数据量**: {total_data} 条
- **分批数量**: {total_batches} 批
- **每批大小**: {batch_size} 条
- **目标节点**: 1124 个Dictionary节点

## 🔧 执行步骤

### 方法1: 完整执行（推荐）
1. 打开Neo4j浏览器: http://localhost:7474
2. 打开文件: `完整分批导入命令.cypher`
3. 复制所有内容到Neo4j查询框
4. 点击执行（可能需要几分钟）

### 方法2: 分步执行（安全）
1. **步骤1**: 执行清理命令
```cypher
MATCH (n:Dictionary) DETACH DELETE n;
```

2. **步骤2**: 创建约束和索引
```cypher
CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;
CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category);
CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags);
```

3. **步骤3-{total_batches + 2}**: 逐批导入数据
   - 从文件中复制每个批次的命令
   - 在Neo4j浏览器中执行
   - 检查每批的验证结果

4. **最终验证**: 执行验证命令
```cypher
MATCH (d:Dictionary) RETURN count(d) as total_nodes;
MATCH (d:Dictionary) RETURN d.category, count(d) as count ORDER BY count DESC;
```

## 📊 预期结果
- **总节点数**: 1124
- **分类分布**:
  - Symptom: 259
  - Metric: 190
  - Component: 181
  - Process: 170
  - TestCase: 104
  - Tool: 102
  - Role: 63
  - Material: 55

## ⚠️ 注意事项
1. **执行前备份**: 如有重要数据请先备份
2. **内存监控**: 大批量导入时注意内存使用
3. **错误处理**: 如遇错误，检查特殊字符或重复数据
4. **分批验证**: 每批执行后检查节点数量

## 🔧 故障排除
- **内存不足**: 减少批次大小到10条
- **字符错误**: 检查单引号和双引号转义
- **重复数据**: 确保term字段唯一
- **连接超时**: 分批执行，避免长时间查询

## ✅ 成功标志
- 总节点数达到1124
- 8个分类完整覆盖
- 无错误信息
- 查询响应正常
"""
    
    guide_file = Path("分批导入执行指南.md")
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"📄 执行指南已保存: {guide_file}")

def main():
    """主函数"""
    print("🚀 生成分批导入命令")
    print("=" * 50)
    
    success = generate_batch_import_commands()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ 分批导入命令生成完成")
        print("=" * 50)
        
        print("📁 生成的文件:")
        print("  🔧 完整命令: 完整分批导入命令.cypher")
        print("  📖 执行指南: 分批导入执行指南.md")
        
        print("\n💡 下一步:")
        print("  1. 访问Neo4j浏览器: http://localhost:7474")
        print("  2. 执行导入命令（选择完整执行或分步执行）")
        print("  3. 验证最终结果: 1124个节点")
        print("  4. 检查8个分类分布")
        
        print("\n🎯 目标:")
        print("  📊 从当前526个节点 → 1124个节点")
        print("  🏷️ 8个Label分类完整覆盖")
        print("  ✅ 图谱数据完全更新")
    else:
        print("\n❌ 命令生成失败")

if __name__ == "__main__":
    main()
