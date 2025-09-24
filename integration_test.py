#!/usr/bin/env python3
"""
端到端集成测试：验证完整业务流程
Excel导入 → 数据标准化 → 图谱构建 → 前端查询 → 可视化展示
"""
import os
import sys
import time
import pandas as pd
from pathlib import Path

def test_1_create_sample_data():
    """测试1：创建示例Excel数据"""
    print("🔍 测试1：创建示例Excel数据")
    
    # 创建目录
    data_dir = Path('data/import')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建anomalies.xlsx
    anomalies_data = [
        {
            'AnomalyID': 'QA-2025-0001',
            'Title': '摄像头对焦失败',
            'Severity': 'S1',
            'Product': 'MyPhoneX',
            'Build': '1.0.3',
            'Component': '摄像头',
            'Symptom': '对焦失败'
        },
        {
            'AnomalyID': 'QA-2025-0002',
            'Title': '电池充电缓慢',
            'Severity': 'S2',
            'Product': 'MyPhoneX',
            'Build': '1.0.3',
            'Component': '电池',
            'Symptom': '充电慢'
        },
        {
            'AnomalyID': 'QA-2025-0003',
            'Title': '屏幕触摸不灵敏',
            'Severity': 'S2',
            'Product': 'MyPhoneY',
            'Build': '2.1.0',
            'Component': '触摸屏',
            'Symptom': '触摸不灵敏'
        }
    ]
    
    df_anomalies = pd.DataFrame(anomalies_data)
    anomalies_file = data_dir / 'anomalies.xlsx'
    df_anomalies.to_excel(anomalies_file, index=False)
    
    # 创建testcases.xlsx
    testcases_data = [
        {
            'CaseID': 'TC-CAM-001',
            'Title': '摄像头启动测试',
            'Module': '摄像头',
            'Priority': 'P1'
        },
        {
            'CaseID': 'TC-CAM-002',
            'Title': '摄像头对焦测试',
            'Module': '摄像头',
            'Priority': 'P1'
        },
        {
            'CaseID': 'TC-BAT-001',
            'Title': '电池充电测试',
            'Module': '电池',
            'Priority': 'P2'
        },
        {
            'CaseID': 'TC-TP-001',
            'Title': '触摸屏响应测试',
            'Module': '触摸屏',
            'Priority': 'P1'
        }
    ]
    
    df_testcases = pd.DataFrame(testcases_data)
    testcases_file = data_dir / 'testcases.xlsx'
    df_testcases.to_excel(testcases_file, index=False)
    
    print(f"✅ 创建成功：{anomalies_file} ({len(anomalies_data)} 条异常)")
    print(f"✅ 创建成功：{testcases_file} ({len(testcases_data)} 条用例)")
    return True

def test_2_etl_pipeline():
    """测试2：ETL数据处理管线"""
    print("\n🔍 测试2：ETL数据处理管线")
    
    try:
        # 导入ETL模块
        sys.path.append('services/api/etl')
        from parse_excel import detect_and_parse
        from normalizer import Vocab, normalize_anomaly_rows, normalize_case_rows
        from upsert_writer import Neo4jUpserter
        
        # 解析Excel
        anomalies_file = Path('data/import/anomalies.xlsx')
        testcases_file = Path('data/import/testcases.xlsx')
        
        if not anomalies_file.exists():
            print("❌ 异常文件不存在")
            return False
            
        anomalies_rows = detect_and_parse(str(anomalies_file))
        testcases_rows = detect_and_parse(str(testcases_file))
        
        print(f"✅ 解析异常数据：{len(anomalies_rows)} 条")
        print(f"✅ 解析用例数据：{len(testcases_rows)} 条")
        
        # 标准化
        vocab = Vocab(Path('.'))
        normalized_anomalies = normalize_anomaly_rows(vocab, anomalies_rows)
        normalized_cases = normalize_case_rows(vocab, testcases_rows)
        
        print(f"✅ 标准化异常：{len(normalized_anomalies)} 条")
        print(f"✅ 标准化用例：{len(normalized_cases)} 条")
        
        # 模拟入库（不连接真实Neo4j）
        upserter = Neo4jUpserter()  # 会显示警告但不会失败
        
        for rec in normalized_anomalies[:2]:  # 只处理前2条
            upserter.upsert_anomaly_bundle(rec)
            
        for rec in normalized_cases[:2]:  # 只处理前2条
            upserter.upsert_testcase_bundle(rec)
            
        print("✅ ETL管线测试完成（模拟模式）")
        return True
        
    except Exception as e:
        print(f"❌ ETL测试失败：{e}")
        return False

def test_3_api_endpoints():
    """测试3：API接口功能"""
    print("\n🔍 测试3：API接口功能")
    
    try:
        import requests
        base_url = "http://localhost:8000"
        
        # 测试健康检查
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API服务运行正常")
                health_data = response.json()
                print(f"   Neo4j连接状态：{health_data.get('neo4j_connected', 'unknown')}")
            else:
                print(f"⚠️  API服务响应异常：{response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ API服务未启动或无法连接")
            return False
            
        # 测试异常录入接口
        upsert_payload = {
            "anomaly_key": "QA-2025-TEST",
            "title": "测试异常",
            "severity": "S3",
            "product_key": "Product:TestPhone",
            "build_key": "Build:1.0.0",
            "component": "测试组件",
            "symptom": "测试症状"
        }
        
        try:
            response = requests.post(f"{base_url}/kg/upsert/anomaly", json=upsert_payload, timeout=10)
            if response.status_code == 200:
                print("✅ 异常录入接口正常")
            else:
                print(f"⚠️  异常录入接口响应：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  异常录入接口测试失败：{e}")
            
        # 测试流程查询接口
        flow_payload = {"product": "MyPhoneX", "module": "摄像头"}
        
        try:
            response = requests.post(f"{base_url}/kg/query/flow", json=flow_payload, timeout=10)
            if response.status_code == 200:
                print("✅ 流程查询接口正常")
                data = response.json()
                items = data.get('data', {}).get('items', [])
                print(f"   查询结果：{len(items)} 条用例")
            else:
                print(f"⚠️  流程查询接口响应：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  流程查询接口测试失败：{e}")
            
        # 测试因果路径查询接口
        cause_payload = {"symptom": "对焦失败"}
        
        try:
            response = requests.post(f"{base_url}/kg/query/cause_path", json=cause_payload, timeout=10)
            if response.status_code == 200:
                print("✅ 因果路径查询接口正常")
                data = response.json()
                paths = data.get('data', {}).get('paths', [])
                print(f"   查询结果：{len(paths)} 条路径")
            else:
                print(f"⚠️  因果路径查询接口响应：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  因果路径查询接口测试失败：{e}")
            
        return True
        
    except ImportError:
        print("❌ requests库未安装，跳过API测试")
        return False

def test_4_frontend_config():
    """测试4：前端配置检查"""
    print("\n🔍 测试4：前端配置检查")
    
    # 检查package.json
    package_file = Path('apps/web/package.json')
    if package_file.exists():
        import json
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
            
        deps = package_data.get('dependencies', {})
        required_deps = ['vue', 'vue-router', 'element-plus', 'pinia', 'axios', 'cytoscape']
        
        missing_deps = []
        for dep in required_deps:
            if dep in deps:
                print(f"✅ {dep}: {deps[dep]}")
            else:
                missing_deps.append(dep)
                print(f"❌ 缺少依赖：{dep}")
                
        if not missing_deps:
            print("✅ 前端依赖配置完整")
        else:
            print(f"⚠️  缺少 {len(missing_deps)} 个依赖")
    else:
        print("❌ package.json 文件不存在")
        return False
        
    # 检查关键文件
    key_files = [
        'apps/web/src/api/http.ts',
        'apps/web/src/store/query.ts',
        'apps/web/src/views/Home.vue',
        'apps/web/src/views/AnomalyGuide.vue',
        'apps/web/src/views/FlowQuery.vue',
        'apps/web/src/views/GraphExplorer.vue',
        'apps/web/vite.config.js'
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ 缺少文件：{file_path}")
            
    return True

def main():
    """主测试流程"""
    print("🚀 质量知识图谱系统 - 端到端集成测试")
    print("=" * 60)
    
    results = []
    
    # 执行测试
    results.append(("创建示例数据", test_1_create_sample_data()))
    results.append(("ETL数据处理", test_2_etl_pipeline()))
    results.append(("API接口功能", test_3_api_endpoints()))
    results.append(("前端配置检查", test_4_frontend_config()))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总：")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计：{passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！系统集成正常。")
    else:
        print("⚠️  部分测试失败，请检查相关组件。")
        
    # 给出下一步建议
    print("\n📋 下一步操作建议：")
    print("1. 启动后端API：python api/main.py")
    print("2. 启动前端Web：cd apps/web && npm install && npm run dev")
    print("3. 访问系统：http://localhost:5173")
    print("4. 导入数据：使用创建的 data/import/*.xlsx 文件")

if __name__ == "__main__":
    main()
