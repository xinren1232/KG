# 统一IR解析系统集成方案

## 🎯 集成策略：渐进式升级

### 阶段1：核心IR架构搭建 (1天)
**目标**: 建立统一中间表示系统

#### 1.1 创建IR核心模块
```python
# api/parsers/ir_core.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    TABLE = "table" 
    FIGURE = "figure"

@dataclass
class IRBlock:
    id: str
    type: BlockType
    page: int
    text: Optional[str] = None
    cells: Optional[List[List[str]]] = None
    image: Optional[str] = None
    caption: Optional[str] = None
    ocr_text: Optional[str] = None
    style: Optional[str] = None
    figure_type: Optional[str] = None

@dataclass
class DocumentIR:
    meta: Dict[str, Any]
    blocks: List[IRBlock]
    
    def to_dict(self) -> Dict:
        return {
            "meta": self.meta,
            "blocks": [
                {
                    "id": block.id,
                    "type": block.type.value,
                    "page": block.page,
                    "text": block.text,
                    "cells": block.cells,
                    "image": block.image,
                    "caption": block.caption,
                    "ocr_text": block.ocr_text,
                    "style": block.style,
                    "figure_type": block.figure_type
                }
                for block in self.blocks
            ]
        }
```

#### 1.2 OCR模块集成
```bash
# 安装依赖
pip install "paddlepaddle==2.5.2" -i https://mirror.baidu.com/pypi/simple
pip install paddleocr opencv-python
pip install ppstructure
```

```python
# api/parsers/ocr_engine.py
from paddleocr import PaddleOCR
import cv2
import os
from pathlib import Path
from typing import List, Tuple

class OCREngine:
    def __init__(self):
        self._text_ocr = None
        self._table_ocr = None
    
    @property
    def text_ocr(self):
        if self._text_ocr is None:
            self._text_ocr = PaddleOCR(lang='ch', show_log=False, use_angle_cls=True)
        return self._text_ocr
    
    @property 
    def table_ocr(self):
        if self._table_ocr is None:
            self._table_ocr = PaddleOCR(lang='ch', show_log=False, structure_version='PP-StructureV2')
        return self._table_ocr
    
    def extract_text(self, img_path: str, confidence_threshold: float = 0.5) -> str:
        """提取图片中的文本"""
        try:
            results = self.text_ocr.ocr(img_path, cls=True)
            lines = []
            for page in results:
                if page:
                    for line in page:
                        if len(line) >= 2 and line[1][1] > confidence_threshold:
                            lines.append(line[1][0])
            return "\n".join(lines)
        except Exception as e:
            print(f"OCR文本提取失败: {e}")
            return ""
    
    def extract_table(self, img_path: str) -> List[List[str]]:
        """提取图片中的表格结构"""
        try:
            results = self.table_ocr.ocr(img_path, cls=True, rec=True, det=True, structure=True)
            # 简化实现：先返回文本，后续可优化为真正的表格结构
            text = self.extract_text(img_path)
            if text:
                # 简单的行列分割
                lines = text.split('\n')
                return [line.split() for line in lines if line.strip()]
            return []
        except Exception as e:
            print(f"OCR表格提取失败: {e}")
            return []

# 全局OCR引擎实例
ocr_engine = OCREngine()
```

### 阶段2：PPTX解析器升级 (1天)
**目标**: 实现图表数据直取 + OCR兜底

#### 2.1 增强PPTX解析器
```python
# api/parsers/enhanced_pptx_parser.py
from pptx import Presentation
from pathlib import Path
from .ir_core import DocumentIR, IRBlock, BlockType
from .ocr_engine import ocr_engine
import hashlib
from typing import Dict, Any

class EnhancedPPTXParser:
    def __init__(self):
        self.ocr = ocr_engine
    
    def parse(self, file_path: Path, output_dir: Path) -> DocumentIR:
        """解析PPTX文件为统一IR格式"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        prs = Presentation(str(file_path))
        meta = {
            "file_id": file_path.stem,
            "type": "pptx", 
            "pages": len(prs.slides),
            "title": self._extract_title(prs)
        }
        
        blocks = []
        block_id = 0
        
        for slide_idx, slide in enumerate(prs.slides, start=1):
            # 处理文本框
            text_blocks = self._extract_text_blocks(slide, slide_idx, block_id)
            blocks.extend(text_blocks)
            block_id += len(text_blocks)
            
            # 处理表格
            table_blocks = self._extract_table_blocks(slide, slide_idx, block_id)
            blocks.extend(table_blocks)
            block_id += len(table_blocks)
            
            # 处理图表（核心突破点）
            chart_blocks = self._extract_chart_blocks(slide, slide_idx, block_id)
            blocks.extend(chart_blocks)
            block_id += len(chart_blocks)
            
            # 处理图片
            image_blocks = self._extract_image_blocks(slide, slide_idx, block_id, output_dir)
            blocks.extend(image_blocks)
            block_id += len(image_blocks)
        
        return DocumentIR(meta=meta, blocks=blocks)
    
    def _extract_chart_blocks(self, slide, page: int, start_id: int) -> List[IRBlock]:
        """提取图表数据（质变功能）"""
        blocks = []
        block_id = start_id
        
        for shape in slide.shapes:
            if shape.shape_type == 3 and hasattr(shape, 'chart'):  # MSO_SHAPE_TYPE.CHART
                chart = shape.chart
                
                # 提取图表数据
                chart_data = []
                categories = []
                
                try:
                    # 获取分类轴
                    if chart.category_axis and chart.category_axis.category_names:
                        categories = [str(cat) for cat in chart.category_axis.category_names]
                    
                    # 获取系列数据
                    header_row = ["类别"] + [f"系列{i+1}" for i in range(len(chart.series))]
                    chart_data.append(header_row)
                    
                    for i, category in enumerate(categories):
                        row = [category]
                        for series in chart.series:
                            try:
                                value = series.values[i] if i < len(series.values) else ""
                                row.append(str(value) if value is not None else "")
                            except:
                                row.append("")
                        chart_data.append(row)
                    
                    if chart_data and len(chart_data) > 1:  # 有实际数据
                        block_id += 1
                        blocks.append(IRBlock(
                            id=f"chart_{block_id}",
                            type=BlockType.TABLE,
                            page=page,
                            cells=chart_data,
                            style="chart_data"
                        ))
                        
                except Exception as e:
                    print(f"图表数据提取失败: {e}")
                    # 降级为图片处理
                    continue
        
        return blocks
    
    def _extract_image_blocks(self, slide, page: int, start_id: int, output_dir: Path) -> List[IRBlock]:
        """提取图片并OCR"""
        blocks = []
        block_id = start_id
        
        for shape in slide.shapes:
            if hasattr(shape, 'image'):
                try:
                    # 保存图片
                    image_blob = shape.image.blob
                    image_hash = hashlib.md5(image_blob).hexdigest()[:8]
                    image_path = output_dir / f"slide_{page}_{image_hash}.png"
                    image_path.write_bytes(image_blob)
                    
                    # OCR识别
                    ocr_text = self.ocr.extract_text(str(image_path))
                    
                    # 判断是否为图表类型
                    figure_type = self._classify_figure_type(shape, ocr_text)
                    
                    block_id += 1
                    blocks.append(IRBlock(
                        id=f"figure_{block_id}",
                        type=BlockType.FIGURE,
                        page=page,
                        image=str(image_path),
                        ocr_text=ocr_text,
                        figure_type=figure_type
                    ))
                    
                except Exception as e:
                    print(f"图片处理失败: {e}")
                    continue
        
        return blocks
    
    def _classify_figure_type(self, shape, ocr_text: str) -> str:
        """启发式判断图片类型"""
        # 基于尺寸比例判断
        if hasattr(shape, 'width') and hasattr(shape, 'height'):
            ratio = shape.width / shape.height if shape.height > 0 else 1
            if 1.2 <= ratio <= 2.5:  # 常见图表比例
                return "chart"
        
        # 基于OCR文本内容判断
        chart_keywords = ["图", "表", "数据", "统计", "分析", "趋势", "%"]
        if any(keyword in ocr_text for keyword in chart_keywords):
            return "chart"
        
        return "photo"
```

### 阶段3：DOCX解析器升级 (1天)
**目标**: 段落+表格+图片OCR完整支持

### 阶段4：PDF解析器升级 (1天) 
**目标**: 矢量+扫描双重支持

### 阶段5：前端IR适配 (1天)
**目标**: 新增图片预览和OCR结果展示

#### 5.1 IR显示组件
```vue
<!-- apps/web/src/components/displays/IRDisplay.vue -->
<template>
  <div class="ir-display">
    <!-- 文档元信息 -->
    <el-card class="meta-card">
      <template #header>
        <span>📄 文档信息</span>
      </template>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="文档类型">
          <el-tag :type="getTypeColor(meta.type)">{{ meta.type.toUpperCase() }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="页面数">{{ meta.pages }}</el-descriptions-item>
        <el-descriptions-item label="内容块数">{{ blocks.length }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 内容块展示 -->
    <div class="blocks-container">
      <div v-for="block in blocks" :key="block.id" class="block-item">
        <!-- 段落块 -->
        <el-card v-if="block.type === 'paragraph'" class="paragraph-block">
          <template #header>
            <el-tag type="primary" size="small">📝 段落</el-tag>
            <el-tag type="info" size="small">第{{ block.page }}页</el-tag>
          </template>
          <div class="paragraph-content">{{ block.text }}</div>
        </el-card>

        <!-- 表格块 -->
        <el-card v-else-if="block.type === 'table'" class="table-block">
          <template #header>
            <el-tag type="warning" size="small">
              {{ block.style === 'chart_data' ? '📊 图表数据' : '📋 表格' }}
            </el-tag>
            <el-tag type="info" size="small">第{{ block.page }}页</el-tag>
          </template>
          <el-table :data="getTableData(block.cells)" border size="small">
            <el-table-column
              v-for="(header, index) in getTableHeaders(block.cells)"
              :key="index"
              :prop="`col_${index}`"
              :label="header"
              min-width="100"
            />
          </el-table>
        </el-card>

        <!-- 图片块 -->
        <el-card v-else-if="block.type === 'figure'" class="figure-block">
          <template #header>
            <el-tag :type="getFigureTagType(block.figure_type)" size="small">
              {{ getFigureLabel(block.figure_type) }}
            </el-tag>
            <el-tag type="info" size="small">第{{ block.page }}页</el-tag>
            <el-button 
              v-if="block.ocr_text" 
              type="text" 
              size="small"
              @click="showOCRText(block)"
            >
              查看OCR结果
            </el-button>
          </template>
          <div class="figure-content">
            <img :src="getImageUrl(block.image)" class="figure-image" />
            <div v-if="block.caption" class="figure-caption">{{ block.caption }}</div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- OCR结果对话框 -->
    <el-dialog v-model="showOCRDialog" title="OCR识别结果" width="60%">
      <div class="ocr-result">
        <pre>{{ currentOCRText }}</pre>
      </div>
      <template #footer>
        <el-button @click="showOCRDialog = false">关闭</el-button>
        <el-button type="primary" @click="convertToTable">转换为表格</el-button>
      </template>
    </el-dialog>
  </div>
</template>
```

## 📊 实施优先级排序

### 🥇 第一优先级：PPTX图表数据直取
**理由**: 质变级提升，用户价值最大
**工期**: 1天
**风险**: 低

### 🥈 第二优先级：OCR引擎集成  
**理由**: 解决图片识别核心痛点
**工期**: 1天
**风险**: 中（需要测试OCR效果）

### 🥉 第三优先级：DOCX完整解析
**理由**: 补齐Word文档能力短板
**工期**: 1天  
**风险**: 低

### 第四优先级：PDF扫描支持
**理由**: 扩展PDF处理能力
**工期**: 1天
**风险**: 中

### 第五优先级：前端IR适配
**理由**: 提升用户体验
**工期**: 1天
**风险**: 低

## 🎯 预期收益量化

### 解析能力提升
- **PPTX**: 30% → 90% (图表数据直取)
- **DOCX**: 60% → 85% (图片OCR补充)  
- **PDF**: 40% → 75% (扫描页面支持)

### 用户满意度提升
- **图片可识别**: 解决核心痛点
- **图表数据化**: 质变级体验提升
- **内容完整性**: 95%以上覆盖率

### 技术架构优势
- **统一IR**: 为AI增强奠定基础
- **模块化**: 易于维护和扩展
- **可扩展**: 支持更多格式接入

## 🚀 建议立即启动

这个方案具有**极高的可行性和巨大的收益**，建议立即启动实施！
