#!/usr/bin/env python3
"""
图谱优化主脚本
整合所有优化步骤
"""
import json
import subprocess
import sys

print("=" * 80)
print("🚀 知识图谱优化执行")
print("=" * 80)

# 步骤1: 修复数据质量
print("\n" + "=" * 80)
print("步骤1: 修复数据质量问题")
print("=" * 80)

try:
    result = subprocess.run([sys.executable, 'fix_data_quality.py'], 
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ 错误: {e}")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

# 步骤2: 同步到Neo4j
print("\n" + "=" * 80)
print("步骤2: 同步词典到Neo4j")
print("=" * 80)

try:
    result = subprocess.run([sys.executable, 'sync_to_neo4j.py'],
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ 错误: {e}")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

# 步骤3: 建立语义关系
print("\n" + "=" * 80)
print("步骤3: 发现语义关系")
print("=" * 80)

try:
    result = subprocess.run([sys.executable, 'build_semantic_relationships.py'],
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ 错误: {e}")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

# 步骤4: 导入语义关系到Neo4j
print("\n" + "=" * 80)
print("步骤4: 导入语义关系到Neo4j")
print("=" * 80)

try:
    result = subprocess.run([sys.executable, 'import_relationships_to_neo4j.py'],
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ 错误: {e}")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

# 步骤5: 生成优化报告
print("\n" + "=" * 80)
print("步骤5: 生成优化报告")
print("=" * 80)

try:
    result = subprocess.run([sys.executable, 'comprehensive_analysis.py'],
                          capture_output=True, text=True, check=True)
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"❌ 错误: {e}")
    print(e.stdout)
    print(e.stderr)
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ 图谱优化完成！")
print("=" * 80)

print("\n📊 优化总结:")
print("  ✅ 数据质量问题已修复")
print("  ✅ 词典已同步到Neo4j")
print("  ✅ 语义关系已建立")
print("  ✅ 优化报告已生成")

print("\n📁 生成的文件:")
print("  - semantic_relationships.json (语义关系数据)")
print("  - dictionary_backup_before_fix.json (备份文件)")

print("\n🎯 下一步:")
print("  1. 查看优化报告")
print("  2. 部署到服务器: ssh root@47.108.152.16")
print("  3. 验证图谱效果")

