#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase

class RelationshipFixer:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password123"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def check_current_status(self):
        """检查当前状态"""
        print("🔍 检查当前图谱状态")
        print("=" * 50)

        with self.driver.session() as session:
            # 节点统计
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)

            total_nodes = 0
            print("📊 当前节点分布:")
            for record in node_result:
                count = record['count']
                total_nodes += count
                print(f"  {record['label']}: {count} 个")

            # 关系统计
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)

            total_rels = 0
            print(f"\n🔗 当前关系分布:")
            rel_list = list(rel_result)
            if rel_list:
                for record in rel_list:
                    count = record['count']
                    total_rels += count
                    print(f"  {record['rel_type']}: {count} 个")
            else:
                print("  (暂无关系)")

            print(f"\n📈 当前总计:")
            print(f"  节点数: {total_nodes}")
            print(f"  关系数: {total_rels}")

            return total_nodes, total_rels

    def create_relationships_safe(self):
        """安全地创建关系"""
        print("\n🔗 安全创建关系")
        print("=" * 50)

        total_created = 0

        with self.driver.session() as session:
            # 1. Component -> Symptom
            print("  创建 Component -> Symptom 关系...")
            try:
                result1 = session.run("""
                    MATCH (c:Component), (s:Symptom)
                    WHERE size(c.tags) > 0 AND size(s.tags) > 0
                    WITH c, s, [tag IN c.tags WHERE tag IN s.tags] AS common_tags,
                         size(c.tags) AS a, size(s.tags) AS b
                    WITH c, s, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (c)-[r:HAS_SYMPTOM]->(s)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result1.single()
                created1 = record['created'] if record else 0
                total_created += created1
                print(f"    创建了 {created1} 个 HAS_SYMPTOM 关系")
            except Exception as e:
                print(f"    ❌ 创建 HAS_SYMPTOM 关系失败: {e}")
                created1 = 0

            # 2. TestCase -> Tool
            print("  创建 TestCase -> Tool 关系...")
            try:
                result2 = session.run("""
                    MATCH (tc:TestCase), (t:Tool)
                    WHERE size(tc.tags) > 0 AND size(t.tags) > 0
                    WITH tc, t, [tag IN tc.tags WHERE tag IN t.tags] AS common_tags,
                         size(tc.tags) AS a, size(t.tags) AS b
                    WITH tc, t, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (tc)-[r:USES_TOOL]->(t)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result2.single()
                created2 = record['created'] if record else 0
                total_created += created2
                print(f"    创建了 {created2} 个 USES_TOOL 关系")
            except Exception as e:
                print(f"    ❌ 创建 USES_TOOL 关系失败: {e}")
                created2 = 0

            # 3. TestCase -> Metric
            print("  创建 TestCase -> Metric 关系...")
            try:
                result3 = session.run("""
                    MATCH (tc:TestCase), (m:Metric)
                    WHERE size(tc.tags) > 0 AND size(m.tags) > 0
                    WITH tc, m, [tag IN tc.tags WHERE tag IN m.tags] AS common_tags,
                         size(tc.tags) AS a, size(m.tags) AS b
                    WITH tc, m, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (tc)-[r:MEASURES]->(m)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result3.single()
                created3 = record['created'] if record else 0
                total_created += created3
                print(f"    创建了 {created3} 个 MEASURES 关系")
            except Exception as e:
                print(f"    ❌ 创建 MEASURES 关系失败: {e}")
                created3 = 0

            # 4. Process -> Material
            print("  创建 Process -> Material 关系...")
            try:
                result4 = session.run("""
                    MATCH (p:Process), (m:Material)
                    WHERE size(p.tags) > 0 AND size(m.tags) > 0
                    WITH p, m, [tag IN p.tags WHERE tag IN m.tags] AS common_tags,
                         size(p.tags) AS a, size(m.tags) AS b
                    WITH p, m, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (p)-[r:CONSUMES]->(m)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result4.single()
                created4 = record['created'] if record else 0
                total_created += created4
                print(f"    创建了 {created4} 个 CONSUMES 关系")
            except Exception as e:
                print(f"    ❌ 创建 CONSUMES 关系失败: {e}")
                created4 = 0

            # 6. TestCase -> Component
            print("  创建 TestCase -> Component 关系...")
            try:
                result_tc_comp = session.run("""
                    MATCH (tc:TestCase), (c:Component)
                    WHERE size(tc.tags) > 0 AND size(c.tags) > 0
                    WITH tc, c, [tag IN tc.tags WHERE tag IN c.tags] AS common_tags,
                         size(tc.tags) AS a, size(c.tags) AS b
                    WITH tc, c, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (tc)-[r:TESTS]->(c)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result_tc_comp.single()
                created_tc_comp = record['created'] if record else 0
                total_created += created_tc_comp
                print(f"    创建了 {created_tc_comp} 个 TESTS 关系")
            except Exception as e:
                print(f"    ❌ 创建 TESTS 关系失败: {e}")
                created_tc_comp = 0

            # 5. Process -> Tool
            print("  创建 Process -> Tool 关系...")
            try:
                result5 = session.run("""
                    MATCH (p:Process), (t:Tool)
                    WHERE size(p.tags) > 0 AND size(t.tags) > 0
                    WITH p, t, [tag IN p.tags WHERE tag IN t.tags] AS common_tags,
                         size(p.tags) AS a, size(t.tags) AS b
                    WITH p, t, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (p)-[r:USES_TOOL]->(t)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result5.single()
                created5 = record['created'] if record else 0
                total_created += created5
                print(f"    创建了 {created5} 个 USES_TOOL 关系")
            except Exception as e:
                print(f"    ❌ 创建 USES_TOOL 关系失败: {e}")
                created5 = 0

            # 6. Component -> Component (相关组件)
            print("  创建 Component -> Component 关系...")
            try:
                result6 = session.run("""
                    MATCH (c1:Component), (c2:Component)
                    WHERE id(c1) < id(c2)
                      AND size(c1.tags) > 0 AND size(c2.tags) > 0
                    WITH c1, c2, [tag IN c1.tags WHERE tag IN c2.tags] AS common_tags,
                         size(c1.tags) AS a, size(c2.tags) AS b
                    WITH c1, c2, common_tags, size(common_tags) AS cCount, a, b,
                         (toFloat(size(common_tags)) / (a + b - size(common_tags))) AS jaccard
                    WHERE cCount >= 2 AND jaccard >= 0.3
                    MERGE (c1)-[r:RELATED_TO]->(c2)
                    SET r.confidence = jaccard,
                        r.inferred = true,
                        r.rule = 'tag_overlap',
                        r.common_tags = common_tags,
                        r.common_count = cCount,
                        r.created_at = datetime()
                    RETURN count(r) as created
                """)
                record = result6.single()
                created6 = record['created'] if record else 0
                total_created += created6
                print(f"    创建了 {created6} 个 RELATED_TO 关系")
            except Exception as e:
                print(f"    ❌ 创建 RELATED_TO 关系失败: {e}")
                created6 = 0

        print(f"\n✅ 关系创建完成，总计: {total_created} 个")
        return total_created

    def verify_final_result(self):
        """验证最终结果"""
        print("\n🔍 验证最终结果")
        print("=" * 50)

        with self.driver.session() as session:
            # 节点统计
            node_result = session.run("""
                MATCH (n)
                WHERE n:Component OR n:Symptom OR n:Tool OR n:Process OR n:TestCase OR n:Material OR n:Role OR n:Metric
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)

            total_nodes = 0
            print("📊 最终节点分布:")
            for record in node_result:
                count = record['count']
                total_nodes += count
                print(f"  {record['label']}: {count} 个")

            # 关系统计
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
                ORDER BY count DESC
            """)

            total_rels = 0
            print(f"\n🔗 最终关系分布:")
            for record in rel_result:
                count = record['count']
                total_rels += count
                print(f"  {record['rel_type']}: {count} 个")

            print(f"\n📈 最终总计:")
            print(f"  节点数: {total_nodes}")
            print(f"  关系数: {total_rels}")

            return total_nodes, total_rels

def main():
    """主函数"""
    print("🎯 修复关系创建")
    print("=" * 80)

    fixer = RelationshipFixer()

    try:
        # 1. 检查当前状态
        current_nodes, current_rels = fixer.check_current_status()

        # 2. 创建关系
        relationships_created = fixer.create_relationships_safe()

        # 3. 验证结果
        final_nodes, final_rels = fixer.verify_final_result()

        # 4. 总结
        print(f"\n" + "=" * 80)
        print(f"🎉 关系修复完成！")
        print(f"=" * 80)

        print(f"📊 修复统计:")
        print(f"  修复前关系数: {current_rels}")
        print(f"  新创建关系数: {relationships_created}")
        print(f"  修复后关系数: {final_rels}")

        print(f"\n📈 最终结果:")
        print(f"  总节点数: {final_nodes} (目标: 1124)")
        print(f"  总关系数: {final_rels}")

        if final_nodes == 1124:
            print(f"\n🎉 完美！图谱包含纯净的1124条词典数据")

        if final_rels > 0:
            print(f"🎉 关系创建成功！包含多种关系类型")

            # 计算关系类型数量
            with fixer.driver.session() as session:
                rel_types_result = session.run("""
                    MATCH ()-[r]->()
                    RETURN DISTINCT type(r) as rel_type
                """)
                rel_types = [record['rel_type'] for record in rel_types_result]
                print(f"📊 关系类型数: {len(rel_types)} 种")
                print(f"  关系类型: {', '.join(rel_types)}")

        print(f"\n🌐 现在可以访问前端查看重建后的图谱:")
        print(f"  - 图谱可视化: http://localhost:5173/#/graph-visualization")
        print(f"  - 词典管理: http://localhost:5173/#/dictionary")

    except Exception as e:
        print(f"❌ 修复过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        fixer.close()

if __name__ == "__main__":
    main()
