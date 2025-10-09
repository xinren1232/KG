#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署首页实时数据修复到服务器
"""

import paramiko
import os
import sys
from pathlib import Path

# 服务器配置
SERVER_HOST = "47.108.152.16"
SERVER_USER = "root"
SERVER_PASSWORD = "Zxylsy.99"
PROJECT_DIR = "/opt/knowledge-graph"

def upload_file(sftp, local_path, remote_path, description=""):
    """上传文件到服务器"""
    try:
        sftp.put(local_path, remote_path)
        print(f"✅ 上传成功: {description or local_path}")
        return True
    except Exception as e:
        print(f"❌ 上传失败: {description or local_path}")
        print(f"   错误: {str(e)}")
        return False

def execute_command(ssh, command, description=""):
    """执行SSH命令"""
    if description:
        print(f"\n{'='*80}")
        print(f"执行: {description}")
        print(f"{'='*80}")
    
    stdin, stdout, stderr = ssh.exec_command(command)
    
    # 实时输出
    for line in stdout:
        print(line.strip())
    
    # 输出错误信息
    error_output = stderr.read().decode('utf-8')
    if error_output:
        print(f"错误输出:\n{error_output}")
    
    return stdout.channel.recv_exit_status()

def main():
    """主函数"""
    print("=" * 80)
    print("开始部署首页实时数据修复到服务器")
    print("=" * 80)
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        print(f"\n连接服务器: {SERVER_HOST}")
        ssh.connect(
            hostname=SERVER_HOST,
            username=SERVER_USER,
            password=SERVER_PASSWORD,
            timeout=30
        )
        print("✅ 服务器连接成功")
        
        # 创建SFTP客户端
        sftp = ssh.open_sftp()
        
        # 上传修复后的Home.vue
        local_file = "apps/web/src/views/Home.vue"
        remote_file = f"{PROJECT_DIR}/apps/web/src/views/Home.vue"
        
        if not os.path.exists(local_file):
            print(f"❌ 本地文件不存在: {local_file}")
            return 1
        
        print(f"\n上传修复后的Home.vue...")
        if not upload_file(sftp, local_file, remote_file, "Home.vue"):
            return 1
        
        # 重新构建前端
        print("\n" + "=" * 80)
        print("重新构建前端")
        print("=" * 80)
        
        exit_code = execute_command(
            ssh,
            f"""cd {PROJECT_DIR}/apps/web && \
                npm run build && \
                echo '✅ 前端构建完成'""",
            "构建前端"
        )
        
        if exit_code != 0:
            print("\n❌ 前端构建失败")
            return exit_code
        
        # 重启前端服务
        print("\n" + "=" * 80)
        print("重启前端服务")
        print("=" * 80)
        
        execute_command(
            ssh,
            "systemctl restart kg-web",
            "重启前端服务"
        )
        
        # 检查服务状态
        print("\n" + "=" * 80)
        print("检查服务状态")
        print("=" * 80)
        
        execute_command(
            ssh,
            "systemctl status kg-web | head -15",
            "前端服务状态"
        )
        
        # 验证修复效果
        print("\n" + "=" * 80)
        print("验证修复效果")
        print("=" * 80)
        
        execute_command(
            ssh,
            f"""cd {PROJECT_DIR} && python3 -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'password123'))
with driver.session() as session:
    # 获取实时统计
    total_terms = session.run('MATCH (t:Term) RETURN count(t) AS count').single()['count']
    total_relations = session.run('MATCH ()-[r]->() RETURN count(r) AS count').single()['count']
    total_categories = session.run('MATCH (c:Category) RETURN count(c) AS count').single()['count']
    total_tags = session.run('MATCH (g:Tag) RETURN count(g) AS count').single()['count']
    
    print(f'✅ 词典条目: {{total_terms}}')
    print(f'✅ 关系数量: {{total_relations}}')
    print(f'✅ 分类数量: {{total_categories}}')
    print(f'✅ 标签数量: {{total_tags}}')
    
    # 验证因果关系
    causes_count = session.run('MATCH ()-[r:CAUSES]->() RETURN count(r) AS count').single()['count']
    print(f'✅ 因果关系: {{causes_count}}')
driver.close()
"
""",
            "验证Neo4j数据"
        )
        
        print("\n" + "=" * 80)
        print("✅ 部署完成！")
        print("=" * 80)
        print("\n请访问 http://47.108.152.16 查看首页数据是否实时更新")
        print("预期显示:")
        print("  - 词典条目: 1333+ (包含新增的因果关系节点)")
        print("  - 关系数量: 17461+ (包含49个新增的因果关系)")
        
        return 0
        
    except paramiko.AuthenticationException:
        print("❌ SSH认证失败，请检查用户名和密码")
        return 1
    except paramiko.SSHException as e:
        print(f"❌ SSH连接错误: {str(e)}")
        return 1
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        ssh.close()
        print("\n服务器连接已关闭")

if __name__ == "__main__":
    sys.exit(main())

