#!/usr/bin/env python3
"""
补充新的词典数据到现有统一词典文件
"""
import csv
import os
from pathlib import Path
from datetime import datetime
import json

def backup_current_unified_data():
    """备份当前统一词典数据"""
    print("💾 备份当前统一词典数据...")
    
    backup_dir = Path("data/dictionary_backup") / f"before_append_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    unified_dir = Path("data/unified_dictionary")
    if unified_dir.exists():
        import shutil
        shutil.copytree(unified_dir, backup_dir / "unified_dictionary")
        print(f"   ✅ 备份完成: {backup_dir / 'unified_dictionary'}")
    
    return backup_dir

def load_existing_data():
    """加载现有的词典数据"""
    print("📖 加载现有词典数据...")
    
    unified_dir = Path("data/unified_dictionary")
    existing_data = {
        "components": [],
        "symptoms": [],
        "causes": [],
        "countermeasures": []
    }
    
    existing_terms = set()  # 用于去重
    
    for category in existing_data.keys():
        file_path = unified_dir / f"{category}.csv"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        term = row.get('term', '').strip()
                        if term:
                            existing_data[category].append(row)
                            existing_terms.add(term.lower())
                print(f"   📋 {category}: {len(existing_data[category])} 条")
            except Exception as e:
                print(f"   ❌ 读取 {category}.csv 失败: {e}")
    
    print(f"   📊 现有词条总数: {len(existing_terms)}")
    return existing_data, existing_terms

def create_new_dictionary_data():
    """创建新的补充词典数据 - 详细版用户体验相关"""
    print("\n📝 准备新的补充词典数据（详细版用户体验相关）...")

    # 您提供的新词典数据 - 详细版用户体验相关
    new_dictionary_data = [
        {"术语": "白点", "别名": "Bright Pixel;白色亮点", "类别": "异常现象", "多标签": "显示相关;外观", "备注": "**定义**: 屏幕像素点常亮为白色。 **判定口径**: ISO9241 标准，>3 个判为不良。 **常见场景**: 出厂检验。 **排查路径**: 检查面板→驱动IC。 **对策**: 加强出厂全检，控制面板良率。"},
        {"术语": "触控失灵", "别名": "触摸屏无响应;Touch Fail", "类别": "异常现象", "多标签": "显示相关;人机交互", "备注": "**定义**: 触摸操作无效或延迟。 **判定口径**: 单点/多点触控测试失败。 **常见场景**: 高湿环境、屏幕贴膜。 **排查路径**: 检查TP模组→固件→驱动IC。 **对策**: 优化算法，改善屏幕贴合。"},
        {"术语": "漏测", "别名": "测试遗漏;Missed Test", "类别": "流程相关", "多标签": "质量体系;测试验证", "备注": "**定义**: 应检项目未执行。 **判定口径**: 测试覆盖率 <100%。 **常见场景**: 产线OBA/功能测试。 **排查路径**: 审核工艺卡→检查治具。 **对策**: 加强自动化测试和流程审核。"},
        {"术语": "频偏", "别名": "频率偏移;Frequency Offset", "类别": "性能指标", "多标签": "通信相关;射频相关", "备注": "**定义**: 无线发射频率偏离标准值。 **判定口径**: 偏移 >±50ppm。 **常见场景**: OTA测试、极端温度。 **排查路径**: 检查晶振→校准电路。 **对策**: 增加温补电路，改善器件精度。"},
        {"术语": "信号弱", "别名": "信号差;Low Signal", "类别": "异常现象", "多标签": "通信相关;用户体验", "备注": "**定义**: 手机在正常网络环境下信号强度不足。 **判定口径**: RSRP < -110dBm。 **常见场景**: 地铁、地下室。 **排查路径**: 检查天线设计→射频通道。 **对策**: 优化天线布局，增加功放。"},
        {"术语": "通话掉线", "别名": "Call Drop", "类别": "异常现象", "多标签": "通信相关;用户体验", "备注": "**定义**: 通话过程中意外中断。 **判定口径**: 掉话率 >2%。 **常见场景**: 移动场景、弱覆盖。 **排查路径**: 抓取log→检查协议栈→网络条件。 **对策**: 优化射频功率控制，改善切换策略。"},
        {"术语": "电池续航不足", "别名": "续航差;Poor Battery Life", "类别": "性能指标", "多标签": "硬件相关;电池", "备注": "**定义**: 单次充电使用时长不足。 **判定口径**: 使用时长低于标称值 20%。 **常见场景**: 高功耗应用。 **排查路径**: 功耗分析→检查电芯容量。 **对策**: 优化系统调度，提升电池能量密度。"},
        {"术语": "充电慢", "别名": "慢充;Slow Charging", "类别": "异常现象", "多标签": "电池;硬件相关", "备注": "**定义**: 充电速率低于设计值。 **判定口径**: 充电电流 < 额定值 70%。 **常见场景**: 使用非原装充电器。 **排查路径**: 检查充电IC→协议识别。 **对策**: 增加兼容性测试，优化协议栈。"},
        {"术语": "充不进电", "别名": "无法充电;Not Charging", "类别": "异常现象", "多标签": "电池;硬件相关", "备注": "**定义**: 手机接入电源无法充电。 **判定口径**: 电池电量无上升。 **常见场景**: 接口损坏、过放保护。 **排查路径**: 检查充电口→电池保护板。 **对策**: 增强接口防护，优化BMS策略。"},
        {"术语": "电池发热", "别名": "充电发烫;Battery Heating", "类别": "异常现象", "多标签": "电池;安全相关", "备注": "**定义**: 电池温度异常升高。 **判定口径**: 电池温度 >50℃。 **常见场景**: 快充、边充边玩。 **排查路径**: 检查快充协议→电芯阻抗。 **对策**: 控制快充功率，提升散热。"},
        {"术语": "电池容量衰减", "别名": "电池老化;Battery Aging", "类别": "性能指标", "多标签": "电池;可靠性", "备注": "**定义**: 电池可用容量下降。 **判定口径**: 循环 500 次后容量 <80%。 **常见场景**: 长期使用。 **排查路径**: 读取电池健康数据。 **对策**: 改善材料体系，增加健康监控。"},
        {"术语": "耗电异常", "别名": "功耗异常;Abnormal Power Drain", "类别": "异常现象", "多标签": "软件相关;电池", "备注": "**定义**: 待机/使用时电量消耗过快。 **判定口径**: 待机功耗 >200mW。 **常见场景**: APP后台运行。 **排查路径**: 分析耗电曲线→定位进程。 **对策**: 优化系统调度，限制异常应用。"},
        {"术语": "过充", "别名": "过度充电;Over Charging", "类别": "异常现象", "多标签": "电池;安全相关", "备注": "**定义**: 电池电压超过安全上限。 **判定口径**: 电压 >4.35V。 **常见场景**: 充电保护失效。 **排查路径**: 检查BMS→充电IC。 **对策**: 增加保护电路，提升电芯一致性。"},
        {"术语": "过放", "别名": "过度放电;Over Discharging", "类别": "异常现象", "多标签": "电池;安全相关", "备注": "**定义**: 电池电压低于安全下限。 **判定口径**: 电压 <3.0V。 **常见场景**: 长时间未充电。 **排查路径**: 检查电池保护板。 **对策**: 增加欠压保护，改善电量计校准。"},
        {"术语": "电池膨胀", "别名": "电芯膨胀;Cell Expansion", "类别": "异常现象", "多标签": "电池;可靠性", "备注": "**定义**: 电芯鼓胀导致结构异常。 **判定口径**: 厚度增加 >10%。 **常见场景**: 高温、寿命末期。 **排查路径**: 检查气胀情况。 **对策**: 优化电芯材料，增加气体吸收层。"},
        {"术语": "屏幕碎裂", "别名": "屏幕破裂;Screen Crack", "类别": "异常现象", "多标签": "显示相关;结构相关", "备注": "**定义**: 显示屏出现裂纹/碎裂。 **判定口径**: 裂纹可见。 **常见场景**: 跌落。 **排查路径**: 检查玻璃材质/结构。 **对策**: 使用康宁大猩猩玻璃，优化保护壳设计。"},
        {"术语": "屏幕进灰", "别名": "显示进灰;Dust Inside Screen", "类别": "异常现象", "多标签": "显示相关;结构相关", "备注": "**定义**: 屏幕层间进入异物。 **判定口径**: 黑屏下可见颗粒。 **常见场景**: 密封不良。 **排查路径**: 检查密封胶→结构间隙。 **对策**: 改善装配工艺，增加洁净度控制。"},
        {"术语": "色偏", "别名": "显示偏色;Color Shift", "类别": "异常现象", "多标签": "显示相关;CMF", "备注": "**定义**: 显示色彩与标准不符。 **判定口径**: ΔE >3。 **常见场景**: 屏幕老化。 **排查路径**: 检查色彩管理→面板一致性。 **对策**: 增加出厂校色，优化算法。"},
        {"术语": "残影", "别名": "烧屏;Image Retention", "类别": "异常现象", "多标签": "显示相关;可靠性", "备注": "**定义**: 静态画面残留。 **判定口径**: 静态图像切换后残留 >30s。 **常见场景**: OLED屏。 **排查路径**: 检查驱动算法→面板寿命。 **对策**: 优化像素刷新，增加均匀老化策略。"},
        {"术语": "闪烁", "别名": "屏闪;Flicker", "类别": "异常现象", "多标签": "显示相关;影像相关", "备注": "**定义**: 屏幕亮度快速变化。 **判定口径**: PWM频率 <240Hz。 **常见场景**: 低亮度使用。 **排查路径**: 检查驱动IC→调光方案。 **对策**: 提升PWM频率，采用DC调光。"}
    ]
        {"术语": "划伤", "别名": "刮伤;Scratch", "类别": "异常现象", "多标签": "外观;可靠性", "备注": "产品表面因摩擦留下的线性痕迹，影响美观，严重时影响功能。"},
        {"术语": "环测", "别名": "环境测试;Environmental Test", "类别": "测试验证", "多标签": "可靠性", "备注": "将手机置于高低温、湿热、振动等模拟环境中，验证其适应能力。"},
        {"术语": "黄斑", "别名": "屏幕黄斑;Yellow Spot", "类别": "异常现象", "多标签": "显示相关", "备注": "OLED屏幕局部出现的黄色斑块，可能与封装或材料老化有关。"},
        {"术语": "灰阶", "别名": "灰度等级;Gray Scale", "类别": "显示相关", "多标签": "性能指标;影像相关", "备注": "表示屏幕从黑到白的亮度层次，层次越多，显示效果越细腻。"},
        {"术语": "回流焊", "别名": "再流焊;Reflow", "类别": "制造工艺", "多标签": "SMT;工艺参数", "备注": "通过加热使预涂的锡膏熔化，实现元器件与PCB焊盘连接的工艺。"},
        {"术语": "混光", "别名": "灯光混合;Light Mixing", "类别": "异常现象", "多标签": "硬件相关;外观", "备注": "不同颜色的LED灯光相互干扰，导致光色不纯，常见于指示灯设计。"},
        {"术语": "击穿", "别名": "电压击穿;Breakdown", "类别": "异常现象", "多标签": "硬件相关;安全相关", "备注": "元器件因过电压导致绝缘失效而损坏，如电容击穿、ESD击穿。"},
        {"术语": "激活", "别名": "电池激活;Battery Activation", "类别": "制造工艺", "多标签": "硬件相关;工艺参数", "备注": "新电池首次充电的特定流程，以稳定其化学性能，但现在多数锂电已不需要。"},
        {"术语": "机模", "别名": "手机模型;Dummy Model", "类别": "工具", "多标签": "项目相关;结构相关", "备注": "无功能的手机外观模型，用于早期结构验证、外观评估和营销展示。"},
        {"术语": "积墨", "别名": "锡膏堆积;Solder Paste Accumulation", "类别": "异常现象", "多标签": "SMT;制造工艺", "备注": "钢网开口堵塞或刮刀压力不当导致锡膏印刷后局部过量，易引起连锡。"},
        {"术语": "基带", "别名": "Baseband", "类别": "硬件相关", "多标签": "部件;通信相关", "备注": "负责移动网络信号处理的芯片组，其软件和硬件故障会导致无服务、通话中断。"},
        {"术语": "基板", "别名": "衬底;Substrate", "类别": "硬件相关", "多标签": "部件;PCB", "备注": "承载芯片和电路的基底材料，如陶瓷基板、BT基板等。"},
        {"术语": "激光", "别名": "激光焊接;Laser Welding", "类别": "制造工艺", "多标签": "工艺参数;结构相关", "备注": "使用激光能量进行精密焊接，常用于电池盖、内部结构件，热影响区小。"},
        {"术语": "极耳", "别名": "电池极耳; Battery Tab", "类别": "硬件相关", "多标签": "部件;安全相关", "备注": "电芯正负极引出的金属带，焊接不良或折断会导致电池无法充电或工作。"},
        {"术语": "夹持", "别名": "夹具夹紧;Clamping", "类别": "制造工艺", "多标签": "工艺参数;工装", "备注": "治具对产品的固定力，过小导致位移，过大可能导致产品变形或压伤。"},
        {"术语": "夹料", "别名": "材料被夹;Material Pinching", "类别": "异常现象", "多标签": "制造工艺;结构相关", "备注": "在装配过程中，线材、FPC等软性材料被外壳或螺丝不当挤压。"},
        {"术语": "假电", "别名": "虚电;False Power", "类别": "异常现象", "多标签": "硬件相关;软件相关", "备注": "手机显示电量充足但迅速关机，通常与电池老化、电量计校准不准有关。"},
        {"术语": "假压", "别名": "虚压;False Pressure", "类别": "异常现象", "多标签": "制造工艺;结构相关", "备注": "螺丝未真正拧紧或扭矩失效，导致连接松动，存在可靠性风险。"},
        {"术语": "检具", "别名": "检验治具;Checking Fixture", "类别": "工具", "多标签": "测试验证;质量体系", "备注": "专门用于快速检测产品尺寸或装配效果的工装，提升检验效率和一致性。"},
        {"术语": "胶厚", "别名": "胶水厚度;Adhesive Thickness", "类别": "制造工艺", "多标签": "工艺参数;结构相关", "备注": "点胶或贴合的胶层厚度，影响粘接强度和密封性能。"},
        {"术语": "胶量", "别名": "点胶量;Dispensing Volume", "类别": "制造工艺", "多标签": "工艺参数", "备注": "点胶机每次挤出的胶水体积，是影响粘接效果的关键参数。"},
        {"术语": "胶印", "别名": "胶水痕迹;Adhesive Mark", "类别": "异常现象", "多标签": "外观;制造工艺", "备注": "胶水溢出或擦拭不净，在产品表面留下可见的痕迹。"},
        {"术语": "焦灼", "别名": "烧焦;Burn Mark", "类别": "异常现象", "多标签": "硬件相关;可靠性", "备注": "局部过热导致塑料或PCB碳化变黑，通常为严重故障的表现。"},
        {"术语": "角胶", "别名": "角落补强胶;Corner Reinforcement", "类别": "制造工艺", "多标签": "结构相关;工艺参数", "备注": "在结构件角落点胶以增强局部强度，常用于应对跌落应力。"},
        {"术语": "铰链", "别名": "转轴;Hinge", "类别": "结构相关", "多标签": "部件;可靠性", "备注": "折叠屏手机的核心机构，要求高寿命、顺滑度和稳定性。"}
    ]

    print(f"   📊 新增词条数: {len(new_dictionary_data)}")
    return new_dictionary_data

def categorize_new_terms(new_data, existing_terms):
    """分类新词条并去重"""
    print("\n📋 分类新词条并去重...")
    
    categories = {
        "components": [],
        "symptoms": [],
        "causes": [],
        "countermeasures": []
    }
    
    duplicates = []
    added_count = 0
    
    for item in new_data:
        term = item["术语"].strip()
        category = item["类别"]
        
        # 检查重复
        if term.lower() in existing_terms:
            duplicates.append(term)
            print(f"   ⚠️  跳过重复词条: {term}")
            continue
        
        # 根据类别分类
        if category in ["硬件相关", "结构相关", "摄像头模组", "影像相关", "性能指标"]:
            categories["components"].append(item)
        elif category in ["异常现象"]:
            categories["symptoms"].append(item)
        elif category in ["工具", "测试验证", "流程相关", "项目相关", "制造工艺", "组织职责", "软件相关"]:
            categories["countermeasures"].append(item)
        else:
            # 默认归类到对策
            categories["countermeasures"].append(item)
        
        existing_terms.add(term.lower())  # 添加到已存在集合
        added_count += 1
    
    print(f"   📊 新增分类结果:")
    print(f"      Components: {len(categories['components'])} 条")
    print(f"      Symptoms: {len(categories['symptoms'])} 条")
    print(f"      Causes: {len(categories['causes'])} 条")
    print(f"      Countermeasures: {len(categories['countermeasures'])} 条")
    print(f"   📊 重复跳过: {len(duplicates)} 条")
    print(f"   📊 实际新增: {added_count} 条")
    
    return categories, duplicates

def append_to_existing_files(existing_data, new_categories):
    """追加新数据到现有文件"""
    print("\n💾 追加新数据到现有文件...")
    
    unified_dir = Path("data/unified_dictionary")
    fieldnames = ['term', 'canonical_name', 'aliases', 'category', 'tags', 'description', 'source_file', 'created_at', 'updated_at']
    
    total_added = 0
    
    for category_name, new_items in new_categories.items():
        if not new_items:
            continue
            
        file_path = unified_dir / f"{category_name}.csv"
        
        # 读取现有数据
        existing_items = existing_data[category_name]
        
        # 转换新数据格式
        converted_items = []
        for item in new_items:
            converted = {
                'term': item['术语'],
                'canonical_name': item['术语'],
                'aliases': item['别名'],
                'category': item['类别'],
                'tags': item['多标签'],
                'description': item['备注'],
                'source_file': 'manual_append',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            converted_items.append(converted)
        
        # 合并数据并重写文件
        all_items = existing_items + converted_items
        
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_items)
        
        print(f"   ✅ 更新文件: {file_path.name} (新增 {len(converted_items)} 条，总计 {len(all_items)} 条)")
        total_added += len(converted_items)
    
    # 更新统计文件
    stats = {
        'total_terms': sum(len(existing_data[cat]) for cat in existing_data.keys()) + total_added,
        'categories': {cat: len(existing_data[cat]) + len(new_categories[cat]) for cat in existing_data.keys()},
        'last_updated': datetime.now().isoformat(),
        'last_append': {
            'date': datetime.now().isoformat(),
            'added_count': total_added,
            'source': 'manual_append_batch_2'
        },
        'unified_directory': str(unified_dir)
    }
    
    with open(unified_dir / "statistics.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"   📊 统计文件已更新")
    print(f"   📊 本次新增总数: {total_added}")
    
    return total_added

def main():
    """主函数"""
    print("🚀 补充新词典数据到统一词典")
    print("=" * 60)
    
    # 1. 备份当前数据
    backup_dir = backup_current_unified_data()
    
    # 2. 加载现有数据
    existing_data, existing_terms = load_existing_data()
    
    # 3. 创建新词典数据
    new_data = create_new_dictionary_data()
    
    # 4. 分类新词条并去重
    new_categories, duplicates = categorize_new_terms(new_data, existing_terms)
    
    # 5. 追加到现有文件
    total_added = append_to_existing_files(existing_data, new_categories)
    
    print("\n" + "=" * 60)
    print("🎉 词典数据补充完成!")
    print(f"💾 备份目录: {backup_dir}")
    print(f"📊 本次新增: {total_added} 条")
    print(f"📊 重复跳过: {len(duplicates)} 条")
    print(f"📁 统一词典目录: data/unified_dictionary")
    
    if duplicates:
        print(f"\n⚠️  跳过的重复词条:")
        for dup in duplicates[:10]:  # 只显示前10个
            print(f"   - {dup}")
        if len(duplicates) > 10:
            print(f"   ... 还有 {len(duplicates) - 10} 个")
    
    print("\n💡 下一步:")
    print("1. 重启API服务以加载新数据")
    print("2. 测试前端词典页面")
    print("3. 验证查重功能")

if __name__ == "__main__":
    main()
    print(f"💾 备份目录: {backup_dir}")
    print(f"📊 本次新增: {total_added} 条")
    print(f"📊 重复跳过: {len(duplicates)} 条")
    print(f"📁 统一词典目录: data/unified_dictionary")
    
    if duplicates:
        print(f"\n⚠️  跳过的重复词条:")
        for dup in duplicates[:10]:  # 只显示前10个
            print(f"   - {dup}")
        if len(duplicates) > 10:
            print(f"   ... 还有 {len(duplicates) - 10} 个")
    
    print("\n💡 下一步:")
    print("1. 重启API服务以加载新数据")
    print("2. 测试前端词典页面")
    print("3. 验证查重功能")

if __name__ == "__main__":
    main()
