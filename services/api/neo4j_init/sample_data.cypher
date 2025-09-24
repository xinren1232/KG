// 创建示例数据

// 创建产品
CREATE (p1:Product {
  name: "iPhone 15",
  model: "A2846",
  category: "smartphone",
  release_date: "2023-09-15",
  status: "active"
});

CREATE (p2:Product {
  name: "Galaxy S24",
  model: "SM-S921",
  category: "smartphone", 
  release_date: "2024-01-17",
  status: "active"
});

// 创建组件
CREATE (c1:Component {
  name: "摄像头模块",
  type: "hardware",
  version: "V2.1",
  supplier: "Sony",
  criticality: "high"
});

CREATE (c2:Component {
  name: "电池模块",
  type: "hardware",
  version: "V1.5",
  supplier: "CATL",
  criticality: "high"
});

CREATE (c3:Component {
  name: "WiFi模块",
  type: "hardware",
  version: "V3.0",
  supplier: "Broadcom",
  criticality: "medium"
});

// 创建测试用例
CREATE (tc1:TestCase {
  id: "TC-CAM-001",
  title: "摄像头对焦功能测试",
  description: "验证摄像头在各种光线条件下的对焦功能",
  priority: "high",
  type: "functional",
  steps: ["打开相机应用", "切换到拍照模式", "点击屏幕进行对焦", "验证对焦效果"],
  expected_result: "摄像头能够正常对焦，图像清晰"
});

CREATE (tc2:TestCase {
  id: "TC-BAT-001", 
  title: "电池充电功能测试",
  description: "验证电池充电功能的正常性",
  priority: "high",
  type: "functional",
  steps: ["连接充电器", "观察充电指示", "检查充电速度"],
  expected_result: "电池能够正常充电，充电指示正确"
});

// 创建异常
CREATE (a1:Anomaly {
  id: "ANO-2024-001",
  title: "摄像头无法对焦",
  description: "在低光环境下摄像头无法正常对焦",
  severity: "high",
  status: "resolved",
  created_date: "2024-01-15",
  resolved_date: "2024-01-20",
  reporter: "张三"
});

// 创建症状
CREATE (s1:Symptom {
  description: "摄像头对焦失败",
  frequency: "occasional"
});

// 创建根因
CREATE (rc1:RootCause {
  description: "传感器校准偏差",
  category: "hardware"
});

// 创建对策
CREATE (cm1:Countermeasure {
  description: "重新校准摄像头传感器",
  steps: ["拆卸摄像头模块", "使用校准设备重新校准", "重新安装并测试"],
  effectiveness: "high"
});

// 建立关系
MATCH (p1:Product {name: "iPhone 15"}), (c1:Component {name: "摄像头模块"})
CREATE (p1)-[:HAS_COMPONENT]->(c1);

MATCH (p1:Product {name: "iPhone 15"}), (c2:Component {name: "电池模块"})
CREATE (p1)-[:HAS_COMPONENT]->(c2);

MATCH (p2:Product {name: "Galaxy S24"}), (c1:Component {name: "摄像头模块"})
CREATE (p2)-[:HAS_COMPONENT]->(c1);

MATCH (c1:Component {name: "摄像头模块"}), (tc1:TestCase {id: "TC-CAM-001"})
CREATE (tc1)-[:TESTS]->(c1);

MATCH (c2:Component {name: "电池模块"}), (tc2:TestCase {id: "TC-BAT-001"})
CREATE (tc2)-[:TESTS]->(c2);

MATCH (a1:Anomaly {id: "ANO-2024-001"}), (c1:Component {name: "摄像头模块"})
CREATE (a1)-[:OCCURS_IN]->(c1);

MATCH (a1:Anomaly {id: "ANO-2024-001"}), (s1:Symptom)
CREATE (a1)-[:HAS_SYMPTOM]->(s1);

MATCH (a1:Anomaly {id: "ANO-2024-001"}), (rc1:RootCause)
CREATE (a1)-[:CAUSED_BY]->(rc1);

MATCH (a1:Anomaly {id: "ANO-2024-001"}), (cm1:Countermeasure)
CREATE (a1)-[:SOLVED_BY]->(cm1);
