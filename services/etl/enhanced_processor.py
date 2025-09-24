#!/usr/bin/env python3
"""
增强版ETL数据处理器
支持多种数据格式、数据验证、清洗和转换
"""

import pandas as pd
import json
import csv
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
from dataclasses import dataclass

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent / "api"))

from database.neo4j_client import Neo4jClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """数据验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    cleaned_data: Optional[pd.DataFrame] = None

@dataclass
class ProcessingStats:
    """处理统计信息"""
    total_records: int = 0
    processed_records: int = 0
    failed_records: int = 0
    skipped_records: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_test_case_data(df: pd.DataFrame) -> ValidationResult:
        """验证测试用例数据"""
        errors = []
        warnings = []
        
        # 检查必要列
        required_columns = ['产品名称', '组件名称', '用例ID', '用例标题']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"缺少必要列: {missing_columns}")
        
        # 检查数据完整性
        for idx, row in df.iterrows():
            if pd.isna(row.get('用例ID')) or not str(row.get('用例ID')).strip():
                errors.append(f"第{idx+1}行: 用例ID不能为空")
            
            if pd.isna(row.get('用例标题')) or not str(row.get('用例标题')).strip():
                errors.append(f"第{idx+1}行: 用例标题不能为空")
            
            # 检查用例ID格式
            case_id = str(row.get('用例ID', '')).strip()
            if case_id and not re.match(r'^TC-[A-Z]+-\d+$', case_id):
                warnings.append(f"第{idx+1}行: 用例ID格式建议为 TC-XXX-001")
        
        # 数据清洗
        cleaned_df = df.copy()
        
        # 清理空白字符
        for col in cleaned_df.select_dtypes(include=['object']).columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            cleaned_df[col] = cleaned_df[col].replace('nan', '')
        
        # 标准化优先级
        if '优先级' in cleaned_df.columns:
            priority_map = {
                '高': 'high', '中': 'medium', '低': 'low', '紧急': 'critical',
                'high': 'high', 'medium': 'medium', 'low': 'low', 'critical': 'critical'
            }
            cleaned_df['优先级'] = cleaned_df['优先级'].map(priority_map).fillna('medium')
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cleaned_data=cleaned_df
        )
    
    @staticmethod
    def validate_anomaly_data(df: pd.DataFrame) -> ValidationResult:
        """验证异常数据"""
        errors = []
        warnings = []
        
        # 检查必要列
        required_columns = ['异常ID', '异常标题', '组件名称']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"缺少必要列: {missing_columns}")
        
        # 检查数据完整性
        for idx, row in df.iterrows():
            if pd.isna(row.get('异常ID')) or not str(row.get('异常ID')).strip():
                errors.append(f"第{idx+1}行: 异常ID不能为空")
            
            # 检查异常ID格式
            anomaly_id = str(row.get('异常ID', '')).strip()
            if anomaly_id and not re.match(r'^ANO-\d{4}-\d+$', anomaly_id):
                warnings.append(f"第{idx+1}行: 异常ID格式建议为 ANO-YYYY-001")
        
        # 数据清洗
        cleaned_df = df.copy()
        
        # 清理空白字符
        for col in cleaned_df.select_dtypes(include=['object']).columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            cleaned_df[col] = cleaned_df[col].replace('nan', '')
        
        # 标准化严重程度
        if '严重程度' in cleaned_df.columns:
            severity_map = {
                '严重': 'critical', '高': 'high', '中': 'medium', '低': 'low',
                'critical': 'critical', 'high': 'high', 'medium': 'medium', 'low': 'low'
            }
            cleaned_df['严重程度'] = cleaned_df['严重程度'].map(severity_map).fillna('medium')
        
        # 标准化状态
        if '状态' in cleaned_df.columns:
            status_map = {
                '开放': 'open', '处理中': 'in_progress', '已解决': 'resolved', '已关闭': 'closed',
                'open': 'open', 'in_progress': 'in_progress', 'resolved': 'resolved', 'closed': 'closed'
            }
            cleaned_df['状态'] = cleaned_df['状态'].map(status_map).fillna('open')
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            cleaned_data=cleaned_df
        )

class EnhancedETLProcessor:
    """增强版ETL处理器"""
    
    def __init__(self):
        self.neo4j_client = Neo4jClient(
            uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASS", "password123")
        )
        self.validator = DataValidator()
        self.stats = ProcessingStats()
    
    def process_file(self, file_path: str, file_type: str = None) -> ProcessingStats:
        """处理单个文件"""
        logger.info(f"开始处理文件: {file_path}")
        self.stats = ProcessingStats(start_time=datetime.now())
        
        try:
            # 自动检测文件类型
            if not file_type:
                file_type = self._detect_file_type(file_path)
            
            # 读取文件
            df = self._read_file(file_path, file_type)
            if df is None:
                return self.stats
            
            self.stats.total_records = len(df)
            
            # 确定数据类型
            data_type = self._detect_data_type(df, file_path)
            
            # 验证和清洗数据
            validation_result = self._validate_data(df, data_type)
            if not validation_result.is_valid:
                logger.error(f"数据验证失败: {validation_result.errors}")
                return self.stats
            
            if validation_result.warnings:
                for warning in validation_result.warnings:
                    logger.warning(warning)
            
            # 处理数据
            if data_type == 'test_case':
                success_count = self._process_test_cases(validation_result.cleaned_data)
            elif data_type == 'anomaly':
                success_count = self._process_anomalies(validation_result.cleaned_data)
            else:
                logger.error(f"未知的数据类型: {data_type}")
                return self.stats
            
            self.stats.processed_records = success_count
            self.stats.failed_records = self.stats.total_records - success_count
            
        except Exception as e:
            logger.error(f"处理文件失败: {e}")
        finally:
            self.stats.end_time = datetime.now()
            self._log_stats()
        
        return self.stats
    
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        ext = Path(file_path).suffix.lower()
        if ext in ['.xlsx', '.xls']:
            return 'excel'
        elif ext == '.csv':
            return 'csv'
        elif ext == '.json':
            return 'json'
        else:
            raise ValueError(f"不支持的文件类型: {ext}")
    
    def _read_file(self, file_path: str, file_type: str) -> Optional[pd.DataFrame]:
        """读取文件"""
        try:
            if file_type == 'excel':
                return pd.read_excel(file_path)
            elif file_type == 'csv':
                return pd.read_csv(file_path, encoding='utf-8-sig')
            elif file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            else:
                raise ValueError(f"不支持的文件类型: {file_type}")
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            return None
    
    def _detect_data_type(self, df: pd.DataFrame, file_path: str) -> str:
        """检测数据类型"""
        file_name = Path(file_path).name.lower()
        
        # 基于文件名检测
        if '测试用例' in file_name or 'testcase' in file_name:
            return 'test_case'
        elif '异常' in file_name or 'anomaly' in file_name:
            return 'anomaly'
        
        # 基于列名检测
        columns = [col.lower() for col in df.columns]
        if '用例id' in columns or '用例标题' in columns:
            return 'test_case'
        elif '异常id' in columns or '异常标题' in columns:
            return 'anomaly'
        
        # 默认返回测试用例
        return 'test_case'
    
    def _validate_data(self, df: pd.DataFrame, data_type: str) -> ValidationResult:
        """验证数据"""
        if data_type == 'test_case':
            return self.validator.validate_test_case_data(df)
        elif data_type == 'anomaly':
            return self.validator.validate_anomaly_data(df)
        else:
            return ValidationResult(False, [f"未知数据类型: {data_type}"], [])
    
    def _process_test_cases(self, df: pd.DataFrame) -> int:
        """处理测试用例数据"""
        success_count = 0
        
        for index, row in df.iterrows():
            try:
                # 创建或更新产品
                self._upsert_product(row['产品名称'])
                
                # 创建或更新组件
                self._upsert_component(row['组件名称'])
                
                # 建立产品-组件关系
                self._create_product_component_relation(row['产品名称'], row['组件名称'])
                
                # 创建测试用例
                self._upsert_test_case(row)
                
                # 建立测试用例-组件关系
                self._create_testcase_component_relation(row['用例ID'], row['组件名称'])
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"处理第{index+1}行测试用例失败: {e}")
                continue
        
        return success_count
    
    def _process_anomalies(self, df: pd.DataFrame) -> int:
        """处理异常数据"""
        success_count = 0
        
        for index, row in df.iterrows():
            try:
                # 创建异常
                self._upsert_anomaly(row)
                
                # 创建症状（如果有）
                if pd.notna(row.get('症状描述')) and str(row.get('症状描述')).strip():
                    self._upsert_symptom(row['症状描述'])
                    self._create_anomaly_symptom_relation(row['异常ID'], row['症状描述'])
                
                # 创建根因（如果有）
                if pd.notna(row.get('根因描述')) and str(row.get('根因描述')).strip():
                    self._upsert_root_cause(row['根因描述'])
                    self._create_anomaly_root_cause_relation(row['异常ID'], row['根因描述'])
                
                # 创建对策（如果有）
                if pd.notna(row.get('对策描述')) and str(row.get('对策描述')).strip():
                    self._upsert_countermeasure(row['对策描述'])
                    self._create_anomaly_countermeasure_relation(row['异常ID'], row['对策描述'])
                
                # 建立异常-组件关系
                if pd.notna(row.get('组件名称')) and str(row.get('组件名称')).strip():
                    self._create_anomaly_component_relation(row['异常ID'], row['组件名称'])
                
                success_count += 1
                
            except Exception as e:
                logger.error(f"处理第{index+1}行异常数据失败: {e}")
                continue
        
        return success_count
    
    def _log_stats(self):
        """记录统计信息"""
        duration = (self.stats.end_time - self.stats.start_time).total_seconds()
        logger.info(f"处理完成 - 总记录: {self.stats.total_records}, "
                   f"成功: {self.stats.processed_records}, "
                   f"失败: {self.stats.failed_records}, "
                   f"耗时: {duration:.2f}秒")
    
    # 数据库操作方法（复用之前的实现）
    def _upsert_product(self, product_name: str):
        """创建或更新产品"""
        query = """
        MERGE (p:Product {name: $name})
        SET p.status = 'active', p.updated_at = datetime()
        RETURN p.name
        """
        self.neo4j_client.execute_write(query, {"name": product_name})
    
    def _upsert_component(self, component_name: str):
        """创建或更新组件"""
        query = """
        MERGE (c:Component {name: $name})
        SET c.type = 'unknown', c.updated_at = datetime()
        RETURN c.name
        """
        self.neo4j_client.execute_write(query, {"name": component_name})
    
    def _create_product_component_relation(self, product_name: str, component_name: str):
        """建立产品-组件关系"""
        query = """
        MATCH (p:Product {name: $product_name})
        MATCH (c:Component {name: $component_name})
        MERGE (p)-[:HAS_COMPONENT]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "product_name": product_name,
            "component_name": component_name
        })
    
    def _upsert_test_case(self, row: pd.Series):
        """创建或更新测试用例"""
        query = """
        MERGE (tc:TestCase {id: $id})
        SET tc.title = $title,
            tc.description = $description,
            tc.priority = $priority,
            tc.type = $type,
            tc.steps = $steps,
            tc.expected_result = $expected_result,
            tc.updated_at = datetime()
        RETURN tc.id
        """
        
        # 处理测试步骤
        steps = row.get('测试步骤', '')
        if isinstance(steps, str) and steps:
            steps = [step.strip() for step in steps.split('\n') if step.strip()]
        else:
            steps = []
        
        self.neo4j_client.execute_write(query, {
            "id": row['用例ID'],
            "title": row['用例标题'],
            "description": row.get('用例描述', ''),
            "priority": row.get('优先级', 'medium'),
            "type": row.get('类型', 'functional'),
            "steps": steps,
            "expected_result": row.get('期望结果', '')
        })
    
    def _create_testcase_component_relation(self, testcase_id: str, component_name: str):
        """建立测试用例-组件关系"""
        query = """
        MATCH (tc:TestCase {id: $testcase_id})
        MATCH (c:Component {name: $component_name})
        MERGE (tc)-[:TESTS]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "testcase_id": testcase_id,
            "component_name": component_name
        })
    
    def _upsert_anomaly(self, row: pd.Series):
        """创建或更新异常"""
        query = """
        MERGE (a:Anomaly {id: $id})
        SET a.title = $title,
            a.description = $description,
            a.severity = $severity,
            a.status = $status,
            a.created_date = $created_date,
            a.reporter = $reporter,
            a.updated_at = datetime()
        RETURN a.id
        """
        self.neo4j_client.execute_write(query, {
            "id": row['异常ID'],
            "title": row['异常标题'],
            "description": row.get('异常描述', ''),
            "severity": row.get('严重程度', 'medium'),
            "status": row.get('状态', 'open'),
            "created_date": str(row.get('创建日期', '')),
            "reporter": row.get('报告人', '')
        })
    
    def _upsert_symptom(self, description: str):
        """创建症状"""
        query = """
        MERGE (s:Symptom {description: $description})
        SET s.updated_at = datetime()
        RETURN s.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _upsert_root_cause(self, description: str):
        """创建根因"""
        query = """
        MERGE (rc:RootCause {description: $description})
        SET rc.updated_at = datetime()
        RETURN rc.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _upsert_countermeasure(self, description: str):
        """创建对策"""
        query = """
        MERGE (cm:Countermeasure {description: $description})
        SET cm.updated_at = datetime()
        RETURN cm.description
        """
        self.neo4j_client.execute_write(query, {"description": description})
    
    def _create_anomaly_symptom_relation(self, anomaly_id: str, symptom_description: str):
        """建立异常-症状关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (s:Symptom {description: $symptom_description})
        MERGE (a)-[:HAS_SYMPTOM]->(s)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "symptom_description": symptom_description
        })
    
    def _create_anomaly_root_cause_relation(self, anomaly_id: str, root_cause_description: str):
        """建立异常-根因关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (rc:RootCause {description: $root_cause_description})
        MERGE (a)-[:CAUSED_BY]->(rc)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "root_cause_description": root_cause_description
        })
    
    def _create_anomaly_countermeasure_relation(self, anomaly_id: str, countermeasure_description: str):
        """建立异常-对策关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (cm:Countermeasure {description: $countermeasure_description})
        MERGE (a)-[:SOLVED_BY]->(cm)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "countermeasure_description": countermeasure_description
        })
    
    def _create_anomaly_component_relation(self, anomaly_id: str, component_name: str):
        """建立异常-组件关系"""
        query = """
        MATCH (a:Anomaly {id: $anomaly_id})
        MATCH (c:Component {name: $component_name})
        MERGE (a)-[:OCCURS_IN]->(c)
        """
        self.neo4j_client.execute_write(query, {
            "anomaly_id": anomaly_id,
            "component_name": component_name
        })
    
    def close(self):
        """关闭连接"""
        self.neo4j_client.close()

def main():
    """主函数"""
    processor = EnhancedETLProcessor()
    
    try:
        # 检查数据目录
        raw_data_dir = Path("../../data/raw")
        if not raw_data_dir.exists():
            logger.error("数据目录不存在: ../../data/raw")
            return
        
        # 处理所有支持的文件
        supported_extensions = ['.xlsx', '.xls', '.csv', '.json']
        processed_files = 0
        
        for file_path in raw_data_dir.iterdir():
            if file_path.suffix.lower() in supported_extensions:
                logger.info(f"处理文件: {file_path}")
                stats = processor.process_file(str(file_path))
                processed_files += 1
        
        if processed_files == 0:
            logger.info("未找到支持的数据文件")
            logger.info(f"支持的格式: {supported_extensions}")
    
    finally:
        processor.close()

if __name__ == "__main__":
    main()
