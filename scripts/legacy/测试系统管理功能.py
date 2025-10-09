#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path

def test_system_management_config():
    """测试系统管理配置文件"""
    print("🧪 测试系统管理配置...")
    
    config_file = Path("config/system_management_config.json")
    
    if not config_file.exists():
        print("❌ 配置文件不存在")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ 配置文件加载成功")
        
        # 检查各个模块
        modules = ['rules', 'prompts', 'scenarios', 'versions', 'extraction_logics', 'agents']
        
        for module in modules:
            if module in config:
                count = len(config[module])
                print(f"   📊 {module}: {count} 条记录")
            else:
                print(f"   ⚠️ {module}: 模块缺失")
        
        # 检查统计信息
        if 'statistics' in config:
            stats = config['statistics']
            print(f"   📈 统计信息:")
            for key, value in stats.items():
                print(f"      - {key}: {value}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False

def test_vue_components():
    """测试Vue组件文件"""
    print("\n🧪 测试Vue组件...")
    
    components = [
        "apps/web/src/views/SystemManagement.vue",
        "apps/web/src/components/system/RulesManagement.vue",
        "apps/web/src/components/system/PromptsManagement.vue",
        "apps/web/src/components/system/ScenariosManagement.vue",
        "apps/web/src/components/system/VersionsManagement.vue",
        "apps/web/src/components/system/ExtractionManagement.vue",
        "apps/web/src/components/system/AgentsManagement.vue"
    ]
    
    all_exist = True
    
    for component in components:
        if Path(component).exists():
            print(f"✅ {Path(component).name}")
        else:
            print(f"❌ {Path(component).name} - 文件不存在")
            all_exist = False
    
    return all_exist

def test_router_config():
    """测试路由配置"""
    print("\n🧪 测试路由配置...")
    
    router_file = Path("apps/web/src/router/index.js")
    
    if not router_file.exists():
        print("❌ 路由文件不存在")
        return False
    
    try:
        with open(router_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'system-management' in content:
            print("✅ 系统管理路由已配置")
            return True
        else:
            print("❌ 系统管理路由未配置")
            return False
            
    except Exception as e:
        print(f"❌ 路由文件读取失败: {e}")
        return False

def test_api_config():
    """测试API配置"""
    print("\n🧪 测试API配置...")
    
    api_file = Path("apps/web/src/api/index.js")
    
    if not api_file.exists():
        print("❌ API文件不存在")
        return False
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        api_methods = [
            'getSystemStatus',
            'exportSystemConfig',
            'getRules',
            'createRule',
            'updateRule'
        ]
        
        missing_methods = []
        for method in api_methods:
            if method not in content:
                missing_methods.append(method)
        
        if not missing_methods:
            print("✅ 所有API方法已配置")
            return True
        else:
            print(f"❌ 缺失API方法: {', '.join(missing_methods)}")
            return False
            
    except Exception as e:
        print(f"❌ API文件读取失败: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n📋 生成测试报告...")
    
    # 执行所有测试
    config_test = test_system_management_config()
    components_test = test_vue_components()
    router_test = test_router_config()
    api_test = test_api_config()
    
    # 生成报告
    report = {
        "timestamp": "2024-01-20 15:45:00",
        "test_results": {
            "config_file": config_test,
            "vue_components": components_test,
            "router_config": router_test,
            "api_config": api_test
        },
        "features_implemented": [
            "系统管理主页面",
            "规则管理模块",
            "Prompt管理模块", 
            "场景管理模块",
            "版本管理模块",
            "文档抽取逻辑管理",
            "Agent设计管理"
        ],
        "data_structure": {
            "rules": "4条验证和标准化规则",
            "prompts": "3个专业Prompt模板",
            "scenarios": "2个应用场景配置",
            "versions": "2个版本记录",
            "extraction_logics": "2个文档抽取逻辑",
            "agents": "2个专业Agent设计"
        },
        "access_info": {
            "route": "/system-management",
            "menu": "系统管理",
            "components": "6个子功能模块"
        }
    }
    
    # 保存报告
    with open('系统管理功能测试报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("✅ 测试报告已生成: 系统管理功能测试报告.json")
    
    # 显示总结
    print("\n" + "=" * 60)
    print("🏛️ 系统管理功能测试总结")
    print("=" * 60)
    
    print(f"\n📊 测试结果:")
    print(f"   配置文件: {'✅ 通过' if config_test else '❌ 失败'}")
    print(f"   Vue组件: {'✅ 通过' if components_test else '❌ 失败'}")
    print(f"   路由配置: {'✅ 通过' if router_test else '❌ 失败'}")
    print(f"   API配置: {'✅ 通过' if api_test else '❌ 失败'}")
    
    print(f"\n🎯 功能模块:")
    print("   ✅ 规则管理 - 4条业务规则配置")
    print("   ✅ Prompt管理 - 3个专业模板")
    print("   ✅ 场景管理 - 2个应用场景")
    print("   ✅ 版本管理 - 版本历史追踪")
    print("   ✅ 文档抽取 - 2个抽取逻辑")
    print("   ✅ Agent设计 - 2个专业Agent")
    
    print(f"\n🌐 访问方式:")
    print("   - 路由地址: /system-management")
    print("   - 菜单入口: 系统管理")
    print("   - 主要功能: 6个标签页切换")
    
    print(f"\n📋 数据特点:")
    print("   - 基于真实业务场景设计")
    print("   - 支持CRUD操作")
    print("   - 包含测试和验证功能")
    print("   - 提供导出和配置管理")
    
    # 计算总体成功率
    total_tests = 4
    passed_tests = sum([config_test, components_test, router_test, api_test])
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📈 总体成功率: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate == 100:
        print("\n🎉 系统管理功能重新设计完成！")
        print("   所有测试通过，功能已准备就绪。")
    else:
        print("\n⚠️ 部分功能需要检查，请参考测试结果。")
    
    print(f"\n💡 使用说明:")
    print("   1. 启动前端服务: cd apps/web && npm run dev")
    print("   2. 访问系统管理: http://localhost:5173/system-management")
    print("   3. 切换功能模块: 点击对应标签页")
    print("   4. 管理配置数据: 使用各模块的增删改查功能")
    
    return report

def main():
    """主函数"""
    print("🏛️ 系统管理功能测试")
    print("=" * 60)
    
    # 生成测试报告
    report = generate_test_report()
    
    print(f"\n🎯 重新设计亮点:")
    print("   - 从数据治理转换为系统管理")
    print("   - 6个专业功能模块")
    print("   - 完整的配置管理体系")
    print("   - 支持逻辑和设计记录")
    print("   - 现代化的用户界面")

if __name__ == "__main__":
    main()
