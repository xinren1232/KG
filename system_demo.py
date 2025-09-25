#!/usr/bin/env python3
"""
知识图谱构建助手 - 系统演示脚本
展示当前系统的核心功能和API能力
"""

import requests
import json
import time
from pathlib import Path

class KnowledgeGraphDemo:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
        
    def print_step(self, step, description):
        print(f"\n📋 步骤 {step}: {description}")
        print("-" * 40)
        
    def test_health_check(self):
        """测试系统健康状态"""
        self.print_step(1, "系统健康检查")
        
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            data = response.json()
            
            print(f"✅ API服务状态: {response.status_code}")
            print(f"✅ 服务信息: {data}")
            return True
            
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            return False
    
    def test_dictionary_api(self):
        """测试词典管理功能"""
        self.print_step(2, "词典数据获取")
        
        try:
            response = self.session.get(f"{self.base_url}/kg/dictionary", timeout=10)
            data = response.json()
            
            if data.get('ok'):
                dictionary = data.get('data', {})
                print(f"✅ 词典API状态: {response.status_code}")
                print(f"✅ 组件词典: {len(dictionary.get('components', []))} 条目")
                print(f"✅ 症状词典: {len(dictionary.get('symptoms', []))} 条目")
                print(f"✅ 根因词典: {len(dictionary.get('causes', []))} 条目")
                
                # 显示部分词典内容
                components = dictionary.get('components', [])[:3]
                if components:
                    print(f"\n📚 组件词典示例:")
                    for comp in components:
                        print(f"   - {comp.get('name')}: {comp.get('description', 'N/A')}")
                        
                return True
            else:
                print(f"❌ 词典API返回错误: {data.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 词典API测试失败: {e}")
            return False
    
    def test_file_upload(self):
        """测试文件上传功能"""
        self.print_step(3, "文件上传测试")
        
        try:
            # 创建测试文件
            test_content = """产品,版本,组件,症状,描述
MyPhoneX,1.0.1,摄像头,对焦失败,无法正确对焦
MyPhoneX,1.0.1,屏幕,黑屏,开机后屏幕无显示
MyPhoneX,1.0.2,电池,发热异常,充电时设备过热"""
            
            files = {'file': ('test_data.csv', test_content, 'text/csv')}
            response = self.session.post(f"{self.base_url}/kg/upload", files=files, timeout=15)
            data = response.json()
            
            if data.get('success'):
                print(f"✅ 文件上传状态: {response.status_code}")
                print(f"✅ 文件ID: {data.get('file_id')}")
                print(f"✅ 文件名: {data.get('filename')}")
                print(f"✅ 文件大小: {data.get('size')} bytes")
                return data.get('file_id')
            else:
                print(f"❌ 文件上传失败: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"❌ 文件上传测试失败: {e}")
            return None
    
    def test_knowledge_extraction(self, file_id):
        """测试知识抽取功能"""
        self.print_step(4, "知识抽取测试")
        
        if not file_id:
            print("❌ 无有效文件ID，跳过知识抽取测试")
            return None
            
        try:
            payload = {
                "file_id": file_id,
                "extraction_type": "auto"
            }
            
            response = self.session.post(
                f"{self.base_url}/kg/extract", 
                json=payload, 
                timeout=20
            )
            data = response.json()
            
            if data.get('success'):
                print(f"✅ 知识抽取状态: {response.status_code}")
                
                entities = data.get('entities', [])
                relations = data.get('relations', [])
                metadata = data.get('metadata', {})
                
                print(f"✅ 提取实体数量: {len(entities)}")
                print(f"✅ 提取关系数量: {len(relations)}")
                print(f"✅ 抽取类型: {metadata.get('extraction_type', 'N/A')}")
                
                # 显示部分实体
                if entities:
                    print(f"\n🔍 实体示例:")
                    for entity in entities[:3]:
                        print(f"   - {entity.get('name')} ({entity.get('type')})")
                
                # 显示部分关系
                if relations:
                    print(f"\n🔗 关系示例:")
                    for relation in relations[:3]:
                        print(f"   - {relation.get('source')} → {relation.get('target')} ({relation.get('type')})")
                
                return {"entities": entities, "relations": relations}
            else:
                print(f"❌ 知识抽取失败: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"❌ 知识抽取测试失败: {e}")
            return None
    
    def test_graph_building(self, knowledge_data):
        """测试图谱构建功能"""
        self.print_step(5, "图谱构建测试")
        
        if not knowledge_data:
            print("❌ 无知识数据，跳过图谱构建测试")
            return False
            
        try:
            payload = {
                "entities": knowledge_data.get('entities', []),
                "relations": knowledge_data.get('relations', []),
                "merge_strategy": "auto"
            }
            
            response = self.session.post(
                f"{self.base_url}/kg/build", 
                json=payload, 
                timeout=20
            )
            data = response.json()
            
            if data.get('success'):
                print(f"✅ 图谱构建状态: {response.status_code}")
                print(f"✅ 创建节点数: {data.get('nodes_created', 0)}")
                print(f"✅ 创建关系数: {data.get('relations_created', 0)}")
                print(f"✅ 构建时间: {data.get('build_time', 'N/A')}")
                return True
            else:
                print(f"❌ 图谱构建失败: {data.get('message')}")
                return False
                
        except Exception as e:
            print(f"❌ 图谱构建测试失败: {e}")
            return False
    
    def test_stats_api(self):
        """测试统计信息API"""
        self.print_step(6, "系统统计信息")
        
        try:
            response = self.session.get(f"{self.base_url}/kg/stats", timeout=10)
            data = response.json()
            
            if data.get('ok'):
                stats = data.get('data', {})
                print(f"✅ 统计API状态: {response.status_code}")
                print(f"✅ 图谱节点数: {stats.get('total_nodes', 0)}")
                print(f"✅ 图谱关系数: {stats.get('total_relations', 0)}")
                print(f"✅ 词典条目数: {stats.get('dictionary_entries', 0)}")
                print(f"✅ 最后更新: {stats.get('last_updated', 'N/A')}")
                return True
            else:
                print(f"❌ 统计API返回错误: {data.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ 统计API测试失败: {e}")
            return False
    
    def run_full_demo(self):
        """运行完整的系统演示"""
        self.print_header("知识图谱构建助手 - 系统功能演示")
        
        print(f"🌐 API服务地址: {self.base_url}")
        print(f"⏰ 演示开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {}
        
        # 1. 健康检查
        results['health'] = self.test_health_check()
        
        # 2. 词典管理
        results['dictionary'] = self.test_dictionary_api()
        
        # 3. 文件上传
        file_id = self.test_file_upload()
        results['upload'] = file_id is not None
        
        # 4. 知识抽取
        knowledge_data = self.test_knowledge_extraction(file_id)
        results['extraction'] = knowledge_data is not None
        
        # 5. 图谱构建
        results['graph_building'] = self.test_graph_building(knowledge_data)
        
        # 6. 统计信息
        results['stats'] = self.test_stats_api()
        
        # 演示总结
        self.print_header("演示结果总结")
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)
        
        print(f"📊 测试总数: {total_tests}")
        print(f"✅ 通过测试: {passed_tests}")
        print(f"❌ 失败测试: {total_tests - passed_tests}")
        print(f"📈 成功率: {passed_tests/total_tests*100:.1f}%")
        
        print(f"\n📋 详细结果:")
        for test_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   - {test_name}: {status}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 所有功能测试通过！系统运行正常。")
        else:
            print(f"\n⚠️  部分功能存在问题，请检查系统配置。")
        
        print(f"\n⏰ 演示结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """主函数"""
    demo = KnowledgeGraphDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()
