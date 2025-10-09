from neo4j import GraphDatabase, Driver
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver: Optional[Driver] = None
        self._connect()
    
    def _connect(self):
        """建立Neo4j连接"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            raise
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行Cypher查询并返回结果"""
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Query execution failed: {query}, error: {e}")
            raise
    
    def execute_write(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """执行写入操作"""
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Write operation failed: {query}, error: {e}")
            raise
    
    # 知识图谱专用查询方法
    
    def get_products(self) -> List[Dict[str, Any]]:
        """获取所有产品"""
        query = """
        MATCH (p:Product)
        RETURN p.name as name, p.model as model, p.category as category, 
               p.release_date as release_date, p.status as status
        ORDER BY p.name
        """
        return self.execute_query(query)
    
    def get_components_by_product(self, product_name: str) -> List[Dict[str, Any]]:
        """根据产品获取组件"""
        query = """
        MATCH (p:Product {name: $product_name})-[:HAS_COMPONENT]->(c:Component)
        RETURN c.name as name, c.type as type, c.version as version, 
               c.supplier as supplier, c.criticality as criticality
        ORDER BY c.name
        """
        return self.execute_query(query, {"product_name": product_name})
    
    def get_test_cases_by_component(self, product_name: str, component_name: str) -> List[Dict[str, Any]]:
        """根据产品和组件获取测试用例"""
        query = """
        MATCH (p:Product {name: $product_name})-[:HAS_COMPONENT]->(c:Component {name: $component_name})
        MATCH (c)<-[:TESTS]-(tc:TestCase)
        RETURN tc.id as id, tc.title as title, tc.description as description,
               tc.priority as priority, tc.type as type, tc.steps as steps,
               tc.expected_result as expected_result
        ORDER BY tc.priority DESC, tc.id
        """
        return self.execute_query(query, {
            "product_name": product_name,
            "component_name": component_name
        })
    
    def get_anomaly_cause_path(self, symptom_description: str) -> List[Dict[str, Any]]:
        """根据症状描述查找异常因果路径"""
        query = """
        MATCH (s:Symptom)
        WHERE s.description CONTAINS $symptom_description
        MATCH (s)<-[:HAS_SYMPTOM]-(a:Anomaly)
        OPTIONAL MATCH (a)-[:CAUSED_BY]->(rc:RootCause)
        OPTIONAL MATCH (a)-[:SOLVED_BY]->(cm:Countermeasure)
        OPTIONAL MATCH (a)-[:OCCURS_IN]->(c:Component)
        RETURN a.id as anomaly_id, a.title as anomaly_title, a.description as anomaly_description,
               a.severity as severity, a.status as status,
               s.description as symptom,
               rc.description as root_cause,
               cm.description as countermeasure, cm.steps as countermeasure_steps,
               c.name as component
        ORDER BY a.severity DESC
        """
        return self.execute_query(query, {"symptom_description": symptom_description})
    
    def upsert_anomaly(self, anomaly_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建或更新异常记录"""
        query = """
        MERGE (a:Anomaly {id: $anomaly_id})
        SET a.title = $title,
            a.description = $description,
            a.severity = $severity,
            a.status = $status,
            a.created_date = $created_date,
            a.reporter = $reporter
        RETURN a.id as id, a.title as title, a.status as status
        """
        return self.execute_query(query, anomaly_data)[0]
    
    def get_graph_data(self, limit: int = 100) -> Dict[str, Any]:
        """获取图谱可视化数据"""
        # 获取节点 - 优先获取有连接的节点
        if limit and limit > 0:
            nodes_query = """
            MATCH (n)
            WHERE n:Product OR n:Component OR n:Anomaly OR n:TestCase OR n:Symptom OR n:Tool OR n:Process OR n:Metric
            WITH n, size((n)--()) as degree
            WHERE degree > 0
            RETURN id(n) as id, labels(n)[0] as label,
                   coalesce(n.name, n.title, n.id, 'Node_' + toString(id(n))) as name,
                   properties(n) as properties,
                   degree
            ORDER BY degree DESC
            LIMIT $limit
            """
            nodes = self.execute_query(nodes_query, {"limit": limit})
        else:
            # 无限制查询所有节点
            nodes_query = """
            MATCH (n)
            WHERE n:Product OR n:Component OR n:Anomaly OR n:TestCase OR n:Symptom OR n:Tool OR n:Process OR n:Metric
            WITH n, size((n)--()) as degree
            WHERE degree > 0
            RETURN id(n) as id, labels(n)[0] as label,
                   coalesce(n.name, n.title, n.id, 'Node_' + toString(id(n))) as name,
                   properties(n) as properties,
                   degree
            ORDER BY degree DESC
            """
            nodes = self.execute_query(nodes_query)

        # 获取这些节点之间的关系
        if nodes:
            node_ids = [node['id'] for node in nodes]
            edges_query = """
            MATCH (n)-[r]->(m)
            WHERE id(n) IN $node_ids AND id(m) IN $node_ids
            RETURN id(n) as source, id(m) as target, type(r) as relationship,
                   properties(r) as properties
            """
            edges = self.execute_query(edges_query, {"node_ids": node_ids})
        else:
            edges = []

        return {"nodes": nodes, "edges": edges}

    def get_global_stats(self) -> Dict[str, Any]:
        """获取全局统计数据"""
        # 获取总节点数和分类统计
        nodes_stats = self.execute_query("""
            MATCH (n)
            WHERE n:Product OR n:Component OR n:Anomaly OR n:TestCase OR n:Symptom OR n:Tool OR n:Process OR n:Metric
            RETURN labels(n)[0] as label, count(n) as count
        """)

        # 获取总关系数
        relations_stats = self.execute_query("""
            MATCH ()-[r]->()
            WHERE (startNode(r):Product OR startNode(r):Component OR startNode(r):Anomaly OR startNode(r):TestCase OR startNode(r):Symptom OR startNode(r):Tool OR startNode(r):Process OR startNode(r):Metric)
              AND (endNode(r):Product OR endNode(r):Component OR endNode(r):Anomaly OR endNode(r):TestCase OR endNode(r):Symptom OR endNode(r):Tool OR endNode(r):Process OR endNode(r):Metric)
            RETURN count(r) as total_relations
        """)

        total_nodes = sum(stat['count'] for stat in nodes_stats)
        total_relations = relations_stats[0]['total_relations'] if relations_stats else 0
        total_categories = len(nodes_stats)

        return {
            'total_nodes': total_nodes,
            'total_relations': total_relations,
            'total_categories': total_categories,
            'total_tags': 0,  # 可以后续添加标签统计
            'categories': {stat['label']: stat['count'] for stat in nodes_stats}
        }
