#!/usr/bin/env python3
"""
增量词典导入工具
支持在现有词典基础上增加新数据，避免重复
"""
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set
import requests

def get_existing_terms() -> Set[str]:
    """获取现有词典中的术语"""
    existing_terms = set()
    
    try:
        response = requests.get("http://localhost:8000/kg/dictionary", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                dict_data = data.get('data', {})
                for category in ['components', 'symptoms', 'causes', 'countermeasures']:
                    for item in dict_data.get(category, []):
                        existing_terms.add(item.get('name', '').strip())
        print(f"✅ 获取到现有术语: {len(existing_terms)} 个")
        return existing_terms
    except Exception as e:
        print(f"⚠️ 无法获取现有术语，将进行全量导入: {e}")
        return set()

def read_existing_csv_terms(file_path: Path) -> Set[str]:
    """读取CSV文件中现有的术语"""
    terms = set()
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    term = row.get('术语', '').strip()
                    if term:
                        terms.add(term)
        except Exception as e:
            print(f"⚠️ 读取 {file_path} 失败: {e}")
    return terms

def categorize_new_data(df: pd.DataFrame) -> Dict[str, List]:
    """按类别分组新数据"""
    categorized = {
        'components': [],
        'symptoms': [],
        'causes': [],
        'countermeasures': []
    }
    
    # 定义类别映射
    category_mapping = {
        '硬件相关': 'components',
        '结构相关': 'components',
        '摄像头模组': 'components',
        '影像相关': 'components',
        '异常现象': 'symptoms',
        '制造工艺': 'causes',
        '软件相关': 'causes',
        '工具': 'countermeasures',
        '测试验证': 'countermeasures',
        '流程相关': 'countermeasures',
        '组织职责': 'countermeasures',
        '项目相关': 'countermeasures'
    }
    
    for _, row in df.iterrows():
        category = row['类别']
        target_category = category_mapping.get(category, 'components')  # 默认归类为组件
        categorized[target_category].append(row.to_dict())
    
    return categorized

def append_to_csv(new_data: List, file_path: Path) -> int:
    """追加数据到CSV文件"""
    if not new_data:
        return 0
    
    # 读取现有数据
    existing_terms = read_existing_csv_terms(file_path)
    
    # 过滤重复数据
    unique_data = []
    for item in new_data:
        term = item['术语'].strip()
        if term not in existing_terms:
            unique_data.append(item)
        else:
            print(f"⚠️ 跳过重复术语: {term}")
    
    if not unique_data:
        print(f"📝 {file_path.name}: 无新数据需要添加")
        return 0
    
    try:
        # 确保文件存在且有表头
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['术语', '别名', '类别', '多标签', '备注'])
        
        # 追加新数据
        with open(file_path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for item in unique_data:
                writer.writerow([
                    item['术语'],
                    item['别名'],
                    item['类别'],
                    item['多标签'],
                    item['备注']
                ])
        
        print(f"✅ {file_path.name}: 新增 {len(unique_data)} 条记录")
        return len(unique_data)
        
    except Exception as e:
        print(f"❌ 写入 {file_path.name} 失败: {e}")
        return 0

def incremental_import(csv_file: str = "new_dictionary_data.csv"):
    """增量导入词典数据"""
    print("🚀 开始增量导入词典数据")
    print("=" * 60)
    
    # 1. 检查输入文件
    if not Path(csv_file).exists():
        print(f"❌ 输入文件不存在: {csv_file}")
        return False
    
    # 2. 读取新数据
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        print(f"📊 读取新数据: {len(df)} 条记录")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False
    
    # 3. 获取现有术语（用于去重）
    existing_terms = get_existing_terms()
    
    # 4. 过滤重复数据
    new_df = df[~df['术语'].isin(existing_terms)]
    duplicate_count = len(df) - len(new_df)
    
    if duplicate_count > 0:
        print(f"⚠️ 发现重复术语: {duplicate_count} 个，已自动过滤")
    
    if len(new_df) == 0:
        print("📝 没有新数据需要导入")
        return True
    
    print(f"✅ 待导入新数据: {len(new_df)} 条")
    
    # 5. 按类别分组
    categorized = categorize_new_data(new_df)
    
    print(f"\n📂 新数据分类统计:")
    for category, items in categorized.items():
        print(f"   {category}: {len(items)} 条")
    
    # 6. 追加到对应文件
    print(f"\n📝 追加到词典文件...")
    
    target_dir = Path("ontology/dictionaries")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    file_mapping = {
        'components': target_dir / 'components.csv',
        'symptoms': target_dir / 'symptoms.csv',
        'causes': target_dir / 'causes.csv',
        'countermeasures': target_dir / 'countermeasures.csv'
    }
    
    total_imported = 0
    for category, file_path in file_mapping.items():
        count = append_to_csv(categorized[category], file_path)
        total_imported += count
    
    print(f"\n🎯 增量导入完成")
    print(f"✅ 新增记录: {total_imported} 条")
    
    return True

def verify_import_result():
    """验证导入结果"""
    print(f"\n🔍 验证导入结果...")
    
    try:
        # 等待API服务响应
        import time
        time.sleep(2)
        
        response = requests.get("http://localhost:8000/kg/dictionary", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                dict_data = data.get('data', {})
                print(f"✅ API验证成功:")
                print(f"   - 组件: {len(dict_data.get('components', []))}")
                print(f"   - 症状: {len(dict_data.get('symptoms', []))}")
                print(f"   - 原因: {len(dict_data.get('causes', []))}")
                print(f"   - 对策: {len(dict_data.get('countermeasures', []))}")
                
                total = sum(len(dict_data.get(key, [])) for key in ['components', 'symptoms', 'causes', 'countermeasures'])
                print(f"   - 总计: {total}")
                
                # 显示最新添加的几个术语
                if dict_data.get('components'):
                    print(f"\n📋 最新组件术语示例:")
                    for i, item in enumerate(dict_data['components'][-3:]):
                        print(f"   {i+1}. {item.get('name', '未知')}")
                
                return total
            else:
                print(f"❌ API返回错误: {data}")
        else:
            print(f"❌ API响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ API验证失败: {e}")
    
    return 0

def main():
    """主函数"""
    print("📚 增量词典导入工具")
    print("=" * 80)
    
    # 检查输入文件
    input_file = "new_dictionary_data.csv"
    if not Path(input_file).exists():
        print(f"❌ 输入文件不存在: {input_file}")
        print("请确保文件存在后重试")
        return
    
    # 执行增量导入
    if incremental_import(input_file):
        # 验证导入结果
        total_count = verify_import_result()
        
        print(f"\n🎉 增量导入完成！")
        print(f"📊 当前词典总计: {total_count} 条")
        print(f"📋 下一步:")
        print(f"1. 访问前端查看更新后的词典")
        print(f"2. 测试新增术语的搜索功能")
        print(f"3. 如需继续添加数据，请准备新的CSV文件")
    else:
        print(f"\n❌ 增量导入失败")

if __name__ == "__main__":
    main()
