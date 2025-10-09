#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neo4j数据库优化脚本 - 创建索引和约束，优化查询性能
"""

import os
import logging
from neo4j import GraphDatabase
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jOptimizer:
    """Neo4j数据库优化器"""
    
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASS", "password123")
        self.driver = None
    
    def connect(self):
        """连接数据库"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("成功连接Neo4j数据库")
        except Exception as e:
            logger.error(f"连接Neo4j失败: {e}")
            raise
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j连接已关闭")
    
    def create_indexes(self):
        """创建索引"""
        logger.info("开始创建索引...")
        
        indexes = [
            # 词典实体索引
            "CREATE INDEX term_name_idx IF NOT EXISTS FOR (t:Term) ON (t.name)",
            "CREATE INDEX term_id_idx IF NOT EXISTS FOR (t:Term) ON (t.id)",
            "CREATE INDEX dictionary_name_idx IF NOT EXISTS FOR (d:Dictionary) ON (d.name)",
            "CREATE INDEX dictionary_id_idx IF NOT EXISTS FOR (d:Dictionary) ON (d.id)",
            
            # 别名索引
            "CREATE INDEX alias_name_idx IF NOT EXISTS FOR (a:Alias) ON (a.name)",
            "CREATE INDEX alias_id_idx IF NOT EXISTS FOR (a:Alias) ON (a.id)",
            
            # 组件索引
            "CREATE INDEX component_name_idx IF NOT EXISTS FOR (c:Component) ON (c.name)",
            "CREATE INDEX component_id_idx IF NOT EXISTS FOR (c:Component) ON (c.id)",
            
            # 症状索引
            "CREATE INDEX symptom_name_idx IF NOT EXISTS FOR (s:Symptom) ON (s.name)",
            "CREATE INDEX symptom_id_idx IF NOT EXISTS FOR (s:Symptom) ON (s.id)",
            
            # 测试用例索引
            "CREATE INDEX testcase_name_idx IF NOT EXISTS FOR (tc:TestCase) ON (tc.name)",
            "CREATE INDEX testcase_id_idx IF NOT EXISTS FOR (tc:TestCase) ON (tc.id)",
            
            # 指标索引
            "CREATE INDEX metric_name_idx IF NOT EXISTS FOR (m:Metric) ON (m.name)",
            "CREATE INDEX metric_id_idx IF NOT EXISTS FOR (m:Metric) ON (m.id)",
            
            # 流程索引
            "CREATE INDEX process_name_idx IF NOT EXISTS FOR (p:Process) ON (p.name)",
            "CREATE INDEX process_id_idx IF NOT EXISTS FOR (p:Process) ON (p.id)",
            
            # 标签索引
            "CREATE INDEX tag_name_idx IF NOT EXISTS FOR (t:Tag) ON (t.name)",
            "CREATE INDEX tag_id_idx IF NOT EXISTS FOR (t:Tag) ON (t.id)",
            
            # 工具索引
            "CREATE INDEX tool_name_idx IF NOT EXISTS FOR (t:Tool) ON (t.name)",
            "CREATE INDEX tool_id_idx IF NOT EXISTS FOR (t:Tool) ON (t.id)",
            
            # 角色索引
            "CREATE INDEX role_name_idx IF NOT EXISTS FOR (r:Role) ON (r.name)",
            "CREATE INDEX role_id_idx IF NOT EXISTS FOR (r:Role) ON (r.id)",
            
            # 材料索引
            "CREATE INDEX material_name_idx IF NOT EXISTS FOR (m:Material) ON (m.name)",
            "CREATE INDEX material_id_idx IF NOT EXISTS FOR (m:Material) ON (m.id)",
            
            # 分类索引
            "CREATE INDEX category_name_idx IF NOT EXISTS FOR (c:Category) ON (c.name)",
            "CREATE INDEX category_id_idx IF NOT EXISTS FOR (c:Category) ON (c.id)",
            
            # 全文搜索索引
            "CREATE FULLTEXT INDEX entity_fulltext_idx IF NOT EXISTS FOR (n:Term|Dictionary|Component|Symptom|TestCase|Metric|Process|Tool|Role|Material|Category) ON EACH [n.name, n.description]",
            
            # 复合索引
            "CREATE INDEX term_name_type_idx IF NOT EXISTS FOR (t:Term) ON (t.name, t.type)",
            "CREATE INDEX component_name_category_idx IF NOT EXISTS FOR (c:Component) ON (c.name, c.category)"
        ]
        
        with self.driver.session() as session:
            for index_query in indexes:
                try:
                    session.run(index_query)
                    logger.info(f"创建索引: {index_query.split('FOR')[0].split('IF')[0].strip()}")
                except Exception as e:
                    logger.warning(f"索引创建失败或已存在: {e}")
        
        logger.info("索引创建完成")
    
    def create_constraints(self):
        """创建约束"""
        logger.info("开始创建约束...")
        
        constraints = [
            # 唯一性约束
            "CREATE CONSTRAINT term_id_unique IF NOT EXISTS FOR (t:Term) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT dictionary_id_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT alias_id_unique IF NOT EXISTS FOR (a:Alias) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT component_id_unique IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT symptom_id_unique IF NOT EXISTS FOR (s:Symptom) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT testcase_id_unique IF NOT EXISTS FOR (tc:TestCase) REQUIRE tc.id IS UNIQUE",
            "CREATE CONSTRAINT metric_id_unique IF NOT EXISTS FOR (m:Metric) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT process_id_unique IF NOT EXISTS FOR (p:Process) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT tag_id_unique IF NOT EXISTS FOR (t:Tag) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT tool_id_unique IF NOT EXISTS FOR (t:Tool) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT role_id_unique IF NOT EXISTS FOR (r:Role) REQUIRE r.id IS UNIQUE",
            "CREATE CONSTRAINT material_id_unique IF NOT EXISTS FOR (m:Material) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT category_id_unique IF NOT EXISTS FOR (c:Category) REQUIRE c.id IS UNIQUE",
            
            # 存在性约束
            "CREATE CONSTRAINT term_name_exists IF NOT EXISTS FOR (t:Term) REQUIRE t.name IS NOT NULL",
            "CREATE CONSTRAINT dictionary_name_exists IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.name IS NOT NULL",
            "CREATE CONSTRAINT component_name_exists IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS NOT NULL"
        ]
        
        with self.driver.session() as session:
            for constraint_query in constraints:
                try:
                    session.run(constraint_query)
                    logger.info(f"创建约束: {constraint_query.split('FOR')[0].split('IF')[0].strip()}")
                except Exception as e:
                    logger.warning(f"约束创建失败或已存在: {e}")
        
        logger.info("约束创建完成")
    
    def analyze_performance(self):
        """分析查询性能"""
        logger.info("开始性能分析...")
        
        performance_queries = [
            # 检查索引使用情况
            "SHOW INDEXES",
            
            # 检查约束
            "SHOW CONSTRAINTS",
            
            # 统计节点数量
            "MATCH (n) RETURN labels(n) as labels, count(n) as count ORDER BY count DESC",
            
            # 统计关系数量
            "MATCH ()-[r]->() RETURN type(r) as type, count(r) as count ORDER BY count DESC",
            
            # 检查孤立节点
            "MATCH (n) WHERE NOT (n)--() RETURN labels(n) as labels, count(n) as count",
            
            # 检查度数分布
            "MATCH (n) WITH n, size((n)--()) as degree RETURN degree, count(n) as count ORDER BY degree DESC LIMIT 10"
        ]
        
        with self.driver.session() as session:
            for query in performance_queries:
                try:
                    result = session.run(query)
                    logger.info(f"查询: {query}")
                    for record in result:
                        logger.info(f"  结果: {dict(record)}")
                    logger.info("---")
                except Exception as e:
                    logger.error(f"性能分析查询失败: {e}")
        
        logger.info("性能分析完成")
    
    def optimize_queries(self):
        """优化常用查询"""
        logger.info("开始查询优化...")
        
        # 预热常用查询
        warmup_queries = [
            # 预热实体查询
            "MATCH (n:Term) RETURN count(n)",
            "MATCH (n:Dictionary) RETURN count(n)",
            "MATCH (n:Component) RETURN count(n)",
            
            # 预热关系查询
            "MATCH ()-[r:RELATED_TO]->() RETURN count(r)",
            "MATCH ()-[r:HAS_TAG]->() RETURN count(r)",
            "MATCH ()-[r:ALIAS_OF]->() RETURN count(r)",
            
            # 预热复杂查询
            "MATCH (n:Term)-[r:RELATED_TO]-(m:Term) RETURN count(r) LIMIT 1000",
            "MATCH (n:Component)-[r:HAS_SYMPTOM]-(s:Symptom) RETURN count(r) LIMIT 1000"
        ]
        
        with self.driver.session() as session:
            for query in warmup_queries:
                try:
                    start_time = datetime.now()
                    result = session.run(query)
                    list(result)  # 消费结果
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    logger.info(f"预热查询完成: {query[:50]}... 耗时: {duration:.3f}秒")
                except Exception as e:
                    logger.error(f"预热查询失败: {e}")
        
        logger.info("查询优化完成")
    
    def cleanup_data(self):
        """清理数据"""
        logger.info("开始数据清理...")
        
        cleanup_queries = [
            # 删除孤立节点（谨慎使用）
            # "MATCH (n) WHERE NOT (n)--() DELETE n",
            
            # 删除重复关系
            """
            MATCH (a)-[r1:RELATED_TO]->(b), (a)-[r2:RELATED_TO]->(b)
            WHERE id(r1) < id(r2)
            DELETE r2
            """,
            
            # 删除自环关系
            "MATCH (n)-[r]->(n) DELETE r",
            
            # 更新统计信息
            "CALL db.stats.retrieve('GRAPH COUNTS')"
        ]
        
        with self.driver.session() as session:
            for query in cleanup_queries:
                try:
                    result = session.run(query)
                    summary = result.consume()
                    logger.info(f"清理查询: {query.strip()[:50]}...")
                    if hasattr(summary, 'counters'):
                        logger.info(f"  删除节点: {summary.counters.nodes_deleted}")
                        logger.info(f"  删除关系: {summary.counters.relationships_deleted}")
                except Exception as e:
                    logger.error(f"数据清理失败: {e}")
        
        logger.info("数据清理完成")
    
    def run_optimization(self):
        """运行完整优化"""
        logger.info("开始Neo4j数据库优化")
        logger.info("=" * 60)
        
        try:
            self.connect()
            
            # 创建索引
            self.create_indexes()
            
            # 创建约束
            self.create_constraints()
            
            # 性能分析
            self.analyze_performance()
            
            # 查询优化
            self.optimize_queries()
            
            # 数据清理（可选）
            # self.cleanup_data()
            
            logger.info("=" * 60)
            logger.info("Neo4j数据库优化完成")
            
        except Exception as e:
            logger.error(f"优化过程中发生错误: {e}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    optimizer = Neo4jOptimizer()
    optimizer.run_optimization()

if __name__ == "__main__":
    main()
