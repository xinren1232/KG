#!/usr/bin/env python3
"""全面诊断服务器状态"""

import subprocess
import json
import time
import requests

SERVER = "root@47.108.152.16"
PASSWORD = "Zxylsy.99"

def ssh_exec(command, show_output=True):
    """执行SSH命令"""
    # 使用sshpass来自动输入密码
    full_cmd = f'sshpass -p "{PASSWORD}" ssh -o StrictHostKeyChecking=no {SERVER} "{command}"'
    print(f"\n执行: {command[:80]}...")
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=False)
        stdout = result.stdout.decode('utf-8', errors='ignore') if result.stdout else ""
        stderr = result.stderr.decode('utf-8', errors='ignore') if result.stderr else ""

        if show_output and stdout:
            print(stdout)
        if stderr and "Warning" not in stderr and "Pseudo-terminal" not in stderr:
            print(f"错误: {stderr}")
        return result.returncode == 0, stdout, stderr
    except Exception as e:
        print(f"执行命令出错: {e}")
        return False, "", str(e)

def main():
    print("="*80)
    print("服务器全面诊断")
    print("="*80)
    
    # 1. 测试服务器连接
    print("\n" + "="*80)
    print("1. 测试服务器连接")
    print("="*80)
    success, output, error = ssh_exec("echo '连接成功'")
    if not success:
        print("✗ 无法连接到服务器")
        print("请检查:")
        print("  1. 服务器IP是否正确")
        print("  2. SSH端口是否开放")
        print("  3. 密码是否正确")
        print(f"\n错误信息: {error}")
        return False
    print("✓ 服务器连接正常")
    
    # 2. 查找项目目录
    print("\n" + "="*80)
    print("2. 查找项目目录")
    print("="*80)
    
    project_dir = None
    for path in ["/opt/kg", "/root/kg", "/home/kg", "~/kg"]:
        success, output, _ = ssh_exec(f"[ -d {path} ] && echo 'EXISTS' || echo 'NOT_FOUND'", show_output=False)
        if "EXISTS" in output:
            project_dir = path
            print(f"✓ 找到项目目录: {project_dir}")
            break
    
    if not project_dir:
        print("✗ 未找到项目目录")
        success, output, _ = ssh_exec("find / -maxdepth 3 -name 'docker-compose.prod.yml' 2>/dev/null | head -5")
        print("可能的项目位置:")
        print(output)
        return False
    
    # 3. 检查项目文件结构
    print("\n" + "="*80)
    print("3. 检查项目文件结构")
    print("="*80)
    
    ssh_exec(f"ls -lh {project_dir}/ | head -20")
    
    # 4. 检查关键文件
    print("\n" + "="*80)
    print("4. 检查关键文件")
    print("="*80)
    
    files_to_check = {
        "前端API配置": f"{project_dir}/apps/web/src/api/index.js",
        "后端API": f"{project_dir}/api/main.py",
        "Docker配置": f"{project_dir}/docker-compose.prod.yml",
        "Nginx配置": f"{project_dir}/nginx/nginx.conf"
    }
    
    file_status = {}
    for name, path in files_to_check.items():
        success, output, _ = ssh_exec(f"[ -f {path} ] && echo 'EXISTS' || echo 'NOT_FOUND'", show_output=False)
        exists = "EXISTS" in output
        file_status[name] = {"path": path, "exists": exists}
        status = "✓" if exists else "✗"
        print(f"{status} {name}: {path}")
    
    # 5. 检查前端超时配置
    print("\n" + "="*80)
    print("5. 检查前端超时配置")
    print("="*80)
    
    if file_status["前端API配置"]["exists"]:
        frontend_file = file_status["前端API配置"]["path"]
        success, output, _ = ssh_exec(f"grep -n 'timeout:' {frontend_file} | head -5")
        
        if "timeout: 10000" in output:
            print("⚠ 发现问题: 前端超时设置为10秒（太短）")
            print("  建议: 改为60秒")
        elif "timeout: 60000" in output:
            print("✓ 前端超时配置正确（60秒）")
        else:
            print("? 前端超时配置未知")
    
    # 6. 检查后端缓存逻辑
    print("\n" + "="*80)
    print("6. 检查后端缓存逻辑")
    print("="*80)
    
    if file_status["后端API"]["exists"]:
        backend_file = file_status["后端API"]["path"]
        # 检查是否有缓存逻辑bug
        success, output, _ = ssh_exec(f"grep -A 20 'def get_graph_visualization_data' {backend_file} | grep -n 'return\\|result\\|缓存' | head -30")
        print("后端缓存相关代码:")
        print(output)
    
    # 7. 检查Docker服务状态
    print("\n" + "="*80)
    print("7. 检查Docker服务状态")
    print("="*80)
    
    ssh_exec(f"cd {project_dir} && docker-compose -f docker-compose.prod.yml ps")
    
    # 8. 检查容器日志
    print("\n" + "="*80)
    print("8. 检查容器日志（最近的错误）")
    print("="*80)
    
    print("\nAPI服务日志:")
    ssh_exec(f"cd {project_dir} && docker-compose -f docker-compose.prod.yml logs api --tail=30 | grep -i 'error\\|timeout\\|exception' || echo '无错误日志'")
    
    print("\n前端服务日志:")
    ssh_exec(f"cd {project_dir} && docker-compose -f docker-compose.prod.yml logs web --tail=30 | grep -i 'error\\|timeout\\|exception' || echo '无错误日志'")
    
    # 9. 测试API响应时间
    print("\n" + "="*80)
    print("9. 测试API响应时间")
    print("="*80)
    
    test_cases = [
        {"name": "健康检查", "url": "http://47.108.152.16/api/health"},
        {"name": "图谱统计", "url": "http://47.108.152.16/api/kg/stats"},
        {"name": "小数据量图谱", "url": "http://47.108.152.16/api/kg/graph?limit=100"},
        {"name": "中等数据量图谱", "url": "http://47.108.152.16/api/kg/graph?limit=500"},
    ]
    
    for test in test_cases:
        try:
            print(f"\n测试: {test['name']}")
            start = time.time()
            r = requests.get(test['url'], timeout=30)
            elapsed = time.time() - start
            
            if r.status_code == 200:
                size = len(r.content)
                print(f"  ✓ 成功 - 响应时间: {elapsed:.2f}秒, 大小: {size} 字节")
                
                # 如果是图谱API，显示节点数
                if '/kg/graph' in test['url']:
                    try:
                        data = r.json()
                        nodes = len(data.get('data', {}).get('sampleNodes', []))
                        rels = len(data.get('data', {}).get('sampleRelations', []))
                        print(f"    节点: {nodes}, 关系: {rels}")
                    except:
                        pass
            else:
                print(f"  ✗ 失败 - 状态码: {r.status_code}")
        except requests.exceptions.Timeout:
            elapsed = time.time() - start
            print(f"  ✗ 超时 - 已等待: {elapsed:.2f}秒")
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    # 10. 检查Neo4j连接
    print("\n" + "="*80)
    print("10. 检查Neo4j连接")
    print("="*80)
    
    ssh_exec(f"cd {project_dir} && docker-compose -f docker-compose.prod.yml exec -T neo4j cypher-shell -u neo4j -p neo4j123 'MATCH (n) RETURN count(n) as total LIMIT 1' 2>&1 || echo 'Neo4j连接失败'")
    
    # 11. 生成诊断报告
    print("\n" + "="*80)
    print("诊断报告总结")
    print("="*80)
    
    print(f"\n项目目录: {project_dir}")
    print("\n文件检查:")
    for name, info in file_status.items():
        status = "✓" if info["exists"] else "✗"
        print(f"  {status} {name}")
    
    print("\n发现的问题:")
    issues = []
    
    # 检查前端超时
    if file_status["前端API配置"]["exists"]:
        success, output, _ = ssh_exec(f"grep 'timeout: 10000' {file_status['前端API配置']['path']}", show_output=False)
        if success and output.strip():
            issues.append({
                "severity": "高",
                "type": "前端超时配置",
                "description": "前端axios超时设置为10秒，可能导致图谱查询超时",
                "solution": "将timeout从10000改为60000"
            })
    
    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"\n  问题 {i} [{issue['severity']}]:")
            print(f"    类型: {issue['type']}")
            print(f"    描述: {issue['description']}")
            print(f"    解决方案: {issue['solution']}")
    else:
        print("  未发现明显问题")
    
    print("\n" + "="*80)
    print("诊断完成")
    print("="*80)
    
    # 询问是否执行修复
    print("\n是否需要执行自动修复？")
    print("修复内容:")
    print("  1. 将前端超时从10秒改为60秒")
    print("  2. 修复后端缓存逻辑bug")
    print("  3. 重启相关服务")
    
    return True, project_dir, file_status

if __name__ == "__main__":
    try:
        result = main()
        if result and len(result) == 3:
            success, project_dir, file_status = result
            print("\n诊断信息已保存，可以继续执行修复")
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

