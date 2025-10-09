// 数据模型不一致修复脚本
// 问题: Term节点应该是Dictionary节点

// 方案1: 替换标签 (推荐)

// 方案1: 将Term节点重新标记为Dictionary
MATCH (t:Term)
SET t:Dictionary
REMOVE t:Term
RETURN count(*) as migrated_count;

// 方案2: 添加标签 (保守)

// 方案2: 为Term节点添加Dictionary标签
MATCH (t:Term)
SET t:Dictionary
RETURN count(*) as updated_count;
