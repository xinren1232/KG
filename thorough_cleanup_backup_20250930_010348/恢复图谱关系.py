#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
from neo4j import GraphDatabase
from pathlib import Path

class RelationshipRestorer:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def check_existing_relations(self):
        """检查现有关系"""
        print("🔍 检查现有关系")
        print("=" * 50)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)
            
            relations = list(result)
            total = sum(r['count'] for r in relations)
            
            print(f"当前关系总数: {total}")
            for rel in relations:
                print(f"  {rel['rel_type']}: {rel['count']} 个")
            
            return relations, total
    
    def check_available_relation_files(self):
        """检查可用的关系文件"""
        print("\n🔍 检查可用的关系文件")
        print("=" * 50)
        
        relation_files = []
        suggestions_dir = Path("data/relations/suggestions")
        
        if suggestions_dir.exists():
            for file in suggestions_dir.glob("*.csv"):
                if file.stat().st_size > 100:  # 只考虑有实际内容的文件
                    try:
                        df = pd.read_csv(file)
                        if len(df) > 0:
                            relation_files.append({
                                'file': str(file),
                                'count': len(df),
                                'type': self.get_relation_type_from_filename(file.name)
                            })
                            print(f"  {file.name}: {len(df)} 条关系 -> {self.get_relation_type_from_filename(file.name)}")
                    except Exception as e:
                        print(f"  ❌ {file.name}: 读取失败 - {e}")
        
        total_available = sum(f['count'] for f in relation_files)
        print(f"\n可用关系总数: {total_available} 条")
        
        return relation_files
    
    def get_relation_type_from_filename(self, filename):
        """从文件名推断关系类型"""
        mapping = {
            'component_has_symptom.csv': 'HAS_SYMPTOM',
            'testcases_measures_metrics.csv': 'MEASURES',
            'testcases_uses_tools.csv': 'USES_TOOL',
            'process_uses_tools.csv': 'USES_TOOL',
            'process_consumes_materials.csv': 'CONSUMES'
        }
        return mapping.get(filename, 'RELATED_TO')
    
    def get_node_labels_from_filename(self, filename):
        """从文件名推断节点标签"""
        mapping = {
            'component_has_symptom.csv': ('Component', 'Symptom'),
            'testcases_measures_metrics.csv': ('TestCase', 'Metric'),
            'testcases_uses_tools.csv': ('TestCase', 'Tool'),
            'process_uses_tools.csv': ('Process', 'Tool'),
            'process_consumes_materials.csv': ('Process', 'Material')
        }
        return mapping.get(filename, ('Unknown', 'Unknown'))
    
    def clear_existing_relations(self):
        """清除现有的错误关系（只保留HAS_SYMPTOM以外的关系）"""
        print("\n🧹 清除现有的HAS_SYMPTOM关系")
        print("=" * 50)
        
        with self.driver.session() as session:
            # 只删除HAS_SYMPTOM关系，因为这些是错误导入的
            result = session.run("""
                MATCH ()-[r:HAS_SYMPTOM]->()
                DELETE r
                RETURN count(r) as deleted_count
            """)
            
            deleted = result.single()['deleted_count']
            print(f"✅ 已删除 {deleted} 个HAS_SYMPTOM关系")
            
            return deleted
    
    def import_relations_from_file(self, file_info, dry_run=False):
        """从文件导入关系"""
        file_path = file_info['file']
        rel_type = file_info['type']
        filename = Path(file_path).name
        source_label, target_label = self.get_node_labels_from_filename(filename)
        
        print(f"\n📥 导入关系: {filename}")
        print(f"  关系类型: ({source_label})-[:{rel_type}]->({target_label})")
        
        try:
            df = pd.read_csv(file_path)
            
            created = 0
            skipped = 0
            missing = 0
            
            with self.driver.session() as session:
                for _, row in df.iterrows():
                    source_term = row['source_term']
                    target_term = row['target_term']
                    confidence = row.get('confidence', 1.0)
                    source = row.get('source', 'auto_import')
                    note = row.get('note', '')
                    
                    if dry_run:
                        # 只检查节点是否存在
                        source_exists = session.run(f"""
                            MATCH (n:{source_label})
                            WHERE n.name = $term OR n.term = $term
                            RETURN count(n) > 0 as exists
                        """, term=source_term).single()['exists']
                        
                        target_exists = session.run(f"""
                            MATCH (n:{target_label})
                            WHERE n.name = $term OR n.term = $term
                            RETURN count(n) > 0 as exists
                        """, term=target_term).single()['exists']
                        
                        if source_exists and target_exists:
                            created += 1
                        else:
                            missing += 1
                    else:
                        # 实际创建关系
                        result = session.run(f"""
                            MATCH (a:{source_label})
                            WHERE a.name = $source_term OR a.term = $source_term
                            MATCH (b:{target_label})
                            WHERE b.name = $target_term OR b.term = $target_term
                            MERGE (a)-[r:{rel_type}]->(b)
                            SET r.confidence = $confidence,
                                r.source = $source,
                                r.note = $note,
                                r.created_at = datetime()
                            RETURN count(r) as created
                        """, source_term=source_term, target_term=target_term, 
                             confidence=confidence, source=source, note=note)
                        
                        if result.single()['created'] > 0:
                            created += 1
                        else:
                            missing += 1
            
            print(f"  ✅ 成功: {created} 个")
            print(f"  ❌ 缺失节点: {missing} 个")
            
            return created, missing
            
        except Exception as e:
            print(f"  ❌ 导入失败: {e}")
            return 0, 0
    
    def restore_all_relations(self, dry_run=False):
        """恢复所有关系"""
        print(f"\n🚀 {'模拟' if dry_run else '开始'}恢复所有关系")
        print("=" * 50)
        
        # 1. 检查现有关系
        existing_relations, existing_total = self.check_existing_relations()
        
        # 2. 检查可用文件
        relation_files = self.check_available_relation_files()
        
        if not relation_files:
            print("❌ 没有找到可用的关系文件")
            return
        
        # 3. 清除错误关系（只在非dry_run模式下）
        if not dry_run and existing_total > 0:
            deleted = self.clear_existing_relations()
        
        # 4. 导入新关系
        total_created = 0
        total_missing = 0
        
        for file_info in relation_files:
            created, missing = self.import_relations_from_file(file_info, dry_run)
            total_created += created
            total_missing += missing
        
        # 5. 验证结果
        if not dry_run:
            print(f"\n🔍 验证导入结果")
            print("=" * 50)
            
            final_relations, final_total = self.check_existing_relations()
            
            print(f"\n📊 导入总结:")
            print(f"  导入前关系数: {existing_total}")
            print(f"  导入后关系数: {final_total}")
            print(f"  新增关系数: {total_created}")
            print(f"  缺失节点数: {total_missing}")
            
            if final_total >= 7000:
                print(f"\n🎉 关系恢复成功！达到预期的7000+关系")
            else:
                print(f"\n⚠️ 关系数量仍不足，可能需要更多关系数据")
        else:
            print(f"\n📊 模拟结果:")
            print(f"  可创建关系数: {total_created}")
            print(f"  缺失节点数: {total_missing}")

def main():
    """主函数"""
    print("🎯 图谱关系恢复工具")
    print("=" * 80)
    
    restorer = RelationshipRestorer()
    
    try:
        # 先进行模拟运行
        print("第一步：模拟运行，检查可恢复的关系数量")
        restorer.restore_all_relations(dry_run=True)
        
        # 询问是否继续
        print(f"\n" + "=" * 80)
        response = input("是否继续执行实际的关系恢复？(y/n): ").strip().lower()
        
        if response == 'y':
            print("\n第二步：执行实际的关系恢复")
            restorer.restore_all_relations(dry_run=False)
        else:
            print("❌ 用户取消操作")
        
    except Exception as e:
        print(f"❌ 恢复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        restorer.close()

if __name__ == "__main__":
    main()
