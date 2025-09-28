#!/usr/bin/env python3
"""
词典质量检查工具
基于专业标准对词典数据进行全面质量检查
"""

import json
import csv
from collections import Counter, defaultdict
from datetime import datetime
import re

class DictionaryQualityChecker:
    """词典质量检查器"""
    
    def __init__(self):
        self.standard_categories = {
            'Symptom', 'Component', 'Tool', 'Process', 
            'TestCase', 'Metric', 'Material', 'Role'
        }
        
        self.standard_tags = self.load_standard_tags()
        self.issues = {
            'critical': [],  # 必须修复
            'warning': [],   # 建议修复
            'info': []       # 信息提示
        }
        
    def load_standard_tags(self):
        """加载标准标签"""
        try:
            with open('data/tag_whitelist.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return {row['tag'] for row in reader if row['tag']}
        except:
            return set()
    
    def check_basic_format(self, data):
        """检查基础格式规范"""
        print("🔍 检查基础格式规范...")
        
        required_fields = ['term', 'aliases', 'category', 'tags', 'description']
        
        for i, item in enumerate(data, 1):
            # 检查必填字段
            for field in required_fields:
                if field not in item or not item[field]:
                    self.issues['critical'].append({
                        'row': i,
                        'term': item.get('term', '未知'),
                        'type': '字段缺失',
                        'issue': f'缺少必填字段: {field}',
                        'suggestion': f'请补充{field}字段的内容'
                    })
            
            # 检查术语长度
            term = item.get('term', '')
            if len(term) < 2 or len(term) > 15:
                self.issues['warning'].append({
                    'row': i,
                    'term': term,
                    'type': '术语长度',
                    'issue': f'术语长度{len(term)}字符，建议2-15字符',
                    'suggestion': '调整术语长度到合理范围'
                })
            
            # 检查描述长度
            desc = item.get('description', '')
            if len(desc) < 20 or len(desc) > 200:
                self.issues['warning'].append({
                    'row': i,
                    'term': term,
                    'type': '描述长度',
                    'issue': f'描述长度{len(desc)}字符，建议20-200字符',
                    'suggestion': '调整描述长度，提供适当详细的说明'
                })
            
            # 检查分类标准
            category = item.get('category', '')
            if category not in self.standard_categories:
                self.issues['critical'].append({
                    'row': i,
                    'term': term,
                    'type': '分类错误',
                    'issue': f'分类"{category}"不在标准分类中',
                    'suggestion': f'请使用标准分类: {", ".join(self.standard_categories)}'
                })
    
    def check_content_logic(self, data):
        """检查内容逻辑"""
        print("🧠 检查内容逻辑...")
        
        # 分类逻辑检查
        category_keywords = {
            'Symptom': ['异常', '故障', '问题', '错误', '失效', '不良', '缺陷'],
            'Component': ['器', '件', '模组', '芯片', '连接器', '电路', '板'],
            'Tool': ['仪', '器', '设备', '工具', '治具', '测试', '检测'],
            'Process': ['工艺', '流程', '过程', '步骤', '方法', '程序'],
            'TestCase': ['测试', '检验', '验证', '试验', '评估'],
            'Metric': ['率', '度', '值', '指标', '参数', '标准'],
            'Material': ['料', '胶', '油', '膜', '粉', '液'],
            'Role': ['师', '员', '手', '岗', '部门', '职责']
        }
        
        for i, item in enumerate(data, 1):
            term = item.get('term', '')
            category = item.get('category', '')
            description = item.get('description', '')
            
            # 检查分类与术语的匹配度
            if category in category_keywords:
                keywords = category_keywords[category]
                if not any(keyword in term or keyword in description for keyword in keywords):
                    self.issues['warning'].append({
                        'row': i,
                        'term': term,
                        'type': '分类匹配',
                        'issue': f'术语和描述中未发现{category}类的典型特征',
                        'suggestion': f'检查分类是否正确，或在描述中体现{category}特征'
                    })
            
            # 检查标签相关性
            tags = item.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(';') if tag.strip()]
            
            # 检查标签是否在标准列表中
            for tag in tags:
                if tag not in self.standard_tags and self.standard_tags:
                    self.issues['warning'].append({
                        'row': i,
                        'term': term,
                        'type': '标签非标准',
                        'issue': f'标签"{tag}"不在标准标签列表中',
                        'suggestion': '使用标准标签或确认是否需要添加新标签'
                    })
    
    def check_duplicates_conflicts(self, data):
        """检查重复和冲突"""
        print("🔄 检查重复和冲突...")
        
        terms = {}
        aliases_map = defaultdict(list)
        
        for i, item in enumerate(data, 1):
            term = item.get('term', '')
            aliases = item.get('aliases', [])
            
            # 检查术语重复
            if term in terms:
                self.issues['critical'].append({
                    'row': i,
                    'term': term,
                    'type': '术语重复',
                    'issue': f'术语"{term}"与第{terms[term]}行重复',
                    'suggestion': '删除重复术语或合并为一个条目'
                })
            else:
                terms[term] = i
            
            # 检查别名冲突
            if isinstance(aliases, str):
                aliases = [alias.strip() for alias in aliases.split(';') if alias.strip()]
            
            for alias in aliases:
                aliases_map[alias].append((i, term))
        
        # 检查别名冲突
        for alias, term_list in aliases_map.items():
            if len(term_list) > 1:
                terms_info = ', '.join([f'{term}(行{row})' for row, term in term_list])
                for row, term in term_list:
                    self.issues['warning'].append({
                        'row': row,
                        'term': term,
                        'type': '别名冲突',
                        'issue': f'别名"{alias}"被多个术语使用: {terms_info}',
                        'suggestion': '检查别名是否应该唯一，或调整别名避免冲突'
                    })
    
    def check_practical_value(self, data):
        """检查实用价值"""
        print("💎 检查实用价值...")
        
        value_keywords = {
            'application': ['应用', '用于', '适用', '场景', '环境'],
            'cause': ['原因', '导致', '由于', '因为', '造成'],
            'effect': ['影响', '后果', '结果', '导致', '引起'],
            'solution': ['解决', '处理', '修复', '改善', '预防']
        }
        
        for i, item in enumerate(data, 1):
            term = item.get('term', '')
            description = item.get('description', '')
            category = item.get('category', '')
            
            # 检查描述的信息丰富度
            if len(description) < 30:
                self.issues['info'].append({
                    'row': i,
                    'term': term,
                    'type': '描述简单',
                    'issue': '描述过于简单，信息量不足',
                    'suggestion': '增加应用场景、重要性或技术细节'
                })
            
            # 检查是否包含有价值的信息
            has_value_info = any(
                any(keyword in description for keyword in keywords)
                for keywords in value_keywords.values()
            )
            
            if not has_value_info:
                self.issues['info'].append({
                    'row': i,
                    'term': term,
                    'type': '价值信息缺失',
                    'issue': '描述缺少应用场景、原因分析或解决方案等有价值信息',
                    'suggestion': '补充实际应用场景、重要性说明或相关技术信息'
                })
            
            # 针对Symptom类的特殊检查
            if category == 'Symptom':
                if not any(keyword in description for keyword in value_keywords['cause']):
                    self.issues['info'].append({
                        'row': i,
                        'term': term,
                        'type': 'Symptom缺少原因',
                        'issue': '症状类术语缺少原因分析',
                        'suggestion': '补充可能的原因或影响因素'
                    })
    
    def generate_statistics(self, data):
        """生成统计信息"""
        total_count = len(data)
        category_dist = Counter(item.get('category', 'Unknown') for item in data)
        
        # 计算完整性
        complete_count = 0
        for item in data:
            if all(item.get(field) for field in ['term', 'aliases', 'category', 'tags', 'description']):
                complete_count += 1
        
        completeness = (complete_count / total_count * 100) if total_count > 0 else 0
        
        # 计算质量分数
        critical_count = len(self.issues['critical'])
        warning_count = len(self.issues['warning'])
        
        # 质量分数计算：基础分10分，每个严重问题扣2分，每个警告扣0.5分
        quality_score = max(0, 10 - (critical_count * 2 + warning_count * 0.5) / total_count * 10)
        
        return {
            'total_count': total_count,
            'completeness': completeness,
            'category_distribution': dict(category_dist),
            'quality_score': quality_score,
            'critical_issues': critical_count,
            'warning_issues': warning_count,
            'info_issues': len(self.issues['info'])
        }
    
    def generate_report(self, data):
        """生成检查报告"""
        print("📊 生成质量检查报告...")
        
        stats = self.generate_statistics(data)
        
        report = f"""# 📊 词典质量检查报告

## 🎯 检查概览
- **检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **词条总数**: {stats['total_count']} 条
- **完整性**: {stats['completeness']:.1f}%
- **质量评分**: {stats['quality_score']:.1f}/10.0

## 📊 统计信息
### 分类分布
"""
        
        for category, count in stats['category_distribution'].items():
            percentage = (count / stats['total_count'] * 100) if stats['total_count'] > 0 else 0
            report += f"- **{category}**: {count} 条 ({percentage:.1f}%)\n"
        
        report += f"""
### 问题统计
- **严重问题**: {stats['critical_issues']} 个 (必须修复)
- **警告问题**: {stats['warning_issues']} 个 (建议修复)
- **信息提示**: {stats['info_issues']} 个 (优化建议)

## 🚨 严重问题清单 (必须修复)
| 行号 | 术语 | 问题类型 | 具体问题 | 修改建议 |
|------|------|----------|----------|----------|"""
        
        for issue in self.issues['critical']:
            report += f"\n| {issue['row']} | {issue['term']} | {issue['type']} | {issue['issue']} | {issue['suggestion']} |"
        
        if not self.issues['critical']:
            report += "\n| - | - | - | 无严重问题 | - |"
        
        report += f"""

## ⚠️ 警告问题清单 (建议修复)
| 行号 | 术语 | 问题类型 | 具体问题 | 优化建议 |
|------|------|----------|----------|----------|"""
        
        for issue in self.issues['warning'][:20]:  # 限制显示前20个
            report += f"\n| {issue['row']} | {issue['term']} | {issue['type']} | {issue['issue']} | {issue['suggestion']} |"
        
        if not self.issues['warning']:
            report += "\n| - | - | - | 无警告问题 | - |"
        elif len(self.issues['warning']) > 20:
            report += f"\n| ... | ... | ... | 还有{len(self.issues['warning'])-20}个警告问题 | 详见完整报告 |"
        
        # 质量评价
        if stats['quality_score'] >= 9:
            quality_level = "优秀"
            quality_desc = "词典质量很高，符合专业标准"
        elif stats['quality_score'] >= 7:
            quality_level = "良好"
            quality_desc = "词典质量较好，有少量需要改进的地方"
        elif stats['quality_score'] >= 5:
            quality_level = "一般"
            quality_desc = "词典质量一般，需要进行一定的改进"
        else:
            quality_level = "较差"
            quality_desc = "词典质量较差，需要大量改进工作"
        
        report += f"""

## 🎯 整体评价与改进建议

### ✅ 质量评级: {quality_level} ({stats['quality_score']:.1f}/10.0)
{quality_desc}

### 🔧 关键改进项 (优先级排序)
"""
        
        # 分析主要问题类型
        critical_types = Counter(issue['type'] for issue in self.issues['critical'])
        warning_types = Counter(issue['type'] for issue in self.issues['warning'])
        
        priority_issues = []
        
        if critical_types:
            top_critical = critical_types.most_common(1)[0]
            priority_issues.append(f"**高优先级**: {top_critical[0]} ({top_critical[1]}个) - 立即修复")
        
        if warning_types:
            top_warning = warning_types.most_common(1)[0]
            priority_issues.append(f"**中优先级**: {top_warning[0]} ({top_warning[1]}个) - 建议修复")
        
        if len(self.issues['info']) > 0:
            priority_issues.append(f"**低优先级**: 信息完善 ({len(self.issues['info'])}个) - 优化建议")
        
        for i, issue in enumerate(priority_issues, 1):
            report += f"{i}. {issue}\n"
        
        if not priority_issues:
            report += "1. **无关键问题**: 词典质量良好，建议继续保持\n"
        
        report += f"""
### 📈 质量提升建议
1. **立即修复**: 解决所有严重问题，确保基础规范
2. **短期改进**: 处理警告问题，提升内容质量
3. **长期完善**: 根据信息提示，持续优化词典价值

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*检查工具: 词典质量检查专家 v1.0*
"""
        
        return report
    
    def check_dictionary(self, data):
        """执行完整的词典检查"""
        print("🔍 开始词典质量检查...")
        print("=" * 50)
        
        # 清空之前的问题记录
        self.issues = {'critical': [], 'warning': [], 'info': []}
        
        # 执行各项检查
        self.check_basic_format(data)
        self.check_content_logic(data)
        self.check_duplicates_conflicts(data)
        self.check_practical_value(data)
        
        # 生成报告
        report = self.generate_report(data)
        
        print("=" * 50)
        print("✅ 词典质量检查完成！")
        
        return report

def main():
    """主函数"""
    print("🔍 词典质量检查工具")
    print("=" * 50)
    
    # 加载词典数据
    try:
        with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📚 成功加载 {len(data)} 条词典数据")
    except Exception as e:
        print(f"❌ 加载词典数据失败: {e}")
        return
    
    # 创建检查器并执行检查
    checker = DictionaryQualityChecker()
    report = checker.check_dictionary(data)
    
    # 保存报告
    with open('词典质量检查报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📋 质量检查报告已保存: 词典质量检查报告.md")
    
    # 显示简要统计
    stats = checker.generate_statistics(data)
    print(f"\n📊 检查结果概览:")
    print(f"  质量评分: {stats['quality_score']:.1f}/10.0")
    print(f"  严重问题: {stats['critical_issues']} 个")
    print(f"  警告问题: {stats['warning_issues']} 个")
    print(f"  信息提示: {stats['info_issues']} 个")

if __name__ == "__main__":
    main()
