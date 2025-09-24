#!/usr/bin/env python3
"""
数据质量检查工具
检查数据完整性、一致性和准确性
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
from dataclasses import dataclass, asdict

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent / "api"))

from database.neo4j_client import Neo4jClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityIssue:
    """质量问题"""
    type: str  # 问题类型: missing, duplicate, inconsistent, invalid
    severity: str  # 严重程度: critical, high, medium, low
    description: str  # 问题描述
    location: str  # 问题位置
    suggestion: str  # 修复建议
    count: int = 1  # 问题数量

@dataclass
class QualityReport:
    """质量报告"""
    file_path: str
    total_records: int
    issues: List[QualityIssue]
    score: float  # 质量分数 (0-100)
    check_time: datetime
    
    def to_dict(self):
        return {
            'file_path': self.file_path,
            'total_records': self.total_records,
            'issues': [asdict(issue) for issue in self.issues],
            'score': self.score,
            'check_time': self.check_time.isoformat(),
            'summary': self.get_summary()
        }
    
    def get_summary(self):
        """获取报告摘要"""
        issue_counts = {}
        for issue in self.issues:
            issue_counts[issue.severity] = issue_counts.get(issue.severity, 0) + issue.count
        
        return {
            'total_issues': sum(issue.count for issue in self.issues),
            'critical_issues': issue_counts.get('critical', 0),
            'high_issues': issue_counts.get('high', 0),
            'medium_issues': issue_counts.get('medium', 0),
            'low_issues': issue_counts.get('low', 0)
        }

class DataQualityChecker:
    """数据质量检查器"""
    
    def __init__(self):
        self.neo4j_client = None
        try:
            self.neo4j_client = Neo4jClient(
                uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                user=os.getenv("NEO4J_USER", "neo4j"),
                password=os.getenv("NEO4J_PASS", "password123")
            )
        except Exception as e:
            logger.warning(f"无法连接Neo4j数据库: {e}")
    
    def check_file_quality(self, file_path: str) -> QualityReport:
        """检查文件数据质量"""
        logger.info(f"开始检查文件质量: {file_path}")
        
        # 读取文件
        df = self._read_file(file_path)
        if df is None:
            return QualityReport(
                file_path=file_path,
                total_records=0,
                issues=[QualityIssue(
                    type="invalid",
                    severity="critical",
                    description="无法读取文件",
                    location="文件",
                    suggestion="检查文件格式和编码"
                )],
                score=0.0,
                check_time=datetime.now()
            )
        
        issues = []
        
        # 检测数据类型
        data_type = self._detect_data_type(df, file_path)
        
        # 基础质量检查
        issues.extend(self._check_basic_quality(df))
        
        # 特定数据类型检查
        if data_type == 'test_case':
            issues.extend(self._check_test_case_quality(df))
        elif data_type == 'anomaly':
            issues.extend(self._check_anomaly_quality(df))
        
        # 数据库一致性检查
        if self.neo4j_client:
            issues.extend(self._check_database_consistency(df, data_type))
        
        # 计算质量分数
        score = self._calculate_quality_score(df, issues)
        
        return QualityReport(
            file_path=file_path,
            total_records=len(df),
            issues=issues,
            score=score,
            check_time=datetime.now()
        )
    
    def _read_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """读取文件"""
        try:
            ext = Path(file_path).suffix.lower()
            if ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
            elif ext == '.csv':
                return pd.read_csv(file_path, encoding='utf-8-sig')
            elif ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return pd.DataFrame(data)
            else:
                return None
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            return None
    
    def _detect_data_type(self, df: pd.DataFrame, file_path: str) -> str:
        """检测数据类型"""
        file_name = Path(file_path).name.lower()
        
        if '测试用例' in file_name or 'testcase' in file_name:
            return 'test_case'
        elif '异常' in file_name or 'anomaly' in file_name:
            return 'anomaly'
        
        columns = [col.lower() for col in df.columns]
        if '用例id' in columns or '用例标题' in columns:
            return 'test_case'
        elif '异常id' in columns or '异常标题' in columns:
            return 'anomaly'
        
        return 'unknown'
    
    def _check_basic_quality(self, df: pd.DataFrame) -> List[QualityIssue]:
        """基础质量检查"""
        issues = []
        
        # 检查空数据
        if df.empty:
            issues.append(QualityIssue(
                type="missing",
                severity="critical",
                description="文件为空",
                location="整个文件",
                suggestion="确保文件包含有效数据"
            ))
            return issues
        
        # 检查重复行
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            issues.append(QualityIssue(
                type="duplicate",
                severity="medium",
                description=f"发现 {duplicate_rows} 行重复数据",
                location="数据行",
                suggestion="删除重复行或检查数据源",
                count=duplicate_rows
            ))
        
        # 检查空值
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                null_percentage = (null_count / len(df)) * 100
                severity = "critical" if null_percentage > 50 else "high" if null_percentage > 20 else "medium"
                
                issues.append(QualityIssue(
                    type="missing",
                    severity=severity,
                    description=f"列 '{col}' 有 {null_count} 个空值 ({null_percentage:.1f}%)",
                    location=f"列: {col}",
                    suggestion="填充空值或检查数据收集过程",
                    count=null_count
                ))
        
        # 检查数据类型一致性
        for col in df.select_dtypes(include=['object']).columns:
            # 检查是否有数字字符串混合
            numeric_like = df[col].astype(str).str.match(r'^\d+\.?\d*$').sum()
            if 0 < numeric_like < len(df):
                issues.append(QualityIssue(
                    type="inconsistent",
                    severity="medium",
                    description=f"列 '{col}' 包含混合数据类型",
                    location=f"列: {col}",
                    suggestion="统一数据类型或分离不同类型的数据"
                ))
        
        return issues
    
    def _check_test_case_quality(self, df: pd.DataFrame) -> List[QualityIssue]:
        """测试用例质量检查"""
        issues = []
        
        # 检查必要列
        required_columns = ['产品名称', '组件名称', '用例ID', '用例标题']
        for col in required_columns:
            if col not in df.columns:
                issues.append(QualityIssue(
                    type="missing",
                    severity="critical",
                    description=f"缺少必要列: {col}",
                    location="列结构",
                    suggestion=f"添加 {col} 列"
                ))
        
        # 检查用例ID格式
        if '用例ID' in df.columns:
            invalid_ids = []
            for idx, case_id in enumerate(df['用例ID']):
                if pd.notna(case_id):
                    case_id_str = str(case_id).strip()
                    if not case_id_str.startswith('TC-'):
                        invalid_ids.append(f"第{idx+1}行: {case_id_str}")
            
            if invalid_ids:
                issues.append(QualityIssue(
                    type="invalid",
                    severity="medium",
                    description=f"用例ID格式不规范: {len(invalid_ids)} 个",
                    location="用例ID列",
                    suggestion="使用 TC-XXX-001 格式",
                    count=len(invalid_ids)
                ))
        
        # 检查优先级值
        if '优先级' in df.columns:
            valid_priorities = ['高', '中', '低', '紧急', 'high', 'medium', 'low', 'critical']
            invalid_priorities = df[~df['优先级'].isin(valid_priorities + [None])]['优先级'].dropna()
            
            if len(invalid_priorities) > 0:
                issues.append(QualityIssue(
                    type="invalid",
                    severity="low",
                    description=f"优先级值不规范: {len(invalid_priorities)} 个",
                    location="优先级列",
                    suggestion="使用标准优先级值: 高/中/低/紧急",
                    count=len(invalid_priorities)
                ))
        
        return issues
    
    def _check_anomaly_quality(self, df: pd.DataFrame) -> List[QualityIssue]:
        """异常数据质量检查"""
        issues = []
        
        # 检查必要列
        required_columns = ['异常ID', '异常标题', '组件名称']
        for col in required_columns:
            if col not in df.columns:
                issues.append(QualityIssue(
                    type="missing",
                    severity="critical",
                    description=f"缺少必要列: {col}",
                    location="列结构",
                    suggestion=f"添加 {col} 列"
                ))
        
        # 检查异常ID格式
        if '异常ID' in df.columns:
            invalid_ids = []
            for idx, anomaly_id in enumerate(df['异常ID']):
                if pd.notna(anomaly_id):
                    anomaly_id_str = str(anomaly_id).strip()
                    if not anomaly_id_str.startswith('ANO-'):
                        invalid_ids.append(f"第{idx+1}行: {anomaly_id_str}")
            
            if invalid_ids:
                issues.append(QualityIssue(
                    type="invalid",
                    severity="medium",
                    description=f"异常ID格式不规范: {len(invalid_ids)} 个",
                    location="异常ID列",
                    suggestion="使用 ANO-YYYY-001 格式",
                    count=len(invalid_ids)
                ))
        
        # 检查严重程度值
        if '严重程度' in df.columns:
            valid_severities = ['严重', '高', '中', '低', 'critical', 'high', 'medium', 'low']
            invalid_severities = df[~df['严重程度'].isin(valid_severities + [None])]['严重程度'].dropna()
            
            if len(invalid_severities) > 0:
                issues.append(QualityIssue(
                    type="invalid",
                    severity="low",
                    description=f"严重程度值不规范: {len(invalid_severities)} 个",
                    location="严重程度列",
                    suggestion="使用标准严重程度值: 严重/高/中/低",
                    count=len(invalid_severities)
                ))
        
        # 检查状态值
        if '状态' in df.columns:
            valid_statuses = ['开放', '处理中', '已解决', '已关闭', 'open', 'in_progress', 'resolved', 'closed']
            invalid_statuses = df[~df['状态'].isin(valid_statuses + [None])]['状态'].dropna()
            
            if len(invalid_statuses) > 0:
                issues.append(QualityIssue(
                    type="invalid",
                    severity="low",
                    description=f"状态值不规范: {len(invalid_statuses)} 个",
                    location="状态列",
                    suggestion="使用标准状态值: 开放/处理中/已解决/已关闭",
                    count=len(invalid_statuses)
                ))
        
        return issues
    
    def _check_database_consistency(self, df: pd.DataFrame, data_type: str) -> List[QualityIssue]:
        """检查数据库一致性"""
        issues = []
        
        try:
            if data_type == 'test_case' and '用例ID' in df.columns:
                # 检查用例ID是否已存在
                existing_ids = self._get_existing_test_case_ids()
                duplicate_ids = df['用例ID'].dropna().tolist()
                duplicates = [id for id in duplicate_ids if id in existing_ids]
                
                if duplicates:
                    issues.append(QualityIssue(
                        type="duplicate",
                        severity="high",
                        description=f"数据库中已存在的用例ID: {len(duplicates)} 个",
                        location="用例ID列",
                        suggestion="使用新的用例ID或更新现有记录",
                        count=len(duplicates)
                    ))
            
            elif data_type == 'anomaly' and '异常ID' in df.columns:
                # 检查异常ID是否已存在
                existing_ids = self._get_existing_anomaly_ids()
                duplicate_ids = df['异常ID'].dropna().tolist()
                duplicates = [id for id in duplicate_ids if id in existing_ids]
                
                if duplicates:
                    issues.append(QualityIssue(
                        type="duplicate",
                        severity="high",
                        description=f"数据库中已存在的异常ID: {len(duplicates)} 个",
                        location="异常ID列",
                        suggestion="使用新的异常ID或更新现有记录",
                        count=len(duplicates)
                    ))
        
        except Exception as e:
            logger.warning(f"数据库一致性检查失败: {e}")
        
        return issues
    
    def _get_existing_test_case_ids(self) -> List[str]:
        """获取现有测试用例ID"""
        query = "MATCH (tc:TestCase) RETURN tc.id as id"
        result = self.neo4j_client.execute_read(query)
        return [record["id"] for record in result]
    
    def _get_existing_anomaly_ids(self) -> List[str]:
        """获取现有异常ID"""
        query = "MATCH (a:Anomaly) RETURN a.id as id"
        result = self.neo4j_client.execute_read(query)
        return [record["id"] for record in result]
    
    def _calculate_quality_score(self, df: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """计算质量分数"""
        if df.empty:
            return 0.0
        
        total_records = len(df)
        total_cells = total_records * len(df.columns)
        
        # 计算扣分
        penalty = 0
        for issue in issues:
            if issue.severity == "critical":
                penalty += issue.count * 10
            elif issue.severity == "high":
                penalty += issue.count * 5
            elif issue.severity == "medium":
                penalty += issue.count * 2
            elif issue.severity == "low":
                penalty += issue.count * 1
        
        # 计算分数 (0-100)
        max_penalty = total_cells * 10  # 假设最坏情况
        score = max(0, 100 - (penalty / max_penalty * 100))
        
        return round(score, 2)
    
    def generate_report(self, report: QualityReport, output_path: str = None):
        """生成质量报告"""
        if output_path is None:
            output_path = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"质量报告已生成: {output_path}")
        return output_path
    
    def close(self):
        """关闭连接"""
        if self.neo4j_client:
            self.neo4j_client.close()

def main():
    """主函数"""
    checker = DataQualityChecker()
    
    try:
        # 检查数据目录
        raw_data_dir = Path("../../data/raw")
        if not raw_data_dir.exists():
            logger.error("数据目录不存在: ../../data/raw")
            return
        
        # 检查所有支持的文件
        supported_extensions = ['.xlsx', '.xls', '.csv', '.json']
        
        for file_path in raw_data_dir.iterdir():
            if file_path.suffix.lower() in supported_extensions:
                logger.info(f"检查文件: {file_path}")
                
                # 执行质量检查
                report = checker.check_file_quality(str(file_path))
                
                # 生成报告
                report_path = checker.generate_report(report)
                
                # 打印摘要
                summary = report.get_summary()
                logger.info(f"质量分数: {report.score}/100")
                logger.info(f"问题总数: {summary['total_issues']}")
                logger.info(f"严重问题: {summary['critical_issues']}")
                logger.info(f"报告文件: {report_path}")
                print("-" * 50)
    
    finally:
        checker.close()

if __name__ == "__main__":
    main()
