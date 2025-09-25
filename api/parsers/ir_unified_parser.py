#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一IR解析器
整合所有格式的解析器，提供统一的解析接口
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging
from .ir_core import DocumentIR, IRConverter
from .enhanced_pptx_parser import EnhancedPPTXParser

logger = logging.getLogger(__name__)

class IRUnifiedParser:
    """统一IR解析器"""
    
    def __init__(self, use_ocr: bool = True, ocr_confidence: float = 0.5):
        """
        初始化统一解析器
        
        Args:
            use_ocr: 是否启用OCR
            ocr_confidence: OCR置信度阈值
        """
        self.use_ocr = use_ocr
        self.ocr_confidence = ocr_confidence
        
        # 初始化各格式解析器
        self.pptx_parser = EnhancedPPTXParser(use_ocr=use_ocr, ocr_confidence=ocr_confidence)
        
        # TODO: 后续添加其他格式解析器
        # self.docx_parser = EnhancedDOCXParser(use_ocr=use_ocr, ocr_confidence=ocr_confidence)
        # self.pdf_parser = EnhancedPDFParser(use_ocr=use_ocr, ocr_confidence=ocr_confidence)
    
    def parse_document(self, file_path: Path, file_ext: str) -> Dict[str, Any]:
        """
        解析文档为统一IR格式
        
        Args:
            file_path: 文件路径
            file_ext: 文件扩展名
            
        Returns:
            解析结果字典
        """
        try:
            logger.info(f"开始IR解析: {file_path} (格式: {file_ext})")
            
            # 创建输出目录
            output_dir = file_path.parent / f"{file_path.stem}_assets"
            
            # 根据文件类型选择解析器
            if file_ext.lower() in {'.pptx', '.ppt'}:
                document_ir = self._parse_pptx(file_path, output_dir)
            elif file_ext.lower() in {'.docx', '.doc'}:
                document_ir = self._parse_docx(file_path, output_dir)
            elif file_ext.lower() == '.pdf':
                document_ir = self._parse_pdf(file_path, output_dir)
            elif file_ext.lower() == '.csv':
                document_ir = self._parse_csv(file_path, output_dir)
            elif file_ext.lower() in {'.txt', '.md', '.rtf'}:
                document_ir = self._parse_text(file_path, output_dir)
            else:
                return {
                    'success': False,
                    'error': f'不支持的文件格式: {file_ext}',
                    'ir': None
                }
            
            logger.info(f"IR解析成功: {len(document_ir.blocks)}个内容块")
            
            return {
                'success': True,
                'ir': document_ir,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"IR解析失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'ir': None
            }
    
    def _parse_pptx(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析PPTX文件"""
        logger.info("使用增强PPTX解析器")
        return self.pptx_parser.parse(file_path, output_dir)
    
    def _parse_docx(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析DOCX文件（暂时使用旧版解析器）"""
        logger.info("使用DOCX解析器（兼容模式）")
        
        # 暂时使用旧版解析器，后续替换为增强版本
        try:
            from .enhanced_document_parser import EnhancedDocumentParser
            
            # 临时重命名文件以便旧解析器识别
            temp_path = file_path.with_suffix('.docx')
            file_path.rename(temp_path)
            
            try:
                parser = EnhancedDocumentParser()
                result = parser.parse_document(temp_path)
                
                if result['success']:
                    # 转换旧格式为IR
                    file_info = {
                        'id': file_path.stem,
                        'filename': file_path.name,
                        'file_type': 'docx'
                    }
                    return IRConverter.from_legacy_format(result['data'], file_info)
                else:
                    raise Exception(result.get('error', '解析失败'))
                    
            finally:
                # 恢复原文件名
                if temp_path.exists():
                    temp_path.rename(file_path)
                    
        except Exception as e:
            logger.error(f"DOCX解析失败: {e}")
            # 返回空IR
            return DocumentIR(
                meta={'file_id': file_path.stem, 'type': 'docx', 'pages': 1},
                blocks=[]
            )
    
    def _parse_pdf(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析PDF文件（暂时使用旧版解析器）"""
        logger.info("使用PDF解析器（兼容模式）")
        
        # 暂时使用旧版解析器，后续替换为增强版本
        try:
            from .enhanced_document_parser import EnhancedDocumentParser
            
            # 临时重命名文件以便旧解析器识别
            temp_path = file_path.with_suffix('.pdf')
            file_path.rename(temp_path)
            
            try:
                parser = EnhancedDocumentParser()
                result = parser.parse_document(temp_path)
                
                if result['success']:
                    # 转换旧格式为IR
                    file_info = {
                        'id': file_path.stem,
                        'filename': file_path.name,
                        'file_type': 'pdf'
                    }
                    return IRConverter.from_legacy_format(result['data'], file_info)
                else:
                    raise Exception(result.get('error', '解析失败'))
                    
            finally:
                # 恢复原文件名
                if temp_path.exists():
                    temp_path.rename(file_path)
                    
        except Exception as e:
            logger.error(f"PDF解析失败: {e}")
            # 返回空IR
            return DocumentIR(
                meta={'file_id': file_path.stem, 'type': 'pdf', 'pages': 1},
                blocks=[]
            )
    
    def _parse_csv(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析CSV文件（暂时使用旧版解析器）"""
        logger.info("使用CSV解析器（兼容模式）")
        
        try:
            from .enhanced_document_parser import EnhancedDocumentParser
            
            # 临时重命名文件以便旧解析器识别
            temp_path = file_path.with_suffix('.csv')
            file_path.rename(temp_path)
            
            try:
                parser = EnhancedDocumentParser()
                result = parser.parse_document(temp_path)
                
                if result['success']:
                    # 转换旧格式为IR
                    file_info = {
                        'id': file_path.stem,
                        'filename': file_path.name,
                        'file_type': 'csv'
                    }
                    return IRConverter.from_legacy_format(result['data'], file_info)
                else:
                    raise Exception(result.get('error', '解析失败'))
                    
            finally:
                # 恢复原文件名
                if temp_path.exists():
                    temp_path.rename(file_path)
                    
        except Exception as e:
            logger.error(f"CSV解析失败: {e}")
            # 返回空IR
            return DocumentIR(
                meta={'file_id': file_path.stem, 'type': 'csv', 'pages': 1},
                blocks=[]
            )
    
    def _parse_text(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析文本文件（暂时使用旧版解析器）"""
        logger.info("使用文本解析器（兼容模式）")
        
        try:
            from .enhanced_document_parser import EnhancedDocumentParser
            
            # 临时重命名文件以便旧解析器识别
            temp_path = file_path.with_suffix('.txt')
            file_path.rename(temp_path)
            
            try:
                parser = EnhancedDocumentParser()
                result = parser.parse_document(temp_path)
                
                if result['success']:
                    # 转换旧格式为IR
                    file_info = {
                        'id': file_path.stem,
                        'filename': file_path.name,
                        'file_type': 'txt'
                    }
                    return IRConverter.from_legacy_format(result['data'], file_info)
                else:
                    raise Exception(result.get('error', '解析失败'))
                    
            finally:
                # 恢复原文件名
                if temp_path.exists():
                    temp_path.rename(file_path)
                    
        except Exception as e:
            logger.error(f"文本解析失败: {e}")
            # 返回空IR
            return DocumentIR(
                meta={'file_id': file_path.stem, 'type': 'txt', 'pages': 1},
                blocks=[]
            )
    
    def get_supported_formats(self) -> set:
        """获取支持的文件格式"""
        return {'.pptx', '.ppt', '.docx', '.doc', '.pdf', '.csv', '.txt', '.md', '.rtf'}
    
    def is_format_supported(self, file_ext: str) -> bool:
        """检查文件格式是否支持"""
        return file_ext.lower() in self.get_supported_formats()
    
    def get_parser_info(self, file_ext: str) -> Dict[str, Any]:
        """获取解析器信息"""
        file_ext = file_ext.lower()
        
        if file_ext in {'.pptx', '.ppt'}:
            return {
                'parser': 'EnhancedPPTXParser',
                'version': '2.0',
                'features': ['图表数据直取', 'OCR兜底', '文本提取', '表格提取', '图片提取'],
                'quality': 'enhanced'
            }
        elif file_ext in {'.docx', '.doc'}:
            return {
                'parser': 'EnhancedDocumentParser',
                'version': '1.0',
                'features': ['文本提取', '表格提取'],
                'quality': 'compatible'
            }
        elif file_ext == '.pdf':
            return {
                'parser': 'EnhancedDocumentParser',
                'version': '1.0',
                'features': ['文本提取', '表格提取'],
                'quality': 'compatible'
            }
        elif file_ext == '.csv':
            return {
                'parser': 'EnhancedDocumentParser',
                'version': '1.0',
                'features': ['结构化数据提取'],
                'quality': 'compatible'
            }
        elif file_ext in {'.txt', '.md', '.rtf'}:
            return {
                'parser': 'EnhancedDocumentParser',
                'version': '1.0',
                'features': ['文本提取'],
                'quality': 'compatible'
            }
        else:
            return {
                'parser': 'None',
                'version': '0.0',
                'features': [],
                'quality': 'unsupported'
            }
