#!/usr/bin/env python3
"""
ETL模块 - 知识图谱构建助手
提供数据抽取、转换和加载功能
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .etl_from_excel import run_etl as run_excel_etl
from .enhanced_etl_processor import EnhancedETLProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_etl(
    file_path: str,
    file_type: str = "excel",
    mapping_file: Optional[str] = None,
    output_dir: Optional[str] = None,
    neo4j_uri: Optional[str] = None,
    neo4j_user: Optional[str] = None,
    neo4j_password: Optional[str] = None,
    batch_size: int = 1000,
    max_workers: int = 4,
    enable_validation: bool = True,
    enable_deduplication: bool = True,
    dry_run: bool = False
) -> dict:
    """
    运行ETL处理
    
    Args:
        file_path: 输入文件路径
        file_type: 文件类型 (excel, csv, json)
        mapping_file: 字段映射配置文件路径
        output_dir: 输出目录
        neo4j_uri: Neo4j连接URI
        neo4j_user: Neo4j用户名
        neo4j_password: Neo4j密码
        batch_size: 批处理大小
        max_workers: 最大工作线程数
        enable_validation: 启用数据验证
        enable_deduplication: 启用去重
        dry_run: 干运行模式（不实际写入数据库）
    
    Returns:
        ETL处理结果统计
    """
    
    # 验证输入文件
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"输入文件不存在: {file_path}")
    
    # 设置默认值
    if output_dir is None:
        output_dir = "./etl_reports"
    
    if mapping_file is None:
        mapping_file = str(Path(__file__).parent / "mapping.yaml")
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"开始ETL处理: {file_path}")
    logger.info(f"文件类型: {file_type}")
    logger.info(f"映射文件: {mapping_file}")
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"批处理大小: {batch_size}")
    logger.info(f"干运行模式: {dry_run}")
    
    try:
        if file_type.lower() == "excel":
            if os.path.exists(mapping_file):
                # 使用增强版ETL处理器
                processor = EnhancedETLProcessor(
                    mapping_file=mapping_file,
                    output_dir=output_dir,
                    neo4j_uri=neo4j_uri,
                    neo4j_user=neo4j_user,
                    neo4j_password=neo4j_password,
                    batch_size=batch_size,
                    max_workers=max_workers,
                    enable_validation=enable_validation,
                    enable_deduplication=enable_deduplication
                )
                
                stats = processor.process_excel(file_path, dry_run=dry_run)
                
                # 返回统计信息
                return {
                    "status": "success",
                    "file_path": file_path,
                    "file_type": file_type,
                    "total_rows": stats.total_rows,
                    "processed_rows": stats.processed_rows,
                    "success_rows": stats.success_rows,
                    "failed_rows": stats.failed_rows,
                    "skipped_rows": stats.skipped_rows,
                    "duplicate_rows": stats.duplicate_rows,
                    "success_rate": stats.success_rate,
                    "duration": stats.duration,
                    "errors": stats.errors[:10],  # 只返回前10个错误
                    "dry_run": dry_run
                }
            else:
                # 使用传统ETL处理器
                logger.warning(f"映射文件不存在，使用传统ETL处理器: {mapping_file}")
                result = run_excel_etl()
                return {
                    "status": "success",
                    "file_path": file_path,
                    "file_type": file_type,
                    "message": "使用传统ETL处理器完成",
                    "result": result
                }
        else:
            raise ValueError(f"不支持的文件类型: {file_type}")
            
    except Exception as e:
        logger.error(f"ETL处理失败: {str(e)}")
        return {
            "status": "error",
            "file_path": file_path,
            "file_type": file_type,
            "error": str(e)
        }

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="知识图谱ETL处理工具")
    
    # 必需参数
    parser.add_argument("file_path", help="输入文件路径")
    
    # 可选参数
    parser.add_argument("--type", "-t", default="excel", 
                       choices=["excel", "csv", "json"],
                       help="文件类型 (默认: excel)")
    
    parser.add_argument("--mapping", "-m", 
                       help="字段映射配置文件路径")
    
    parser.add_argument("--output", "-o", 
                       help="输出目录 (默认: ./etl_reports)")
    
    parser.add_argument("--neo4j-uri", 
                       default=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                       help="Neo4j连接URI")
    
    parser.add_argument("--neo4j-user", 
                       default=os.getenv("NEO4J_USER", "neo4j"),
                       help="Neo4j用户名")
    
    parser.add_argument("--neo4j-password", 
                       default=os.getenv("NEO4J_PASS", "password123"),
                       help="Neo4j密码")
    
    parser.add_argument("--batch-size", "-b", type=int, default=1000,
                       help="批处理大小 (默认: 1000)")
    
    parser.add_argument("--max-workers", "-w", type=int, default=4,
                       help="最大工作线程数 (默认: 4)")
    
    parser.add_argument("--no-validation", action="store_true",
                       help="禁用数据验证")
    
    parser.add_argument("--no-deduplication", action="store_true",
                       help="禁用去重")
    
    parser.add_argument("--dry-run", action="store_true",
                       help="干运行模式（不实际写入数据库）")
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细输出")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 运行ETL
    try:
        result = run_etl(
            file_path=args.file_path,
            file_type=args.type,
            mapping_file=args.mapping,
            output_dir=args.output,
            neo4j_uri=args.neo4j_uri,
            neo4j_user=args.neo4j_user,
            neo4j_password=args.neo4j_password,
            batch_size=args.batch_size,
            max_workers=args.max_workers,
            enable_validation=not args.no_validation,
            enable_deduplication=not args.no_deduplication,
            dry_run=args.dry_run
        )
        
        # 输出结果
        print("\n" + "="*60)
        print("ETL处理完成")
        print("="*60)
        print(f"状态: {result['status']}")
        print(f"文件: {result['file_path']}")
        print(f"类型: {result['file_type']}")
        
        if result['status'] == 'success' and 'total_rows' in result:
            print(f"总行数: {result['total_rows']}")
            print(f"处理行数: {result['processed_rows']}")
            print(f"成功行数: {result['success_rows']}")
            print(f"失败行数: {result['failed_rows']}")
            print(f"跳过行数: {result['skipped_rows']}")
            print(f"重复行数: {result['duplicate_rows']}")
            print(f"成功率: {result['success_rate']:.2%}")
            if result['duration']:
                print(f"处理时间: {result['duration']:.2f}秒")
            
            if result['errors']:
                print(f"\n前{len(result['errors'])}个错误:")
                for i, error in enumerate(result['errors'], 1):
                    print(f"  {i}. 行{error.get('row_index', '?')}: {error.get('message', '未知错误')}")
        
        elif result['status'] == 'error':
            print(f"错误: {result['error']}")
            sys.exit(1)
        
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n处理失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
