#!/usr/bin/env python3
"""
API代码重构启动脚本
自动创建目录结构并生成模板文件
"""

import paramiko
import os
from datetime import datetime

class RefactoringHelper:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ssh = None
        self.project_dir = "/opt/knowledge-graph/api"
    
    def connect(self):
        """连接服务器"""
        print(f"🔌 连接服务器 {self.host}...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.username, password=self.password)
        print("✅ 连接成功")
    
    def execute_command(self, command, description=""):
        """执行命令"""
        if description:
            print(f"\n📝 {description}")
        
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "warning" not in error.lower():
            print(f"   ⚠️ {error[:200]}")
        
        return output, error
    
    def backup_main_py(self):
        """备份main.py"""
        print("\n" + "="*80)
        print("📦 步骤1: 备份main.py")
        print("="*80)
        
        backup_script = f"""
cd {self.project_dir}
if [ -f main.py ]; then
    cp main.py main.py.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ 已备份main.py"
    ls -lh main.py*
else
    echo "⚠️ main.py不存在"
fi
"""
        
        output, error = self.execute_command(backup_script, "备份main.py")
        print(output)
    
    def create_directory_structure(self):
        """创建目录结构"""
        print("\n" + "="*80)
        print("📁 步骤2: 创建目录结构")
        print("="*80)
        
        structure_script = f"""
cd {self.project_dir}

# 创建目录
mkdir -p routers services models utils

# 创建__init__.py文件
touch routers/__init__.py
touch services/__init__.py
touch models/__init__.py
touch utils/__init__.py

echo "✅ 目录结构创建完成"
tree -L 2 . || ls -la
"""
        
        output, error = self.execute_command(structure_script, "创建目录结构")
        print(output)
    
    def create_router_templates(self):
        """创建router模板文件"""
        print("\n" + "="*80)
        print("📄 步骤3: 创建Router模板")
        print("="*80)
        
        # Graph Router
        graph_router = '''"""
图谱相关API路由
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys
sys.path.append('..')
from cache.redis_manager import cache_result

router = APIRouter(prefix="/kg", tags=["知识图谱"])

@router.get("/stats")
@cache_result("stats", ttl=300)
async def get_statistics():
    """获取图谱统计信息"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": {
            "total_nodes": 0,
            "total_relationships": 0
        }
    }

@router.get("/graph")
@cache_result("graph", ttl=600)
async def get_graph_data(
    limit: int = Query(100, ge=1, le=5000),
    show_all: bool = Query(False)
):
    """获取图谱数据"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": {
            "nodes": [],
            "relationships": []
        }
    }

@router.get("/entities")
async def get_entities(entity_type: Optional[str] = None):
    """获取实体列表"""
    # TODO: 从main.py移动代码
    return {"ok": True, "data": []}

@router.get("/relations")
async def get_relations():
    """获取关系列表"""
    # TODO: 从main.py移动代码
    return {"ok": True, "data": []}
'''
        
        # Dictionary Router
        dictionary_router = '''"""
词典相关API路由
"""
from fastapi import APIRouter, Query
from typing import Optional
import sys
sys.path.append('..')
from cache.redis_manager import cache_result

router = APIRouter(prefix="/kg", tags=["词典管理"])

@router.get("/dictionary")
@cache_result("dictionary", ttl=1800)
async def get_dictionary(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=10000),
    category: Optional[str] = None,
    search: Optional[str] = None
):
    """获取词典数据"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": [],
        "total": 0
    }

@router.get("/dictionary/categories")
@cache_result("dict_categories", ttl=3600)
async def get_categories():
    """获取分类列表"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": []
    }

@router.get("/dictionary/stats")
@cache_result("dict_stats", ttl=600)
async def get_dictionary_stats():
    """获取词典统计"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": {
            "total_terms": 0,
            "total_categories": 0
        }
    }
'''
        
        # Stats Router
        stats_router = '''"""
统计相关API路由
"""
from fastapi import APIRouter
import sys
sys.path.append('..')
from cache.redis_manager import cache_result

router = APIRouter(prefix="/kg", tags=["统计分析"])

@router.get("/real-stats")
@cache_result("real_stats", ttl=300)
async def get_real_statistics():
    """获取实时统计"""
    # TODO: 从main.py移动代码
    return {
        "ok": True,
        "data": {}
    }
'''
        
        # 创建文件
        create_files_script = f"""
cd {self.project_dir}/routers

# Graph Router
cat > graph.py << 'EOF'
{graph_router}
EOF

# Dictionary Router
cat > dictionary.py << 'EOF'
{dictionary_router}
EOF

# Stats Router
cat > stats.py << 'EOF'
{stats_router}
EOF

# __init__.py
cat > __init__.py << 'EOF'
from . import graph, dictionary, stats

__all__ = ['graph', 'dictionary', 'stats']
EOF

echo "✅ Router模板创建完成"
ls -lh
"""
        
        output, error = self.execute_command(create_files_script, "创建Router模板")
        print(output)
    
    def create_cache_management(self):
        """创建缓存管理端点"""
        print("\n" + "="*80)
        print("🗄️ 步骤4: 创建缓存管理端点")
        print("="*80)
        
        cache_router = '''"""
缓存管理API路由
"""
from fastapi import APIRouter, Query
import sys
sys.path.append('..')
from cache.redis_manager import redis_manager

router = APIRouter(prefix="/cache", tags=["缓存管理"])

@router.post("/clear")
async def clear_cache(pattern: str = Query("*", description="缓存键模式")):
    """清除缓存"""
    try:
        if redis_manager.redis:
            keys = await redis_manager.redis.keys(pattern)
            if keys:
                await redis_manager.redis.delete(*keys)
                return {
                    "ok": True,
                    "message": f"已清除 {len(keys)} 个缓存",
                    "count": len(keys)
                }
            else:
                return {
                    "ok": True,
                    "message": "没有匹配的缓存",
                    "count": 0
                }
        else:
            return {
                "ok": False,
                "message": "Redis未连接"
            }
    except Exception as e:
        return {
            "ok": False,
            "message": f"清除缓存失败: {str(e)}"
        }

@router.get("/stats")
async def cache_stats():
    """缓存统计"""
    try:
        if redis_manager.redis:
            info = await redis_manager.redis.info("stats")
            hits = info.get("keyspace_hits", 0)
            misses = info.get("keyspace_misses", 0)
            total = hits + misses
            hit_rate = hits / total if total > 0 else 0
            
            return {
                "ok": True,
                "data": {
                    "hits": hits,
                    "misses": misses,
                    "total_requests": total,
                    "hit_rate": f"{hit_rate*100:.1f}%",
                    "total_keys": await redis_manager.redis.dbsize()
                }
            }
        else:
            return {
                "ok": False,
                "message": "Redis未连接"
            }
    except Exception as e:
        return {
            "ok": False,
            "message": f"获取统计失败: {str(e)}"
        }
'''
        
        create_cache_script = f"""
cd {self.project_dir}/routers

cat > cache.py << 'EOF'
{cache_router}
EOF

echo "✅ 缓存管理端点创建完成"
"""
        
        output, error = self.execute_command(create_cache_script, "创建缓存管理")
        print(output)
    
    def create_refactoring_guide(self):
        """创建重构指南"""
        print("\n" + "="*80)
        print("📖 步骤5: 创建重构指南")
        print("="*80)
        
        guide = f"""# API重构指南

## 已完成的工作

### 1. 目录结构
```
{self.project_dir}/
├── main.py (原文件，已备份)
├── main.py.backup.YYYYMMDD_HHMMSS
├── routers/
│   ├── __init__.py
│   ├── graph.py (图谱API)
│   ├── dictionary.py (词典API)
│   ├── stats.py (统计API)
│   └── cache.py (缓存管理)
├── services/
│   └── __init__.py
├── models/
│   └── __init__.py
└── utils/
    └── __init__.py
```

### 2. Router模板
已创建4个router模板文件，包含基本的API端点结构。

## 下一步操作

### 步骤1: 从main.py提取代码

1. **提取图谱相关代码** → `routers/graph.py`
   - get_statistics()
   - get_graph_data()
   - get_entities()
   - get_relations()

2. **提取词典相关代码** → `routers/dictionary.py`
   - get_dictionary()
   - get_categories()
   - get_dictionary_stats()

3. **提取统计相关代码** → `routers/stats.py`
   - get_real_statistics()

### 步骤2: 修改main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import graph, dictionary, stats, cache
from cache.redis_manager import redis_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.disconnect()

app = FastAPI(
    title="知识图谱核心API",
    version="2.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(graph.router)
app.include_router(dictionary.router)
app.include_router(stats.router)
app.include_router(cache.router)

@app.get("/")
async def root():
    return {{
        "message": "知识图谱核心API",
        "version": "2.1.0",
        "docs": "/docs"
    }}
```

### 步骤3: 测试

```bash
# 重启API服务
systemctl restart kg-api

# 测试端点
curl http://localhost:8000/health
curl http://localhost:8000/kg/stats
curl http://localhost:8000/cache/stats

# 查看API文档
open http://localhost:8000/docs
```

### 步骤4: 验证

- [ ] 所有API端点正常工作
- [ ] 缓存功能正常
- [ ] API文档正确显示
- [ ] 性能没有下降

## 注意事项

1. **保留备份**: main.py.backup文件不要删除
2. **逐步迁移**: 一次迁移一个router，测试通过后再继续
3. **保持兼容**: 确保API端点路径不变
4. **测试缓存**: 验证缓存装饰器正常工作

## 回滚方案

如果出现问题，可以快速回滚：

```bash
cd {self.project_dir}
cp main.py.backup.* main.py
systemctl restart kg-api
```

---

**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**下次检查**: 重构完成后
"""
        
        save_guide_script = f"""
cd {self.project_dir}

cat > REFACTORING_GUIDE.md << 'EOF'
{guide}
EOF

echo "✅ 重构指南创建完成"
cat REFACTORING_GUIDE.md
"""
        
        output, error = self.execute_command(save_guide_script, "创建重构指南")
        print(output)
    
    def run_all(self):
        """执行所有步骤"""
        try:
            self.connect()
            
            self.backup_main_py()
            self.create_directory_structure()
            self.create_router_templates()
            self.create_cache_management()
            self.create_refactoring_guide()
            
            print("\n" + "="*80)
            print("🎉 重构准备工作完成！")
            print("="*80)
            print("\n下一步:")
            print("1. 查看重构指南: cat /opt/knowledge-graph/api/REFACTORING_GUIDE.md")
            print("2. 开始迁移代码: 从main.py提取代码到各个router")
            print("3. 测试验证: 确保所有API正常工作")
            print("4. 重启服务: systemctl restart kg-api")
            
        except Exception as e:
            print(f"\n❌ 执行失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.ssh:
                self.ssh.close()

def main():
    print("="*80)
    print("🔧 API代码重构 - 准备工作")
    print("="*80)
    
    helper = RefactoringHelper(
        host="47.108.152.16",
        username="root",
        password="Zxylsy.99"
    )
    
    helper.run_all()

if __name__ == "__main__":
    main()

