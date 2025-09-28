// 批次 14 - 4 条语句
// 执行前请确保Neo4j连接正常

CREATE (:Tool {name: '威布尔分布', aliases: ["Weibull分布"], tags: ["可靠性", "质量体系", "工具"], definition: '常用于可靠性数据分析的概率分布模型', example: '威布尔分布', sub_category: '统计工具', source: '词典扩展', status: 'active', updated_at: '2025-09-26 09:15:10'});
CREATE (:Tool {name: '阿伦尼乌斯模型', aliases: ["温度加速模型"], tags: ["可靠性", "质量体系", "工具"], definition: '基于化学反应速率理论的温度加速模型', example: '阿伦尼乌斯模型', sub_category: '加速模型', source: '词典扩展', status: 'active', updated_at: '2025-09-26 09:15:10'});
CREATE (:Tool {name: '艾林模型', aliases: ["温度-湿度加速模型"], tags: ["可靠性", "质量体系", "工具"], definition: '考虑温度和湿度共同作用的加速模型', example: '艾林模型', sub_category: '加速模型', source: '词典扩展', status: 'active', updated_at: '2025-09-26 09:15:10'});
CREATE (:Tool {name: '科芬-曼森关系', aliases: ["温度循环加速模型"], tags: ["可靠性", "质量体系", "工具"], definition: '基于疲劳损伤理论的温度循环加速模型', example: '科芬-曼森模型', sub_category: '加速模型', source: '词典扩展', status: 'active', updated_at: '2025-09-26 09:15:10'});
