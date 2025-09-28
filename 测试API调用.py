#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_api_endpoints():
    """测试所有相关的API端点"""
    print("🧪 测试API端点...")
    
    endpoints = [
        {
            'name': '健康检查',
            'url': 'http://localhost:8000/health',
            'method': 'GET'
        },
        {
            'name': '数据治理信息',
            'url': 'http://localhost:8000/kg/governance-data',
            'method': 'GET'
        },
        {
            'name': '图谱可视化数据',
            'url': 'http://localhost:8000/kg/graph-data',
            'method': 'GET'
        },
        {
            'name': '真实统计数据',
            'url': 'http://localhost:8000/kg/real-stats',
            'method': 'GET'
        }
    ]
    
    results = {}
    
    for endpoint in endpoints:
        print(f"\n🔍 测试 {endpoint['name']}...")
        try:
            response = requests.get(endpoint['url'], timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint['name']}: 响应正常")
                
                try:
                    data = response.json()
                    if data.get('success') or data.get('ok'):
                        print(f"   📊 数据格式正确")
                        
                        # 显示关键信息
                        if 'data' in data:
                            if endpoint['name'] == '数据治理信息':
                                overview = data['data'].get('data_overview', {})
                                print(f"   - 总条目: {overview.get('total_entries', 'N/A')}")
                                print(f"   - 质量分: {overview.get('quality_score', 'N/A')}%")
                            elif endpoint['name'] == '图谱可视化数据':
                                stats = data['data'].get('stats', {})
                                print(f"   - 节点数: {stats.get('totalNodes', 'N/A')}")
                                print(f"   - 关系数: {stats.get('totalRelations', 'N/A')}")
                        
                        results[endpoint['name']] = 'success'
                    else:
                        print(f"   ⚠️ 数据格式异常")
                        results[endpoint['name']] = 'format_error'
                        
                except json.JSONDecodeError:
                    print(f"   ❌ JSON解析失败")
                    results[endpoint['name']] = 'json_error'
                    
            else:
                print(f"❌ {endpoint['name']}: HTTP {response.status_code}")
                print(f"   响应内容: {response.text[:200]}...")
                results[endpoint['name']] = f'http_{response.status_code}'
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint['name']}: 连接失败")
            results[endpoint['name']] = 'connection_error'
        except requests.exceptions.Timeout:
            print(f"❌ {endpoint['name']}: 请求超时")
            results[endpoint['name']] = 'timeout'
        except Exception as e:
            print(f"❌ {endpoint['name']}: 未知错误 - {e}")
            results[endpoint['name']] = f'error_{str(e)}'
    
    return results

def check_frontend_service():
    """检查前端服务状态"""
    print("\n🌐 检查前端服务...")
    
    try:
        response = requests.get('http://localhost:5173', timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务正常运行")
            return True
        else:
            print(f"❌ 前端服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 前端服务连接失败: {e}")
        print("   请启动前端服务: cd apps/web && npm run dev")
        return False

def generate_fix_guide():
    """生成修复指南"""
    print("\n📋 生成修复指南...")
    
    # 测试API
    api_results = test_api_endpoints()
    frontend_ok = check_frontend_service()
    
    # 生成报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "api_results": api_results,
        "frontend_status": frontend_ok,
        "issues_fixed": [
            "修复了 apiClient.getGovernanceData 方法调用错误",
            "更新了API导入方式从 apiClient 到 api",
            "确保了API方法名称的一致性"
        ],
        "troubleshooting": {
            "api_not_running": "python api/main.py",
            "frontend_not_running": "cd apps/web && npm run dev",
            "clear_cache": "Ctrl+Shift+R 或 Cmd+Shift+R",
            "check_console": "F12 -> Console 查看错误信息"
        }
    }
    
    # 保存报告
    with open('API调用修复报告.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("✅ 修复报告已生成: API调用修复报告.json")
    
    # 显示总结
    print("\n" + "=" * 60)
    print("🔧 API调用问题修复总结")
    print("=" * 60)
    
    print(f"\n📊 API测试结果:")
    for endpoint, result in api_results.items():
        status = "✅ 正常" if result == 'success' else f"❌ {result}"
        print(f"   {endpoint}: {status}")
    
    print(f"\n🌐 前端服务: {'✅ 正常' if frontend_ok else '❌ 异常'}")
    
    print(f"\n🔧 已修复的问题:")
    print("   ✅ 修复了 API 方法调用错误")
    print("   ✅ 统一了 API 导入方式")
    print("   ✅ 确保了方法名称一致性")
    
    print(f"\n🚀 下一步操作:")
    
    # 检查是否有API问题
    api_issues = [k for k, v in api_results.items() if v != 'success']
    if api_issues:
        print("   ⚠️ API服务问题:")
        for issue in api_issues:
            if 'connection_error' in api_results[issue]:
                print(f"   - 启动API服务: python api/main.py")
                break
    
    if not frontend_ok:
        print("   ⚠️ 前端服务问题:")
        print("   - 启动前端服务: cd apps/web && npm run dev")
    
    print("   1. 确保所有服务已启动")
    print("   2. 清除浏览器缓存 (Ctrl+Shift+R)")
    print("   3. 访问数据治理页面: http://localhost:5173/governance")
    print("   4. 检查浏览器控制台是否还有错误")
    
    print(f"\n🌐 访问地址:")
    print("   - 数据治理页面: http://localhost:5173/governance")
    print("   - API文档: http://localhost:8000/docs")
    print("   - 主页: http://localhost:5173")
    
    # 成功率统计
    success_count = sum(1 for result in api_results.values() if result == 'success')
    total_count = len(api_results)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"\n📈 API成功率: {success_rate:.1f}% ({success_count}/{total_count})")
    
    if success_rate == 100 and frontend_ok:
        print("\n🎉 所有问题已解决！系统运行正常。")
    else:
        print("\n⚠️ 部分问题需要处理，请参考上述指南。")
    
    return report

def main():
    """主函数"""
    print("🔧 API调用问题修复工具")
    print("=" * 60)
    
    # 生成修复指南
    report = generate_fix_guide()
    
    print(f"\n💡 快速修复命令:")
    print("   # 启动API服务")
    print("   python api/main.py")
    print("   ")
    print("   # 启动前端服务")
    print("   cd apps/web && npm run dev")

if __name__ == "__main__":
    main()
