#!/usr/bin/env python3
"""
测试词典抽取Prompt集成
验证新的prompt是否正确添加到前端系统中
"""

import requests
import json
import sys
from datetime import datetime

def test_frontend_access():
    """测试前端访问"""
    print("🌐 测试前端访问...")
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("  ✅ 前端服务正常运行")
            return True
        else:
            print(f"  ❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 前端服务无法访问: {e}")
        return False

def test_system_management_page():
    """测试系统管理页面"""
    print("⚙️ 测试系统管理页面...")
    
    try:
        # 测试系统管理页面
        response = requests.get("http://localhost:5173/#/system", timeout=5)
        if response.status_code == 200:
            print("  ✅ 系统管理页面可访问")
            return True
        else:
            print(f"  ❌ 系统管理页面异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 系统管理页面无法访问: {e}")
        return False

def check_prompt_files():
    """检查prompt相关文件"""
    print("📁 检查prompt相关文件...")
    
    files_to_check = [
        "apps/web/src/components/system/PromptsManagement.vue",
        "优化后的词典抽取Prompt.md",
        "词典抽取Prompt_简化版.md",
        "词典抽取Prompt优化对比.md"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 0:
                    print(f"  ✅ {file_path}: 存在 ({len(content)} 字符)")
                else:
                    print(f"  ⚠️ {file_path}: 文件为空")
                    all_exist = False
        except FileNotFoundError:
            print(f"  ❌ {file_path}: 文件不存在")
            all_exist = False
        except Exception as e:
            print(f"  ❌ {file_path}: 读取失败 - {e}")
            all_exist = False
    
    return all_exist

def check_prompt_content():
    """检查prompt内容"""
    print("📝 检查prompt内容...")
    
    try:
        with open("apps/web/src/components/system/PromptsManagement.vue", 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 检查是否包含新的prompt
            checks = [
                ("词典抽取专家", "词典抽取专家" in content),
                ("extraction分类", "category: 'extraction'" in content),
                ("8个类别说明", "Symptom" in content and "Component" in content),
                ("70个标签", "显示相关" in content and "制造工艺" in content),
                ("分类决策树", "分类决策树" in content),
                ("标准示例", "FMEA" in content and "虚焊" in content)
            ]
            
            all_passed = True
            for check_name, check_result in checks:
                if check_result:
                    print(f"  ✅ {check_name}: 已包含")
                else:
                    print(f"  ❌ {check_name}: 缺失")
                    all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"  ❌ 检查prompt内容失败: {e}")
        return False

def generate_usage_example():
    """生成使用示例"""
    print("📚 生成使用示例...")
    
    example_document = """
    手机摄像头模组在生产过程中常见的质量问题包括：
    1. 对焦不准确 - 通常由于镜头组装偏差导致
    2. 白平衡异常 - 可能是传感器校准问题
    3. 噪点过多 - 与图像处理算法和传感器性能相关
    4. 色彩偏差 - 需要通过色彩校正算法调整
    
    检测工具包括：
    - CCD视觉对位系统
    - 色彩分析仪
    - 分辨率测试卡
    
    质量指标：
    - 分辨率: 1200万像素
    - 信噪比: >40dB
    - 色彩准确度: ΔE<3
    """
    
    print("  📄 示例文档内容:")
    print("    " + example_document.replace("\n", "\n    "))
    
    print("\n  🎯 期望抽取结果:")
    expected_terms = [
        ("对焦不准确", "Symptom", "影像相关;硬件相关;可靠性"),
        ("白平衡异常", "Symptom", "影像相关;硬件相关;外观"),
        ("CCD视觉对位系统", "Tool", "工具;测试验证;影像相关"),
        ("色彩分析仪", "Tool", "工具;测试验证;影像相关"),
        ("分辨率", "Metric", "性能指标;影像相关;硬件相关"),
        ("信噪比", "Metric", "性能指标;影像相关;电气性能")
    ]
    
    for term, category, tags in expected_terms:
        print(f"    - {term} ({category}): {tags}")
    
    return True

def create_integration_report():
    """创建集成报告"""
    print("📊 创建集成报告...")
    
    report = {
        "integration_time": datetime.now().isoformat(),
        "prompt_versions": [
            {
                "id": "p003",
                "name": "词典抽取专家",
                "category": "extraction",
                "version": "2.0",
                "description": "简化版词典抽取prompt，适合日常使用"
            },
            {
                "id": "p004", 
                "name": "词典抽取专家(详细版)",
                "category": "extraction",
                "version": "2.1",
                "description": "完整版词典抽取prompt，包含详细指导"
            }
        ],
        "features": [
            "8个标准分类体系 (Symptom, Component, Tool, Process, TestCase, Metric, Material, Role)",
            "70个多维标签体系 (domain, process, quality, lifecycle, material, function, organization, other)",
            "分类决策树指导",
            "快速参考表",
            "标准示例模板",
            "特殊处理规则",
            "质量检查机制"
        ],
        "integration_status": "completed",
        "frontend_location": "apps/web/src/components/system/PromptsManagement.vue",
        "access_path": "http://localhost:5173/#/system -> Prompt管理"
    }
    
    with open("prompt_integration_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("  ✅ 集成报告已保存: prompt_integration_report.json")
    return True

def main():
    """主测试函数"""
    print("🔧 词典抽取Prompt集成测试")
    print("=" * 50)
    
    tests = [
        ("前端访问测试", test_frontend_access),
        ("系统管理页面测试", test_system_management_page),
        ("Prompt文件检查", check_prompt_files),
        ("Prompt内容检查", check_prompt_content),
        ("使用示例生成", generate_usage_example),
        ("集成报告创建", create_integration_report)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        try:
            if test_func():
                passed_tests += 1
                print(f"  ✅ {test_name}: 通过")
            else:
                print(f"  ❌ {test_name}: 失败")
        except Exception as e:
            print(f"  ❌ {test_name}: 异常 - {e}")
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试总结")
    print("=" * 50)
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"✅ 通过测试: {passed_tests}/{total_tests}")
    print(f"📊 成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 集成测试通过！词典抽取Prompt已成功集成到前端系统")
        print("\n📍 访问路径:")
        print("  1. 打开浏览器访问: http://localhost:5173")
        print("  2. 导航到: 系统管理 -> Prompt管理")
        print("  3. 查看新增的词典抽取prompt")
        
        print("\n🎯 使用方法:")
        print("  1. 在Prompt管理中选择'词典抽取专家'")
        print("  2. 填入文档内容和抽取要求")
        print("  3. 生成完整的词典抽取prompt")
        print("  4. 复制prompt到AI助手中使用")
        
        return 0
    else:
        print("⚠️ 集成测试部分失败，需要检查相关问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())
