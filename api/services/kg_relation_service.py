#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱关系服务
"""

from neo4j import GraphDatabase
from typing import Dict, List, Optional, Tuple
import hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class KGRelationService:
    """知识图谱关系服务"""
    
    def __init__(self, uri: str, user: str, password: str):
        """初始化"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """关闭连接"""
        self.driver.close()
    
    def _generate_source_hash(self, source_name: str, target_name: str, 
                             evidence: str, source: str) -> str:
        """生成source_hash"""
        hash_input = f"{source_name}|{target_name}|{evidence}|{source}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _determine_status(self, confidence: float) -> str:
        """根据置信度确定状态"""
        if confidence >= 0.8:
            return 'verified'
        elif confidence >= 0.6:
            return 'plausible'
        else:
            return 'uncertain'
    
    def upsert_relation(self, relation_type: str, source: Dict, target: Dict, 
                       props: Dict) -> Tuple[bool, str, Optional[str]]:
        """
        插入或更新关系
        
        Args:
            relation_type: 关系类型
            source: 源节点 {name, category}
            target: 目标节点 {name, category}
            props: 关系属性
        
        Returns:
            (success, message, relation_id)
        """
        with self.driver.session() as session:
            try:
                # 生成source_hash
                source_hash = self._generate_source_hash(
                    source['name'], target['name'],
                    props.get('evidence', ''), props.get('source', '')
                )
                
                # 检查是否已存在
                existing = session.run("""
                    MATCH (s:Term {name: $source_name, category: $source_cat})
                          -[r]->
                          (t:Term {name: $target_name, category: $target_cat})
                    WHERE r.source_hash = $source_hash
                    RETURN type(r) as rel_type, id(r) as rel_id
                """, source_name=source['name'], source_cat=source['category'],
                     target_name=target['name'], target_cat=target['category'],
                     source_hash=source_hash).single()
                
                if existing:
                    return (False, f"关系已存在: {existing['rel_type']}", str(existing['rel_id']))
                
                # 确定状态
                status = self._determine_status(props.get('confidence', 0.7))
                
                # 准备属性
                rel_props = {
                    'confidence': props.get('confidence', 0.7),
                    'evidence': props.get('evidence', ''),
                    'source': props.get('source', 'manual'),
                    'source_hash': source_hash,
                    'status': status,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                # 添加可选属性
                optional_fields = [
                    'doc_id', 'chunk_id', 'severity', 'phase',
                    'effectiveness', 'risk', 'cost_level', 'evidence_level',
                    'criticality', 'interface', 'mode', 'direction',
                    'coverage', 'env', 'method', 'threshold'
                ]
                for field in optional_fields:
                    if field in props:
                        rel_props[field] = props[field]
                
                # 创建关系
                result = session.run(f"""
                    MERGE (s:Term {{name: $source_name, category: $source_cat}})
                    MERGE (t:Term {{name: $target_name, category: $target_cat}})
                    CREATE (s)-[r:{relation_type}]->(t)
                    SET r = $props
                    RETURN id(r) as rel_id
                """, source_name=source['name'], source_cat=source['category'],
                     target_name=target['name'], target_cat=target['category'],
                     props=rel_props).single()
                
                rel_id = result['rel_id']
                logger.info(f"创建关系: {relation_type} ({source['name']} -> {target['name']})")
                
                return (True, "关系创建成功", str(rel_id))
                
            except Exception as e:
                logger.error(f"创建关系失败: {str(e)}")
                return (False, f"创建关系失败: {str(e)}", None)
    
    def batch_upsert_relations(self, relations: List[Dict]) -> Dict:
        """
        批量插入关系
        
        Args:
            relations: 关系列表
        
        Returns:
            {success: int, failed: int, errors: List[str]}
        """
        success_count = 0
        failed_count = 0
        errors = []
        created_ids = []
        
        for i, rel in enumerate(relations):
            success, message, rel_id = self.upsert_relation(
                rel['relation_type'],
                rel['source'],
                rel['target'],
                rel['props']
            )
            
            if success:
                success_count += 1
                if rel_id:
                    created_ids.append(rel_id)
            else:
                failed_count += 1
                errors.append(f"关系 {i+1}: {message}")
        
        return {
            'success': success_count,
            'failed': failed_count,
            'errors': errors,
            'created_ids': created_ids
        }
    
    def detect_conflicts(self, relation_type: str, source: Dict, target: Dict) -> List[Dict]:
        """
        检测冲突关系
        
        Args:
            relation_type: 关系类型
            source: 源节点
            target: 目标节点
        
        Returns:
            冲突关系列表
        """
        with self.driver.session() as session:
            # 定义冲突规则
            conflict_rules = {
                'CAUSES': ['PREVENTS'],  # 如果A导致B，则A不应该预防B
                'PREVENTS': ['CAUSES'],
                'RESOLVED_BY': [],
                'DEPENDS_ON': []
            }
            
            if relation_type not in conflict_rules:
                return []
            
            conflict_types = conflict_rules[relation_type]
            if not conflict_types:
                return []
            
            # 查询冲突关系
            conflict_query = f"""
                MATCH (s:Term {{name: $source_name, category: $source_cat}})
                      -[r]->
                      (t:Term {{name: $target_name, category: $target_cat}})
                WHERE type(r) IN $conflict_types
                RETURN type(r) as rel_type, r.confidence as confidence, 
                       r.evidence as evidence, r.source as source
            """
            
            result = session.run(
                conflict_query,
                source_name=source['name'], source_cat=source['category'],
                target_name=target['name'], target_cat=target['category'],
                conflict_types=conflict_types
            )
            
            conflicts = []
            for record in result:
                conflicts.append({
                    'type': record['rel_type'],
                    'confidence': record['confidence'],
                    'evidence': record['evidence'],
                    'source': record['source']
                })
            
            return conflicts
    
    def get_relation_stats(self) -> Dict:
        """获取关系统计"""
        with self.driver.session() as session:
            # 关系类型统计
            result = session.run("""
                MATCH ()-[r:CAUSES|RESOLVED_BY|PREVENTS|DEPENDS_ON|INTERACTS_WITH|DETECTS|TESTS|MEASURES|AFFECTS]->()
                RETURN type(r) as rel_type,
                       count(r) as total,
                       avg(r.confidence) as avg_confidence,
                       sum(CASE WHEN r.status = 'verified' THEN 1 ELSE 0 END) as verified,
                       sum(CASE WHEN r.status = 'plausible' THEN 1 ELSE 0 END) as plausible,
                       sum(CASE WHEN r.status = 'uncertain' THEN 1 ELSE 0 END) as uncertain,
                       sum(CASE WHEN r.confidence < 0.7 THEN 1 ELSE 0 END) as low_confidence
                ORDER BY total DESC
            """)
            
            stats = []
            for record in result:
                stats.append({
                    'type': record['rel_type'],
                    'total': record['total'],
                    'avg_confidence': round(record['avg_confidence'], 3) if record['avg_confidence'] else 0,
                    'verified': record['verified'],
                    'plausible': record['plausible'],
                    'uncertain': record['uncertain'],
                    'low_confidence': record['low_confidence']
                })
            
            return {'relation_stats': stats}

