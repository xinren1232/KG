#!/usr/bin/env python3
"""
ETL批处理脚本 - 完整的Excel到Neo4j数据流水线
"""
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
import argparse

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from etl.parse_excel import ExcelParser
from etl.normalizer import DataNormalizer
from etl.upsert_writer import Neo4jUpsertWriter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    """ETL流水线"""
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.parser = ExcelParser()
        self.normalizer = DataNormalizer()
        self.writer = Neo4jUpsertWriter(neo4j_uri, neo4j_user, neo4j_password)
    
    def process_anomalies_file(self, file_path: str) -> Dict[str, Any]:
        """处理异常数据文件"""
        logger.info(f"开始处理异常文件: {file_path}")
        
        try:
            # 1. 解析Excel
            raw_anomalies = self.parser.parse_anomalies(file_path)
            logger.info(f"解析到 {len(raw_anomalies)} 条原始异常记录")
            
            # 2. 标准化数据
            normalized_anomalies = []
            for raw_anomaly in raw_anomalies:
                normalized = self.normalizer.normalize_anomaly_record(raw_anomaly)
                normalized_anomalies.append(normalized)
            
            logger.info(f"标准化 {len(normalized_anomalies)} 条异常记录")
            
            # 3. 写入Neo4j
            stats = self.writer.batch_upsert_anomalies(normalized_anomalies)
            
            result = {
                'file': file_path,
                'type': 'anomalies',
                'parsed': len(raw_anomalies),
                'normalized': len(normalized_anomalies),
                'success': stats['success'],
                'failed': stats['failed']
            }
            
            logger.info(f"异常文件处理完成: {result}")
            return result
            
        except Exception as e:
            logger.error(f"处理异常文件失败: {e}")
            return {
                'file': file_path,
                'type': 'anomalies',
                'error': str(e)
            }
    
    def process_testcases_file(self, file_path: str) -> Dict[str, Any]:
        """处理测试用例文件"""
        logger.info(f"开始处理测试用例文件: {file_path}")
        
        try:
            # 1. 解析Excel
            raw_testcases = self.parser.parse_testcases(file_path)
            logger.info(f"解析到 {len(raw_testcases)} 条原始测试用例")
            
            # 2. 标准化数据
            normalized_testcases = []
            for raw_testcase in raw_testcases:
                normalized = self.normalizer.normalize_testcase_record(raw_testcase)
                normalized_testcases.append(normalized)
            
            logger.info(f"标准化 {len(normalized_testcases)} 条测试用例")
            
            # 3. 写入Neo4j
            stats = self.writer.batch_upsert_testcases(normalized_testcases)
            
            result = {
                'file': file_path,
                'type': 'testcases',
                'parsed': len(raw_testcases),
                'normalized': len(normalized_testcases),
                'success': stats['success'],
                'failed': stats['failed']
            }
            
            logger.info(f"测试用例文件处理完成: {result}")
            return result
            
        except Exception as e:
            logger.error(f"处理测试用例文件失败: {e}")
            return {
                'file': file_path,
                'type': 'testcases',
                'error': str(e)
            }
    
    def process_directory(self, directory: str) -> List[Dict[str, Any]]:
        """处理目录中的所有Excel文件"""
        results = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"目录不存在: {directory}")
            return results
        
        # 查找Excel文件
        excel_files = list(dir_path.glob("*.xlsx")) + list(dir_path.glob("*.xls"))
        logger.info(f"找到 {len(excel_files)} 个Excel文件")
        
        for excel_file in excel_files:
            file_name = excel_file.name.lower()
            
            # 根据文件名判断类型
            if any(keyword in file_name for keyword in ['anomal', '异常', '问题', 'issue']):
                result = self.process_anomalies_file(str(excel_file))
            elif any(keyword in file_name for keyword in ['testcase', '测试', '用例', 'case']):
                result = self.process_testcases_file(str(excel_file))
            else:
                # 默认尝试作为异常文件处理
                logger.info(f"文件类型未知，尝试作为异常文件处理: {excel_file}")
                result = self.process_anomalies_file(str(excel_file))
            
            results.append(result)
        
        return results
    
    def get_final_stats(self) -> Dict[str, Any]:
        """获取最终统计信息"""
        return self.writer.get_stats()
    
    def close(self):
        """关闭连接"""
        self.writer.close()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ETL批处理脚本')
    parser.add_argument('--input', '-i', required=True, help='输入文件或目录路径')
    parser.add_argument('--type', '-t', choices=['anomalies', 'testcases', 'auto'], 
                       default='auto', help='文件类型')
    parser.add_argument('--neo4j-uri', default='bolt://localhost:7687', help='Neo4j URI')
    parser.add_argument('--neo4j-user', default='neo4j', help='Neo4j用户名')
    parser.add_argument('--neo4j-password', default='password123', help='Neo4j密码')
    
    args = parser.parse_args()
    
    # 从环境变量获取配置
    neo4j_uri = os.getenv('NEO4J_URI', args.neo4j_uri)
    neo4j_user = os.getenv('NEO4J_USER', args.neo4j_user)
    neo4j_password = os.getenv('NEO4J_PASS', args.neo4j_password)
    
    logger.info("开始ETL批处理")
    logger.info(f"输入: {args.input}")
    logger.info(f"类型: {args.type}")
    logger.info(f"Neo4j: {neo4j_uri}")
    
    # 创建ETL流水线
    pipeline = ETLPipeline(neo4j_uri, neo4j_user, neo4j_password)
    
    try:
        input_path = Path(args.input)
        results = []
        
        if input_path.is_file():
            # 处理单个文件
            if args.type == 'anomalies':
                result = pipeline.process_anomalies_file(str(input_path))
            elif args.type == 'testcases':
                result = pipeline.process_testcases_file(str(input_path))
            else:
                # 自动判断
                file_name = input_path.name.lower()
                if any(keyword in file_name for keyword in ['anomal', '异常', '问题']):
                    result = pipeline.process_anomalies_file(str(input_path))
                else:
                    result = pipeline.process_testcases_file(str(input_path))
            
            results.append(result)
            
        elif input_path.is_dir():
            # 处理目录
            results = pipeline.process_directory(str(input_path))
        
        else:
            logger.error(f"输入路径无效: {args.input}")
            return
        
        # 输出结果
        logger.info("=" * 60)
        logger.info("ETL处理结果汇总:")
        
        total_success = 0
        total_failed = 0
        
        for result in results:
            if 'error' in result:
                logger.error(f"文件 {result['file']} 处理失败: {result['error']}")
            else:
                logger.info(f"文件 {result['file']} ({result['type']}): "
                          f"成功 {result['success']}, 失败 {result['failed']}")
                total_success += result['success']
                total_failed += result['failed']
        
        logger.info(f"总计: 成功 {total_success}, 失败 {total_failed}")
        
        # 获取最终统计
        final_stats = pipeline.get_final_stats()
        logger.info("图谱最终统计:")
        for entity_type, count in final_stats.items():
            logger.info(f"  {entity_type}: {count}")
        
    except Exception as e:
        logger.error(f"ETL处理失败: {e}")
        raise
    
    finally:
        pipeline.close()
        logger.info("ETL批处理完成")

if __name__ == "__main__":
    main()
