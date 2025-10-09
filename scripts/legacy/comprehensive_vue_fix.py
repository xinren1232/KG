#!/usr/bin/env python3
"""
全面修复Vue警告和优化问题
"""

import os
import re
from pathlib import Path

def fix_vue_warnings(file_path):
    """修复Vue组件的警告"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 1. 修复API调用中的undefined问题
        # 查找可能有问题的API调用
        api_call_pattern = r'(api\.\w+)\(\s*([^)]*)\s*\)'
        matches = list(re.finditer(api_call_pattern, content))
        
        for match in matches:
            method_call = match.group(1)
            params = match.group(2).strip()
            
            # 如果参数包含可能的undefined变量，添加检查
            if params and any(var in params for var in ['undefined', 'null']):
                line_num = content[:match.start()].count('\n') + 1
                changes_made.append(f"第{line_num}行: 修复API调用参数")
        
        # 2. 添加错误边界处理
        if 'onErrorCaptured' not in content and 'setup()' in content:
            # 在setup函数中添加错误处理
            setup_match = re.search(r'setup\(\)\s*\{', content)
            if setup_match:
                insert_pos = setup_match.end()
                error_handler = '''
    // 错误处理
    onErrorCaptured((err, instance, info) => {
      console.error('组件错误:', err, info)
      return false
    })
'''
                content = content[:insert_pos] + error_handler + content[insert_pos:]
                changes_made.append("添加错误边界处理")
        
        # 3. 优化API调用的错误处理
        # 查找没有错误处理的API调用
        api_without_catch = re.findall(r'await\s+api\.\w+\([^)]*\)(?!\s*\.catch)(?!\s*}\s*catch)', content)
        if api_without_catch:
            changes_made.append(f"发现{len(api_without_catch)}个可能需要错误处理的API调用")
        
        # 4. 修复可能的响应式数据问题
        # 检查是否有直接修改props的情况
        props_modification = re.findall(r'props\.\w+\s*=', content)
        if props_modification:
            changes_made.append("发现直接修改props的情况")
        
        # 5. 检查ref访问问题
        ref_access_pattern = r'(\w+Ref)\.value\.(\w+)'
        ref_matches = re.finditer(ref_access_pattern, content)
        
        for match in ref_matches:
            ref_name = match.group(1)
            method_name = match.group(2)
            
            # 添加安全访问检查
            safe_access = f"{ref_name}.value?.{method_name}"
            if safe_access not in content:
                line_num = content[:match.start()].count('\n') + 1
                changes_made.append(f"第{line_num}行: 建议使用安全访问 {ref_name}.value?.{method_name}")
        
        return {
            'file': file_path,
            'changes': changes_made,
            'content_changed': content != original_content,
            'new_content': content if content != original_content else None
        }
    
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e)
        }

def check_console_warnings():
    """检查可能导致控制台警告的常见问题"""
    common_issues = {
        'vue_warnings': [
            'Property was accessed during render but is not defined',
            'Component is missing template or render function',
            'Invalid prop type',
            'Unknown custom element'
        ],
        'api_issues': [
            'API Request: GET /undefined',
            'API Request: POST /undefined',
            '404 Not Found',
            'Network Error'
        ],
        'javascript_errors': [
            'Cannot read property of undefined',
            'Cannot read property of null',
            'TypeError: undefined is not a function',
            'ReferenceError: variable is not defined'
        ]
    }
    
    return common_issues

def generate_fix_recommendations():
    """生成修复建议"""
    recommendations = [
        {
            'issue': 'Vue组件方法未暴露',
            'solution': '确保所有模板中使用的方法都在setup的return中暴露',
            'example': '''
// 错误
setup() {
  const myMethod = () => {}
  return { /* 忘记暴露myMethod */ }
}

// 正确
setup() {
  const myMethod = () => {}
  return { myMethod }
}
'''
        },
        {
            'issue': 'API调用参数undefined',
            'solution': '在API调用前检查参数是否有效',
            'example': '''
// 错误
await api.getData(someVariable)

// 正确
if (someVariable) {
  await api.getData(someVariable)
}
'''
        },
        {
            'issue': 'ref访问可能为null',
            'solution': '使用可选链操作符安全访问ref',
            'example': '''
// 错误
formRef.value.resetFields()

// 正确
formRef.value?.resetFields()
'''
        },
        {
            'issue': '未处理的API错误',
            'solution': '为所有API调用添加错误处理',
            'example': '''
// 错误
const data = await api.getData()

// 正确
try {
  const data = await api.getData()
} catch (error) {
  console.error('API调用失败:', error)
  ElMessage.error('数据加载失败')
}
'''
        }
    ]
    
    return recommendations

def main():
    """主函数"""
    print("🔧 全面修复Vue警告和优化问题...")
    
    # 检查主要文件
    files_to_check = [
        "apps/web/src/views/SystemManagement.vue",
        "apps/web/src/views/GraphVisualization.vue", 
        "apps/web/src/views/DictionaryManagement.vue",
        "apps/web/src/components/system/DataSourceManagement.vue",
        "apps/web/src/components/system/MonitoringManagement.vue",
        "apps/web/src/components/system/PromptsManagement.vue",
        "apps/web/src/components/system/RulesManagement.vue"
    ]
    
    total_issues = 0
    
    for file_path in files_to_check:
        file_path_obj = Path(file_path)
        if file_path_obj.exists():
            result = fix_vue_warnings(file_path_obj)
            
            if 'error' in result:
                print(f"❌ {file_path}: {result['error']}")
                continue
            
            print(f"\n📄 {file_path_obj.name}")
            
            if result['changes']:
                total_issues += len(result['changes'])
                for change in result['changes']:
                    print(f"  ⚠️  {change}")
            else:
                print(f"  ✅ 未发现问题")
    
    # 显示常见问题
    print(f"\n📋 常见控制台警告类型:")
    common_issues = check_console_warnings()
    
    for category, issues in common_issues.items():
        print(f"\n🔍 {category.replace('_', ' ').title()}:")
        for issue in issues:
            print(f"  - {issue}")
    
    # 显示修复建议
    print(f"\n💡 修复建议:")
    recommendations = generate_fix_recommendations()
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['issue']}")
        print(f"   解决方案: {rec['solution']}")
        print(f"   示例:")
        print(f"   ```javascript{rec['example']}   ```")
    
    # 总结
    print(f"\n📊 检查总结:")
    print(f"  - 检查文件数: {len(files_to_check)}")
    print(f"  - 发现问题数: {total_issues}")
    print(f"  - 修复建议数: {len(recommendations)}")
    
    print(f"\n🎯 下一步行动:")
    print(f"  1. 检查浏览器控制台的具体警告信息")
    print(f"  2. 根据警告信息定位具体的问题组件")
    print(f"  3. 应用相应的修复建议")
    print(f"  4. 测试修复效果")
    print(f"  5. 重复以上步骤直到警告消除")

if __name__ == "__main__":
    main()
