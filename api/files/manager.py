#!/usr/bin/env python3
"""
文件管理与状态机
"""

from pathlib import Path
from enum import Enum
import json
import time
import uuid
import logging

logger = logging.getLogger(__name__)

# 基础路径
BASE = Path(__file__).resolve().parent.parent
UPLOAD = BASE / "uploads"
CACHE = BASE / "cache"

# 确保目录存在
UPLOAD.mkdir(exist_ok=True)
CACHE.mkdir(exist_ok=True)

class FileStatus(str, Enum):
    """文件处理状态"""
    uploaded = "uploaded"      # 已上传
    parsing = "parsing"        # 解析中
    parsed = "parsed"          # 解析完成
    failed = "failed"          # 解析失败
    committed = "committed"    # 已入库

def new_upload(filename: str) -> str:
    """创建新的上传记录"""
    uid = str(uuid.uuid4())
    meta = {
        "id": uid,
        "name": filename,
        "status": FileStatus.uploaded,
        "created": int(time.time()),
        "updated": int(time.time())
    }
    
    meta_file = CACHE / f"{uid}.json"
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    logger.info(f"创建新上传记录: {uid} - {filename}")
    return uid

def write_file(uid: str, content: bytes) -> Path:
    """保存文件内容"""
    file_path = UPLOAD / uid
    file_path.write_bytes(content)
    
    logger.info(f"保存文件: {uid}, 大小: {len(content)} bytes")
    return file_path

def set_status(uid: str, status: FileStatus, error: str = None, **kwargs):
    """更新文件状态"""
    meta_file = CACHE / f"{uid}.json"
    
    if not meta_file.exists():
        logger.error(f"文件元数据不存在: {uid}")
        return
    
    meta = json.loads(meta_file.read_text(encoding='utf-8'))
    meta["status"] = status
    meta["updated"] = int(time.time())

    if error:
        meta["error"] = error

    # 添加额外信息
    for key, value in kwargs.items():
        meta[key] = value

    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    logger.info(f"更新文件状态: {uid} -> {status}")
    if error:
        logger.error(f"文件处理错误: {uid} - {error}")

def get_meta(uid: str) -> dict:
    """获取文件元数据"""
    meta_file = CACHE / f"{uid}.json"
    
    if not meta_file.exists():
        logger.error(f"文件元数据不存在: {uid}")
        return {"error": "文件不存在"}
    
    return json.loads(meta_file.read_text(encoding='utf-8'))

def save_preview(uid: str, data: dict):
    """保存解析预览数据"""
    preview_file = CACHE / f"{uid}.preview.json"
    preview_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    logger.info(f"保存预览数据: {uid}, 实体: {len(data.get('entities', []))}, 关系: {len(data.get('relations', []))}")

def load_preview(uid: str) -> dict:
    """加载解析预览数据"""
    preview_file = CACHE / f"{uid}.preview.json"
    
    if not preview_file.exists():
        return {"entities": [], "relations": [], "metadata": {}}
    
    return json.loads(preview_file.read_text(encoding='utf-8'))

def get_file_path(uid: str) -> Path:
    """获取文件路径"""
    return UPLOAD / uid

def save_log(uid: str, log_content: str):
    """保存处理日志"""
    log_file = CACHE / f"{uid}.log"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {log_content}\n")

def get_log(uid: str) -> str:
    """获取处理日志"""
    log_file = CACHE / f"{uid}.log"
    
    if not log_file.exists():
        return "暂无日志"
    
    return log_file.read_text(encoding="utf-8")

def cleanup_old_files(days: int = 7):
    """清理旧文件"""
    cutoff = time.time() - (days * 24 * 3600)
    
    for meta_file in CACHE.glob("*.json"):
        if meta_file.name.endswith(".preview.json"):
            continue
            
        try:
            meta = json.loads(meta_file.read_text(encoding='utf-8'))
            if meta.get("created", 0) < cutoff:
                uid = meta["id"]
                
                # 删除相关文件
                (UPLOAD / uid).unlink(missing_ok=True)
                (CACHE / f"{uid}.preview.json").unlink(missing_ok=True)
                (CACHE / f"{uid}.log").unlink(missing_ok=True)
                meta_file.unlink(missing_ok=True)
                
                logger.info(f"清理旧文件: {uid}")
        except Exception as e:
            logger.error(f"清理文件失败: {meta_file} - {e}")

def list_files(status: FileStatus = None, limit: int = 100) -> list:
    """列出文件"""
    files = []
    
    for meta_file in CACHE.glob("*.json"):
        if meta_file.name.endswith(".preview.json"):
            continue
            
        try:
            meta = json.loads(meta_file.read_text(encoding='utf-8'))
            if status is None or meta.get("status") == status:
                files.append(meta)
        except Exception as e:
            logger.error(f"读取文件元数据失败: {meta_file} - {e}")
    
    # 按创建时间倒序
    files.sort(key=lambda x: x.get("created", 0), reverse=True)
    
    return files[:limit]
