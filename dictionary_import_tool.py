#!/usr/bin/env python3
"""
词典导入工具
支持从CSV文件导入词典数据到指定分类
"""
import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Set

def analyze_import_data(csv_file: str) -> Dict:
    """分析导入数据"""
    print(f"📊 分析导入文件: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        # 检查必需字段
        required_fields = ['术语', '别名', '类别', '多标签', '备注']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"❌ 缺少必需字段: {missing_fields}")
            return None
        
        # 统计信息
        total_records = len(df)
        categories = df['类别'].value_counts().to_dict()
        
        print(f"✅ 总记录数: {total_records}")
        print(f"📋 类别分布:")
        for category, count in categories.items():
            print(f"   - {category}: {count} 条")
        
        return {
            'total': total_records,
            'categories': categories,
            'data': df
        }
        
    except Exception as e:
        print(f"❌ 分析文件失败: {e}")
        return None

def categorize_data(df: pd.DataFrame) -> Dict[str, List]:
    """按类别分组数据"""
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
        '异常现象': 'symptoms',
        '制造工艺': 'causes',
        '软件相关': 'causes',
        '工具': 'countermeasures',
        '测试验证': 'countermeasures',
        '流程相关': 'countermeasures',
        '组织职责': 'countermeasures',
        '项目相关': 'countermeasures',
        '影像相关': 'components',
        '显示相关': 'components'
    }
    
    for _, row in df.iterrows():
        category = row['类别']
        target_category = category_mapping.get(category, 'components')  # 默认归类为组件
        categorized[target_category].append(row.to_dict())
    
    return categorized

def write_category_file(category_data: List, file_path: Path):
    """写入分类文件"""
    if not category_data:
        print(f"⚠️ {file_path.name} 无数据，跳过")
        return 0
    
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(['术语', '别名', '类别', '多标签', '备注'])
            
            # 写入数据
            for item in category_data:
                writer.writerow([
                    item['术语'],
                    item['别名'],
                    item['类别'],
                    item['多标签'],
                    item['备注']
                ])
        
        print(f"✅ {file_path.name}: {len(category_data)} 条记录")
        return len(category_data)
        
    except Exception as e:
        print(f"❌ 写入 {file_path.name} 失败: {e}")
        return 0

def import_dictionary(csv_file: str = "dictionary_import_template.csv"):
    """导入词典数据"""
    print("🚀 开始导入词典数据")
    print("=" * 50)
    
    # 1. 分析导入数据
    analysis = analyze_import_data(csv_file)
    if not analysis:
        return False
    
    # 2. 按类别分组
    print(f"\n📂 按类别分组数据...")
    categorized = categorize_data(analysis['data'])
    
    for category, items in categorized.items():
        print(f"   {category}: {len(items)} 条")
    
    # 3. 写入分类文件
    print(f"\n📝 写入词典文件...")
    
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
        count = write_category_file(categorized[category], file_path)
        total_imported += count
    
    # 4. 验证导入结果
    print(f"\n🎯 导入完成")
    print(f"✅ 总计导入: {total_imported} 条记录")
    print(f"📁 目标目录: {target_dir}")
    
    return True

def verify_import():
    """验证导入结果"""
    print(f"\n🔍 验证导入结果...")
    
    try:
        import requests
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
                
                # 显示示例数据
                if dict_data.get('components'):
                    print(f"\n📋 示例数据:")
                    for i, item in enumerate(dict_data['components'][:3]):
                        print(f"   {i+1}. {item.get('name', '未知')}: {item.get('description', '无描述')[:50]}...")
                
                return True
            else:
                print(f"❌ API返回错误: {data}")
        else:
            print(f"❌ API响应异常: {response.status_code}")
    except Exception as e:
        print(f"❌ API验证失败: {e}")
    
    return False

def main():
    """主函数"""
    print("📚 词典导入工具")
    print("=" * 80)
    
    # 检查模板文件
    template_file = "dictionary_import_template.csv"
    if not Path(template_file).exists():
        print(f"❌ 模板文件不存在: {template_file}")
        print("请先创建模板文件或指定正确的CSV文件路径")
        return
    
    # 导入词典
    if import_dictionary(template_file):
        # 验证导入结果
        verify_import()
        
        print(f"\n🎉 词典导入完成！")
        print(f"📋 下一步:")
        print(f"1. 访问前端查看词典管理页面")
        print(f"2. 测试词典搜索和筛选功能")
        print(f"3. 如需添加更多数据，请编辑CSV文件后重新导入")
    else:
        print(f"\n❌ 词典导入失败")

if __name__ == "__main__":
    main()
