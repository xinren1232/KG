# 知识图谱词典配置
# 统一数据源路径配置

# 主要数据源（推荐使用）
PRIMARY_DICTIONARY_PATH = "ontology/dictionaries"

# 支持的词典类型
DICTIONARY_TYPES = [
    "components",      # 组件词典
    "symptoms",        # 症状词典  
    "causes",          # 原因词典
    "countermeasures"  # 对策词典
]

# 标准字段定义
STANDARD_FIELDS = [
    "term",           # 术语名称（必填）
    "canonical_name", # 标准名称（必填）
    "aliases",        # 别名列表（可选）
    "category",       # 分类（必填）
    "description"     # 描述（推荐）
]

# 数据质量要求
QUALITY_REQUIREMENTS = {
    "min_completeness": 95,  # 最低完整性要求95%
    "required_fields": ["term", "canonical_name", "category"],
    "recommended_fields": ["description", "aliases"]
}
