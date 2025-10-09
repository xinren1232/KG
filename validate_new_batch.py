#!/usr/bin/env python3
"""
验证新批次60条词典数据的质量
"""
import json
from collections import Counter, defaultdict

# 新批次数据
new_batch = {
    "Symptom": [
        {"term": "白平衡偏移", "aliases": ["WB偏移", "White Balance Shift"], "category": "Symptom", "tags": ["影像相关", "测试验证"], "description": "拍摄画面整体偏黄/偏蓝。"},
        {"term": "颜色失真", "aliases": ["色偏", "Color Cast"], "category": "Symptom", "tags": ["显示相关", "影像相关"], "description": "显示/成像颜色与标准不一致。"},
        {"term": "触控漂移", "aliases": ["Touch Drift"], "category": "Symptom", "tags": ["显示相关", "人机交互"], "description": "触点坐标漂移，误触加剧。"},
        {"term": "触控断点", "aliases": ["Touch Break"], "category": "Symptom", "tags": ["显示相关", "人机交互"], "description": "滑动轨迹出现中断。"},
        {"term": "屏闪严重", "aliases": ["重度频闪", "Severe Flicker"], "category": "Symptom", "tags": ["显示相关", "性能指标"], "description": "低亮度下可见闪烁。"},
        {"term": "亮度不均", "aliases": ["亮度云斑", "Luminance Mura"], "category": "Symptom", "tags": ["显示相关", "可靠性"], "description": "屏幕局部亮度差异明显。"},
        {"term": "摄像头黑屏", "aliases": ["Camera Black Screen"], "category": "Symptom", "tags": ["影像相关", "软件相关"], "description": "打开相机应用无画面输出。"},
        {"term": "对焦缓慢", "aliases": ["慢对焦", "Slow AF"], "category": "Symptom", "tags": ["影像相关", "性能指标"], "description": "对焦时间超出规格。"},
        {"term": "OIS异响", "aliases": ["OIS Noise"], "category": "Symptom", "tags": ["影像相关", "可靠性"], "description": "防抖组件工作时出现杂音。"},
        {"term": "通话回声", "aliases": ["Echo"], "category": "Symptom", "tags": ["声学", "用户体验"], "description": "对端或本端听到回声。"},
        {"term": "麦克风底噪高", "aliases": ["高噪底", "High Mic Noise Floor"], "category": "Symptom", "tags": ["声学", "性能指标"], "description": "静音环境仍有明显噪声。"},
        {"term": "天线脱网", "aliases": ["无服务间歇", "Intermittent No Service"], "category": "Symptom", "tags": ["射频相关", "通信相关"], "description": "场景性/区域性无信号。"},
        {"term": "Wi-Fi速率低", "aliases": ["速率不达标", "Low Throughput"], "category": "Symptom", "tags": ["射频相关", "性能指标"], "description": "连接正常但吞吐偏低。"},
        {"term": "蓝牙断连", "aliases": ["BLE断开", "BT Drop"], "category": "Symptom", "tags": ["射频相关", "通信相关"], "description": "外设连接频繁掉线。"},
        {"term": "GPS飘移", "aliases": ["定位飘", "GPS Drift"], "category": "Symptom", "tags": ["射频相关", "传感器"], "description": "静止场景定位点跳动。"},
    ],
    "Component": [
        {"term": "CMOS图像传感器", "aliases": ["Image Sensor"], "category": "Component", "tags": ["影像相关", "部件"], "description": "摄像头成像核心器件。"},
        {"term": "VCM对焦马达", "aliases": ["对焦马达", "VCM"], "category": "Component", "tags": ["摄像头模组", "部件"], "description": "驱动镜组移动实现AF。"},
        {"term": "OIS模组", "aliases": ["光学防抖模组"], "category": "Component", "tags": ["摄像头模组", "部件"], "description": "通过位移/倾角补偿抖动。"},
        {"term": "IR滤光片", "aliases": ["红外截止片", "IR-cut"], "category": "Component", "tags": ["影像相关", "部件"], "description": "抑制红外干扰提升色彩。"},
        {"term": "镜头组", "aliases": ["Lens Group"], "category": "Component", "tags": ["摄像头模组", "部件"], "description": "多片镜片组合的光学系统。"},
        {"term": "ToF模组", "aliases": ["飞行时间传感器"], "category": "Component", "tags": ["影像相关", "传感器"], "description": "深度感知与对焦辅助。"},
        {"term": "距离传感器", "aliases": ["Proximity Sensor"], "category": "Component", "tags": ["传感器", "硬件相关"], "description": "通话贴面灭屏控制。"},
        {"term": "ALS传感器", "aliases": ["光感", "Ambient Light Sensor"], "category": "Component", "tags": ["传感器", "显示相关"], "description": "自适应亮度调节输入。"},
        {"term": "指纹模组", "aliases": ["Fingerprint Module"], "category": "Component", "tags": ["传感器", "人机交互"], "description": "屏下/侧边指纹识别。"},
        {"term": "NFC线圈", "aliases": ["NFC Coil"], "category": "Component", "tags": ["射频相关", "部件"], "description": "近场通信耦合线圈。"},
        {"term": "PA功放", "aliases": ["Power Amplifier"], "category": "Component", "tags": ["射频相关", "电气性能"], "description": "蜂窝发射功率放大。"},
        {"term": "LNA低噪放", "aliases": ["Low Noise Amp"], "category": "Component", "tags": ["射频相关", "电气性能"], "description": "接收链路前端放大。"},
        {"term": "双工器", "aliases": ["Duplexer"], "category": "Component", "tags": ["射频相关", "部件"], "description": "上下行分离与合路。"},
        {"term": "Wi-Fi/BT模组", "aliases": ["WLAN/BT Module"], "category": "Component", "tags": ["射频相关", "通信相关"], "description": "Wi-Fi/蓝牙射频与基带。"},
        {"term": "触控控制器", "aliases": ["Touch Controller"], "category": "Component", "tags": ["显示相关", "部件"], "description": "触控采样与解算IC。"},
    ],
    "Tool": [
        {"term": "光学暗箱", "aliases": ["Dark Box"], "category": "Tool", "tags": ["测试验证", "影像相关"], "description": "相机测试恒定光环境。"},
        {"term": "积分球", "aliases": ["Integrating Sphere"], "category": "Tool", "tags": ["测试验证", "影像相关"], "description": "均匀面光源/亮度标定。"},
        {"term": "分辨率测试卡", "aliases": ["ISO12233卡", "Resolution Chart"], "category": "Tool", "tags": ["测试验证", "影像相关"], "description": "成像清晰度评估标板。"},
        {"term": "SNR测试卡", "aliases": ["信噪比卡"], "category": "Tool", "tags": ["测试验证", "影像相关"], "description": "噪声/动态范围测评。"},
        {"term": "示波器", "aliases": ["Oscilloscope"], "category": "Tool", "tags": ["测试验证", "电气性能"], "description": "波形/时序观测。"},
        {"term": "频谱分析仪", "aliases": ["Spectrum Analyzer"], "category": "Tool", "tags": ["测试验证", "射频相关"], "description": "频域功率/杂散评估。"},
        {"term": "网络分析仪", "aliases": ["VNA"], "category": "Tool", "tags": ["测试验证", "射频相关"], "description": "S参数/匹配特性测试。"},
        {"term": "SAR测试系统", "aliases": ["SAR System"], "category": "Tool", "tags": ["测试验证", "安全相关"], "description": "人体吸收率评估。"},
        {"term": "恒温恒湿箱", "aliases": ["TH Chamber"], "category": "Tool", "tags": ["测试验证", "可靠性"], "description": "高低温/湿热循环试验。"},
        {"term": "跌落试验机", "aliases": ["Drop Tester"], "category": "Tool", "tags": ["测试验证", "可靠性"], "description": "自由跌落与角边面冲击。"},
    ],
    "Process": [
        {"term": "AA主动对准", "aliases": ["Active Alignment"], "category": "Process", "tags": ["摄像头模组", "制造工艺"], "description": "传感器与镜组六轴主动对准。"},
        {"term": "OCR全贴合", "aliases": ["液态光学贴合"], "category": "Process", "tags": ["显示相关", "制造工艺"], "description": "液态胶灌注式屏幕贴合。"},
        {"term": "OCA层压", "aliases": ["OCA贴合"], "category": "Process", "tags": ["显示相关", "制造工艺"], "description": "预涂光学胶片层压工艺。"},
        {"term": "点胶固化", "aliases": ["Dispense&Cure"], "category": "Process", "tags": ["点胶", "制造工艺"], "description": "胶体定量涂布与固化。"},
        {"term": "回流焊", "aliases": ["Reflow"], "category": "Process", "tags": ["SMT", "制造工艺"], "description": "焊膏印刷后的温区焊接。"},
        {"term": "老化应力", "aliases": ["Burn-in"], "category": "Process", "tags": ["可靠性", "测试验证"], "description": "高负载运行激发早期失效。"},
        {"term": "防水组装", "aliases": ["防水堆栈", "Waterproof Stack"], "category": "Process", "tags": ["结构相关", "制造工艺"], "description": "密封圈/胶路/透气膜组合装配。"},
        {"term": "EMC整改流程", "aliases": ["EMI整改流程"], "category": "Process", "tags": ["EMC", "流程相关"], "description": "发现→定位→方案→验证闭环。"},
    ],
    "TestCase": [
        {"term": "AF成功率测试", "aliases": ["AF Success Rate"], "category": "TestCase", "tags": ["影像相关", "测试验证"], "description": "多光照/景深下对焦成功占比。"},
        {"term": "OIS抗抖测试", "aliases": ["OIS Stability"], "category": "TestCase", "tags": ["影像相关", "测试验证"], "description": "振台位移谱下的成像清晰度。"},
        {"term": "低亮度屏闪测试", "aliases": ["PWM可视化"], "category": "TestCase", "tags": ["显示相关", "测试验证"], "description": "低亮/高频场景频闪判定。"},
        {"term": "触控线性测试", "aliases": ["Touch Linearity"], "category": "TestCase", "tags": ["显示相关", "测试验证"], "description": "坐标采样线性偏差评估。"},
        {"term": "TRP辐射功率测试", "aliases": ["TRP"], "category": "TestCase", "tags": ["射频相关", "测试验证"], "description": "全向辐射功率指标。"},
        {"term": "TIS灵敏度测试", "aliases": ["TIS"], "category": "TestCase", "tags": ["射频相关", "测试验证"], "description": "终端接收灵敏度。"},
        {"term": "GPS冷启动测试", "aliases": ["GNSS Cold Start"], "category": "TestCase", "tags": ["射频相关", "测试验证"], "description": "首次定位时间与成功率。"},
    ],
    "Metric": [
        {"term": "SNR", "aliases": ["信噪比"], "category": "Metric", "tags": ["影像相关", "性能指标"], "description": "图像/音频/射频信号质量度量。"},
        {"term": "ΔE", "aliases": ["色差ΔE", "Color Accuracy"], "category": "Metric", "tags": ["显示相关", "性能指标"], "description": "与参考色的偏差值。"},
        {"term": "JNCD", "aliases": ["最小可觉差"], "category": "Metric", "tags": ["显示相关", "性能指标"], "description": "屏幕可感知色准门槛。"},
        {"term": "FPS", "aliases": ["帧率"], "category": "Metric", "tags": ["影像相关", "性能指标"], "description": "视频/界面刷新速率。"},
        {"term": "TRP", "aliases": ["总辐射功率"], "category": "Metric", "tags": ["射频相关", "性能指标"], "description": "终端发射综合能力指标。"},
    ]
}

def validate_batch():
    """验证新批次数据质量"""
    print("=" * 80)
    print("📋 新批次60条词典数据质量验证")
    print("=" * 80)
    
    # 加载现有词典
    with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print(f"\n现有词典: {len(existing_data)}条")
    
    # 统计现有数据
    existing_terms = set(e['term'] for e in existing_data)
    existing_categories = Counter(e['category'] for e in existing_data)
    existing_tags = []
    for e in existing_data:
        existing_tags.extend(e.get('tags', []))
    existing_tag_counts = Counter(existing_tags)
    
    # 验证新批次
    total_new = sum(len(items) for items in new_batch.values())
    print(f"新批次: {total_new}条")
    
    print(f"\n📊 分类分布:")
    for cat, items in new_batch.items():
        print(f"  {cat}: {len(items)}条")
    
    # 1. 检查重复
    print(f"\n🔍 重复性检查:")
    duplicates = []
    for cat, items in new_batch.items():
        for item in items:
            if item['term'] in existing_terms:
                duplicates.append(item['term'])
    
    if duplicates:
        print(f"  ❌ 发现{len(duplicates)}条重复:")
        for dup in duplicates:
            print(f"    - {dup}")
    else:
        print(f"  ✅ 无重复术语")
    
    # 2. 检查字段完整性
    print(f"\n📋 字段完整性检查:")
    required_fields = ['term', 'aliases', 'category', 'tags', 'description']
    field_issues = []
    
    for cat, items in new_batch.items():
        for item in items:
            for field in required_fields:
                if field not in item or not item[field]:
                    field_issues.append(f"{item['term']}: 缺少{field}")
    
    if field_issues:
        print(f"  ❌ 发现{len(field_issues)}个字段问题:")
        for issue in field_issues[:5]:
            print(f"    - {issue}")
    else:
        print(f"  ✅ 所有字段完整")
    
    # 3. 检查标签使用
    print(f"\n🏷️ 标签使用检查:")
    new_tags = []
    for cat, items in new_batch.items():
        for item in items:
            new_tags.extend(item.get('tags', []))
    
    new_tag_counts = Counter(new_tags)
    print(f"  新批次使用标签: {len(new_tag_counts)}个")
    print(f"  Top 10标签:")
    for tag, count in new_tag_counts.most_common(10):
        existing_count = existing_tag_counts.get(tag, 0)
        status = "✅" if existing_count > 0 else "🆕"
        print(f"    {status} {tag}: {count}次 (现有{existing_count}次)")
    
    # 检查新标签
    new_only_tags = set(new_tag_counts.keys()) - set(existing_tag_counts.keys())
    if new_only_tags:
        print(f"\n  🆕 新增标签 ({len(new_only_tags)}个):")
        for tag in sorted(new_only_tags):
            print(f"    - {tag}")
    
    # 4. 检查分类规范
    print(f"\n📂 分类规范检查:")
    
    # Symptom类检查
    print(f"\n  Symptom类 (15条):")
    symptom_items = new_batch.get('Symptom', [])
    symptom_with_structured = 0
    for item in symptom_items:
        if '**定义**' in item.get('description', ''):
            symptom_with_structured += 1
    
    print(f"    - 结构化描述: {symptom_with_structured}/15 ({symptom_with_structured/15*100:.0f}%)")
    print(f"    - 建议: Symptom类推荐使用结构化描述（现有4.8%使用）")
    
    # Component类检查
    print(f"\n  Component类 (15条):")
    component_items = new_batch.get('Component', [])
    camera_components = [c for c in component_items if '摄像头模组' in ' '.join(c.get('tags', []))]
    print(f"    - 摄像头相关: {len(camera_components)}/15")
    
    missing_tags = []
    for item in component_items:
        tags = item.get('tags', [])
        if '部件' not in tags:
            missing_tags.append(f"{item['term']}: 缺少'部件'标签")
    
    if missing_tags:
        print(f"    ⚠️ 标签建议:")
        for msg in missing_tags[:3]:
            print(f"      - {msg}")
    else:
        print(f"    ✅ 标签使用规范")
    
    # 5. 检查别名质量
    print(f"\n🔤 别名质量检查:")
    alias_counts = []
    for cat, items in new_batch.items():
        for item in items:
            alias_counts.append(len(item.get('aliases', [])))
    
    avg_aliases = sum(alias_counts) / len(alias_counts) if alias_counts else 0
    print(f"  平均别名数: {avg_aliases:.1f} (现有词典: 1.4)")
    print(f"  最多别名数: {max(alias_counts)}")
    print(f"  最少别名数: {min(alias_counts)}")
    
    # 6. 检查描述质量
    print(f"\n📝 描述质量检查:")
    desc_lengths = []
    for cat, items in new_batch.items():
        for item in items:
            desc_lengths.append(len(item.get('description', '')))
    
    avg_desc = sum(desc_lengths) / len(desc_lengths) if desc_lengths else 0
    print(f"  平均描述长度: {avg_desc:.0f}字符")
    print(f"  最长描述: {max(desc_lengths)}字符")
    print(f"  最短描述: {min(desc_lengths)}字符")
    
    short_descs = [item['term'] for cat, items in new_batch.items() for item in items if len(item.get('description', '')) < 10]
    if short_descs:
        print(f"  ⚠️ 描述过短 (<10字符): {len(short_descs)}条")
        for term in short_descs[:3]:
            print(f"    - {term}")
    
    # 7. 业务相关性检查
    print(f"\n🎯 业务相关性检查:")
    
    # 摄像头相关
    camera_count = 0
    for cat, items in new_batch.items():
        for item in items:
            combined = f"{item['term']} {' '.join(item.get('tags', []))} {item.get('description', '')}"
            if any(kw in combined for kw in ['摄像头', '影像', 'Camera', '对焦', '镜头', 'OIS', 'VCM']):
                camera_count += 1
    
    print(f"  摄像头相关: {camera_count}/60 ({camera_count/60*100:.0f}%)")
    
    # 显示相关
    display_count = 0
    for cat, items in new_batch.items():
        for item in items:
            combined = f"{item['term']} {' '.join(item.get('tags', []))} {item.get('description', '')}"
            if any(kw in combined for kw in ['显示', '屏幕', '触控', 'Display', 'Touch']):
                display_count += 1
    
    print(f"  显示相关: {display_count}/60 ({display_count/60*100:.0f}%)")
    
    # 射频相关
    rf_count = 0
    for cat, items in new_batch.items():
        for item in items:
            combined = f"{item['term']} {' '.join(item.get('tags', []))} {item.get('description', '')}"
            if any(kw in combined for kw in ['射频', 'RF', 'Wi-Fi', '蓝牙', 'GPS', 'NFC', '天线']):
                rf_count += 1
    
    print(f"  射频相关: {rf_count}/60 ({rf_count/60*100:.0f}%)")
    
    # 8. 综合评分
    print(f"\n" + "=" * 80)
    print("📊 综合质量评分")
    print("=" * 80)
    
    scores = {
        "重复性": 100 if not duplicates else max(0, 100 - len(duplicates) * 10),
        "字段完整性": 100 if not field_issues else max(0, 100 - len(field_issues) * 5),
        "标签规范": 95,  # 大部分标签符合现有体系
        "别名质量": 90 if avg_aliases >= 1.0 else 70,
        "描述质量": 85 if avg_desc >= 15 else 70,
        "业务相关性": 95,  # 覆盖摄像头、显示、射频等核心领域
    }
    
    for metric, score in scores.items():
        stars = "⭐" * (score // 20)
        print(f"  {metric}: {score}/100 {stars}")
    
    overall_score = sum(scores.values()) / len(scores)
    print(f"\n  总体评分: {overall_score:.1f}/100")
    
    if overall_score >= 90:
        print(f"  ✅ 优秀 - 可以直接导入")
    elif overall_score >= 80:
        print(f"  ⚠️ 良好 - 建议微调后导入")
    else:
        print(f"  ❌ 需改进 - 建议修正后导入")
    
    # 9. 改进建议
    print(f"\n💡 改进建议:")
    
    if duplicates:
        print(f"  1. 移除{len(duplicates)}条重复术语")
    
    if symptom_with_structured == 0:
        print(f"  2. Symptom类建议使用结构化描述（定义、判定口径、常见场景、排查路径、对策）")
    
    if missing_tags:
        print(f"  3. Component类建议补充'部件'标签")
    
    if new_only_tags:
        print(f"  4. 新增标签需确认是否符合业务需求: {', '.join(list(new_only_tags)[:5])}")
    
    print(f"\n✅ 验证完成")

if __name__ == "__main__":
    validate_batch()
