#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程检查阿里云服务器状态
"""

import urllib.request
import urllib.error
import json
import sys

SERVER_IP = "47.108.152.16"

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}{title}{Colors.NC}")
    print('='*70)

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.NC}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.NC}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.NC}")

def test_url(url, description):
    """测试URL访问"""
    try:
        print(f"\n测试: {description}")
        print(f"URL: {url}")
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        response = urllib.request.urlopen(req, timeout=10)
        status = response.status
        content = response.read().decode('utf-8')
        
        print(f"状态码: {status}")
        
        if status == 200:
            print_success(f"{description} - 访问成功")
            
            # 尝试解析JSON
            try:
                data = json.loads(content)
                print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
                return True, data
            except:
                # 不是JSON，显示HTML内容
                print(f"响应内容 (前500字符): {content[:500]}")
                return True, content
        else:
            print_warning(f"{description} - 状态码: {status}")
            return False, None
            
    except urllib.error.HTTPError as e:
        print_error(f"{description} - HTTP错误: {e.code} {e.reason}")
        try:
            error_content = e.read().decode('utf-8')
            print(f"错误详情: {error_content[:300]}")
        except:
            pass
        return False, None
        
    except urllib.error.URLError as e:
        print_error(f"{description} - URL错误: {e.reason}")
        return False, None
        
    except Exception as e:
        print_error(f"{description} - 异常: {str(e)}")
        return False, None

def main():
    print(f"""
{'='*70}
阿里云服务器状态检查
服务器IP: {SERVER_IP}
{'='*70}
    """)
    
    results = {}
    
    # 1. 测试主页
    print_section("1. 测试前端主页")
    success, data = test_url(f"http://{SERVER_IP}/", "前端主页")
    results['frontend'] = success
    
    # 2. 测试健康检查
    print_section("2. 测试健康检查端点")
    success, data = test_url(f"http://{SERVER_IP}/health", "健康检查")
    results['health'] = success
    
    # 3. 测试API根路径
    print_section("3. 测试API根路径")
    success, data = test_url(f"http://{SERVER_IP}/api/", "API根路径")
    results['api_root'] = success
    
    # 4. 测试/kg/real-stats
    print_section("4. 测试 /api/kg/real-stats")
    success, data = test_url(f"http://{SERVER_IP}/api/kg/real-stats", "真实统计数据")
    results['real_stats'] = success
    
    if success and data:
        print("\n详细数据:")
        if isinstance(data, dict):
            if 'data' in data and 'stats' in data['data']:
                stats = data['data']['stats']
                print(f"  总节点数: {stats.get('totalNodes', 'N/A')}")
                print(f"  总关系数: {stats.get('totalRelations', 'N/A')}")
                print(f"  总术语数: {stats.get('totalTerms', 'N/A')}")
                print(f"  总分类数: {stats.get('totalCategories', 'N/A')}")
    
    # 5. 测试其他API端点
    print_section("5. 测试其他API端点")
    
    endpoints = [
        ("/api/kg/stats", "图谱统计"),
        ("/api/kg/dictionary", "词典数据"),
        ("/api/kg/dictionary/categories", "词典分类"),
    ]
    
    for endpoint, desc in endpoints:
        success, data = test_url(f"http://{SERVER_IP}{endpoint}", desc)
        results[endpoint] = success
    
    # 6. 总结
    print_section("检查结果总结")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"\n总计: {total} 项检查")
    print_success(f"通过: {passed} 项")
    if failed > 0:
        print_error(f"失败: {failed} 项")
    
    print("\n详细结果:")
    for key, value in results.items():
        status = "✓ 通过" if value else "✗ 失败"
        color = Colors.GREEN if value else Colors.RED
        print(f"  {color}{status}{Colors.NC} - {key}")
    
    # 7. 问题诊断和建议
    print_section("问题诊断和修复建议")
    
    if not results.get('frontend'):
        print_error("前端无法访问")
        print("可能原因:")
        print("  1. Nginx容器未运行")
        print("  2. dist目录不存在或为空")
        print("  3. nginx配置错误")
        print("\n修复建议:")
        print("  ssh root@47.108.152.16")
        print("  cd /opt/kg")
        print("  docker-compose -f docker-compose.prod.yml ps")
        print("  docker-compose -f docker-compose.prod.yml logs nginx")
    
    if not results.get('api_root'):
        print_error("\nAPI服务无法访问")
        print("可能原因:")
        print("  1. API容器未运行")
        print("  2. API服务启动失败")
        print("  3. Nginx反向代理配置错误")
        print("\n修复建议:")
        print("  ssh root@47.108.152.16")
        print("  cd /opt/kg")
        print("  docker-compose -f docker-compose.prod.yml restart api")
        print("  docker-compose -f docker-compose.prod.yml logs api")
    
    if not results.get('real_stats'):
        print_error("\n/kg/real-stats端点失败")
        print("可能原因:")
        print("  1. API服务内部错误")
        print("  2. Redis连接失败")
        print("  3. Neo4j连接失败")
        print("  4. 配置文件缺失")
        print("\n修复建议:")
        print("  # 检查API日志")
        print("  ssh root@47.108.152.16")
        print("  cd /opt/kg")
        print("  docker-compose -f docker-compose.prod.yml logs api --tail=100")
        print("")
        print("  # 重启相关服务")
        print("  docker-compose -f docker-compose.prod.yml restart redis")
        print("  docker-compose -f docker-compose.prod.yml restart api")
        print("")
        print("  # 检查配置文件")
        print("  docker exec kg_api_prod ls -la /app/config/")
        print("  docker exec kg_api_prod cat /app/config/frontend_real_data.json")
    
    if results.get('frontend') and not results.get('api_root'):
        print_warning("\n前端可访问但API不可访问")
        print("这是典型的502 Bad Gateway错误")
        print("说明Nginx正常，但无法连接到后端API服务")
        print("\n立即修复:")
        print("  ssh root@47.108.152.16 'cd /opt/kg && docker-compose -f docker-compose.prod.yml restart api'")
    
    # 8. 快速修复命令
    print_section("快速修复命令")
    print("""
# 方案1: 重启API服务
ssh root@47.108.152.16 << 'EOF'
cd /opt/kg
docker-compose -f docker-compose.prod.yml restart redis
docker-compose -f docker-compose.prod.yml restart api
docker-compose -f docker-compose.prod.yml ps
EOF

# 方案2: 查看详细日志
ssh root@47.108.152.16 << 'EOF'
cd /opt/kg
docker-compose -f docker-compose.prod.yml logs api --tail=100
EOF

# 方案3: 完全重启所有服务
ssh root@47.108.152.16 << 'EOF'
cd /opt/kg
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml logs -f
EOF
    """)
    
    print(f"\n{'='*70}")
    print(f"{Colors.GREEN}检查完成{Colors.NC}")
    print('='*70)
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n检查已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}检查过程出错: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

