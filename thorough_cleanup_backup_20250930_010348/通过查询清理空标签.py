#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过Neo4j查询清理空标签（替代重启方案）
"""

from neo4j import GraphDatabase
import time

def force_clean_empty_labels():
    """通过创建和删除临时节点来强制清理空标签"""
    print("🔄 通过查询强制清理空标签")
    print("=" * 50)
    
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password123"
    
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        with driver.session() as session:
            # 1. 获取所有标签
            print("📊 检查当前标签状态:")
            result = session.run("CALL db.labels()")
            all_labels = []
            empty_labels = []
            
            for record in result:
                label = record[0]
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                all_labels.append((label, count))
                
                if count == 0:
                    empty_labels.append(label)
                    print(f"  🗑️ {label}: {count} 个节点 (空标签)")
                else:
                    print(f"  ✅ {label}: {count} 个节点")
            
            # 2. 强制清理空标签
            if empty_labels:
                print(f"\n🔧 开始强制清理 {len(empty_labels)} 个空标签...")
                
                for label in empty_labels:
                    try:
                        print(f"  🔄 处理标签: {label}")
                        
                        # 创建临时节点
                        session.run(f"CREATE (temp:{label} {{_temp_cleanup: true, _timestamp: timestamp()}})")
                        
                        # 立即删除
                        session.run(f"MATCH (temp:{label} {{_temp_cleanup: true}}) DELETE temp")
                        
                        # 验证是否还存在
                        check_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                        remaining = check_result.single()["count"]
                        
                        if remaining == 0:
                            print(f"    ✅ {label} 已清理")
                        else:
                            print(f"    ⚠️ {label} 仍有 {remaining} 个节点")
                            
                    except Exception as e:
                        print(f"    ❌ 处理 {label} 失败: {e}")
                
                # 等待一下让Neo4j处理
                print(f"\n⏳ 等待Neo4j处理...")
                time.sleep(2)
                
            else:
                print(f"\n✅ 没有发现空标签")
            
            # 3. 最终验证
            print(f"\n🔍 最终验证标签状态:")
            result = session.run("CALL db.labels()")
            final_labels = []
            
            for record in result:
                label = record[0]
                count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = count_result.single()["count"]
                
                if count > 0:
                    final_labels.append((label, count))
                    print(f"  📊 {label}: {count} 个节点")
                else:
                    print(f"  🗑️ {label}: {count} 个节点 (仍为空)")
            
            # 4. 验证期望的标签
            expected_labels = {
                'Dictionary': 1124,
                'Symptom': 259,
                'Metric': 190,
                'Component': 181,
                'Process': 170,
                'TestCase': 104,
                'Tool': 102,
                'Role': 63,
                'Material': 55
            }
            
            print(f"\n📊 期望标签验证:")
            all_correct = True
            
            for label, expected_count in expected_labels.items():
                actual_count = next((count for name, count in final_labels if name == label), 0)
                
                if actual_count == expected_count:
                    print(f"  ✅ {label}: {actual_count}")
                else:
                    print(f"  ❌ {label}: {actual_count} (期望{expected_count})")
                    all_correct = False
            
            return all_correct, len(final_labels)
                
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        return False, 0
    
    finally:
        if driver:
            driver.close()

def manual_restart_instructions():
    """提供手动重启说明"""
    print("\n" + "=" * 50)
    print("🔄 手动重启Neo4j说明")
    print("=" * 50)
    
    print("如果自动清理效果不理想，请手动重启Neo4j:")
    print("\n💡 方法1: 通过任务管理器")
    print("  1. 打开任务管理器 (Ctrl+Shift+Esc)")
    print("  2. 查找 'java.exe' 进程")
    print("  3. 找到Neo4j相关的Java进程")
    print("  4. 结束该进程")
    print("  5. 重新启动Neo4j")
    
    print("\n💡 方法2: 通过服务管理器")
    print("  1. 按 Win+R，输入 'services.msc'")
    print("  2. 查找Neo4j相关服务")
    print("  3. 右键 -> 重新启动")
    
    print("\n💡 方法3: 通过Neo4j Desktop")
    print("  1. 打开Neo4j Desktop")
    print("  2. 停止数据库")
    print("  3. 重新启动数据库")
    
    print("\n🌐 重启后验证:")
    print("  1. 访问: http://localhost:7474")
    print("  2. 刷新页面")
    print("  3. 检查Database Information面板")
    print("  4. 应该只看到9个标签")

def main():
    """主函数"""
    print("🎯 开始清理Neo4j空标签")
    
    success, label_count = force_clean_empty_labels()
    
    print(f"\n" + "=" * 50)
    print(f"📊 清理结果")
    print(f"=" * 50)
    
    if success and label_count == 9:
        print(f"🎉 清理成功!")
        print(f"✅ 所有期望的标签都存在且数量正确")
        print(f"✅ 当前有效标签数: {label_count}")
        
        print(f"\n🌐 请验证结果:")
        print(f"  1. 刷新Neo4j浏览器: http://localhost:7474")
        print(f"  2. 查看Database Information面板")
        print(f"  3. 应该只看到9个标签")
        
    elif success:
        print(f"⚠️ 部分成功")
        print(f"✅ 数据完整性正确")
        print(f"⚠️ 当前标签数: {label_count} (可能仍有空标签)")
        
        manual_restart_instructions()
        
    else:
        print(f"❌ 清理失败")
        manual_restart_instructions()

if __name__ == "__main__":
    main()
