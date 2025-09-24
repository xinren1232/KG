#!/usr/bin/env python3
"""
知识图谱推理引擎
集成图数据库推理算法，实现实体链接、关系推断、异常模式识别等高级功能

技术栈:
- NetworkX: 图算法和分析
- scikit-learn: 机器学习算法
- pandas: 数据处理
- Neo4j: 图数据库查询
"""
import json
import pandas as pd
import networkx as nx
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import logging
from collections import defaultdict, Counter
import numpy as np

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGraphEngine:
    """知识图谱推理引擎"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.entity_embeddings = {}
        self.pattern_rules = self._load_pattern_rules()
        
    def _load_pattern_rules(self) -> Dict[str, List[Dict]]:
        """加载推理规则"""
        return {
            'anomaly_patterns': [
                {
                    'name': '组件故障传播',
                    'pattern': 'Anomaly -[:AFFECTS]-> Component -[:PART_OF]-> Product',
                    'inference': 'Product -[:HAS_RISK]-> Anomaly'
                },
                {
                    'name': '相似症状聚类',
                    'pattern': 'Symptom1 -[:SIMILAR_TO]-> Symptom2',
                    'inference': 'Anomaly1 -[:RELATED_TO]-> Anomaly2'
                },
                {
                    'name': '供应商质量关联',
                    'pattern': 'Supplier -[:SUPPLIES]-> Component <-[:AFFECTS]- Anomaly',
                    'inference': 'Supplier -[:QUALITY_ISSUE]-> Anomaly'
                }
            ],
            'test_patterns': [
                {
                    'name': '测试覆盖推理',
                    'pattern': 'TestCase -[:TESTS]-> Component <-[:AFFECTS]- Anomaly',
                    'inference': 'TestCase -[:SHOULD_DETECT]-> Anomaly'
                },
                {
                    'name': '测试优先级推理',
                    'pattern': 'Component -[:HAS_HIGH_FAILURE_RATE]-> True',
                    'inference': 'TestCase -[:HIGH_PRIORITY]-> Component'
                }
            ]
        }
    
    def load_knowledge_graph(self, kg_data: Dict[str, Any]):
        """加载知识图谱数据"""
        logger.info("加载知识图谱数据到推理引擎")
        
        # 清空现有图
        self.graph.clear()
        
        # 添加节点
        for node in kg_data.get('nodes', []):
            self.graph.add_node(
                node['key'],
                type=node['type'],
                name=node['name'],
                **node.get('properties', {})
            )
        
        # 添加边
        for rel in kg_data.get('relationships', []):
            self.graph.add_edge(
                rel['source_key'],
                rel['target_key'],
                relation=rel['relation_type'],
                **rel.get('properties', {})
            )
        
        logger.info(f"图谱加载完成: {self.graph.number_of_nodes()} 节点, {self.graph.number_of_edges()} 边")
    
    def detect_anomaly_patterns(self) -> List[Dict[str, Any]]:
        """检测异常模式"""
        logger.info("检测异常模式")
        patterns = []
        
        # 1. 高频故障组件识别
        component_failure_count = defaultdict(int)
        for node, data in self.graph.nodes(data=True):
            if data.get('type') == 'Anomaly':
                # 查找影响的组件
                for neighbor in self.graph.neighbors(node):
                    neighbor_data = self.graph.nodes[neighbor]
                    if neighbor_data.get('type') == 'Component':
                        component_failure_count[neighbor] += 1
        
        # 识别高风险组件
        if component_failure_count:
            max_failures = max(component_failure_count.values())
            high_risk_components = [
                comp for comp, count in component_failure_count.items()
                if count >= max_failures * 0.7  # 超过70%最大值的组件
            ]
            
            patterns.append({
                'type': 'high_risk_components',
                'description': '高风险组件识别',
                'components': high_risk_components,
                'failure_counts': dict(component_failure_count)
            })
        
        # 2. 供应商质量问题聚类
        supplier_issues = defaultdict(list)
        for node, data in self.graph.nodes(data=True):
            if data.get('type') == 'Supplier':
                # 查找供应商相关的异常
                for path in nx.all_simple_paths(self.graph, node, 
                                               [n for n, d in self.graph.nodes(data=True) 
                                                if d.get('type') == 'Anomaly'], cutoff=3):
                    if len(path) >= 3:  # 至少经过一个中间节点
                        anomaly_node = path[-1]
                        supplier_issues[node].append(anomaly_node)
        
        if supplier_issues:
            patterns.append({
                'type': 'supplier_quality_issues',
                'description': '供应商质量问题聚类',
                'supplier_issues': dict(supplier_issues)
            })
        
        # 3. 症状相似性分析
        symptom_similarity = self._analyze_symptom_similarity()
        if symptom_similarity:
            patterns.append({
                'type': 'symptom_clusters',
                'description': '相似症状聚类',
                'clusters': symptom_similarity
            })
        
        return patterns
    
    def _analyze_symptom_similarity(self) -> List[Dict[str, Any]]:
        """分析症状相似性"""
        symptom_nodes = [
            (node, data) for node, data in self.graph.nodes(data=True)
            if data.get('type') == 'Symptom'
        ]
        
        if len(symptom_nodes) < 2:
            return []
        
        clusters = []
        
        # 简单的基于关键词的相似性分析
        symptom_keywords = {}
        for node, data in symptom_nodes:
            name = data.get('name', '')
            keywords = set(name.split())
            symptom_keywords[node] = keywords
        
        # 查找相似症状
        processed = set()
        for i, (node1, data1) in enumerate(symptom_nodes):
            if node1 in processed:
                continue
                
            cluster = [node1]
            keywords1 = symptom_keywords[node1]
            
            for j, (node2, data2) in enumerate(symptom_nodes[i+1:], i+1):
                if node2 in processed:
                    continue
                    
                keywords2 = symptom_keywords[node2]
                # 计算Jaccard相似度
                intersection = len(keywords1 & keywords2)
                union = len(keywords1 | keywords2)
                
                if union > 0 and intersection / union > 0.3:  # 30%相似度阈值
                    cluster.append(node2)
                    processed.add(node2)
            
            if len(cluster) > 1:
                clusters.append({
                    'symptoms': cluster,
                    'similarity_score': len(set.intersection(*[symptom_keywords[s] for s in cluster])) / 
                                      len(set.union(*[symptom_keywords[s] for s in cluster]))
                })
                processed.update(cluster)
        
        return clusters
    
    def recommend_test_cases(self, anomaly_key: str) -> List[Dict[str, Any]]:
        """为异常推荐相关测试用例"""
        logger.info(f"为异常 {anomaly_key} 推荐测试用例")
        
        recommendations = []
        
        if anomaly_key not in self.graph:
            return recommendations
        
        # 查找异常影响的组件
        affected_components = []
        for neighbor in self.graph.neighbors(anomaly_key):
            neighbor_data = self.graph.nodes[neighbor]
            if neighbor_data.get('type') == 'Component':
                affected_components.append(neighbor)
        
        # 查找测试这些组件的测试用例
        for component in affected_components:
            for node, data in self.graph.nodes(data=True):
                if data.get('type') == 'TestCase':
                    # 检查是否有路径连接测试用例和组件
                    try:
                        if nx.has_path(self.graph, node, component):
                            recommendations.append({
                                'testcase_key': node,
                                'testcase_name': data.get('name', ''),
                                'component': component,
                                'relevance_score': self._calculate_relevance_score(node, anomaly_key),
                                'reason': f'测试受影响组件: {self.graph.nodes[component].get("name", component)}'
                            })
                    except:
                        continue
        
        # 按相关性排序
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return recommendations[:10]  # 返回前10个推荐
    
    def _calculate_relevance_score(self, testcase_key: str, anomaly_key: str) -> float:
        """计算测试用例与异常的相关性分数"""
        try:
            # 基于图距离计算相关性
            if nx.has_path(self.graph, testcase_key, anomaly_key):
                path_length = nx.shortest_path_length(self.graph, testcase_key, anomaly_key)
                return 1.0 / (1.0 + path_length)
            else:
                return 0.0
        except:
            return 0.0
    
    def analyze_centrality(self) -> Dict[str, Any]:
        """分析图中心性"""
        logger.info("分析图中心性")
        
        # 转换为无向图进行中心性分析
        undirected_graph = self.graph.to_undirected()
        
        # 度中心性
        degree_centrality = nx.degree_centrality(undirected_graph)
        
        # 介数中心性
        betweenness_centrality = nx.betweenness_centrality(undirected_graph)
        
        # 特征向量中心性
        try:
            eigenvector_centrality = nx.eigenvector_centrality(undirected_graph, max_iter=1000)
        except:
            eigenvector_centrality = {}
        
        # 找出最重要的节点
        top_nodes = {
            'degree': sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10],
            'betweenness': sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10],
            'eigenvector': sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        }
        
        return {
            'centrality_scores': {
                'degree': degree_centrality,
                'betweenness': betweenness_centrality,
                'eigenvector': eigenvector_centrality
            },
            'top_nodes': top_nodes,
            'analysis': self._interpret_centrality(top_nodes)
        }
    
    def _interpret_centrality(self, top_nodes: Dict[str, List[Tuple[str, float]]]) -> Dict[str, str]:
        """解释中心性分析结果"""
        interpretations = {}
        
        # 度中心性解释
        if top_nodes['degree']:
            top_degree_node = top_nodes['degree'][0][0]
            node_data = self.graph.nodes[top_degree_node]
            interpretations['degree'] = f"连接最多的节点: {node_data.get('name', top_degree_node)} ({node_data.get('type', 'Unknown')})"
        
        # 介数中心性解释
        if top_nodes['betweenness']:
            top_betweenness_node = top_nodes['betweenness'][0][0]
            node_data = self.graph.nodes[top_betweenness_node]
            interpretations['betweenness'] = f"最关键的桥接节点: {node_data.get('name', top_betweenness_node)} ({node_data.get('type', 'Unknown')})"
        
        return interpretations
    
    def find_anomaly_root_causes(self, anomaly_key: str) -> List[Dict[str, Any]]:
        """查找异常的根本原因"""
        logger.info(f"查找异常 {anomaly_key} 的根本原因")
        
        root_causes = []
        
        if anomaly_key not in self.graph:
            return root_causes
        
        # 查找所有可能的根因路径
        for node, data in self.graph.nodes(data=True):
            if data.get('type') == 'RootCause':
                try:
                    if nx.has_path(self.graph, anomaly_key, node):
                        paths = list(nx.all_simple_paths(self.graph, anomaly_key, node, cutoff=5))
                        for path in paths:
                            root_causes.append({
                                'root_cause': node,
                                'root_cause_name': data.get('name', ''),
                                'path': path,
                                'path_length': len(path),
                                'confidence': 1.0 / len(path)  # 路径越短，置信度越高
                            })
                except:
                    continue
        
        # 按置信度排序
        root_causes.sort(key=lambda x: x['confidence'], reverse=True)
        
        return root_causes
    
    def generate_insights(self) -> Dict[str, Any]:
        """生成知识图谱洞察"""
        logger.info("生成知识图谱洞察")
        
        insights = {
            'graph_statistics': {
                'nodes': self.graph.number_of_nodes(),
                'edges': self.graph.number_of_edges(),
                'density': nx.density(self.graph),
                'connected_components': nx.number_weakly_connected_components(self.graph)
            },
            'anomaly_patterns': self.detect_anomaly_patterns(),
            'centrality_analysis': self.analyze_centrality(),
            'entity_distribution': self._analyze_entity_distribution()
        }
        
        return insights
    
    def _analyze_entity_distribution(self) -> Dict[str, int]:
        """分析实体类型分布"""
        distribution = defaultdict(int)
        for node, data in self.graph.nodes(data=True):
            entity_type = data.get('type', 'Unknown')
            distribution[entity_type] += 1
        
        return dict(distribution)

def main():
    """主函数 - 演示推理引擎功能"""
    engine = KnowledgeGraphEngine()
    
    # 加载知识图谱数据
    kg_file = "data/processed/extracted_knowledge_graph.json"
    if Path(kg_file).exists():
        with open(kg_file, 'r', encoding='utf-8') as f:
            kg_data = json.load(f)
        
        engine.load_knowledge_graph(kg_data)
        
        # 生成洞察
        insights = engine.generate_insights()
        
        # 保存洞察结果
        insights_file = "data/processed/kg_insights.json"
        with open(insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights, f, ensure_ascii=False, indent=2)
        
        print("🧠 知识图谱推理分析完成!")
        print(f"📊 图谱统计: {insights['graph_statistics']['nodes']} 节点, {insights['graph_statistics']['edges']} 边")
        print(f"🔍 发现模式: {len(insights['anomaly_patterns'])} 个")
        print(f"💾 洞察已保存到: {insights_file}")

if __name__ == "__main__":
    main()
