#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OCR引擎模块
基于PaddleOCR实现文本和表格识别
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import logging

# 设置日志
logger = logging.getLogger(__name__)

class OCREngine:
    """OCR识别引擎"""
    
    def __init__(self, use_gpu: bool = False, lang: str = 'ch'):
        """
        初始化OCR引擎
        
        Args:
            use_gpu: 是否使用GPU
            lang: 语言设置，'ch'为中文，'en'为英文
        """
        self.use_gpu = use_gpu
        self.lang = lang
        self._text_ocr = None
        self._table_ocr = None
        self._initialized = False
    
    def _init_engines(self):
        """延迟初始化OCR引擎"""
        if self._initialized:
            return

        try:
            from paddleocr import PaddleOCR

            # 初始化文本OCR
            self._text_ocr = PaddleOCR(
                lang=self.lang,
                use_gpu=self.use_gpu,
                show_log=False,
                use_angle_cls=True,
                det_model_dir=None,
                rec_model_dir=None,
                cls_model_dir=None
            )

            # 初始化表格OCR（如果可用）
            try:
                self._table_ocr = PaddleOCR(
                    lang=self.lang,
                    use_gpu=self.use_gpu,
                    show_log=False,
                    structure_version='PP-StructureV2'
                )
                logger.info("表格OCR引擎初始化成功")
            except Exception as e:
                logger.warning(f"表格OCR引擎初始化失败: {e}")
                self._table_ocr = None

            self._initialized = True
            logger.info(f"OCR引擎初始化成功 (GPU: {self.use_gpu}, 语言: {self.lang})")

        except ImportError as e:
            logger.warning(f"PaddleOCR未安装，OCR功能将被禁用: {e}")
            self._text_ocr = None
            self._table_ocr = None
            self._initialized = True
        except Exception as e:
            logger.warning(f"OCR引擎初始化失败，OCR功能将被禁用: {e}")
            self._text_ocr = None
            self._table_ocr = None
            self._initialized = True
    
    @property
    def text_ocr(self):
        """获取文本OCR引擎"""
        if not self._initialized:
            self._init_engines()
        return self._text_ocr
    
    @property
    def table_ocr(self):
        """获取表格OCR引擎"""
        if not self._initialized:
            self._init_engines()
        return self._table_ocr
    
    def extract_text(self, img_path: str, confidence_threshold: float = 0.5) -> str:
        """
        提取图片中的文本

        Args:
            img_path: 图片路径
            confidence_threshold: 置信度阈值

        Returns:
            识别出的文本
        """
        try:
            if not Path(img_path).exists():
                logger.error(f"图片文件不存在: {img_path}")
                return ""

            # 检查OCR引擎是否可用
            if not self.text_ocr:
                logger.warning(f"OCR引擎不可用，跳过文本提取: {img_path}")
                return ""

            # 执行OCR识别
            results = self.text_ocr.ocr(img_path, cls=True)

            if not results or not results[0]:
                logger.warning(f"OCR未识别到文本: {img_path}")
                return ""

            # 提取文本行
            lines = []
            for line in results[0]:
                if len(line) >= 2:
                    text, confidence = line[1]
                    if confidence > confidence_threshold:
                        lines.append(text)
                    else:
                        logger.debug(f"低置信度文本被过滤: {text} (置信度: {confidence:.2f})")

            result_text = "\n".join(lines)
            logger.info(f"OCR文本提取成功: {len(lines)}行, {len(result_text)}字符")
            return result_text

        except Exception as e:
            logger.error(f"OCR文本提取失败 {img_path}: {e}")
            return ""
    
    def extract_table(self, img_path: str, confidence_threshold: float = 0.5) -> List[List[str]]:
        """
        提取图片中的表格结构

        Args:
            img_path: 图片路径
            confidence_threshold: 置信度阈值

        Returns:
            表格数据（二维数组）
        """
        try:
            if not Path(img_path).exists():
                logger.error(f"图片文件不存在: {img_path}")
                return []

            # 如果没有OCR引擎，返回空
            if not self.text_ocr:
                logger.warning("OCR引擎不可用，跳过表格提取")
                return []

            # 如果没有表格OCR引擎，降级为文本提取
            if not self.table_ocr:
                logger.warning("表格OCR不可用，降级为文本提取")
                text = self.extract_text(img_path, confidence_threshold)
                return self._text_to_table(text)

            # 执行表格OCR
            results = self.table_ocr.ocr(img_path, cls=True, rec=True, det=True, structure=True)

            if not results:
                logger.warning(f"表格OCR未识别到内容: {img_path}")
                return []

            # 解析表格结构
            tables = []
            for result in results:
                if isinstance(result, dict) and result.get('type') == 'table':
                    table_data = self._parse_table_structure(result)
                    if table_data:
                        tables.extend(table_data)

            if tables:
                logger.info(f"表格OCR提取成功: {len(tables)}行")
                return tables
            else:
                # 降级为文本提取
                logger.warning("表格结构识别失败，降级为文本提取")
                text = self.extract_text(img_path, confidence_threshold)
                return self._text_to_table(text)

        except Exception as e:
            logger.error(f"表格OCR提取失败 {img_path}: {e}")
            # 降级为文本提取
            text = self.extract_text(img_path, confidence_threshold)
            return self._text_to_table(text)
    
    def _parse_table_structure(self, table_result: Dict[str, Any]) -> List[List[str]]:
        """解析表格结构识别结果"""
        try:
            # 这里需要根据PaddleOCR的实际返回格式来解析
            # 由于PP-Structure的返回格式比较复杂，这里提供一个简化版本
            
            if 'res' in table_result:
                res = table_result['res']
                if isinstance(res, dict) and 'boxes' in res:
                    # 简化处理：按坐标重建表格
                    boxes = res['boxes']
                    # 这里应该有更复杂的表格重建逻辑
                    # 暂时返回空，让其降级为文本处理
                    return []
            
            return []
            
        except Exception as e:
            logger.error(f"表格结构解析失败: {e}")
            return []
    
    def _text_to_table(self, text: str) -> List[List[str]]:
        """将文本转换为表格格式（简单启发式方法）"""
        if not text.strip():
            return []
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # 尝试检测表格分隔符
        table_data = []
        for line in lines:
            # 检测常见的表格分隔符
            if '\t' in line:
                row = [cell.strip() for cell in line.split('\t')]
            elif '|' in line and line.count('|') >= 2:
                row = [cell.strip() for cell in line.split('|') if cell.strip()]
            elif '，' in line or ',' in line:
                # 逗号分隔
                separator = '，' if '，' in line else ','
                row = [cell.strip() for cell in line.split(separator)]
            else:
                # 空格分隔（需要更智能的处理）
                row = [cell for cell in line.split() if cell]
            
            if len(row) > 1:  # 至少两列才认为是表格行
                table_data.append(row)
        
        return table_data
    
    def get_text_confidence(self, img_path: str) -> float:
        """
        获取文本识别的平均置信度

        Args:
            img_path: 图片路径

        Returns:
            平均置信度
        """
        try:
            # 检查OCR引擎是否可用
            if not self.text_ocr:
                logger.warning("OCR引擎不可用，返回0置信度")
                return 0.0

            results = self.text_ocr.ocr(img_path, cls=True)

            if not results or not results[0]:
                return 0.0

            confidences = []
            for line in results[0]:
                if len(line) >= 2:
                    _, confidence = line[1]
                    confidences.append(confidence)

            return sum(confidences) / len(confidences) if confidences else 0.0

        except Exception as e:
            logger.error(f"获取置信度失败 {img_path}: {e}")
            return 0.0
    
    def preprocess_image(self, img_path: str, output_path: str = None) -> str:
        """
        图片预处理以提高OCR效果
        
        Args:
            img_path: 输入图片路径
            output_path: 输出图片路径，如果为None则覆盖原图
            
        Returns:
            处理后的图片路径
        """
        try:
            # 读取图片
            img = cv2.imread(img_path)
            if img is None:
                logger.error(f"无法读取图片: {img_path}")
                return img_path
            
            # 转换为灰度图
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 去噪
            denoised = cv2.medianBlur(gray, 3)
            
            # 二值化
            _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # 保存处理后的图片
            if output_path is None:
                output_path = img_path
            
            cv2.imwrite(output_path, binary)
            logger.info(f"图片预处理完成: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"图片预处理失败 {img_path}: {e}")
            return img_path

# 全局OCR引擎实例
_global_ocr_engine = None

def get_ocr_engine(use_gpu: bool = False, lang: str = 'ch') -> OCREngine:
    """获取全局OCR引擎实例"""
    global _global_ocr_engine
    
    if _global_ocr_engine is None:
        _global_ocr_engine = OCREngine(use_gpu=use_gpu, lang=lang)
    
    return _global_ocr_engine

# 便捷函数
def ocr_text(img_path: str, confidence_threshold: float = 0.5) -> str:
    """便捷的文本OCR函数"""
    engine = get_ocr_engine()
    return engine.extract_text(img_path, confidence_threshold)

def ocr_table(img_path: str, confidence_threshold: float = 0.5) -> List[List[str]]:
    """便捷的表格OCR函数"""
    engine = get_ocr_engine()
    return engine.extract_table(img_path, confidence_threshold)
