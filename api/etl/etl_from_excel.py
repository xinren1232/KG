#!/usr/bin/env python3
"""
ETL脚本：从Excel文件导入来料异常数据到Neo4j知识图谱
基于ontology v0.2设计
"""
import os
import pandas as pd
from neo4j import GraphDatabase
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量配置
EXCEL_PATH = os.getenv("EXCEL_PATH", "./data/来料问题洗后版.xlsx")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password123")

def norm_key(prefix: str, val: str) -> str:
    """标准化实体键值"""
    return f"{prefix}:{str(val).strip()}"

def safe_str(val) -> str:
    """安全字符串转换"""
    if pd.isna(val) or val is None:
        return ""
    return str(val).strip()

def safe_int(val) -> int:
    """安全整数转换"""
    try:
        if pd.isna(val) or val is None:
            return 0
        return int(float(val))
    except (ValueError, TypeError):
        return 0

def safe_float(val) -> float:
    """安全浮点数转换"""
    try:
        if pd.isna(val) or val is None:
            return 0.0
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def run_etl():
    """执行ETL流程"""
    logger.info(f"开始ETL流程，读取文件: {EXCEL_PATH}")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(EXCEL_PATH)
        logger.info(f"成功读取Excel文件，共{len(df)}行数据")
    except Exception as e:
        logger.error(f"读取Excel文件失败: {e}")
        return
    
    # 连接Neo4j
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
        logger.info("成功连接Neo4j数据库")
    except Exception as e:
        logger.error(f"连接Neo4j失败: {e}")
        return
    
    # 处理数据
    processed_count = 0
    error_count = 0
    
    with driver.session() as session:
        for idx, row in df.iterrows():
            try:
                # 提取字段数据
                factory = safe_str(row.get("工厂名称", "")) or "未知工厂"
                project = safe_str(row.get("项目名称", "")) or "未知项目"
                phase = safe_str(row.get("项目阶段", ""))
                mcode = safe_str(row.get("物料编码", "")) or safe_str(row.get("物料编码8码", ""))
                mdesc = safe_str(row.get("物料描述", "")) or "未知物料"
                title = safe_str(row.get("问题描述", "")) or "来料异常"
                defect_num = safe_int(row.get("不良数量", 0))
                defect_rate = safe_float(row.get("不良率", 0))
                symptom = safe_str(row.get("不良现象", "")) or safe_str(row.get("问题描述", ""))
                root_cause = safe_str(row.get("根因", "")) or safe_str(row.get("原因分析", ""))
                cm_temp = safe_str(row.get("临时措施", ""))
                cm_tech = safe_str(row.get("技术措施", ""))
                cm_mgmt = safe_str(row.get("管理措施", ""))
                owner = safe_str(row.get("问题分析责任人", "")) or safe_str(row.get("责任人", ""))
                date_str = safe_str(row.get("日期", "")) or safe_str(row.get("发生日期", ""))
                supplier = safe_str(row.get("供应商", ""))
                
                # 生成主键
                akey = norm_key("Anomaly", f"{factory}-{date_str}-{mcode or 'NA'}-{idx}")
                mkey = norm_key("Material", mcode or mdesc)
                fkey = norm_key("Factory", factory)
                pkey = norm_key("Project", project)
                
                # 创建主要实体和关系
                main_query = """
                MERGE (a:Anomaly {key: $akey})
                  ON CREATE SET 
                    a.title = $title, 
                    a.defects_number = $defects_number, 
                    a.defect_rate = $defect_rate, 
                    a.date = $date, 
                    a.created_at = timestamp()
                  ON MATCH SET 
                    a.title = $title, 
                    a.defects_number = $defects_number, 
                    a.defect_rate = $defect_rate, 
                    a.date = $date, 
                    a.updated_at = timestamp()
                
                MERGE (f:Factory {key: $fkey}) 
                  ON CREATE SET f.name = $factory
                
                MERGE (p:Project {key: $pkey}) 
                  ON CREATE SET p.name = $project, p.phase = $phase
                
                MERGE (m:Material {key: $mkey}) 
                  ON CREATE SET m.code = $mcode, m.desc = $mdesc
                
                MERGE (a)-[:HAPPENED_IN]->(f)
                MERGE (a)-[:RELATED_TO]->(p)
                MERGE (a)-[:INVOLVES]->(m)
                """
                
                session.run(main_query, 
                    akey=akey, title=title, defects_number=defect_num, 
                    defect_rate=defect_rate, date=date_str,
                    fkey=fkey, factory=factory, 
                    pkey=pkey, project=project, phase=phase,
                    mkey=mkey, mcode=mcode, mdesc=mdesc
                )
                
                # 创建症状关系
                if symptom:
                    session.run("""
                        MERGE (s:Symptom {name: $name}) 
                        WITH s 
                        MATCH (a:Anomaly {key: $akey}) 
                        MERGE (a)-[:HAS_SYMPTOM]->(s)
                    """, name=symptom, akey=akey)
                
                # 创建根因关系
                if root_cause:
                    session.run("""
                        MERGE (r:RootCause {name: $name}) 
                        WITH r 
                        MATCH (a:Anomaly {key: $akey}) 
                        MERGE (a)-[:HAS_ROOTCAUSE]->(r)
                    """, name=root_cause, akey=akey)
                
                # 创建对策关系
                countermeasures = [
                    (cm_temp, "临时"),
                    (cm_tech, "技术"), 
                    (cm_mgmt, "管理")
                ]
                
                for cm, ctype in countermeasures:
                    if cm:
                        session.run("""
                            MERGE (c:Countermeasure {name: $name})
                              ON CREATE SET c.type = $type
                            WITH c 
                            MATCH (a:Anomaly {key: $akey})
                            OPTIONAL MATCH (r:RootCause)<-[:HAS_ROOTCAUSE]-(a)
                            FOREACH (root IN CASE WHEN r IS NOT NULL THEN [r] ELSE [] END |
                                MERGE (root)-[:RESOLVED_BY]->(c)
                            )
                        """, name=cm, type=ctype, akey=akey)
                
                # 创建责任人关系
                if owner:
                    okey = norm_key("Owner", owner)
                    session.run("""
                        MERGE (o:Owner {key: $okey})
                          ON CREATE SET o.name = $name
                        WITH o 
                        MATCH (a:Anomaly {key: $akey})
                        MERGE (a)-[:OWNED_BY]->(o)
                    """, okey=okey, name=owner, akey=akey)
                
                # 创建供应商关系
                if supplier:
                    skey = norm_key("Supplier", supplier)
                    session.run("""
                        MERGE (s:Supplier {key: $skey})
                          ON CREATE SET s.name = $name
                        WITH s 
                        MATCH (m:Material {key: $mkey})
                        MERGE (m)-[:SUPPLIED_BY]->(s)
                    """, skey=skey, name=supplier, mkey=mkey)
                
                processed_count += 1
                if processed_count % 10 == 0:
                    logger.info(f"已处理 {processed_count} 条记录")
                    
            except Exception as e:
                error_count += 1
                logger.error(f"处理第{idx+1}行数据时出错: {e}")
                continue
    
    driver.close()
    logger.info(f"ETL流程完成！成功处理: {processed_count} 条，错误: {error_count} 条")

if __name__ == "__main__":
    run_etl()
