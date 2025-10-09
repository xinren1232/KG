#!/usr/bin/env python3
"""
立即可执行的优化脚本
在服务器上执行以下优化：
1. 创建Neo4j索引
2. 测试缓存效果
3. 性能基准测试
4. 生成优化报告
"""

import paramiko
import time
import json
from datetime import datetime

class ImmediateOptimizer:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.ssh = None
        self.results = {}
    
    def connect(self):
        """连接服务器"""
        print(f"🔌 连接服务器 {self.host}...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.host, username=self.username, password=self.password)
        print("✅ 连接成功")
    
    def execute_command(self, command, description=""):
        """执行命令"""
        if description:
            print(f"\n📝 {description}")
        print(f"   命令: {command[:100]}...")
        
        stdin, stdout, stderr = self.ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error and "warning" not in error.lower():
            print(f"   ⚠️ 错误: {error[:200]}")
        
        return output, error
    
    def create_neo4j_indexes(self):
        """创建Neo4j索引"""
        print("\n" + "="*80)
        print("📊 步骤1: 创建Neo4j索引")
        print("="*80)
        
        # 创建索引脚本
        index_script = """
cat > /tmp/create_indexes.cypher << 'EOF'
// 术语索引
CREATE INDEX term_name_idx IF NOT EXISTS FOR (n:Term) ON (n.name);
CREATE INDEX term_category_idx IF NOT EXISTS FOR (n:Term) ON (n.category);

// 标签索引
CREATE INDEX tag_name_idx IF NOT EXISTS FOR (n:Tag) ON (n.name);

// 分类索引
CREATE INDEX category_name_idx IF NOT EXISTS FOR (n:Category) ON (n.name);

// 别名索引
CREATE INDEX alias_name_idx IF NOT EXISTS FOR (n:Alias) ON (n.name);

// 组件索引
CREATE INDEX component_name_idx IF NOT EXISTS FOR (n:Component) ON (n.name);

// 症状索引
CREATE INDEX symptom_name_idx IF NOT EXISTS FOR (n:Symptom) ON (n.name);

// 全文搜索索引
CREATE FULLTEXT INDEX term_fulltext_idx IF NOT EXISTS 
FOR (n:Term) ON EACH [n.name, n.description];

// 显示所有索引
SHOW INDEXES;
EOF

# 执行索引创建
docker exec kg_neo4j cypher-shell -u neo4j -p password123 < /tmp/create_indexes.cypher 2>&1 || \
cypher-shell -u neo4j -p password123 < /tmp/create_indexes.cypher 2>&1
"""
        
        output, error = self.execute_command(index_script, "创建Neo4j索引")
        
        if "term_name_idx" in output or "already exists" in output.lower():
            print("✅ 索引创建成功")
            self.results['neo4j_indexes'] = "成功"
        else:
            print("⚠️ 索引创建可能失败，请手动检查")
            self.results['neo4j_indexes'] = "需要检查"
        
        return output
    
    def test_cache_performance(self):
        """测试缓存性能"""
        print("\n" + "="*80)
        print("🚀 步骤2: 测试缓存性能")
        print("="*80)
        
        test_script = """
python3 << 'EOF'
import requests
import time
import json

def test_endpoint(url, name):
    # 第一次请求 (缓存未命中)
    start = time.time()
    try:
        r1 = requests.get(url, timeout=30)
        time1 = time.time() - start
        
        # 等待1秒
        time.sleep(1)
        
        # 第二次请求 (缓存命中)
        start = time.time()
        r2 = requests.get(url, timeout=30)
        time2 = time.time() - start
        
        improvement = ((time1 - time2) / time1 * 100) if time1 > 0 else 0
        
        return {
            "name": name,
            "first_request": round(time1, 3),
            "cached_request": round(time2, 3),
            "improvement": round(improvement, 1),
            "status": "✅" if improvement > 20 else "⚠️"
        }
    except Exception as e:
        return {
            "name": name,
            "error": str(e),
            "status": "❌"
        }

# 测试多个端点
endpoints = [
    ("http://localhost:8000/health", "健康检查"),
    ("http://localhost:8000/kg/stats", "统计数据"),
    ("http://localhost:8000/kg/graph?limit=100", "图谱数据(小)"),
]

print("\\n缓存性能测试结果:")
print("-" * 80)

results = []
for url, name in endpoints:
    result = test_endpoint(url, name)
    results.append(result)
    
    if "error" in result:
        print(f"{result['status']} {name}: 错误 - {result['error']}")
    else:
        print(f"{result['status']} {name}:")
        print(f"   首次请求: {result['first_request']}s")
        print(f"   缓存请求: {result['cached_request']}s")
        print(f"   性能提升: {result['improvement']}%")

print("\\n" + json.dumps(results, indent=2, ensure_ascii=False))
EOF
"""
        
        output, error = self.execute_command(test_script, "测试缓存性能")
        print(output)
        
        # 解析结果
        try:
            if "✅" in output:
                self.results['cache_test'] = "缓存工作正常"
            else:
                self.results['cache_test'] = "缓存可能未启用"
        except:
            self.results['cache_test'] = "测试失败"
        
        return output
    
    def benchmark_api_performance(self):
        """API性能基准测试"""
        print("\n" + "="*80)
        print("📈 步骤3: API性能基准测试")
        print("="*80)
        
        benchmark_script = """
python3 << 'EOF'
import requests
import time
import statistics

def benchmark_endpoint(url, name, iterations=5):
    times = []
    success_count = 0
    
    for i in range(iterations):
        try:
            start = time.time()
            r = requests.get(url, timeout=30)
            duration = time.time() - start
            
            if r.status_code == 200:
                success_count += 1
                times.append(duration)
        except Exception as e:
            print(f"   请求失败: {e}")
    
    if times:
        return {
            "name": name,
            "avg": round(statistics.mean(times), 3),
            "min": round(min(times), 3),
            "max": round(max(times), 3),
            "success_rate": round(success_count / iterations * 100, 1)
        }
    else:
        return {"name": name, "error": "所有请求失败"}

endpoints = [
    ("http://localhost:8000/health", "健康检查"),
    ("http://localhost:8000/kg/stats", "统计数据"),
    ("http://localhost:8000/kg/graph?limit=100", "图谱(100节点)"),
    ("http://localhost:8000/kg/graph?limit=500", "图谱(500节点)"),
    ("http://localhost:8000/kg/dictionary", "词典数据"),
]

print("\\nAPI性能基准测试 (5次请求平均):")
print("-" * 80)

for url, name in endpoints:
    result = benchmark_endpoint(url, name)
    
    if "error" in result:
        print(f"❌ {name}: {result['error']}")
    else:
        status = "✅" if result['avg'] < 2.0 else "⚠️" if result['avg'] < 5.0 else "❌"
        print(f"{status} {name}:")
        print(f"   平均: {result['avg']}s | 最小: {result['min']}s | 最大: {result['max']}s | 成功率: {result['success_rate']}%")
EOF
"""
        
        output, error = self.execute_command(benchmark_script, "执行性能基准测试")
        print(output)
        
        # 解析结果
        if "✅" in output:
            self.results['performance'] = "性能良好"
        elif "⚠️" in output:
            self.results['performance'] = "性能一般，需要优化"
        else:
            self.results['performance'] = "性能较差，急需优化"
        
        return output
    
    def check_redis_status(self):
        """检查Redis状态"""
        print("\n" + "="*80)
        print("🔍 步骤4: 检查Redis缓存状态")
        print("="*80)
        
        redis_script = """
python3 << 'EOF'
import subprocess
import json

# 检查Redis是否运行
try:
    # 尝试Docker方式
    result = subprocess.run(
        ["docker", "exec", "kg_redis", "redis-cli", "INFO", "stats"],
        capture_output=True, text=True, timeout=5
    )
    
    if result.returncode != 0:
        # 尝试直接连接
        result = subprocess.run(
            ["redis-cli", "INFO", "stats"],
            capture_output=True, text=True, timeout=5
        )
    
    output = result.stdout
    
    if "keyspace_hits" in output:
        print("✅ Redis运行正常")
        print("\\nRedis统计信息:")
        for line in output.split("\\n"):
            if "keyspace" in line.lower() or "connected" in line.lower():
                print(f"   {line}")
    else:
        print("⚠️ Redis可能未运行")
        
except Exception as e:
    print(f"❌ Redis检查失败: {e}")
    print("\\n建议: 启动Redis服务以启用缓存功能")
EOF
"""
        
        output, error = self.execute_command(redis_script, "检查Redis状态")
        print(output)
        
        if "✅" in output:
            self.results['redis'] = "运行正常"
        else:
            self.results['redis'] = "未运行或未配置"
        
        return output
    
    def analyze_system_resources(self):
        """分析系统资源"""
        print("\n" + "="*80)
        print("💻 步骤5: 系统资源分析")
        print("="*80)
        
        resource_script = """
python3 << 'EOF'
import psutil
import json

# CPU
cpu_percent = psutil.cpu_percent(interval=1)
cpu_count = psutil.cpu_count()

# 内存
mem = psutil.virtual_memory()
mem_total_gb = mem.total / (1024**3)
mem_used_gb = mem.used / (1024**3)
mem_percent = mem.percent

# 磁盘
disk = psutil.disk_usage('/')
disk_total_gb = disk.total / (1024**3)
disk_used_gb = disk.used / (1024**3)
disk_percent = disk.percent

print("\\n系统资源使用情况:")
print("-" * 80)
print(f"CPU:")
print(f"   核心数: {cpu_count}")
print(f"   使用率: {cpu_percent}%")
print(f"   状态: {'✅ 正常' if cpu_percent < 70 else '⚠️ 偏高' if cpu_percent < 90 else '❌ 过高'}")

print(f"\\n内存:")
print(f"   总量: {mem_total_gb:.1f} GB")
print(f"   已用: {mem_used_gb:.1f} GB")
print(f"   使用率: {mem_percent:.1f}%")
print(f"   状态: {'✅ 正常' if mem_percent < 70 else '⚠️ 偏高' if mem_percent < 90 else '❌ 过高'}")

print(f"\\n磁盘:")
print(f"   总量: {disk_total_gb:.1f} GB")
print(f"   已用: {disk_used_gb:.1f} GB")
print(f"   使用率: {disk_percent:.1f}%")
print(f"   状态: {'✅ 正常' if disk_percent < 70 else '⚠️ 偏高' if disk_percent < 90 else '❌ 过高'}")

# 优化建议
print("\\n💡 优化建议:")
if mem_percent > 70:
    print("   - 内存使用偏高，建议增加Redis缓存以减少数据库查询")
if cpu_percent > 50:
    print("   - CPU使用偏高，建议优化查询和添加缓存")
if disk_percent > 70:
    print("   - 磁盘使用偏高，建议清理日志和临时文件")
if mem_percent < 50 and cpu_percent < 30:
    print("   - 系统资源充足，可以考虑增加缓存大小和并发数")
EOF
"""
        
        output, error = self.execute_command(resource_script, "分析系统资源")
        print(output)
        
        return output
    
    def generate_optimization_report(self):
        """生成优化报告"""
        print("\n" + "="*80)
        print("📄 生成优化报告")
        print("="*80)
        
        report = f"""
# 立即优化执行报告

**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**服务器**: {self.host}

## 执行结果

### 1. Neo4j索引创建
状态: {self.results.get('neo4j_indexes', '未执行')}

### 2. Redis缓存
状态: {self.results.get('redis', '未检查')}

### 3. 缓存性能测试
状态: {self.results.get('cache_test', '未测试')}

### 4. API性能
状态: {self.results.get('performance', '未测试')}

## 下一步行动

### 立即执行 (今天)
1. 如果Redis未运行，启动Redis服务
2. 如果索引创建失败，手动创建索引
3. 重启API服务以应用优化

### 短期优化 (本周)
1. 在API代码中启用缓存装饰器
2. 优化慢查询
3. 添加API限流

### 中期优化 (本月)
1. 拆分API路由
2. 添加认证授权
3. 完善监控体系

## 性能目标

- API响应时间: <5秒 (P95)
- 缓存命中率: >80%
- 系统可用性: >99.5%

---

**报告生成**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 保存报告到服务器
        save_script = f"""
cat > /tmp/optimization_report.md << 'EOF'
{report}
EOF

echo "✅ 报告已保存到: /tmp/optimization_report.md"
cat /tmp/optimization_report.md
"""
        
        output, error = self.execute_command(save_script, "保存优化报告")
        
        return report
    
    def run_all_optimizations(self):
        """执行所有优化"""
        try:
            self.connect()
            
            # 1. 创建索引
            self.create_neo4j_indexes()
            
            # 2. 检查Redis
            self.check_redis_status()
            
            # 3. 测试缓存
            self.test_cache_performance()
            
            # 4. 性能基准测试
            self.benchmark_api_performance()
            
            # 5. 系统资源分析
            self.analyze_system_resources()
            
            # 6. 生成报告
            report = self.generate_optimization_report()
            
            print("\n" + "="*80)
            print("🎉 优化执行完成！")
            print("="*80)
            print("\n" + report)
            
            return report
            
        except Exception as e:
            print(f"\n❌ 优化执行失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.ssh:
                self.ssh.close()
                print("\n🔌 SSH连接已关闭")

def main():
    """主函数"""
    print("="*80)
    print("🚀 知识图谱系统 - 立即优化脚本")
    print("="*80)
    
    # 服务器信息
    host = "47.108.152.16"
    username = "root"
    password = "Zxylsy.99"
    
    optimizer = ImmediateOptimizer(host, username, password)
    optimizer.run_all_optimizations()

if __name__ == "__main__":
    main()

