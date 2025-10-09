#!/usr/bin/env python3
"""测试修复结果"""

import requests
import time

SERVER_URL = "http://47.108.152.16"

print("="*80)
print("测试修复结果")
print("="*80)

# 测试不同的API端点
test_cases = [
    {
        "name": "健康检查",
        "url": f"{SERVER_URL}/api/health",
        "timeout": 10
    },
    {
        "name": "图谱统计",
        "url": f"{SERVER_URL}/api/kg/stats",
        "timeout": 10
    },
    {
        "name": "真实统计数据",
        "url": f"{SERVER_URL}/api/kg/real-stats",
        "timeout": 10
    },
    {
        "name": "小数据量图谱 (limit=100)",
        "url": f"{SERVER_URL}/api/kg/graph?limit=100&show_all=false",
        "timeout": 30
    },
    {
        "name": "中等数据量图谱 (limit=500)",
        "url": f"{SERVER_URL}/api/kg/graph?limit=500&show_all=false",
        "timeout": 30
    },
    {
        "name": "大数据量图谱 (limit=1000)",
        "url": f"{SERVER_URL}/api/kg/graph?limit=1000&show_all=false",
        "timeout": 60
    },
    {
        "name": "显示全部 (limit=5000)",
        "url": f"{SERVER_URL}/api/kg/graph?limit=5000&show_all=true",
        "timeout": 60
    }
]

results = []

for test in test_cases:
    print(f"\n{'='*80}")
    print(f"测试: {test['name']}")
    print(f"URL: {test['url']}")
    print(f"超时设置: {test['timeout']}秒")
    print('='*80)
    
    try:
        start = time.time()
        response = requests.get(test['url'], timeout=test['timeout'])
        elapsed = time.time() - start
        
        result = {
            "name": test['name'],
            "success": True,
            "status_code": response.status_code,
            "response_time": elapsed,
            "size": len(response.content)
        }
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"响应大小: {len(response.content)} 字节")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # 如果是图谱API，显示节点和关系数
                if '/kg/graph' in test['url']:
                    nodes = len(data.get('data', {}).get('sampleNodes', []))
                    rels = len(data.get('data', {}).get('sampleRelations', []))
                    result['nodes'] = nodes
                    result['relations'] = rels
                    print(f"节点数: {nodes}")
                    print(f"关系数: {rels}")
                
                # 如果是统计API，显示统计信息
                elif '/stats' in test['url']:
                    stats = data.get('data', {}).get('stats', {}) or data.get('stats', {})
                    if stats:
                        print(f"统计信息:")
                        for key, value in stats.items():
                            if isinstance(value, dict):
                                print(f"  {key}: {len(value)} 项")
                            else:
                                print(f"  {key}: {value}")
                
                print(f"✓ 测试成功")
            except Exception as e:
                print(f"⚠ JSON解析失败: {e}")
                result['parse_error'] = str(e)
        else:
            print(f"✗ 请求失败")
            result['success'] = False
        
        results.append(result)
        
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        print(f"✗ 超时 - 已等待 {elapsed:.2f}秒")
        results.append({
            "name": test['name'],
            "success": False,
            "error": "timeout",
            "response_time": elapsed
        })
    except Exception as e:
        print(f"✗ 错误: {e}")
        results.append({
            "name": test['name'],
            "success": False,
            "error": str(e)
        })

# 总结
print(f"\n{'='*80}")
print("测试总结")
print('='*80)

success_count = sum(1 for r in results if r.get('success', False))
total_count = len(results)

print(f"\n总计: {total_count} 项测试")
print(f"成功: {success_count} 项")
print(f"失败: {total_count - success_count} 项")

print("\n详细结果:")
for r in results:
    status = "✓" if r.get('success', False) else "✗"
    name = r['name']
    if r.get('success', False):
        time_str = f"{r['response_time']:.2f}秒"
        if 'nodes' in r:
            print(f"  {status} {name}: {time_str}, {r['nodes']} 节点, {r['relations']} 关系")
        else:
            print(f"  {status} {name}: {time_str}")
    else:
        error = r.get('error', '未知错误')
        print(f"  {status} {name}: {error}")

print(f"\n{'='*80}")
print("修复效果评估")
print('='*80)

if success_count == total_count:
    print("\n✓ 所有测试通过！修复成功！")
    print("\n前端超时问题已解决:")
    print("  - 前端axios超时: 10秒 → 60秒")
    print("  - 后端缓存逻辑已修复")
    print("\n现在可以正常使用图谱可视化功能了！")
elif success_count > 0:
    print(f"\n⚠ 部分测试通过 ({success_count}/{total_count})")
    print("\n建议:")
    print("  1. 检查失败的API端点")
    print("  2. 查看服务器日志")
    print("  3. 确认Neo4j服务是否正常运行")
else:
    print("\n✗ 所有测试失败")
    print("\n可能的原因:")
    print("  1. 服务未正确重启")
    print("  2. Neo4j数据库未运行")
    print("  3. 网络连接问题")

print(f"\n{'='*80}")

