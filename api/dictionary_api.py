#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
词典管理API接口
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import io
import logging
from pathlib import Path

from .dictionary_manager import DictionaryManager, DictionaryEntry

logger = logging.getLogger(__name__)

# 初始化词典管理器
dictionary_manager = DictionaryManager()

# Pydantic模型
class DictionaryEntryModel(BaseModel):
    term: str
    aliases: List[str] = []
    category: str
    tags: List[str] = []
    definition: str = ""

class DictionaryResponse(BaseModel):
    success: bool
    message: str = ""
    data: Optional[Dict[str, Any]] = None

class BatchImportRequest(BaseModel):
    data: List[Dict[str, str]]
    strategy: str = "add_new"  # add_new, update_existing, merge

# API路由
def setup_dictionary_routes(app: FastAPI):
    """设置词典管理路由"""
    
    @app.get("/kg/dictionary/entries", response_model=DictionaryResponse)
    async def get_dictionary_entries(
        category: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ):
        """获取词典条目列表"""
        try:
            # 搜索条目
            if search:
                entries = dictionary_manager.search_entries(search, category)
            else:
                entries = list(dictionary_manager.entries.values())
                if category:
                    entries = [e for e in entries if e.category == category]
            
            # 分页
            total = len(entries)
            start = (page - 1) * page_size
            end = start + page_size
            page_entries = entries[start:end]
            
            # 转换为字典格式
            entries_data = []
            for entry in page_entries:
                entries_data.append({
                    'id': entry.get_hash(),
                    'term': entry.term,
                    'aliases': entry.aliases,
                    'category': entry.category,
                    'tags': entry.tags,
                    'definition': entry.definition,
                    'source': entry.source,
                    'created_at': entry.created_at,
                    'updated_at': entry.updated_at,
                    'version': entry.version
                })
            
            return DictionaryResponse(
                success=True,
                data={
                    'entries': entries_data,
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total + page_size - 1) // page_size
                }
            )
            
        except Exception as e:
            logger.error(f"获取词典条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/kg/dictionary/entries", response_model=DictionaryResponse)
    async def create_dictionary_entry(entry_data: DictionaryEntryModel):
        """创建词典条目"""
        try:
            entry = DictionaryEntry(
                term=entry_data.term,
                aliases=entry_data.aliases,
                category=entry_data.category,
                tags=entry_data.tags,
                definition=entry_data.definition,
                source="manual"
            )
            
            success = dictionary_manager.add_entry(entry)
            if success:
                dictionary_manager.save_dictionary()
                return DictionaryResponse(
                    success=True,
                    message="词典条目创建成功",
                    data={'id': entry.get_hash()}
                )
            else:
                return DictionaryResponse(
                    success=False,
                    message="词典条目已存在"
                )
                
        except Exception as e:
            logger.error(f"创建词典条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.put("/kg/dictionary/entries/{entry_id}", response_model=DictionaryResponse)
    async def update_dictionary_entry(entry_id: str, entry_data: DictionaryEntryModel):
        """更新词典条目"""
        try:
            entry = DictionaryEntry(
                term=entry_data.term,
                aliases=entry_data.aliases,
                category=entry_data.category,
                tags=entry_data.tags,
                definition=entry_data.definition,
                source="manual"
            )
            
            dictionary_manager.update_entry(entry)
            dictionary_manager.save_dictionary()
            
            return DictionaryResponse(
                success=True,
                message="词典条目更新成功"
            )
            
        except Exception as e:
            logger.error(f"更新词典条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.delete("/kg/dictionary/entries/{entry_id}", response_model=DictionaryResponse)
    async def delete_dictionary_entry(entry_id: str):
        """删除词典条目"""
        try:
            # 通过ID查找条目
            if entry_id in dictionary_manager.entries:
                entry = dictionary_manager.entries[entry_id]
                success = dictionary_manager.delete_entry(entry.term, entry.category)
                
                if success:
                    dictionary_manager.save_dictionary()
                    return DictionaryResponse(
                        success=True,
                        message="词典条目删除成功"
                    )
            
            return DictionaryResponse(
                success=False,
                message="词典条目不存在"
            )
            
        except Exception as e:
            logger.error(f"删除词典条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/kg/dictionary/duplicates", response_model=DictionaryResponse)
    async def find_duplicates():
        """查找重复条目"""
        try:
            duplicates = dictionary_manager.find_duplicates()
            
            return DictionaryResponse(
                success=True,
                data={
                    'duplicates': duplicates,
                    'count': len(duplicates)
                }
            )
            
        except Exception as e:
            logger.error(f"查找重复条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/kg/dictionary/remove-duplicates", response_model=DictionaryResponse)
    async def remove_duplicates(strategy: str = "keep_latest"):
        """清除重复条目"""
        try:
            result = dictionary_manager.remove_duplicates(strategy)
            dictionary_manager.save_dictionary()
            
            return DictionaryResponse(
                success=True,
                message=f"重复清除完成: 删除{result['entries_removed']}条，合并{result['entries_merged']}条",
                data=result
            )
            
        except Exception as e:
            logger.error(f"清除重复条目失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/kg/dictionary/batch-import", response_model=DictionaryResponse)
    async def batch_import_dictionary(request: BatchImportRequest):
        """批量导入词典"""
        try:
            result = dictionary_manager.batch_import_from_table(request.data)
            dictionary_manager.save_dictionary()
            
            return DictionaryResponse(
                success=True,
                message=f"批量导入完成: 新增{result['imported']}条，更新{result['updated']}条",
                data=result
            )
            
        except Exception as e:
            logger.error(f"批量导入失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/kg/dictionary/import-file", response_model=DictionaryResponse)
    async def import_dictionary_file(file: UploadFile = File(...)):
        """从文件导入词典"""
        try:
            # 读取文件内容
            content = await file.read()
            
            if file.filename.endswith('.csv'):
                # CSV文件
                df = pd.read_csv(io.StringIO(content.decode('utf-8-sig')))
            elif file.filename.endswith(('.xlsx', '.xls')):
                # Excel文件
                df = pd.read_excel(io.BytesIO(content))
            else:
                raise HTTPException(status_code=400, detail="不支持的文件格式")
            
            # 转换为字典列表
            data = df.to_dict('records')
            
            # 批量导入
            result = dictionary_manager.batch_import_from_table(data)
            dictionary_manager.save_dictionary()
            
            return DictionaryResponse(
                success=True,
                message=f"文件导入完成: 新增{result['imported']}条，更新{result['updated']}条",
                data=result
            )
            
        except Exception as e:
            logger.error(f"文件导入失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/kg/dictionary/export")
    async def export_dictionary():
        """导出词典"""
        try:
            from fastapi.responses import FileResponse
            
            file_path = dictionary_manager.export_to_csv()
            
            return FileResponse(
                path=file_path,
                filename=file_path.name,
                media_type='text/csv'
            )
            
        except Exception as e:
            logger.error(f"导出词典失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/kg/dictionary/statistics", response_model=DictionaryResponse)
    async def get_dictionary_statistics():
        """获取词典统计信息"""
        try:
            stats = dictionary_manager.get_statistics()
            
            return DictionaryResponse(
                success=True,
                data=stats
            )
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/kg/dictionary/categories", response_model=DictionaryResponse)
    async def get_categories():
        """获取所有类别"""
        try:
            categories = set()
            for entry in dictionary_manager.entries.values():
                if entry.category:
                    categories.add(entry.category)
            
            return DictionaryResponse(
                success=True,
                data={'categories': sorted(list(categories))}
            )
            
        except Exception as e:
            logger.error(f"获取类别失败: {e}")
            raise HTTPException(status_code=500, detail=str(e))
