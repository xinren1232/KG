#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱查询服务
"""

from neo4j import GraphDatabase
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class KGQueryService:
    """知识图谱查询服务"""
    
    def __init__(self, uri: str, user: str, password: str):
        """初始化"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        """关闭连接"""
        self.driver.close()
    
    def diagnose(self, symptom: str, max_depth: int = 3, min_confidence: float = 0.6) -> Dict:
        """
        故障诊断：查找症状的根因链路
        
        Args:
            symptom: 症状名称
            max_depth: 最大深度
            min_confidence: 最小置信度
        
        Returns:
            诊断结果
        """
        with self.driver.session() as session:
            # 查找因果链路
            result = session.run("""
                MATCH path = (symptom:Term {name: $symptom})<-[:CAUSES*1..3]-(cause:Term)
                WHERE all(r in relationships(path) WHERE r.confidence >= $min_conf)
                WITH path, 
                     reduce(conf = 1.0, r in relationships(path) | conf * r.confidence) as chain_confidence
                WHERE chain_confidence >= $min_conf
                RETURN [n in nodes(path) | {name: n.name, category: n.category}] as nodes,
                       [r in relationships(path) | {
                           type: type(r), 
                           confidence: r.confidence, 
                           evidence: r.evidence,
                           severity: r.severity,
                           phase: r.phase
                       }] as relations,
                       chain_confidence
                ORDER BY chain_confidence DESC
                LIMIT 10
            """, symptom=symptom, min_conf=min_confidence)
            
            causal_chains = []
            for record in result:
                causal_chains.append({
                    'nodes': record['nodes'],
                    'relations': record['relations'],
                    'confidence': round(record['chain_confidence'], 3)
                })
            
            # 查找解决方案
            result = session.run("""
                MATCH (symptom:Term {name: $symptom})-[r:RESOLVED_BY]->(solution:Term)
                WHERE r.confidence >= $min_conf
                RETURN solution.name as solution,
                       solution.category as category,
                       solution.description as description,
                       r.confidence as confidence,
                       r.effectiveness as effectiveness,
                       r.risk as risk,
                       r.cost_level as cost_level,
                       r.evidence as evidence
                ORDER BY r.effectiveness DESC, r.confidence DESC
                LIMIT 5
            """, symptom=symptom, min_conf=min_confidence)
            
            solutions = []
            for record in result:
                solutions.append({
                    'name': record['solution'],
                    'category': record['category'],
                    'description': record['description'],
                    'confidence': record['confidence'],
                    'effectiveness': record['effectiveness'],
                    'risk': record['risk'],
                    'cost_level': record['cost_level'],
                    'evidence': record['evidence']
                })
            
            return {
                'symptom': symptom,
                'causal_chains': causal_chains,
                'solutions': solutions,
                'total_chains': len(causal_chains),
                'total_solutions': len(solutions)
            }
    
    def get_prevention_measures(self, symptom: str, min_confidence: float = 0.6) -> Dict:
        """
        获取预防措施
        
        Args:
            symptom: 症状名称
            min_confidence: 最小置信度
        
        Returns:
            预防措施列表
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (solution:Term)-[r:PREVENTS]->(symptom:Term {name: $symptom})
                WHERE r.confidence >= $min_conf
                RETURN solution.name as measure,
                       solution.category as category,
                       solution.description as description,
                       r.confidence as confidence,
                       r.evidence_level as evidence_level,
                       r.evidence as evidence
                ORDER BY r.confidence DESC
            """, symptom=symptom, min_conf=min_confidence)
            
            measures = []
            for record in result:
                measures.append({
                    'name': record['measure'],
                    'category': record['category'],
                    'description': record['description'],
                    'confidence': record['confidence'],
                    'evidence_level': record['evidence_level'],
                    'evidence': record['evidence']
                })
            
            return {
                'symptom': symptom,
                'prevention_measures': measures,
                'total': len(measures)
            }
    
    def get_test_path(self, target: str, target_category: str, 
                     min_confidence: float = 0.6) -> Dict:
        """
        获取测试路径
        
        Args:
            target: 目标名称（组件/流程/症状）
            target_category: 目标分类
            min_confidence: 最小置信度
        
        Returns:
            测试路径
        """
        with self.driver.session() as session:
            # 查找测试用例
            result = session.run("""
                MATCH (test:Term {category: 'TestCase'})-[r:TESTS|DETECTS]->(target:Term {name: $target, category: $category})
                WHERE r.confidence >= $min_conf
                RETURN test.name as test_name,
                       test.description as description,
                       type(r) as relation_type,
                       r.confidence as confidence,
                       r.coverage as coverage,
                       r.env as env,
                       r.method as method,
                       r.evidence as evidence
                ORDER BY r.confidence DESC
            """, target=target, category=target_category, min_conf=min_confidence)
            
            tests = []
            for record in result:
                tests.append({
                    'name': record['test_name'],
                    'description': record['description'],
                    'relation_type': record['relation_type'],
                    'confidence': record['confidence'],
                    'coverage': record['coverage'],
                    'env': record['env'],
                    'method': record['method'],
                    'evidence': record['evidence']
                })
            
            # 查找测试指标
            result = session.run("""
                MATCH (test:Term {category: 'TestCase'})-[r1:TESTS|DETECTS]->(target:Term {name: $target, category: $category})
                MATCH (test)-[r2:MEASURES]->(metric:Term {category: 'Metric'})
                WHERE r1.confidence >= $min_conf AND r2.confidence >= $min_conf
                RETURN test.name as test_name,
                       metric.name as metric_name,
                       metric.description as metric_desc,
                       r2.threshold as threshold,
                       r2.method as method
            """, target=target, category=target_category, min_conf=min_confidence)
            
            metrics = []
            for record in result:
                metrics.append({
                    'test_name': record['test_name'],
                    'metric_name': record['metric_name'],
                    'metric_description': record['metric_desc'],
                    'threshold': record['threshold'],
                    'method': record['method']
                })
            
            return {
                'target': target,
                'category': target_category,
                'tests': tests,
                'metrics': metrics,
                'total_tests': len(tests),
                'total_metrics': len(metrics)
            }
    
    def get_dependencies(self, component: str, direction: str = 'both', 
                        max_depth: int = 2, min_confidence: float = 0.6) -> Dict:
        """
        获取组件依赖关系
        
        Args:
            component: 组件名称
            direction: 方向 (upstream/downstream/both)
            max_depth: 最大深度
            min_confidence: 最小置信度
        
        Returns:
            依赖关系
        """
        with self.driver.session() as session:
            dependencies = {}
            
            # 上游依赖（当前组件依赖的其他组件）
            if direction in ['upstream', 'both']:
                result = session.run(f"""
                    MATCH path = (comp:Term {{name: $component}})-[:DEPENDS_ON*1..{max_depth}]->(dep:Term)
                    WHERE all(r in relationships(path) WHERE r.confidence >= $min_conf)
                    WITH path,
                         reduce(conf = 1.0, r in relationships(path) | conf * r.confidence) as chain_confidence
                    RETURN [n in nodes(path) | {{name: n.name, category: n.category}}] as nodes,
                           [r in relationships(path) | {{
                               criticality: r.criticality,
                               interface: r.interface,
                               confidence: r.confidence,
                               evidence: r.evidence
                           }}] as relations,
                           chain_confidence
                    ORDER BY chain_confidence DESC
                    LIMIT 20
                """, component=component, min_conf=min_confidence)
                
                upstream = []
                for record in result:
                    upstream.append({
                        'nodes': record['nodes'],
                        'relations': record['relations'],
                        'confidence': round(record['chain_confidence'], 3)
                    })
                dependencies['upstream'] = upstream
            
            # 下游依赖（依赖当前组件的其他组件）
            if direction in ['downstream', 'both']:
                result = session.run(f"""
                    MATCH path = (dep:Term)-[:DEPENDS_ON*1..{max_depth}]->(comp:Term {{name: $component}})
                    WHERE all(r in relationships(path) WHERE r.confidence >= $min_conf)
                    WITH path,
                         reduce(conf = 1.0, r in relationships(path) | conf * r.confidence) as chain_confidence
                    RETURN [n in nodes(path) | {{name: n.name, category: n.category}}] as nodes,
                           [r in relationships(path) | {{
                               criticality: r.criticality,
                               interface: r.interface,
                               confidence: r.confidence,
                               evidence: r.evidence
                           }}] as relations,
                           chain_confidence
                    ORDER BY chain_confidence DESC
                    LIMIT 20
                """, component=component, min_conf=min_confidence)
                
                downstream = []
                for record in result:
                    downstream.append({
                        'nodes': record['nodes'],
                        'relations': record['relations'],
                        'confidence': round(record['chain_confidence'], 3)
                    })
                dependencies['downstream'] = downstream
            
            return {
                'component': component,
                'direction': direction,
                'dependencies': dependencies,
                'total_upstream': len(dependencies.get('upstream', [])),
                'total_downstream': len(dependencies.get('downstream', []))
            }

