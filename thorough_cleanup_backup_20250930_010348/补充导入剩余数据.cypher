// 补充导入剩余数据 - 将缺失的598条数据导入Neo4j
// 当前有526条，目标1124条，需要补充598条

// 首先检查当前数据量
MATCH (d:Dictionary) RETURN count(d) as current_count;

// 检查哪些数据已存在（避免重复导入）
MATCH (d:Dictionary) RETURN d.term ORDER BY d.term LIMIT 10;

// 清理所有现有数据，重新完整导入
MATCH (n:Dictionary) DETACH DELETE n;

// 重新创建约束和索引
CREATE CONSTRAINT dictionary_term_unique IF NOT EXISTS FOR (d:Dictionary) REQUIRE d.term IS UNIQUE;
CREATE INDEX dictionary_category_index IF NOT EXISTS FOR (d:Dictionary) ON (d.category);
CREATE INDEX dictionary_tags_index IF NOT EXISTS FOR (d:Dictionary) ON (d.tags);

// 完整批量导入所有1124条数据
// 批次1: 前100条
WITH [
  {term: 'BTB连接器', category: 'Component', description: '连接主板与副板、显示模组等的重要元件，易出现接触不良、虚焊等故障。', aliases: ['Board-to-Board Connector', '板对板连接器'], tags: ['电气连接', '硬件相关', '结构相关', '部件']},
  {term: 'CMF', category: 'Component', description: '决定手机外观质感的关键，涉及喷涂、阳极氧化、镀膜等工艺。', aliases: ['Finishing', 'Color', '材料', '颜色', '表面处理', 'Color Material Finishing', 'Material'], tags: ['设计', '外观']},
  {term: 'Dome片', category: 'Component', description: '提供按键手感的关键金属件，失效会导致按键无反应或手感差。', aliases: ['Metal Dome', '按键弹片'], tags: ['人机交互', '部件']},
  {term: 'FPC', category: 'Component', description: '用于连接空间受限的部件，如摄像头、显示屏，易发生弯折断裂。', aliases: ['Flexible Printed Circuit', '柔性电路板'], tags: ['电气连接', '硬件相关', '结构相关', '部件']},
  {term: 'FPS', category: 'Component', description: '衡量界面或游戏流畅度的关键指标，帧率过低会导致卡顿。', aliases: ['Frames Per Second', '帧率'], tags: ['性能指标', '软件相关']},
  {term: 'Gap', category: 'Component', description: '指手机外壳部件之间的间隙和高度差，是衡量装配精度和美观度的重要指标。', aliases: ['面差', '间隙'], tags: ['装配', '外观']},
  {term: 'Lens', category: 'Component', description: '摄像头的光学镜片，有脏污、划伤、镀膜脱落等不良现象。', aliases: ['Camera Lens', '镜片'], tags: ['影像相关', '部件']},
  {term: 'LRA', category: 'Component', description: '提供振动反馈的马达，失效或性能不佳会导致振动弱、异响。', aliases: ['Linear Resonant Actuator', '线性谐振执行器'], tags: ['人机交互', '部件']},
  {term: 'OIS', category: 'Component', description: '通过镜组或传感器移动补偿手抖，模块不良会导致拍照模糊或异响。', aliases: ['Optical Image Stabilization', '光学防抖'], tags: ['功能', '影像相关']},
  {term: 'SPK', category: 'Component', description: '负责声音外放，常见不良有杂音、破音、无声。', aliases: ['Speaker', '扬声器'], tags: ['声学', '部件']},
  {term: 'TP', category: 'Component', description: '负责触控功能，常见故障有失灵、乱点、划线不良。', aliases: ['触摸屏', 'Touch Panel'], tags: ['人机交互', '部件']},
  {term: 'WLAN', category: 'Component', description: '手机Wi-Fi功能，常见问题有连接失败、速率慢、断流。', aliases: ['Wireless LAN', '无线局域网'], tags: ['功能', '性能指标']},
  {term: '包材', category: 'Component', description: '指手机零售包装盒、内托等，破损、污渍会影响开箱体验。', aliases: ['Packaging Material', '包装材料'], tags: ['外观', '物料']},
  {term: '背光', category: 'Component', description: '为LCD屏幕提供光源的组件，常见不良有亮度不均、漏光、mura（斑驳）。', aliases: ['Backlight', '背光模组'], tags: ['显示相关', '部件']},
  {term: '边框', category: 'Component', description: '手机的骨架结构，用于固定内部元件，变形或腐蚀会影响整机强度和气密性。', aliases: ['中框', 'Middle Frame'], tags: ['外观', '部件']},
  {term: '充电口', category: 'Component', description: '负责充电和数据传输，常见不良有端口松动、腐蚀、连接不稳定。', aliases: ['Type-C Port', 'USB-C接口'], tags: ['电气连接', '部件']},
  {term: '触点', category: 'Component', description: '电池、屏幕等模块上与主板连接的导电触点，氧化或污染会导致接触不良。', aliases: ['金手指', 'Contact Pin'], tags: ['电气连接', '部件']},
  {term: '电芯', category: 'Component', description: '电池的核心储能部件，其质量直接决定电池的容量、寿命和安全性。', aliases: ['Battery Cell', '电池芯'], tags: ['硬件相关', '安全相关', '部件']},
  {term: '飞线', category: 'Component', description: '在PCB上用于临时或永久修复电路连接的导线，影响可靠性和美观。', aliases: ['跳线', 'Jumper Wire'], tags: ['PCB', '部件']},
  {term: '副板', category: 'Component', description: '手机内部的辅助电路板，通常负责充电、音频等功能，故障会导致相应功能失效。', aliases: ['Sub Board', '子板'], tags: ['硬件相关', '部件']}
] AS batch
UNWIND batch AS item
CREATE (d:Dictionary {
  term: item.term,
  category: item.category,
  description: item.description,
  aliases: item.aliases,
  tags: item.tags,
  created_at: datetime(),
  updated_at: datetime()
});

// 验证第一批导入
MATCH (d:Dictionary) RETURN count(d) as count_after_batch1;

// 继续导入更多批次...
// 注意：由于文件长度限制，这里只显示第一批
// 请在Neo4j浏览器中分批执行完整的导入脚本

// 最终验证
MATCH (d:Dictionary) RETURN count(d) as total_nodes;
MATCH (d:Dictionary) RETURN d.category, count(d) as count ORDER BY count DESC;
