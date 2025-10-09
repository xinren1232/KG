# 🚀 服务器词典和图谱更新部署指南

> **服务器**: 47.108.152.16  
> **部署时间**: 2025-10-06  
> **更新内容**: 新增51条词典数据（1275 → 1326）

---

## 📋 部署前检查清单

### 本地准备
- ✅ 词典数据已更新: `api/data/dictionary.json` (1326条)
- ✅ 数据质量已验证: 综合评分 89.9/100
- ✅ 同步脚本已准备: `sync_to_neo4j.py`
- ✅ 部署脚本已准备: `deploy_to_server.sh`

### 服务器状态
- ⚠️ 需要确认: Neo4j服务运行状态
- ⚠️ 需要确认: 后端API服务运行状态
- ⚠️ 需要确认: 磁盘空间充足

---

## 🎯 部署方案

### 方案A: 自动化部署（推荐）⭐⭐⭐⭐⭐

**使用部署脚本一键完成**

```bash
# Windows PowerShell
bash deploy_to_server.sh

# 或者使用Git Bash
./deploy_to_server.sh
```

**脚本执行步骤**:
1. 备份服务器现有词典
2. 上传更新后的词典文件
3. 上传Neo4j同步脚本
4. 在服务器上同步到Neo4j
5. 重启后端API服务
6. 验证部署结果

**预计时间**: 3-5分钟

---

### 方案B: 手动部署（备选）

#### 步骤1: 备份服务器数据

```bash
ssh root@47.108.152.16

cd /opt/knowledge-graph
mkdir -p backups
cp api/data/dictionary.json backups/dictionary_backup_$(date +%Y%m%d_%H%M%S).json
```

#### 步骤2: 上传词典文件

```bash
# 在本地执行
scp api/data/dictionary.json root@47.108.152.16:/opt/knowledge-graph/api/data/
```

#### 步骤3: 上传同步脚本

```bash
# 在本地执行
scp sync_to_neo4j.py root@47.108.152.16:/opt/knowledge-graph/
```

#### 步骤4: 同步到Neo4j

```bash
# 在服务器上执行
ssh root@47.108.152.16

cd /opt/knowledge-graph
python3 sync_to_neo4j.py
```

#### 步骤5: 重启API服务

```bash
# 在服务器上执行
systemctl restart kg-api
systemctl status kg-api
```

#### 步骤6: 验证部署

```bash
# 检查API状态
curl http://47.108.152.16/kg/stats
```

---

## 🔍 验证步骤

### 1. 检查词典数量

**访问**: http://47.108.152.16/kg/dictionary

**预期结果**:
```json
{
  "total": 1326,
  "categories": {
    "Symptom": 280,
    "TestCase": 242,
    "Metric": 197,
    "Component": 194,
    "Process": 186,
    "Tool": 109,
    "Role": 63,
    "Material": 55
  }
}
```

### 2. 检查图谱统计

**访问**: http://47.108.152.16/kg/stats

**预期结果**:
```json
{
  "nodes": 1421,
  "relationships": 4910,
  "categories": 8,
  "tags": 129
}
```

### 3. 测试新增术语搜索

**测试用例**:

```bash
# 测试1: 搜索新增的Symptom
curl "http://47.108.152.16/kg/search?q=白平衡偏移"

# 测试2: 搜索新增的Component
curl "http://47.108.152.16/kg/search?q=CMOS图像传感器"

# 测试3: 搜索新增的Tool
curl "http://47.108.152.16/kg/search?q=光学暗箱"

# 测试4: 搜索新增的TestCase
curl "http://47.108.152.16/kg/search?q=AF成功率测试"
```

### 4. 检查图谱可视化

**访问**: http://47.108.152.16

**检查项**:
- ✅ 图谱节点数量显示为 1421
- ✅ 新增节点正确显示颜色
- ✅ 节点标签正确显示
- ✅ 图例完整显示

---

## 🔧 Neo4j同步详细说明

### 同步脚本功能

`sync_to_neo4j.py` 脚本会执行以下操作：

1. **连接Neo4j数据库**
   - URI: bolt://localhost:7687
   - 用户: neo4j
   - 密码: password123

2. **创建节点**
   - Term节点: 1326个（词典条目）
   - Tag节点: 129个（标签）
   - Category节点: 8个（分类）

3. **创建关系**
   - HAS_TAG: Term → Tag
   - BELONGS_TO: Term → Category

4. **统计验证**
   - 节点总数
   - 关系总数
   - 各类型节点数量

### 同步模式

**增量同步（默认）**:
```bash
python3 sync_to_neo4j.py
```
- 保留现有图谱数据
- 仅添加新增节点和关系
- 更新已存在节点的属性

**完全重建（可选）**:
```bash
python3 sync_to_neo4j.py --clear
```
- ⚠️ 清空现有图谱
- 重新创建所有节点和关系
- 用于修复数据不一致问题

---

## ⚠️ 注意事项

### 1. 备份重要性

**必须备份**:
- ✅ dictionary.json
- ✅ Neo4j数据库（可选）

**备份位置**: `/opt/knowledge-graph/backups/`

### 2. 服务中断

**预计中断时间**: 1-2分钟
- API服务重启: ~10秒
- Neo4j同步: ~30-60秒

**建议**: 在业务低峰期执行

### 3. 回滚方案

**如果部署失败**:

```bash
# 1. 恢复词典文件
ssh root@47.108.152.16
cd /opt/knowledge-graph
cp backups/dictionary_backup_*.json api/data/dictionary.json

# 2. 重启服务
systemctl restart kg-api

# 3. 验证
curl http://47.108.152.16/kg/stats
```

### 4. 常见问题

**问题1: Neo4j连接失败**
```
解决: 检查Neo4j服务状态
systemctl status neo4j
systemctl start neo4j
```

**问题2: API服务启动失败**
```
解决: 查看日志
journalctl -u kg-api -n 50
```

**问题3: 词典文件权限错误**
```
解决: 修正权限
chown -R root:root /opt/knowledge-graph/api/data/
chmod 644 /opt/knowledge-graph/api/data/dictionary.json
```

---

## 📊 部署后数据对比

| 项目 | 部署前 | 部署后 | 变化 |
|------|--------|--------|------|
| 词典总数 | 1,275 | 1,326 | +51 (+4.0%) |
| Symptom | 266 | 280 | +14 (+5.3%) |
| Component | 181 | 194 | +13 (+7.2%) |
| Tool | 103 | 109 | +6 (+5.8%) |
| Process | 179 | 186 | +7 (+3.9%) |
| TestCase | 235 | 242 | +7 (+3.0%) |
| Metric | 193 | 197 | +4 (+2.1%) |
| Material | 55 | 55 | 0 (待下批) |
| Role | 63 | 63 | 0 |

### 新增内容亮点

**摄像头领域** (+20条):
- Component: CMOS图像传感器、VCM对焦马达、OIS模组、IR滤光片、镜头组、ToF模组
- Symptom: 白平衡偏移、摄像头黑屏、对焦缓慢、OIS异响
- TestCase: AF成功率测试、OIS抗抖测试
- Tool: 光学暗箱、分辨率测试卡、SNR测试卡

**显示领域** (+13条):
- Component: ALS传感器、触控控制器
- Symptom: 颜色失真、触控漂移、触控断点、屏闪严重
- TestCase: 低亮度屏闪测试、触控线性测试
- Process: OCR全贴合、OCA层压
- Metric: ΔE、JNCD

**射频领域** (+16条):
- Component: NFC线圈、PA功放、LNA低噪放、Wi-Fi/BT模组
- Symptom: 天线脱网、Wi-Fi速率低、蓝牙断连、GPS飘移
- TestCase: TRP辐射功率测试、TIS灵敏度测试、GPS冷启动测试
- Metric: SNR、TRP

**其他领域** (+2条):
- Symptom: 通话回声、麦克风底噪高
- Component: 指纹模组

---

## ✅ 部署检查表

### 部署前
- [ ] 本地词典数据已更新 (1326条)
- [ ] 数据质量已验证 (89.9/100)
- [ ] 备份脚本已准备
- [ ] 同步脚本已准备
- [ ] 部署脚本已准备

### 部署中
- [ ] 服务器数据已备份
- [ ] 词典文件已上传
- [ ] 同步脚本已上传
- [ ] Neo4j同步已完成
- [ ] API服务已重启

### 部署后
- [ ] 词典数量验证 (1326条)
- [ ] 图谱节点验证 (1421个)
- [ ] 新增术语搜索测试
- [ ] 图谱可视化检查
- [ ] API响应正常

---

## 🚀 开始部署

### 快速部署命令

```bash
# 1. 确保在项目根目录
cd d:\KG

# 2. 执行部署脚本
bash deploy_to_server.sh

# 3. 等待部署完成（3-5分钟）

# 4. 验证部署
curl http://47.108.152.16/kg/stats
```

### 预期输出

```
================================================================================
📦 开始部署词典和图谱更新到服务器
================================================================================

1️⃣ 备份服务器现有数据...
✅ 备份完成

2️⃣ 上传更新后的词典文件...
✅ 词典文件上传完成

3️⃣ 上传Neo4j同步脚本...
✅ 同步脚本上传完成

4️⃣ 在服务器上同步到Neo4j图谱...
✅ Neo4j同步完成

5️⃣ 重启后端API服务...
✅ API服务已重启

6️⃣ 验证部署...
{
  "nodes": 1421,
  "relationships": 4910,
  "dictionary_count": 1326
}

================================================================================
✅ 部署完成！
================================================================================
```

---

**准备好了吗？执行 `bash deploy_to_server.sh` 开始部署！**
