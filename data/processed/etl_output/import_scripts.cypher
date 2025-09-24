// Scripts for data\import\anomalies.xlsx
MERGE (n:Entity:Component {key: 'Component:相机'})
SET n.name = '相机';

MERGE (n:Entity:Component {key: 'Component:摄像头'})
SET n.name = '摄像头';

MERGE (n:Entity:Component {key: 'Component:电池'})
SET n.name = '电池';

MERGE (n:Entity:Severity {key: 'Severity:S2'})
SET n.name = 'S2';

MERGE (n:Entity:Severity {key: 'Severity:S3'})
SET n.name = 'S3';

MERGE (n:Entity:Product {key: 'Product:MyPhoneX'})
SET n.name = 'MyPhoneX';

MERGE (n:Entity:Symptom {key: 'Symptom:充电慢'})
SET n.name = '充电慢';

MATCH (a:Entity {key: 'Product:MyPhoneX'})
MATCH (b:Entity {key: 'Component:摄像头'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneX'})
MATCH (b:Entity {key: 'Component:电池'})
MERGE (a)-[r:INCLUDES]->(b);

// Scripts for data\import\来料问题先后版.xlsx
MERGE (n:Entity:AnomalyID {key: 'AnomalyID:IQC-2024-001'})
SET n.name = 'IQC-2024-001';

MERGE (n:Entity:AnomalyID {key: 'AnomalyID:IQC-2024-005'})
SET n.name = 'IQC-2024-005';

MERGE (n:Entity:AnomalyID {key: 'AnomalyID:IQC-2024-002'})
SET n.name = 'IQC-2024-002';

MERGE (n:Entity:AnomalyID {key: 'AnomalyID:IQC-2024-004'})
SET n.name = 'IQC-2024-004';

MERGE (n:Entity:AnomalyID {key: 'AnomalyID:IQC-2024-003'})
SET n.name = 'IQC-2024-003';

MERGE (n:Entity:Supplier {key: 'Supplier:广州AA精密制造有限公司'})
SET n.name = '广州AA精密制造有限公司';

MERGE (n:Entity:Supplier {key: 'Supplier:深圳BB电子有限公司'})
SET n.name = '深圳BB电子有限公司';

MERGE (n:Entity:Supplier {key: 'Supplier:供应商'})
SET n.name = '供应商';

MERGE (n:Entity:Supplier {key: 'Supplier:东莞YY科技股份有限公司'})
SET n.name = '东莞YY科技股份有限公司';

MERGE (n:Entity:Supplier {key: 'Supplier:苏州ZZ光电技术有限公司'})
SET n.name = '苏州ZZ光电技术有限公司';

MERGE (n:Entity:Supplier {key: 'Supplier:深圳XX电子有限公司'})
SET n.name = '深圳XX电子有限公司';

MERGE (n:Entity:Component {key: 'Component:触摸屏'})
SET n.name = '触摸屏';

MERGE (n:Entity:Component {key: 'Component:屏幕'})
SET n.name = '屏幕';

MERGE (n:Entity:Component {key: 'Component:摄像头'})
SET n.name = '摄像头';

MERGE (n:Entity:Component {key: 'Component:电池'})
SET n.name = '电池';

MERGE (n:Entity:Component {key: 'Component:LCD'})
SET n.name = 'LCD';

MERGE (n:Entity:Component {key: 'Component:显示屏'})
SET n.name = '显示屏';

MERGE (n:Entity:Component {key: 'Component:OLED'})
SET n.name = 'OLED';

MERGE (n:Entity:Component {key: 'Component:镜头'})
SET n.name = '镜头';

MERGE (n:Entity:Component {key: 'Component:电芯'})
SET n.name = '电芯';

MERGE (n:Entity:Component {key: 'Component:扬声器'})
SET n.name = '扬声器';

MERGE (n:Entity:Symptom {key: 'Symptom:现象'})
SET n.name = '现象';

MERGE (n:Entity:Symptom {key: 'Symptom:音质异常'})
SET n.name = '音质异常';

MERGE (n:Entity:Symptom {key: 'Symptom:触摸响应不灵敏'})
SET n.name = '触摸响应不灵敏';

MERGE (n:Entity:Symptom {key: 'Symptom:对焦功能异常'})
SET n.name = '对焦功能异常';

MERGE (n:Entity:Symptom {key: 'Symptom:色彩偏差'})
SET n.name = '色彩偏差';

MERGE (n:Entity:Symptom {key: 'Symptom:杂音'})
SET n.name = '杂音';

MERGE (n:Entity:Severity {key: 'Severity:S2'})
SET n.name = 'S2';

MERGE (n:Entity:Severity {key: 'Severity:S1'})
SET n.name = 'S1';

MERGE (n:Entity:Severity {key: 'Severity:S3'})
SET n.name = 'S3';

MERGE (n:Entity:Product {key: 'Product:MyPhoneZ'})
SET n.name = 'MyPhoneZ';

MERGE (n:Entity:Product {key: 'Product:MyPhoneX'})
SET n.name = 'MyPhoneX';

MERGE (n:Entity:Product {key: 'Product:MyPhoneY'})
SET n.name = 'MyPhoneY';

MERGE (n:Entity:Status {key: 'Status:处理中'})
SET n.name = '处理中';

MERGE (n:Entity:Status {key: 'Status:分析中'})
SET n.name = '分析中';

MERGE (n:Entity:Status {key: 'Status:已关闭'})
SET n.name = '已关闭';

MERGE (n:Entity:RootCause {key: 'RootCause:磁力不足'})
SET n.name = '磁力不足';

MERGE (n:Entity:RootCause {key: 'RootCause:内阻偏高'})
SET n.name = '内阻偏高';

MERGE (n:Entity:RootCause {key: 'RootCause:导电层工艺缺陷'})
SET n.name = '导电层工艺缺陷';

MERGE (n:Entity:RootCause {key: 'RootCause:色温偏差'})
SET n.name = '色温偏差';

MERGE (n:Entity:RootCause {key: 'RootCause:根因'})
SET n.name = '根因';

MERGE (n:Entity:RootCause {key: 'RootCause:工艺问题'})
SET n.name = '工艺问题';

MERGE (n:Entity:Anomaly {key: 'Anomaly:IQC-2024-001'})
SET n.name = 'IQC-2024-001'
, n.batch_number = 'LOT-20241201-A', n.supplier = '深圳XX电子有限公司', n.component = '摄像头模组', n.component_model = 'CAM-8MP-001', n.symptom = '摄像头对焦功能异常，无法正常对焦', n.category = '功能异常', n.severity = 'S1', n.discovered_at = '2024-12-01 09:30:00', n.discovered_by = '张三', n.product = 'MyPhoneX', n.affected_quantity = '500', n.status = '处理中', n.root_cause = '镜头组装工艺问题', n.corrective_action = '要求供应商改进装配工艺', n.preventive_action = '增加来料检验项目', n.notes = '已通知供应商，等待改善方案';

MERGE (n:Entity:Anomaly {key: 'Anomaly:IQC-2024-002'})
SET n.name = 'IQC-2024-002'
, n.batch_number = 'LOT-20241202-B', n.supplier = '东莞YY科技股份有限公司', n.component = '电池模组', n.component_model = 'BAT-4000mAh-002', n.symptom = '电池充电速度明显低于规格要求', n.category = '性能不达标', n.severity = 'S2', n.discovered_at = '2024-12-02 14:15:00', n.discovered_by = '李四', n.product = 'MyPhoneY', n.affected_quantity = '200', n.status = '已关闭', n.root_cause = '电芯内阻偏高', n.corrective_action = '更换电芯供应商', n.preventive_action = '建立电芯内阻检测标准', n.closed_at = '2024-12-05 16:00:00', n.notes = '问题已解决，新批次验证通过';

MERGE (n:Entity:Anomaly {key: 'Anomaly:IQC-2024-003'})
SET n.name = 'IQC-2024-003'
, n.batch_number = 'LOT-20241203-C', n.supplier = '苏州ZZ光电技术有限公司', n.component = '显示屏', n.component_model = 'LCD-6.1-OLED-003', n.symptom = '屏幕显示出现色彩偏差，偏红现象', n.category = '外观缺陷', n.severity = 'S2', n.discovered_at = '2024-12-03 11:20:00', n.discovered_by = '王五', n.product = 'MyPhoneZ', n.affected_quantity = '150', n.status = '分析中', n.root_cause = '背光模组色温偏差', n.corrective_action = '调整背光模组参数', n.preventive_action = '增加色温检测工序', n.notes = '正在进行根因分析';

MERGE (n:Entity:Anomaly {key: 'Anomaly:IQC-2024-004'})
SET n.name = 'IQC-2024-004'
, n.batch_number = 'LOT-20241204-D', n.supplier = '广州AA精密制造有限公司', n.component = '触摸屏', n.component_model = 'TP-6.1-CAP-004', n.symptom = '触摸响应不灵敏，存在死区', n.category = '功能异常', n.severity = 'S1', n.discovered_at = '2024-12-04 08:45:00', n.discovered_by = '赵六', n.product = 'MyPhoneX', n.affected_quantity = '300', n.status = '处理中', n.root_cause = 'ITO导电层工艺缺陷', n.corrective_action = '重新制作ITO导电层', n.preventive_action = '加强ITO层质量控制', n.notes = '已退回供应商重工';

MERGE (n:Entity:Anomaly {key: 'Anomaly:IQC-2024-005'})
SET n.name = 'IQC-2024-005'
, n.batch_number = 'LOT-20241205-E', n.supplier = '深圳BB电子有限公司', n.component = '扬声器', n.component_model = 'SPK-STEREO-005', n.symptom = '扬声器音质异常，有杂音', n.category = '性能不达标', n.severity = 'S3', n.discovered_at = '2024-12-05 15:30:00', n.discovered_by = '孙七', n.product = 'MyPhoneY', n.affected_quantity = '100', n.status = '已关闭', n.root_cause = '磁铁磁力不足', n.corrective_action = '更换高性能磁铁', n.preventive_action = '建立磁力测试标准', n.closed_at = '2024-12-06 10:00:00', n.notes = '已验证新批次合格';

MATCH (a:Entity {key: 'Anomaly:IQC-2024-001'})
MATCH (b:Entity {key: 'Component:摄像头模组'})
MERGE (a)-[r:AFFECTS]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-001'})
MATCH (b:Entity {key: 'Severity:S1'})
MERGE (a)-[r:HAS_SEVERITY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-001'})
MATCH (b:Entity {key: 'Symptom:摄像头对焦功能异常，无法正常对焦'})
MERGE (a)-[r:HAS_SYMPTOM]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneX'})
MATCH (b:Entity {key: 'Component:摄像头模组'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-001'})
MATCH (b:Entity {key: 'RootCause:镜头组装工艺问题'})
MERGE (a)-[r:CAUSED_BY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-002'})
MATCH (b:Entity {key: 'Component:电池模组'})
MERGE (a)-[r:AFFECTS]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-002'})
MATCH (b:Entity {key: 'Severity:S1'})
MERGE (a)-[r:HAS_SEVERITY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-002'})
MATCH (b:Entity {key: 'Symptom:电池充电速度明显低于规格要求'})
MERGE (a)-[r:HAS_SYMPTOM]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneY'})
MATCH (b:Entity {key: 'Component:电池模组'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-002'})
MATCH (b:Entity {key: 'RootCause:电芯内阻偏高'})
MERGE (a)-[r:CAUSED_BY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-003'})
MATCH (b:Entity {key: 'Component:显示屏'})
MERGE (a)-[r:AFFECTS]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-003'})
MATCH (b:Entity {key: 'Severity:S1'})
MERGE (a)-[r:HAS_SEVERITY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-003'})
MATCH (b:Entity {key: 'Symptom:屏幕显示出现色彩偏差，偏红现象'})
MERGE (a)-[r:HAS_SYMPTOM]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneZ'})
MATCH (b:Entity {key: 'Component:显示屏'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-003'})
MATCH (b:Entity {key: 'RootCause:背光模组色温偏差'})
MERGE (a)-[r:CAUSED_BY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-004'})
MATCH (b:Entity {key: 'Component:触摸屏'})
MERGE (a)-[r:AFFECTS]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-004'})
MATCH (b:Entity {key: 'Severity:S1'})
MERGE (a)-[r:HAS_SEVERITY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-004'})
MATCH (b:Entity {key: 'Symptom:触摸响应不灵敏，存在死区'})
MERGE (a)-[r:HAS_SYMPTOM]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneX'})
MATCH (b:Entity {key: 'Component:触摸屏'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-004'})
MATCH (b:Entity {key: 'RootCause:ITO导电层工艺缺陷'})
MERGE (a)-[r:CAUSED_BY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-005'})
MATCH (b:Entity {key: 'Component:扬声器'})
MERGE (a)-[r:AFFECTS]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-005'})
MATCH (b:Entity {key: 'Severity:S1'})
MERGE (a)-[r:HAS_SEVERITY]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-005'})
MATCH (b:Entity {key: 'Symptom:扬声器音质异常，有杂音'})
MERGE (a)-[r:HAS_SYMPTOM]->(b);

MATCH (a:Entity {key: 'Product:MyPhoneY'})
MATCH (b:Entity {key: 'Component:扬声器'})
MERGE (a)-[r:INCLUDES]->(b);

MATCH (a:Entity {key: 'Anomaly:IQC-2024-005'})
MATCH (b:Entity {key: 'RootCause:磁铁磁力不足'})
MERGE (a)-[r:CAUSED_BY]->(b);

// Scripts for data\import\相关测试用例.xlsx
MERGE (n:Entity:Component {key: 'Component:触摸屏'})
SET n.name = '触摸屏';

MERGE (n:Entity:Component {key: 'Component:摄像头'})
SET n.name = '摄像头';

MERGE (n:Entity:Component {key: 'Component:电池'})
SET n.name = '电池';

MERGE (n:Entity:Component {key: 'Component:LCD'})
SET n.name = 'LCD';

MERGE (n:Entity:Component {key: 'Component:显示屏'})
SET n.name = '显示屏';

MERGE (n:Entity:Component {key: 'Component:触控'})
SET n.name = '触控';

MERGE (n:Entity:Component {key: 'Component:相机'})
SET n.name = '相机';

MERGE (n:Entity:Component {key: 'Component:扬声器'})
SET n.name = '扬声器';

MERGE (n:Entity:Severity {key: 'Severity:P2'})
SET n.name = 'P2';

MERGE (n:Entity:Severity {key: 'Severity:P1'})
SET n.name = 'P1';

MERGE (n:Entity:Product {key: 'Product:MyPhoneZ'})
SET n.name = 'MyPhoneZ';

MERGE (n:Entity:Product {key: 'Product:MyPhoneX'})
SET n.name = 'MyPhoneX';

MERGE (n:Entity:Product {key: 'Product:MyPhoneY'})
SET n.name = 'MyPhoneY';

MERGE (n:Entity:Symptom {key: 'Symptom:色彩偏差'})
SET n.name = '色彩偏差';

MERGE (n:Entity:Symptom {key: 'Symptom:杂音'})
SET n.name = '杂音';

