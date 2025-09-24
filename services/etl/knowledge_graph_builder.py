#!/usr/bin/env python3
"""
知识图谱构建器
将抽取的实体和关系构建成Neo4j知识图谱
"""

import logging
import os

from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
import hashlib
from collections import defaultdict, Counter

from neo4j import GraphDatabase
from file_extractor import ExtractedEntity, ExtractedRelation, ExtractionResult

logger = logging.getLogger(__name__)

@dataclass
class GraphStats:
    """图谱统计信息"""
    total_nodes: int
    total_relationships: int
    node_types: Dict[str, int]
    relationship_types: Dict[str, int]
    source_files: List[str]

class KnowledgeGraphBuilder:
    """知识图谱构建器"""

    def __init__(self, neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j",
                 neo4j_password: str = "password"):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.driver = None

        # 实体去重和合并配置
        self.entity_similarity_threshold = 0.8
        self.merge_strategies = {
            'product': self._merge_product_entities,
            'component': self._merge_component_entities,
            'test_case': self._merge_test_case_entities,
            'anomaly': self._merge_anomaly_entities
        }

    def connect(self):
        """连接Neo4j数据库"""
        try:
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            # 测试连接
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("Neo4j连接成功")
        except Exception as e:
            logger.error(f"Neo4j连接失败: {e}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.driver:
            self.driver.close()

    def initialize_schema(self):
        """初始化图谱模式"""
        with self.driver.session() as session:
            # 创建约束和索引
            constraints = [
                "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
                "CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT component_id IF NOT EXISTS FOR (c:Component) REQUIRE c.id IS UNIQUE",
                "CREATE CONSTRAINT test_case_id IF NOT EXISTS FOR (t:TestCase) REQUIRE t.id IS UNIQUE",
                "CREATE CONSTRAINT anomaly_id IF NOT EXISTS FOR (a:Anomaly) REQUIRE a.id IS UNIQUE",
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"创建约束: {constraint}")
                except Exception as e:
                    logger.warning(f"约束创建失败 (可能已存在): {e}")

            # 创建索引
            indexes = [
                "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
                "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
                "CREATE INDEX source_file IF NOT EXISTS FOR (e:Entity) ON (e.source_file)",
            ]

            for index in indexes:
                try:
                    session.run(index)
                    logger.info(f"创建索引: {index}")
                except Exception as e:
                    logger.warning(f"索引创建失败 (可能已存在): {e}")

    def build_graph_from_extraction(self, extraction_result: ExtractionResult) -> Dict[str, Any]:
        """从抽取结果构建知识图谱"""
        if not self.driver:
            self.connect()

        # 数据预处理和去重
        cleaned_entities = self._clean_and_deduplicate_entities(extraction_result.entities)
        cleaned_relations = self._clean_and_deduplicate_relations(extraction_result.relations)

        # 构建图谱
        id_to_key = {e.id: getattr(e, 'key', None) for e in cleaned_entities}
        with self.driver.session() as session:
            # 创建实体节点（按 key 幂等）
            created_nodes = self._create_entities(session, cleaned_entities)

            # 创建关系（按 key 连接）
            created_relationships = self._create_relationships(session, cleaned_relations, id_to_key)

            # 更新文件元数据
            self._update_file_metadata(session, extraction_result)

        return {
            'created_nodes': created_nodes,
            'created_relationships': created_relationships,
            'source_file': extraction_result.file_path,
            'processing_errors': extraction_result.errors
        }

    def _clean_and_deduplicate_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """清洗和去重实体"""
        # 按类型分组
        entities_by_type = defaultdict(list)
        for entity in entities:
            entities_by_type[entity.type].append(entity)

        cleaned_entities = []

        for entity_type, type_entities in entities_by_type.items():
            # 去重和合并
            if entity_type in self.merge_strategies:
                merged_entities = self.merge_strategies[entity_type](type_entities)
            else:
                merged_entities = self._default_merge_entities(type_entities)

            cleaned_entities.extend(merged_entities)

        return cleaned_entities

    def _clean_and_deduplicate_relations(self, relations: List[ExtractedRelation]) -> List[ExtractedRelation]:
        """清洗和去重关系"""
        # 使用集合去重相同的关系
        unique_relations = {}

        for relation in relations:
            # 创建关系的唯一标识
            relation_key = (
                relation.source_entity,
                relation.target_entity,
                relation.relation_type
            )

            if relation_key not in unique_relations:
                unique_relations[relation_key] = relation
            else:
                # 合并属性和提高置信度
                existing = unique_relations[relation_key]
                existing.confidence = max(existing.confidence, relation.confidence)
                existing.properties.update(relation.properties)

        return list(unique_relations.values())

    def _create_entities(self, session, entities: List[ExtractedEntity]) -> int:
        """创建实体节点（按 key 幂等）"""
        created_count = 0

        for entity in entities:
            # 构建节点标签：通用 Entity + 具体业务标签
            label = entity.properties.get('label') if isinstance(entity.properties, dict) else None
            label = label or entity.type.title()
            labels = ['Entity', label]
            labels_str = ':'.join(labels)

            # 元数据与属性
            properties = {
                'key': getattr(entity, 'key', None),
                'id': entity.id,
                'name': entity.name,
                'type': label,
                'source': entity.source_file,
                'doc_id': os.path.basename(entity.source_file) if entity.source_file else None,
                'source_location': entity.source_location,
                'created_by': 'etl',
                **(entity.properties or {})
            }

            # 创建或更新（按 key）
            cypher = f"""
            MERGE (e:{labels_str} {{key: $key}})
            SET e += $properties,
                e.created_at = coalesce(e.created_at, datetime()),
                e.updated_at = datetime()
            RETURN e
            """

            try:
                result = session.run(cypher, key=properties['key'], properties=properties)
                if result.single():
                    created_count += 1
            except Exception as e:
                logger.error(f"创建实体节点失败 key={properties.get('key')}: {e}")

        logger.info(f"创建了 {created_count} 个实体节点")
        return created_count

    def _create_relationships(self, session, relations: List[ExtractedRelation], id_to_key: Dict[str, str]) -> int:
        """创建关系（按 key 匹配节点，标准化关系类型）"""
        created_count = 0
        REL_MAP = {
            'CONTAINS': 'INCLUDES',
            'TESTS': 'RESULT_OF',
            'AFFECTS': 'AFFECTS',
            'BELONGS_TO': 'BELONGS_TO',
            'CO_OCCURS': 'DOCUMENTED_IN',
            'RELATED_TO': 'DOCUMENTED_IN',
            'HAS_SYMPTOM': 'HAS_SYMPTOM',
            'CAUSES': 'CAUSES',
            'RESOLVED_BY': 'RESOLVED_BY',
            'DUPLICATE_OF': 'DUPLICATE_OF',
            'SUPPLIED_BY': 'SUPPLIED_BY',
            'OWNED_BY': 'OWNED_BY',
            'DOCUMENTED_IN': 'DOCUMENTED_IN',
            'INCLUDES': 'INCLUDES',
        }

        for relation in relations:
            source_key = id_to_key.get(relation.source_entity)
            target_key = id_to_key.get(relation.target_entity)
            if not source_key or not target_key:
                continue
            rtype = REL_MAP.get(relation.relation_type.upper(), relation.relation_type.upper())

            properties = {
                'confidence': relation.confidence,
                'source': relation.source_file,
                **(relation.properties or {})
            }

            cypher = f"""
            MATCH (source {{key: $source_key}})
            MATCH (target {{key: $target_key}})
            MERGE (source)-[r:{rtype}]->(target)
            SET r += $properties,
                r.created_at = coalesce(r.created_at, datetime()),
                r.updated_at = datetime()
            RETURN r
            """

            try:
                result = session.run(
                    cypher,
                    source_key=source_key,
                    target_key=target_key,
                    properties=properties
                )
                if result.single():
                    created_count += 1
            except Exception as e:
                logger.error(f"创建关系失败 {source_key}->{target_key}: {e}")

        logger.info(f"创建了 {created_count} 个关系")
        return created_count

    def _update_file_metadata(self, session, extraction_result: ExtractionResult):
        """更新文件元数据"""
        metadata = {
            'file_path': extraction_result.file_path,
            'file_type': extraction_result.file_type,
            'processed_at': 'datetime()',
            'entity_count': len(extraction_result.entities),
            'relation_count': len(extraction_result.relations),
            'errors': extraction_result.errors,
            **extraction_result.metadata
        }

        cypher = """
        MERGE (f:File {path: $file_path})
        SET f += $metadata,
            f.processed_at = datetime()
        RETURN f
        """

        try:
            session.run(cypher, file_path=extraction_result.file_path, metadata=metadata)
            logger.info(f"更新文件元数据: {extraction_result.file_path}")
        except Exception as e:
            logger.error(f"更新文件元数据失败: {e}")

    def _merge_product_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """合并产品实体"""
        return self._merge_by_name_similarity(entities, threshold=0.9)

    def _merge_component_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """合并组件实体"""
        return self._merge_by_name_similarity(entities, threshold=0.8)

    def _merge_test_case_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """合并测试用例实体"""
        # 测试用例通常有唯一ID，按ID合并
        return self._merge_by_exact_name(entities)

    def _merge_anomaly_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """合并异常实体"""
        return self._merge_by_name_similarity(entities, threshold=0.85)

    def _default_merge_entities(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """默认实体合并策略"""
        return self._merge_by_name_similarity(entities, threshold=0.8)

    def _merge_by_name_similarity(self, entities: List[ExtractedEntity], threshold: float = 0.8) -> List[ExtractedEntity]:
        """基于名称相似度合并实体"""
        if not entities:
            return []

        merged = []
        used_indices = set()

        for i, entity1 in enumerate(entities):
            if i in used_indices:
                continue

            # 找到相似的实体
            similar_entities = [entity1]
            used_indices.add(i)

            for j, entity2 in enumerate(entities[i+1:], i+1):
                if j in used_indices:
                    continue

                similarity = self._calculate_name_similarity(entity1.name, entity2.name)
                if similarity >= threshold:
                    similar_entities.append(entity2)
                    used_indices.add(j)

            # 合并相似实体
            merged_entity = self._merge_similar_entities(similar_entities)
            merged.append(merged_entity)

        return merged

    def _merge_by_exact_name(self, entities: List[ExtractedEntity]) -> List[ExtractedEntity]:
        """基于精确名称合并实体"""
        entity_groups = defaultdict(list)

        for entity in entities:
            entity_groups[entity.name].append(entity)

        merged = []
        for name, group in entity_groups.items():
            merged_entity = self._merge_similar_entities(group)
            merged.append(merged_entity)

        return merged

    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """计算名称相似度"""
        # 简单的Jaccard相似度
        set1 = set(name1.lower().split())
        set2 = set(name2.lower().split())

        if not set1 and not set2:
            return 1.0

        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        return intersection / union if union > 0 else 0.0

    def _merge_similar_entities(self, entities: List[ExtractedEntity]) -> ExtractedEntity:
        """合并相似实体"""
        if len(entities) == 1:
            return entities[0]

        # 选择最完整的实体作为基础
        base_entity = max(entities, key=lambda e: len(e.properties))

        # 合并属性
        merged_properties = {}
        source_files = set()
        source_locations = []

        for entity in entities:
            merged_properties.update(entity.properties)
            source_files.add(entity.source_file)
            source_locations.append(entity.source_location)

        # 创建合并后的实体
        merged_entity = ExtractedEntity(
            id=base_entity.id,
            name=base_entity.name,
            type=base_entity.type,
            properties={
                **merged_properties,
                'merged_from': len(entities),
                'all_source_files': list(source_files)
            },
            source_file=base_entity.source_file,
            source_location='; '.join(source_locations)
        )

        return merged_entity

    def get_graph_stats(self) -> GraphStats:
        """获取图谱统计信息"""
        if not self.driver:
            self.connect()

        with self.driver.session() as session:
            # 节点统计
            node_stats = session.run("""
                MATCH (n:Entity)
                RETURN n.type as type, count(n) as count
            """).data()

            # 关系统计
            rel_stats = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
            """).data()

            # 总数统计
            total_nodes = session.run("MATCH (n:Entity) RETURN count(n) as count").single()['count']
            total_rels = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()['count']

            # 源文件统计
            source_files = session.run("""
                MATCH (f:File)
                RETURN f.path as file_path
            """).data()

        return GraphStats(
            total_nodes=total_nodes,
            total_relationships=total_rels,
            node_types={item['type']: item['count'] for item in node_stats},
            relationship_types={item['type']: item['count'] for item in rel_stats},
            source_files=[item['file_path'] for item in source_files]
        )

    def query_graph(self, cypher_query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行图谱查询"""
        if not self.driver:
            self.connect()

        with self.driver.session() as session:
            result = session.run(cypher_query, parameters or {})
            return result.data()

    def clear_graph(self):
        """清空图谱数据"""
        if not self.driver:
            self.connect()

        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("图谱数据已清空")

# 使用示例
if __name__ == "__main__":
    from file_extractor import FileExtractor

    # 初始化
    extractor = FileExtractor()
    builder = KnowledgeGraphBuilder()

    try:
        # 连接数据库并初始化模式
        builder.connect()
        builder.initialize_schema()

        # 处理测试文件
        test_files = [
            "../../data/raw/测试用例样本数据.xlsx",
            "../../data/raw/异常数据样本.xlsx"
        ]

        for file_path in test_files:
            if os.path.exists(file_path):
                print(f"\n处理文件: {file_path}")

                # 抽取数据
                extraction_result = extractor.extract_file(file_path)

                # 构建图谱
                build_result = builder.build_graph_from_extraction(extraction_result)

                print(f"创建节点: {build_result['created_nodes']}")
                print(f"创建关系: {build_result['created_relationships']}")

        # 显示图谱统计
        stats = builder.get_graph_stats()
        print("\n图谱统计:")
        print(f"总节点数: {stats.total_nodes}")
        print(f"总关系数: {stats.total_relationships}")
        print(f"节点类型: {stats.node_types}")
        print(f"关系类型: {stats.relationship_types}")

    finally:
        builder.close()
