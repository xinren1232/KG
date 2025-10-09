# ✅ 知识图谱数据补充完整清单

> **执行指南**: 按优先级逐步补充，每完成一批即可导入验证  
> **数据格式**: CSV格式，字段：术语,别名,类别,多标签,备注  
> **目标**: 从1275条 → 2000+条，评分从89.1 → 95+

---

## 📋 第一批：核心急需补充（200条）

### ✅ Material物料类（45条）- 已提供

**状态**: ✅ 已完成清单  
**数量**: 45条  
**分类**: EMC材料、热管理材料、光学材料、胶粘剂、结构材料等

<details>
<summary>点击查看完整清单（45条）</summary>

| 术语 | 别名 | 类别 | 多标签 | 备注 |
|------|------|------|--------|------|
| 导电泡棉 | Conductive Foam | Material | 物料;EMC;装配 | 屏蔽与接地用泡棉，填充缝隙抑制辐射。 |
| 屏蔽罩 | Shielding Can | Material | 物料;EMC;PCB | 焊接在PCB上的金属罩，屏蔽射频/高速器件。 |
| 导电布 | Conductive Fabric | Material | 物料;EMC | 织物型屏蔽材料，柔性粘贴易成型。 |
| 铜箔胶带 | Copper Foil Tape | Material | 物料;EMC;接地 | 背胶铜箔，常用于接地/补强屏蔽。 |
| 铝箔胶带 | Aluminum Foil Tape | Material | 物料;EMC;热管理 | 轻质导电/导热贴片，便于大面积覆盖。 |
| 镍镀层 | Nickel Plating | Material | 物料;CMF;EMC | 基材表面电镀镍层，兼顾外观与屏蔽。 |
| 石墨散热片 | Graphite Sheet | Material | 物料;热管理;硬件相关 | 各向异性导热片，导热率高、轻薄。 |
| 导热硅脂 | Thermal Grease | Material | 物料;热管理 | 介于器件与散热器之间填隙导热。 |
| 导热硅胶垫 | Thermal Pad | Material | 物料;热管理;装配 | 软性导热界面材料，容差补偿好。 |
| 石墨烯涂层 | Graphene Coating | Material | 物料;热管理;CMF | 超薄导热/散热涂层，局部热点治理。 |
| 相变导热材料 | PCM;Phase Change | Material | 物料;热管理 | 升温时吸热变相，缓解热峰值。 |
| IR滤光片 | IR Filter | Material | 物料;影像相关 | 滤除红外光，保证成像色彩准确。 |
| OCA光学胶 | OCA | Material | 物料;显示相关;点胶 | 触控/显示层间全贴合用光学胶。 |
| OCR光学胶 | OCR | Material | 物料;显示相关;点胶 | 液态灌胶式光学胶，适应曲面。 |
| 偏光片 | Polarizer | Material | 物料;显示相关 | LCD关键光学片，决定对比度与可视性。 |
| 增亮膜 | BEF;Brightness Film | Material | 物料;显示相关 | 提升出光效率与亮度均匀性。 |
| 扩散膜 | Diffuser Film | Material | 物料;显示相关 | 均匀背光，消除热点。 |
| 黑白墨 | Black&White Ink | Material | 物料;CMF;外观 | 遮光/遮盖用油墨，常用于边框。 |
| UV胶 | Ultraviolet Glue | Material | 物料;点胶;结构相关 | UV固化胶，固化快用于镜头/装饰件。 |
| 厌氧胶 | Anaerobic Adhesive | Material | 物料;点胶;装配 | 无空气接触固化，常用于螺纹锁固。 |
| 瞬干胶 | CA;瞬间胶 | Material | 物料;点胶;装配 | 快速固化，适配小面积定位。 |
| 结构胶 | Structural Adhesive | Material | 物料;点胶;结构相关 | 高强度承载用胶，耐疲劳。 |
| 发泡胶带 | Foam Tape | Material | 物料;装配;外观 | 缝隙填充/缓冲/密封用双面泡棉。 |
| 亚克力胶带 | Acrylic Tape | Material | 物料;装配 | 高粘接强度，耐候性好。 |
| PET离型膜 | Release Film | Material | 物料;装配 | 保护胶面/器件表面，便于工序转移。 |
| PI胶带 | Kapton Tape | Material | 物料;PCB;热管理 | 耐高温绝缘胶带，回流/维修常用。 |
| 泡棉垫片 | Foam Gasket | Material | 物料;结构相关 | 密封/防尘/缓冲垫片。 |
| 防水透气膜 | Vent Membrane | Material | 物料;可靠性 | 兼顾防水与压力平衡，提升气密/声学。 |
| 麦拉片 | Mylar | Material | 物料;绝缘;结构相关 | 绝缘/介电/屏蔽隔断用薄膜。 |
| EMI导电胶 | Conductive Adhesive | Material | 物料;EMC;点胶 | 胶体内含导电填料，点胶成型屏蔽。 |
| 含银导电胶 | Silver Epoxy | Material | 物料;EMC;封装 | 高导电性，器件互连/修补。 |
| UV黑胶 | UV Black | Material | 物料;点胶;影像相关 | 光学防溢光封堵，抑制杂散光。 |
| 防指纹涂层 | AF Coating | Material | 物料;CMF;外观 | 疏油疏水，提升触感与清洁度。 |
| 防眩涂层 | AG Coating | Material | 物料;显示相关;CMF | 降低反射，改善户外可读性。 |
| 防反涂层 | AR Coating | Material | 物料;显示相关;CMF | 降低界面反射，提高透过率。 |
| UV清洗剂 | UV Cleaner | Material | 物料;制造工艺 | 去除UV胶残留/污染的专用溶剂。 |
| 无水乙醇 | Ethanol | Material | 物料;清洁;制造工艺 | 常用清洗/脱水溶剂。 |
| 异丙醇 | IPA | Material | 物料;清洁;制造工艺 | PCB/镜片清洁常用溶剂。 |
| 丙酮 | Acetone | Material | 物料;清洁;制造工艺 | 强溶剂，迅速去油墨/残胶（注意兼容）。 |
| 环氧树脂 | Epoxy | Material | 物料;封装;结构相关 | 高强度胶粘/封装材料。 |
| ABS塑料 | ABS | Material | 物料;结构相关 | 外壳常用工程塑料，韧性好。 |
| PC塑料 | Polycarbonate | Material | 物料;结构相关 | 高强度透明塑料，抗冲击。 |
| 铝合金 | Aluminum Alloy | Material | 物料;结构相关;CMF | 轻质高强，机加工/阳极常用。 |
| 不锈钢 | Stainless Steel | Material | 物料;结构相关;CMF | 强度与耐腐蚀兼顾，外观/骨架。 |
| LCP材料 | LCP | Material | 物料;射频相关;电气性能 | 低介损高频材料，天线/射频走线基材。 |

</details>

**导入方式**: 直接使用提供的表格数据，转换为CSV格式导入

---

### 🎯 摄像头硬件组件（20条）- 待补充

**优先级**: ⭐⭐⭐⭐⭐  
**类别**: Component  
**标签**: 部件;硬件相关;摄像头模组

```
待补充清单:
1. 图像传感器,CMOS Sensor;Image Sensor;Sensor,Component,部件;硬件相关;摄像头模组,将光信号转换为电信号的核心器件，常见品牌有Sony、Samsung、OmniVision
2. VCM马达,音圈马达;Voice Coil Motor;对焦马达,Component,部件;硬件相关;摄像头模组,驱动镜头移动实现自动对焦的马达，失效会导致对焦失败或异响
3. ISP,图像信号处理器;Image Signal Processor,Component,部件;软件相关;摄像头模组,负责图像优化处理，包括降噪、白平衡、色彩校正等
4. 红外滤光片,IR Filter;IR Cut Filter,Component,部件;硬件相关;摄像头模组,过滤红外光线，防止红外光干扰成像质量
5. 镜头模组,Lens Module;镜头组,Component,部件;硬件相关;摄像头模组,由多片镜片组成的光学系统，决定成像质量
6. 镜头座,Lens Holder;Lens Barrel,Component,部件;结构相关;摄像头模组,固定镜片的结构件，精度影响光轴对准
7. 对焦驱动IC,AF Driver IC,Component,部件;硬件相关;摄像头模组,控制VCM马达的驱动芯片
8. OIS光学防抖,Optical Image Stabilization;防抖,Component,部件;硬件相关;摄像头模组,通过镜头或传感器位移补偿抖动，提升成像稳定性
9. 闪光灯模组,Flash Module;LED闪光灯,Component,部件;硬件相关;摄像头模组,提供补光，改善暗光拍摄效果
10. 前置摄像头,Front Camera;自拍摄像头,Component,部件;硬件相关;摄像头模组,用于自拍和视频通话的前置摄像头
11. 后置摄像头,Rear Camera;主摄像头,Component,部件;硬件相关;摄像头模组,主要拍摄摄像头，通常位于手机背面
12. 广角镜头,Wide Angle Lens;超广角,Component,部件;硬件相关;摄像头模组,视场角大于80度的镜头，适合风景拍摄
13. 长焦镜头,Telephoto Lens;远摄镜头,Component,部件;硬件相关;摄像头模组,焦距较长，实现光学变焦和远距拍摄
14. 微距镜头,Macro Lens,Component,部件;硬件相关;摄像头模组,专门用于近距离拍摄的镜头
15. ToF传感器,Time of Flight Sensor;飞行时间传感器,Component,部件;硬件相关;摄像头模组,通过测量光飞行时间获取深度信息
16. 激光对焦模组,Laser AF Module,Component,部件;硬件相关;摄像头模组,发射激光测距辅助对焦，提升暗光对焦速度
17. PDAF相位对焦,Phase Detection Auto Focus,Component,部件;硬件相关;摄像头模组,通过相位差检测实现快速对焦
18. 双摄模组,Dual Camera Module,Component,部件;硬件相关;摄像头模组,两个摄像头协同工作，实现景深或变焦
19. 三摄模组,Triple Camera Module,Component,部件;硬件相关;摄像头模组,三个摄像头组合，覆盖广角、主摄、长焦
20. 潜望式镜头,Periscope Lens,Component,部件;硬件相关;摄像头模组,横向排列光路，实现高倍光学变焦
```

---

### 🔴 摄像头症状问题（15条）- 待补充

**优先级**: ⭐⭐⭐⭐⭐  
**类别**: Symptom  
**标签**: 异常现象;影像相关;摄像头模组

```
待补充清单:
1. 对焦慢,Slow Focus;对焦速度慢,Symptom,异常现象;影像相关;摄像头模组,对焦时间超过正常范围，影响抓拍体验
2. 拍照模糊,Blurry Photo;成像模糊,Symptom,异常现象;影像相关;摄像头模组,照片清晰度不足，细节丢失
3. 白平衡异常,White Balance Error;色温偏差,Symptom,异常现象;影像相关;摄像头模组,照片色温不准确，偏黄或偏蓝
4. 曝光异常,Exposure Error;曝光不准,Symptom,异常现象;影像相关;摄像头模组,照片过曝或欠曝，亮度不合理
5. 色彩偏差,Color Shift;色彩失真,Symptom,异常现象;影像相关;摄像头模组,照片色彩还原不准确
6. 噪点过多,High Noise;噪声大,Symptom,异常现象;影像相关;摄像头模组,暗光或高ISO下噪点明显，影响画质
7. 暗角,Vignetting;四角发暗,Symptom,异常现象;影像相关;摄像头模组,照片四周亮度低于中心
8. 鬼影,Ghosting;重影,Symptom,异常现象;影像相关;摄像头模组,强光源周围出现虚影
9. 炫光,Flare;光斑,Symptom,异常现象;影像相关;摄像头模组,逆光时出现光斑或光晕
10. 摄像头黑屏,Camera Black Screen;摄像头无显示,Symptom,异常现象;影像相关;摄像头模组,打开相机应用无图像显示
11. 摄像头花屏,Camera Distortion;图像异常,Symptom,异常现象;影像相关;摄像头模组,图像出现条纹、色块等异常
12. 摄像头异响,Camera Noise;对焦异响,Symptom,异常现象;影像相关;摄像头模组,对焦或拍摄时发出异常声音
13. 摄像头发热,Camera Overheating;摄像头温度高,Symptom,异常现象;影像相关;摄像头模组,长时间使用摄像头温度异常升高
14. 录像卡顿,Video Lag;视频不流畅,Symptom,异常现象;影像相关;摄像头模组,录制视频时出现卡顿或掉帧
15. 对焦漂移,Focus Drift;跑焦,Symptom,异常现象;影像相关;摄像头模组,对焦后焦点位置发生偏移
```

---

### 📊 质量管理方法（15条）- 待补充

**优先级**: ⭐⭐⭐⭐⭐  
**类别**: Tool  
**标签**: 质量体系;测试验证;工具

```
待补充清单:
1. 8D报告,8 Disciplines;8D方法,Tool,质量体系;问题解决;工具,系统化问题解决方法，包含8个步骤从根因到预防
2. FMEA,失效模式与影响分析;Failure Mode and Effects Analysis,Tool,质量体系;风险管理;工具,预防性分析工具，识别潜在失效模式及其影响
3. SPC,统计过程控制;Statistical Process Control,Tool,质量体系;过程控制;工具,利用统计方法监控和控制过程稳定性
4. MSA,测量系统分析;Measurement System Analysis,Tool,质量体系;测试验证;工具,评估测量系统的准确性、精密度和稳定性
5. APQP,产品质量先期策划;Advanced Product Quality Planning,Tool,质量体系;项目管理;工具,产品开发全流程质量策划方法
6. PPAP,生产件批准程序;Production Part Approval Process,Tool,质量体系;供应商管理;工具,确保供应商能够满足生产要求的验证流程
7. 5Why分析,5 Whys Analysis;五问法,Tool,质量体系;根因分析;工具,通过连续5次追问"为什么"找到问题根因
8. 鱼骨图,Fishbone Diagram;Ishikawa Diagram;因果图,Tool,质量体系;根因分析;工具,图形化展示问题与原因的因果关系
9. 帕累托图,Pareto Chart;80/20法则,Tool,质量体系;数据分析;工具,识别影响最大的少数关键因素
10. 控制图,Control Chart;管制图,Tool,质量体系;过程控制;工具,监控过程是否处于统计受控状态
11. 过程能力分析,Process Capability Analysis;Cpk,Tool,质量体系;过程评估;工具,评估过程满足规格要求的能力
12. 根因分析,Root Cause Analysis;RCA,Tool,质量体系;问题解决;工具,系统化方法找到问题的根本原因
13. 纠正预防措施,CAPA;Corrective and Preventive Action,Tool,质量体系;持续改进;工具,针对问题采取纠正和预防措施
14. 质量门,Quality Gate;质量关卡,Tool,质量体系;项目管理;工具,项目各阶段的质量检查点和放行标准
15. 质量审核,Quality Audit;审核,Tool,质量体系;合规性;工具,系统化检查质量体系的符合性和有效性
```

---

### 🔍 质量检验术语（10条）- 待补充

**优先级**: ⭐⭐⭐⭐⭐  
**类别**: Process  
**标签**: 质量体系;测试验证;制造工艺

```
待补充清单:
1. IQC,来料质量控制;Incoming Quality Control,Process,质量体系;测试验证;制造工艺,对供应商来料进行质量检验和控制
2. IPQC,制程质量控制;In-Process Quality Control,Process,质量体系;测试验证;制造工艺,生产过程中的质量监控和控制
3. FQC,最终质量控制;Final Quality Control,Process,质量体系;测试验证;制造工艺,成品出货前的最终质量检验
4. OQC,出货质量控制;Outgoing Quality Control,Process,质量体系;测试验证;制造工艺,出货前的质量确认和放行
5. OBA,开箱审核;Open Box Audit,Process,质量体系;测试验证;用户体验,模拟用户开箱检查产品质量和包装
6. 首件检验,First Article Inspection;FAI,Process,质量体系;测试验证;制造工艺,生产首件的全面检验确认
7. 巡检,Patrol Inspection;巡回检验,Process,质量体系;测试验证;制造工艺,定时巡查生产线质量状况
8. 全检,100% Inspection;逐件检验,Process,质量体系;测试验证;制造工艺,对所有产品进行逐一检验
9. 抽检,Sampling Inspection;抽样检验,Process,质量体系;测试验证;制造工艺,按一定比例抽取样品进行检验
10. 免检,Inspection Waiver;免检放行,Process,质量体系;供应商管理;制造工艺,对优质供应商实施的免检政策
```

---

## 📋 第二批：重要补充（150条）

### 🎬 摄像头测试方法（15条）
### 🏭 摄像头工艺流程（10条）
### 📏 摄像头性能指标（5条）
### 📊 质量指标（10条）
### 📜 质量标准（8条）
### 📺 显示屏技术术语（15条）
### 🔴 显示屏症状（10条）
### 🧪 显示屏测试（10条）
### 📡 射频组件（15条）
### 🔴 射频症状（10条）
### 🧪 射频测试（11条）
### ⚡ 电池相关术语（15条）
### 🔊 音频相关术语（16条）

**详细清单**: 参见 `DATA_SUPPLEMENT_PLAN.md`

---

## 📋 第三批：根因与解决方案（100条）

### 🔍 根因分类（30条）
- 硬件根因（10条）
- 软件根因（10条）
- 工艺根因（10条）

### 💡 解决方案分类（40条）
- 硬件解决方案（10条）
- 软件解决方案（10条）
- 工艺解决方案（10条）
- 预防措施（10条）

### 🔗 关系建立（30条关系类型定义）

**详细清单**: 参见 `DATA_SUPPLEMENT_PLAN.md`

---

## 📝 执行步骤

### Step 1: 准备CSV文件
```bash
# 创建CSV文件，包含以下字段
术语,别名,类别,多标签,备注
```

### Step 2: 分批导入
```bash
# 第一批：Material + 摄像头 + 质量体系（155条）
# 第二批：显示屏 + 射频 + 电池音频（150条）
# 第三批：根因 + 解决方案（100条）
```

### Step 3: 验证导入
```bash
# 运行质量检查脚本
python check_dictionary_quality.py
```

### Step 4: 建立关系
```cypher
# 使用Cypher语句建立节点间关系
# 参见 DATA_SUPPLEMENT_PLAN.md 第二章
```

---

## ✅ 预期成果

**第一批完成后**:
- 术语数: 1275 → 1430 (+155)
- Material覆盖: 55 → 100 (+45)
- 摄像头覆盖: 35 → 70 (+35)
- 质量体系覆盖: 7 → 32 (+25)

**全部完成后**:
- 术语数: 1275 → 2000+ (+725)
- 关系数: 4910 → 10000+ (+5090)
- 综合评分: 89.1 → 95+
- 智能助手能力: 全面提升

---

**建议**: 先完成第一批（Material已有+摄像头+质量体系），验证效果后再继续后续批次。
