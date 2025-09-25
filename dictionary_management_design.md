# 词典管理系统设计文档

## 🎯 系统概述

词典管理系统是知识图谱构建助手的核心组件，专门用于管理标准化词典，支持重复清除、批量导入、持续更新等功能。

## 🏗️ 系统架构

```
📚 词典管理系统
├── 🗄️ 数据层
│   ├── DictionaryEntry (词典条目数据结构)
│   ├── JSON存储 (主要存储)
│   └── CSV导入导出 (兼容性)
├── 🔧 业务层
│   ├── DictionaryManager (核心管理器)
│   ├── 重复检测算法
│   ├── 智能合并策略
│   └── 批量导入处理
├── 🌐 API层
│   ├── RESTful接口
│   ├── 文件上传处理
│   └── 错误处理机制
└── 🖥️ 前端层
    ├── Vue3组件
    ├── 交互式界面
    └── 实时反馈
```

## 📊 数据结构设计

### 词典条目 (DictionaryEntry)

```python
@dataclass
class DictionaryEntry:
    term: str                    # 主术语
    aliases: List[str]           # 别名列表
    category: str                # 类别
    tags: List[str]              # 多标签
    definition: str              # 定义/备注
    source: str = "manual"       # 来源：manual/import/auto
    created_at: str = None       # 创建时间
    updated_at: str = None       # 更新时间
    version: int = 1             # 版本号
```

### 存储格式

```json
{
  "version": "1.0",
  "updated_at": "2025-01-24T10:30:00",
  "total_entries": 116,
  "entries": [
    {
      "term": "AQL",
      "aliases": ["接收质量限", "Acceptable Quality Level"],
      "category": "工具",
      "tags": ["测试验证", "质量体系"],
      "definition": "抽样检验的标准，用于来料或出货检验时判定批合格与否。",
      "source": "import",
      "created_at": "2025-01-24T10:00:00",
      "updated_at": "2025-01-24T10:00:00",
      "version": 1
    }
  ]
}
```

## 🔍 核心功能设计

### 1. 重复检测算法

```python
def find_duplicates(self) -> List[Dict[str, Any]]:
    """
    重复检测策略：
    1. 术语标准化（小写、去空格）
    2. 主术语和别名统一比较
    3. 按术语分组，找出重复项
    4. 返回详细的重复信息
    """
```

**检测规则**：
- 主术语相同 → 重复
- 主术语与别名相同 → 重复
- 别名之间相同 → 重复
- 忽略大小写和空格

### 2. 智能合并策略

#### 策略选项：
1. **keep_latest**: 保留最新更新的条目
2. **keep_first**: 保留最早创建的条目
3. **merge**: 智能合并所有信息

#### 合并算法：
```python
def _merge_entries(self, entries: List[DictionaryEntry]) -> DictionaryEntry:
    """
    智能合并策略：
    1. 主术语：选择最短的非空术语
    2. 别名：合并所有别名，去重
    3. 标签：合并所有标签，去重
    4. 定义：选择最详细的定义
    5. 类别：选择最常见的类别
    """
```

### 3. 批量导入处理

#### 支持格式：
- **CSV文件**: 标准逗号分隔
- **Excel文件**: .xlsx, .xls格式
- **表格数据**: JSON数组格式

#### 字段映射：
| 输入字段 | 内部字段 | 处理方式 |
|---------|---------|---------|
| 术语 | term | 必填，主键 |
| 别名 | aliases | 分号分隔，自动解析 |
| 类别 | category | 必填，分类标识 |
| 多标签 | tags | 分号分隔，自动解析 |
| 备注 | definition | 可选，详细说明 |

### 4. 数据持久化

#### 存储策略：
- **主存储**: JSON格式，结构化存储
- **备份机制**: 自动创建时间戳备份
- **版本控制**: 保留最近10个备份
- **迁移支持**: 从旧CSV格式自动迁移

## 🌐 API接口设计

### RESTful API端点

| 方法 | 端点 | 功能 | 参数 |
|-----|------|------|------|
| GET | `/kg/dictionary/entries` | 获取词典条目 | category, search, page, page_size |
| POST | `/kg/dictionary/entries` | 创建词典条目 | DictionaryEntryModel |
| PUT | `/kg/dictionary/entries/{id}` | 更新词典条目 | DictionaryEntryModel |
| DELETE | `/kg/dictionary/entries/{id}` | 删除词典条目 | - |
| GET | `/kg/dictionary/duplicates` | 查找重复条目 | - |
| POST | `/kg/dictionary/remove-duplicates` | 清除重复条目 | strategy |
| POST | `/kg/dictionary/batch-import` | 批量导入 | BatchImportRequest |
| POST | `/kg/dictionary/import-file` | 文件导入 | file |
| GET | `/kg/dictionary/export` | 导出词典 | - |
| GET | `/kg/dictionary/statistics` | 获取统计信息 | - |
| GET | `/kg/dictionary/categories` | 获取所有类别 | - |

### 响应格式

```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "entries": [...],
    "total": 116,
    "page": 1,
    "page_size": 50,
    "total_pages": 3
  }
}
```

## 🖥️ 前端界面设计

### 主要组件

1. **工具栏**
   - 搜索框：支持术语、别名、定义搜索
   - 类别筛选：下拉选择器
   - 操作按钮：新增、查找重复、导入、导出

2. **统计面板**
   - 总词条数
   - 总别名数
   - 类别数量
   - 平均别名数

3. **数据表格**
   - 分页显示
   - 排序功能
   - 批量选择
   - 行内编辑

4. **对话框**
   - 新增/编辑词条
   - 重复项管理
   - 批量导入
   - 确认操作

### 交互设计

#### 重复项处理流程：
1. 点击"查找重复"按钮
2. 系统扫描并显示重复项列表
3. 用户选择处理策略：
   - 保留最新
   - 保留最早
   - 智能合并
4. 确认操作并显示结果

#### 批量导入流程：
1. 点击"批量导入"按钮
2. 拖拽或选择文件
3. 系统解析文件内容
4. 显示导入预览
5. 确认导入并显示结果

## 🔧 技术实现

### 后端技术栈
- **Python 3.8+**: 核心语言
- **FastAPI**: Web框架
- **Pydantic**: 数据验证
- **Pandas**: 数据处理
- **pathlib**: 文件操作

### 前端技术栈
- **Vue 3**: 前端框架
- **Element Plus**: UI组件库
- **Composition API**: 状态管理
- **Axios**: HTTP客户端

### 数据处理
- **JSON**: 主要存储格式
- **CSV**: 导入导出格式
- **Excel**: 批量导入支持
- **MD5**: 条目唯一标识

## 📈 性能优化

### 算法优化
1. **哈希索引**: 使用MD5哈希快速定位条目
2. **分页加载**: 大数据集分页处理
3. **增量更新**: 只更新变化的数据
4. **缓存机制**: 统计信息缓存

### 内存优化
1. **懒加载**: 按需加载数据
2. **对象池**: 重用数据对象
3. **垃圾回收**: 及时清理无用数据

## 🛡️ 错误处理

### 数据验证
- 必填字段检查
- 数据类型验证
- 长度限制检查
- 特殊字符过滤

### 异常处理
- 文件读写异常
- 网络请求异常
- 数据解析异常
- 业务逻辑异常

### 用户反馈
- 详细错误信息
- 操作结果提示
- 进度状态显示
- 回滚机制支持

## 🚀 扩展性设计

### 插件机制
- 自定义导入格式
- 自定义合并策略
- 自定义验证规则

### 集成接口
- 外部词典API
- 翻译服务集成
- 同义词库对接

### 多语言支持
- 国际化框架
- 多语言词典
- 本地化界面

## 📊 监控指标

### 业务指标
- 词典条目总数
- 重复项发现率
- 导入成功率
- 用户活跃度

### 技术指标
- API响应时间
- 数据库查询性能
- 内存使用情况
- 错误发生率

## 🎯 未来规划

### 短期目标 (1-2个月)
- [ ] 完善重复检测算法
- [ ] 优化批量导入性能
- [ ] 增加更多文件格式支持
- [ ] 完善错误处理机制

### 中期目标 (3-6个月)
- [ ] 实现智能推荐功能
- [ ] 添加版本控制系统
- [ ] 集成外部词典API
- [ ] 支持协作编辑

### 长期目标 (6-12个月)
- [ ] 机器学习辅助管理
- [ ] 多租户支持
- [ ] 分布式部署
- [ ] 高可用架构
