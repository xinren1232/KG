#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统一中间表示（IR）核心模块
为所有文档格式提供统一的数据结构
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

class BlockType(Enum):
    """内容块类型枚举"""
    PARAGRAPH = "paragraph"  # 段落文本
    TABLE = "table"         # 表格数据
    FIGURE = "figure"       # 图片/图表

class FigureType(Enum):
    """图片类型枚举"""
    CHART = "chart"         # 图表
    PHOTO = "photo"         # 照片
    SCAN = "scan"           # 扫描件
    DIAGRAM = "diagram"     # 示意图
    UNKNOWN = "unknown"     # 未知类型

@dataclass
class IRBlock:
    """统一内容块数据结构"""
    id: str                                    # 块唯一标识
    type: BlockType                           # 块类型
    page: int                                 # 所在页面
    text: Optional[str] = None                # 文本内容（段落）
    cells: Optional[List[List[str]]] = None   # 表格单元格数据
    image: Optional[str] = None               # 图片路径
    caption: Optional[str] = None             # 图片标题
    ocr_text: Optional[str] = None            # OCR识别文本
    style: Optional[str] = None               # 样式信息
    figure_type: Optional[str] = None         # 图片类型
    confidence: Optional[float] = None        # 识别置信度
    metadata: Optional[Dict[str, Any]] = None # 额外元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            "id": self.id,
            "type": self.type.value if isinstance(self.type, BlockType) else self.type,
            "page": self.page
        }
        
        # 只包含非空字段
        if self.text is not None:
            result["text"] = self.text
        if self.cells is not None:
            result["cells"] = self.cells
        if self.image is not None:
            result["image"] = self.image
        if self.caption is not None:
            result["caption"] = self.caption
        if self.ocr_text is not None:
            result["ocr_text"] = self.ocr_text
        if self.style is not None:
            result["style"] = self.style
        if self.figure_type is not None:
            result["figure_type"] = self.figure_type
        if self.confidence is not None:
            result["confidence"] = self.confidence
        if self.metadata is not None:
            result["metadata"] = self.metadata
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IRBlock':
        """从字典创建IRBlock实例"""
        # 转换type为枚举
        block_type = BlockType(data["type"]) if isinstance(data["type"], str) else data["type"]
        
        return cls(
            id=data["id"],
            type=block_type,
            page=data["page"],
            text=data.get("text"),
            cells=data.get("cells"),
            image=data.get("image"),
            caption=data.get("caption"),
            ocr_text=data.get("ocr_text"),
            style=data.get("style"),
            figure_type=data.get("figure_type"),
            confidence=data.get("confidence"),
            metadata=data.get("metadata")
        )

@dataclass
class DocumentIR:
    """文档统一中间表示"""
    meta: Dict[str, Any]      # 文档元信息
    blocks: List[IRBlock]     # 内容块列表
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "meta": self.meta,
            "blocks": [block.to_dict() for block in self.blocks]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentIR':
        """从字典创建DocumentIR实例"""
        blocks = [IRBlock.from_dict(block_data) for block_data in data["blocks"]]
        return cls(meta=data["meta"], blocks=blocks)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'DocumentIR':
        """从JSON字符串创建DocumentIR实例"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, file_path: Union[str, Path]) -> None:
        """保存到文件"""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load(cls, file_path: Union[str, Path]) -> 'DocumentIR':
        """从文件加载"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    def get_blocks_by_type(self, block_type: BlockType) -> List[IRBlock]:
        """按类型获取内容块"""
        return [block for block in self.blocks if block.type == block_type]
    
    def get_blocks_by_page(self, page: int) -> List[IRBlock]:
        """按页面获取内容块"""
        return [block for block in self.blocks if block.page == page]
    
    def get_text_content(self) -> str:
        """获取所有文本内容"""
        text_parts = []
        
        for block in self.blocks:
            if block.type == BlockType.PARAGRAPH and block.text:
                text_parts.append(block.text)
            elif block.type == BlockType.TABLE and block.cells:
                # 表格转换为文本
                table_text = []
                for row in block.cells:
                    table_text.append("\t".join(row))
                text_parts.append("\n".join(table_text))
            elif block.type == BlockType.FIGURE and block.ocr_text:
                text_parts.append(block.ocr_text)
        
        return "\n\n".join(text_parts)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取文档统计信息"""
        stats = {
            "total_blocks": len(self.blocks),
            "paragraphs": len(self.get_blocks_by_type(BlockType.PARAGRAPH)),
            "tables": len(self.get_blocks_by_type(BlockType.TABLE)),
            "figures": len(self.get_blocks_by_type(BlockType.FIGURE)),
            "pages": self.meta.get("pages", 1),
            "file_type": self.meta.get("type", "unknown")
        }
        
        # 计算文本统计
        text_content = self.get_text_content()
        stats["total_chars"] = len(text_content)
        stats["total_words"] = len(text_content.split()) if text_content else 0
        
        # 按页面统计
        page_stats = {}
        for page in range(1, stats["pages"] + 1):
            page_blocks = self.get_blocks_by_page(page)
            page_stats[f"page_{page}"] = {
                "blocks": len(page_blocks),
                "paragraphs": len([b for b in page_blocks if b.type == BlockType.PARAGRAPH]),
                "tables": len([b for b in page_blocks if b.type == BlockType.TABLE]),
                "figures": len([b for b in page_blocks if b.type == BlockType.FIGURE])
            }
        
        stats["page_stats"] = page_stats
        
        return stats

class IRConverter:
    """IR格式转换器"""
    
    @staticmethod
    def to_legacy_format(ir: DocumentIR) -> Dict[str, Any]:
        """转换为旧版格式（兼容现有前端）"""
        raw_data = []
        entities = []
        relations = []
        
        # 转换内容块为原始数据记录
        for i, block in enumerate(ir.blocks):
            record = {
                "_row_number": i + 1,
                "block_id": block.id,
                "block_type": block.type.value,
                "page_number": block.page
            }
            
            if block.type == BlockType.PARAGRAPH:
                record.update({
                    "content_type": "paragraph",
                    "content": block.text or "",
                    "style": block.style,
                    "word_count": len(block.text.split()) if block.text else 0,
                    "char_count": len(block.text) if block.text else 0,
                    "paragraph_number": i + 1
                })
            elif block.type == BlockType.TABLE:
                record.update({
                    "content_type": "table",
                    "table_rows": len(block.cells) if block.cells else 0,
                    "table_cols": len(block.cells[0]) if block.cells and block.cells[0] else 0
                })
                # 添加表格单元格数据
                if block.cells:
                    for row_idx, row in enumerate(block.cells):
                        for col_idx, cell in enumerate(row):
                            record[f"cell_{row_idx}_{col_idx}"] = cell
            elif block.type == BlockType.FIGURE:
                record.update({
                    "content_type": "figure",
                    "image_path": block.image,
                    "figure_type": block.figure_type,
                    "ocr_text": block.ocr_text or "",
                    "caption": block.caption or "",
                    "confidence": block.confidence
                })
            
            raw_data.append(record)
        
        # 构建元数据
        metadata = {
            "total_blocks": len(ir.blocks),
            "total_pages": ir.meta.get("pages", 1),
            "file_type": ir.meta.get("type", "unknown"),
            **ir.get_statistics()
        }
        
        return {
            "raw_data": raw_data,
            "entities": entities,
            "relations": relations,
            "metadata": metadata
        }
    
    @staticmethod
    def from_legacy_format(legacy_data: Dict[str, Any], file_info: Dict[str, Any]) -> DocumentIR:
        """从旧版格式转换为IR（用于兼容）"""
        meta = {
            "file_id": file_info.get("id", "unknown"),
            "type": file_info.get("file_type", "unknown"),
            "pages": legacy_data.get("metadata", {}).get("total_pages", 1),
            "title": file_info.get("filename", "")
        }
        
        blocks = []
        for record in legacy_data.get("raw_data", []):
            content_type = record.get("content_type", "paragraph")

            # 映射旧版格式的content_type到新的BlockType
            if content_type in ["text", "paragraph"]:
                block = IRBlock(
                    id=record.get("block_id", f"b_{record.get('_row_number', 1)}"),
                    type=BlockType.PARAGRAPH,
                    page=record.get("page_number", 1),
                    text=record.get("content", ""),
                    style=record.get("style")
                )
            elif content_type == "table":
                # 重建表格数据 - 从旧格式的列数据重建
                cells = []
                content = record.get("content", "")
                if content and "|" in content:
                    # 简单的表格行解析
                    row = [cell.strip() for cell in content.split("|")]
                    cells = [row]

                block = IRBlock(
                    id=record.get("block_id", f"t_{record.get('_row_number', 1)}"),
                    type=BlockType.TABLE,
                    page=record.get("page_number", 1),
                    cells=cells
                )
            elif content_type == "figure":
                block = IRBlock(
                    id=record.get("block_id", f"f_{record.get('_row_number', 1)}"),
                    type=BlockType.FIGURE,
                    page=record.get("page_number", 1),
                    image=record.get("image_path"),
                    ocr_text=record.get("ocr_text"),
                    caption=record.get("caption"),
                    figure_type=record.get("figure_type"),
                    confidence=record.get("confidence")
                )
            else:
                # 默认作为段落处理
                block = IRBlock(
                    id=record.get("block_id", f"b_{record.get('_row_number', 1)}"),
                    type=BlockType.PARAGRAPH,
                    page=record.get("page_number", 1),
                    text=record.get("content", ""),
                    style=record.get("style")
                )

            blocks.append(block)
        
        return DocumentIR(meta=meta, blocks=blocks)

# 工具函数
def create_paragraph_block(block_id: str, page: int, text: str, style: str = None) -> IRBlock:
    """创建段落块"""
    return IRBlock(
        id=block_id,
        type=BlockType.PARAGRAPH,
        page=page,
        text=text,
        style=style
    )

def create_table_block(block_id: str, page: int, cells: List[List[str]], style: str = None) -> IRBlock:
    """创建表格块"""
    return IRBlock(
        id=block_id,
        type=BlockType.TABLE,
        page=page,
        cells=cells,
        style=style
    )

def create_figure_block(block_id: str, page: int, image_path: str, 
                       ocr_text: str = None, caption: str = None, 
                       figure_type: str = None, confidence: float = None) -> IRBlock:
    """创建图片块"""
    return IRBlock(
        id=block_id,
        type=BlockType.FIGURE,
        page=page,
        image=image_path,
        ocr_text=ocr_text,
        caption=caption,
        figure_type=figure_type,
        confidence=confidence
    )
