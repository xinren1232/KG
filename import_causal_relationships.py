#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入因果关系数据到Neo4j知识图谱
用于服务器端执行
"""

import json
from neo4j import GraphDatabase
import sys

# Neo4j连接配置
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

# 因果关系数据
CAUSAL_RELATIONSHIPS = {
    "relationships": [
        {
            "source": "背胶压合治具颗粒杂质",
            "relation_type": "CAUSES",
            "target": "电池盖裂纹",
            "confidence": 0.9,
            "evidence": "背胶压合治具，在压合时局部受压力不均匀时产生裂纹，确认为治具上存在颗粒杂质导致不良",
            "confidence_reason": "包含明确因果关系词'导致'，有具体的失效机理描述"
        },
        {
            "source": "转印生产现场粉尘污染",
            "relation_type": "CAUSES",
            "target": "电池盖颗粒白点异色",
            "confidence": 0.8,
            "evidence": "转印生产现场有粉尘污染/毛丝/颗粒杂质绒线吸附在产品表面产生",
            "confidence_reason": "明确的因果关系描述，有具体的污染源和结果"
        },
        {
            "source": "隧道炉积尘",
            "relation_type": "CAUSES",
            "target": "玻璃镜片白点",
            "confidence": 0.9,
            "evidence": "隧道炉生产时间周期过长，有积尘，丝印后过隧道炉有灰尘点落在玻璃上，形成白点",
            "confidence_reason": "包含明确的因果链条和具体的失效机理"
        },
        {
            "source": "电镀机台未清洁到位",
            "relation_type": "CAUSES",
            "target": "玻璃镜片白点",
            "confidence": 0.8,
            "evidence": "电镀机台未清洁到位，在镀产品是尘点打在了产品表面，造成的白点",
            "confidence_reason": "明确的因果关系词'造成'，有具体的工艺过程描述"
        },
        {
            "source": "蚀刻过程中两片产品叠加",
            "relation_type": "CAUSES",
            "target": "玻璃镜片压痕",
            "confidence": 0.9,
            "evidence": "蚀刻过程中两片产品叠加一起，产品拿出来后酸洗药水再两片叠加处未及时流出，导致有药水的地方一直还在蚀刻从而出现压痕不良",
            "confidence_reason": "详细的失效机理描述，包含'导致'等明确因果关系词"
        },
        {
            "source": "温度冲击微跌试验",
            "relation_type": "TRIGGERS",
            "target": "摄像头模组对焦模糊",
            "confidence": 0.8,
            "evidence": "温度冲击+微跌第二轮（正反3200次+4面200次）NG拍照对焦模糊",
            "confidence_reason": "有具体的测试条件和结果，但缺乏详细的失效机理"
        },
        {
            "source": "镜头镜片脱落",
            "relation_type": "CAUSES",
            "target": "摄像头模组对焦模糊",
            "confidence": 0.9,
            "evidence": "拆解1pcs发现镜头镜片脱落",
            "confidence_reason": "直接的物理失效证据，因果关系明确"
        },
        {
            "source": "EOS/ESD损伤",
            "relation_type": "CAUSES",
            "target": "芯片开路不良",
            "confidence": 0.9,
            "evidence": "芯片厂分析：热点检查，D4N附近发现热点存在，判断损伤是EOS/ESD导致",
            "confidence_reason": "专业芯片厂商分析结果，有具体的检测数据支持"
        },
        {
            "source": "转印机台滚筒螺丝松动",
            "relation_type": "CAUSES",
            "target": "转印胶水厚度不均",
            "confidence": 0.8,
            "evidence": "转印机台滚筒螺丝松动，造成滚压压力与速度不稳定，转印胶水厚度偏厚或者偏薄",
            "confidence_reason": "明确的机械故障原因和结果描述"
        },
        {
            "source": "转印胶水厚度不均",
            "relation_type": "CAUSES",
            "target": "固化后色差",
            "confidence": 0.8,
            "evidence": "转印胶水厚度偏厚或者偏薄，固化后形成色差",
            "confidence_reason": "明确的工艺过程因果关系"
        },
        {
            "source": "天线保压压头磨损",
            "relation_type": "CAUSES",
            "target": "中框裂纹压伤",
            "confidence": 0.9,
            "evidence": "天线保压压头由于磨损严重，技术员在压头上粘贴绒布，导致压头大于产品宽度，造成产品压伤、裂纹不良",
            "confidence_reason": "详细的失效机理描述，包含'导致'、'造成'等因果关系词"
        },
        {
            "source": "泡棉压合机台异常",
            "relation_type": "CAUSES",
            "target": "泡棉压合不到位",
            "confidence": 0.8,
            "evidence": "泡棉压合岗位机台异常，压合不到位导致的",
            "confidence_reason": "明确的设备故障和结果描述"
        },
        {
            "source": "整机组装过程过压或大电流",
            "relation_type": "CAUSES",
            "target": "喇叭杂音不良",
            "confidence": 0.7,
            "evidence": "在整机组装过程中受到过压或者大电流，对产品造成永久性的性能损伤",
            "confidence_reason": "供应商分析结果，但缺乏具体的测试数据验证"
        },
        {
            "source": "门限适配问题",
            "relation_type": "CAUSES",
            "target": "听筒THD失真",
            "confidence": 0.6,
            "evidence": "门限适配问题",
            "confidence_reason": "描述过于简单，缺乏详细的技术分析"
        },
        {
            "source": "TPU原料特性长时间放置",
            "relation_type": "CAUSES",
            "target": "保护套发黄",
            "confidence": 0.9,
            "evidence": "由于TPU原料特性，做好的成品保护套放置时间过长会产生变色发黄现象",
            "confidence_reason": "明确的材料特性和时间因素描述"
        },
        {
            "source": "框胶受损液晶气泡",
            "relation_type": "CAUSES",
            "target": "屏幕黑影不良",
            "confidence": 0.8,
            "evidence": "框胶受损，液晶气泡；切割导致断面裂纹，框胶受损，液晶进入空气形成气泡，显示为黑影不良",
            "confidence_reason": "详细的失效机理分析，有具体的物理过程描述"
        },
        {
            "source": "磨粉浓度过高",
            "relation_type": "CAUSES",
            "target": "屏幕表面凹印",
            "confidence": 0.8,
            "evidence": "磨粉浓度越高对产品表面的摩擦就越大，容易出现凹印不良",
            "confidence_reason": "明确的工艺参数和结果关系"
        },
        {
            "source": "定位柱高度设计过长",
            "relation_type": "CAUSES",
            "target": "孔位变形",
            "confidence": 0.9,
            "evidence": "夹具定位柱高度设计过长、定位柱倒角偏小，加工操作过程中拿偏产品导致孔位拉变形",
            "confidence_reason": "具体的设计缺陷和失效机理描述"
        },
        {
            "source": "CNC振刀碰到产品",
            "relation_type": "CAUSES",
            "target": "边缘掉漆",
            "confidence": 0.8,
            "evidence": "CNC振刀碰到产品，形成边缘漆",
            "confidence_reason": "明确的机械加工故障和结果"
        },
        {
            "source": "叠片点数方式",
            "relation_type": "CAUSES",
            "target": "玻璃镜片短装",
            "confidence": 0.8,
            "evidence": "出货组点数时候是叠片点数，导致漏发现，误判点数总数量与订单数量无差异，未发现短装",
            "confidence_reason": "明确的操作方法缺陷和结果"
        },
        {
            "source": "点胶长度离圆弧位置较远",
            "relation_type": "CAUSES",
            "target": "保护套铁片起翘",
            "confidence": 0.8,
            "evidence": "点胶长度离圆弧位置较远，保压后会出现不均匀，导致部分产品胶量过少，造成起翘不良产生",
            "confidence_reason": "详细的工艺过程分析和因果关系"
        },
        {
            "source": "膜片电镀操作员手法不当",
            "relation_type": "CAUSES",
            "target": "玻璃电池盖脏污异色",
            "confidence": 0.8,
            "evidence": "膜片电镀装锅和电镀锅装入电镀仓时，操作员手法不当造成产品脏污",
            "confidence_reason": "明确的操作问题和结果描述"
        },
        {
            "source": "镀膜机清洁不彻底",
            "relation_type": "CAUSES",
            "target": "镀膜异色点",
            "confidence": 0.8,
            "evidence": "镀膜机清洁不彻底，镀膜过程中微尘依附在产品表面形成异色点",
            "confidence_reason": "明确的设备维护问题和污染结果"
        },
        {
            "source": "软对硬贴付设备粘着板粘性降低",
            "relation_type": "CAUSES",
            "target": "贴合气泡",
            "confidence": 0.8,
            "evidence": "设备粘着板使用过程中粘性降低，撕膜后OCA被轻微带起形变，贴合时不能使OCA完全有效的粘附CG，进行高温消泡时会有过剩气体渗入到OCA边缘形成气泡",
            "confidence_reason": "详细的设备老化和失效机理分析"
        },
        {
            "source": "员工产品拿取手法不当",
            "relation_type": "CAUSES",
            "target": "CG表面划伤",
            "confidence": 0.7,
            "evidence": "员工在生产过程中产品拿取时手法不当：丢放、重叠等，存在造成CG划伤等风险",
            "confidence_reason": "操作不当的描述，但使用'存在风险'等不确定词语"
        },
        {
            "source": "自动化设备三伤防护不到位",
            "relation_type": "CAUSES",
            "target": "中框划伤磨花",
            "confidence": 0.8,
            "evidence": "自动化设备三伤防护未做到位，部分边边角角未防护到位，设备异常处理中技术员在拿产品过程中触碰到设备，正常不良的发生",
            "confidence_reason": "明确的设备防护缺陷和操作风险"
        },
        {
            "source": "灯罩背面背胶未激活",
            "relation_type": "CAUSES",
            "target": "面壳灯罩起翘",
            "confidence": 0.9,
            "evidence": "前壳组装灯罩时灯罩背面背胶未激活，致使灯角未粘牢长时间储存导致起翘不良发生",
            "confidence_reason": "明确的工艺缺陷和时间因素导致的失效"
        },
        {
            "source": "70W混用33W/45W外壳",
            "relation_type": "CAUSES",
            "target": "充电器LED灯亮度差异",
            "confidence": 0.9,
            "evidence": "70W混用33W/45W外壳，70W及以上因有灯效要求，使用不透光胶料，导致灯光亮度差异",
            "confidence_reason": "明确的物料混用和材料特性差异导致的问题"
        },
        {
            "source": "生产线转线未清理干净",
            "relation_type": "CAUSES",
            "target": "外壳混用",
            "confidence": 0.8,
            "evidence": "生产线转线，上一机型面壳未清理干净，未按要求做产线清换线check list稽核确认，导致尾数外壳混用",
            "confidence_reason": "明确的生产管理缺陷和结果"
        },
        {
            "source": "天气变冷静电",
            "relation_type": "CAUSES",
            "target": "落尘吸附产生颗粒",
            "confidence": 0.7,
            "evidence": "天气变冷静电导致落尘吸附素材表面，除尘不到位产生颗粒",
            "confidence_reason": "环境因素和物理现象的关联，但机理描述相对简单"
        },
        {
            "source": "电容内裂短路",
            "relation_type": "CAUSES",
            "target": "指纹模组测试fail",
            "confidence": 0.9,
            "evidence": "电容内裂短路，导致TX这一路短路，TX是Pixel的控制电路，短路后会导致芯片Pixel电路工作不正常，体现为在暗光环境下曝光不正常",
            "confidence_reason": "详细的电路失效分析，有具体的技术机理"
        },
        {
            "source": "背光小FPC干涉剐蹭",
            "relation_type": "CAUSES",
            "target": "屏幕漏光灯影",
            "confidence": 0.8,
            "evidence": "背光小FPC存在干涉剐蹭缺口，导致K1线路断开点灯灯影",
            "confidence_reason": "明确的物理损伤和电路失效关系"
        },
        {
            "source": "油墨烘烤温度不足",
            "relation_type": "CAUSES",
            "target": "达因值偏低",
            "confidence": 0.8,
            "evidence": "由于前面四道工序、是使用隧道炉表干，受天气变冷原因，在工艺参数不变的情况下，过程隧道炉烘烤产品时，产品的干燥度属于临界点转态，丝印成品后，底层的油墨受自然风干，会挥发油污到产品表面，导致达因值偏低",
            "confidence_reason": "详细的工艺过程分析和环境因素影响"
        },
        {
            "source": "中框精雕侧键孔宽度偏小",
            "relation_type": "CAUSES",
            "target": "按键卡键不良",
            "confidence": 0.9,
            "evidence": "中框精雕侧键孔宽度中间偏小（超标准下限0.03mm），中框与按键两者组配后局部间隙为零配，导致整机出现按键卡键不良",
            "confidence_reason": "具体的尺寸数据和装配间隙分析"
        },
        {
            "source": "开机员换刀后未送测尺寸",
            "relation_type": "CAUSES",
            "target": "电池盖尺寸超下限",
            "confidence": 0.8,
            "evidence": "开机员换刀后只填写记录未送测尺寸，换刀后尺寸超下限导致不良产生",
            "confidence_reason": "明确的操作流程缺失和质量控制问题"
        },
        {
            "source": "FPC绑定表面脏污",
            "relation_type": "CAUSES",
            "target": "HAST实验后屏显横线条",
            "confidence": 0.8,
            "evidence": "初步推断为FPC绑定表面脏污HSAT实验后脏污上浮导致绑定失效，实验后出现线条问题",
            "confidence_reason": "合理的失效机理推断，有实验验证支持"
        },
        {
            "source": "制程返修品未二次保压",
            "relation_type": "CAUSES",
            "target": "屏幕漏光",
            "confidence": 0.9,
            "evidence": "确认背光为制程返修品背光，原因为制程不良人工返修后未进行二次保压，致使遮光胶激活率偏下限≥要求70%实测72.5%，在温度实验后遮光胶与胶框分层导致成品出现漏光现象",
            "confidence_reason": "详细的工艺流程缺失和具体的测试数据支持"
        },
        {
            "source": "多个Panel同时翻转",
            "relation_type": "CAUSES",
            "target": "屏幕端子区域破损",
            "confidence": 0.8,
            "evidence": "在Tray盘中集中作业，贴完后集中一起翻转Panel，多个Panel同时翻转时易造成磕碰",
            "confidence_reason": "明确的操作方法和物理碰撞风险"
        },
        {
            "source": "绿色周转盘老化",
            "relation_type": "CAUSES",
            "target": "贴合白点异物",
            "confidence": 0.7,
            "evidence": "绿色周转盘经过脱泡、过UV，使用时间长，慢慢老化，与FOG接触产生粉尘在FOG上，贴合撕膜时进入上片表面，导致贴合异物",
            "confidence_reason": "合理的老化机理分析，但证据相对间接"
        },
        {
            "source": "LCD CF层受外力撞击",
            "relation_type": "CAUSES",
            "target": "屏幕黑团",
            "confidence": 0.8,
            "evidence": "LCD CF层受外力撞击破裂框胶开裂导致产品漏液黑团",
            "confidence_reason": "明确的物理损伤和失效机理"
        },
        {
            "source": "LGP网点受外力挤压",
            "relation_type": "CAUSES",
            "target": "屏幕白斑",
            "confidence": 0.8,
            "evidence": "异常产生原理分析为4、7区BL受外力挤压或磨擦产生局部受损，出现白印现象",
            "confidence_reason": "详细的失效分析和位置定位"
        },
        {
            "source": "Fanout区域金属膜破",
            "relation_type": "CAUSES",
            "target": "屏幕竖线",
            "confidence": 0.9,
            "evidence": "Fanout区域存在金属膜破，FIB切片结果为GE层膜破，为LCD原材异常",
            "confidence_reason": "专业的失效分析技术和具体的检测结果"
        },
        {
            "source": "胶水涂布后开放时间过长",
            "relation_type": "CAUSES",
            "target": "书本盒开胶",
            "confidence": 0.8,
            "evidence": "产线开线生产时，拉线物料堆积，导致胶水涂布后，开放时间长（胶水正常开放时间1Min±20s），没有及时刮边压盒，胶水超过开放时间，导致包盒局部出现假粘，边缘起翘",
            "confidence_reason": "详细的工艺时间控制和胶水特性分析"
        },
        {
            "source": "逆向UV未完全干透",
            "relation_type": "CAUSES",
            "target": "封套烫金粘花",
            "confidence": 0.8,
            "evidence": "生产未按工艺流程卡执行，逆向UV还未完全干透，已工艺啤切，埋口，全检入库，仓库产品叠放积压受力，产品局部的UV逆向粘花",
            "confidence_reason": "明确的工艺流程违规和材料固化不足问题"
        },
        {
            "source": "压铸模后模模腔积碳",
            "relation_type": "CAUSES",
            "target": "面壳断柱钢片破损",
            "confidence": 0.8,
            "evidence": "压铸模后模模腔成型孔内积碳，导致部分素材产品出胚不顺畅，五金柱子根部拉模，产生暗裂，产品物料在各制成生产及物料周转过程中受外力影响造成裂纹加重从而断裂",
            "confidence_reason": "详细的模具问题和应力集中失效分析"
        },
        {
            "source": "PE片自动化贴合设备针头残胶",
            "relation_type": "CAUSES",
            "target": "中框气密性测试NG",
            "confidence": 0.8,
            "evidence": "PE片是自动化设变贴合，辅料贴合后再进行点胶，在点胶过程中机台设备针头上残胶，在压合后吸附在治具上模，导致偏位",
            "confidence_reason": "明确的设备维护问题和工艺偏差"
        },
        {
            "source": "注塑模具磨损间隙大",
            "relation_type": "CAUSES",
            "target": "中框孔位塑胶高出",
            "confidence": 0.8,
            "evidence": "互配模具此孔位模磨损间隙大跑披锋，注塑员工加铲披锋时拉高塑胶高出导致顶屏不良",
            "confidence_reason": "明确的模具磨损和操作问题导致的尺寸偏差"
        },
        {
            "source": "打包房物料点数纰漏",
            "relation_type": "CAUSES",
            "target": "卡托短装",
            "confidence": 0.9,
            "evidence": "打包房物料全检错漏混后，点数时出现纰漏，监控视频显示双盘点数，其中有两盘点的单数，最后计算按照双数，少2盘物料未能察觉",
            "confidence_reason": "有监控视频证据支持的具体操作错误"
        },
        {
            "source": "面漆厚度低于标准值",
            "relation_type": "CAUSES",
            "target": "中框铅笔硬度NG",
            "confidence": 0.9,
            "evidence": "该批铅笔硬度NG品产品表面局部位置面漆厚度低于标准值（标准：22±3um 实际：16um），导致铅笔硬度NG",
            "confidence_reason": "具体的测量数据和标准对比，明确的因果关系"
        }
    ]
}


class CausalRelationshipImporter:
    """因果关系导入器"""
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
        
    def create_term_if_not_exists(self, tx, term_name, category="Symptom"):
        """创建术语节点（如果不存在）"""
        query = """
        MERGE (t:Term {name: $name})
        ON CREATE SET 
            t.category = $category,
            t.created_at = datetime(),
            t.source = 'causal_relationship_import'
        RETURN t
        """
        result = tx.run(query, name=term_name, category=category)
        return result.single()
    
    def create_causal_relationship(self, tx, source, target, relation_type, confidence, evidence, confidence_reason):
        """创建因果关系"""
        query = """
        MATCH (s:Term {name: $source})
        MATCH (t:Term {name: $target})
        MERGE (s)-[r:CAUSES]->(t)
        ON CREATE SET
            r.confidence = $confidence,
            r.evidence = $evidence,
            r.confidence_reason = $confidence_reason,
            r.created_at = datetime(),
            r.source = 'causal_relationship_import'
        ON MATCH SET
            r.confidence = $confidence,
            r.evidence = $evidence,
            r.confidence_reason = $confidence_reason,
            r.updated_at = datetime()
        RETURN s, r, t
        """
        result = tx.run(
            query,
            source=source,
            target=target,
            confidence=confidence,
            evidence=evidence,
            confidence_reason=confidence_reason
        )
        return result.single()
    
    def import_relationships(self, relationships_data):
        """导入所有因果关系"""
        stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        with self.driver.session() as session:
            for rel in relationships_data["relationships"]:
                stats["total"] += 1
                try:
                    # 创建源节点
                    session.execute_write(
                        self.create_term_if_not_exists,
                        rel["source"],
                        "Symptom"  # 默认分类
                    )
                    
                    # 创建目标节点
                    session.execute_write(
                        self.create_term_if_not_exists,
                        rel["target"],
                        "Symptom"  # 默认分类
                    )
                    
                    # 创建关系
                    session.execute_write(
                        self.create_causal_relationship,
                        rel["source"],
                        rel["target"],
                        rel["relation_type"],
                        rel["confidence"],
                        rel["evidence"],
                        rel["confidence_reason"]
                    )
                    
                    stats["success"] += 1
                    print(f"✅ 成功导入: {rel['source']} -> {rel['target']}")
                    
                except Exception as e:
                    stats["failed"] += 1
                    error_msg = f"❌ 失败: {rel['source']} -> {rel['target']}: {str(e)}"
                    stats["errors"].append(error_msg)
                    print(error_msg)
        
        return stats


def main():
    """主函数"""
    print("=" * 80)
    print("开始导入因果关系数据到Neo4j知识图谱")
    print("=" * 80)
    
    # 创建导入器
    importer = CausalRelationshipImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    
    try:
        # 导入关系
        stats = importer.import_relationships(CAUSAL_RELATIONSHIPS)
        
        # 打印统计信息
        print("\n" + "=" * 80)
        print("导入完成统计")
        print("=" * 80)
        print(f"总数: {stats['total']}")
        print(f"成功: {stats['success']}")
        print(f"失败: {stats['failed']}")
        
        if stats['errors']:
            print("\n错误详情:")
            for error in stats['errors']:
                print(f"  {error}")
        
        print("=" * 80)
        
        # 返回状态码
        return 0 if stats['failed'] == 0 else 1
        
    except Exception as e:
        print(f"\n❌ 导入过程发生错误: {str(e)}")
        return 1
        
    finally:
        importer.close()


if __name__ == "__main__":
    sys.exit(main())

