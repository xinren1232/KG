#!/usr/bin/env python3
"""
优化Vue组件，修复常见的Vue警告
"""

import os
import re
from pathlib import Path

def fix_vue_component_warnings(file_path):
    """修复Vue组件的常见警告"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 移除未使用的导入
        # 检查ElMessageBox是否被使用
        if 'ElMessageBox' in content and not re.search(r'ElMessageBox\.(confirm|alert|prompt)', content):
            content = re.sub(r',\s*ElMessageBox', '', content)
            content = re.sub(r'ElMessageBox\s*,\s*', '', content)
            content = re.sub(r'import\s*{\s*ElMessageBox\s*}', 'import {}', content)
        
        # 检查api导入是否被使用
        if 'import api from' in content and not re.search(r'api\.[a-zA-Z]', content):
            content = re.sub(r"import\s+api\s+from\s+['\"]@/api['\"]", '', content)
        
        # 2. 修复defineExpose问题（如果存在）
        if 'defineExpose' in content:
            # 确保defineExpose在setup函数的最后
            setup_match = re.search(r'setup\(\)\s*\{(.*?)return\s*\{(.*?)\}', content, re.DOTALL)
            if setup_match:
                setup_content = setup_match.group(1)
                return_content = setup_match.group(2)
                
                # 如果有defineExpose，确保它在return之前
                if 'defineExpose' in setup_content:
                    # 移除现有的defineExpose
                    setup_content = re.sub(r'defineExpose\([^)]*\)\s*', '', setup_content)
                    
                    # 在return之前添加defineExpose
                    methods_to_expose = []
                    method_names = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*,|\s*$)', return_content)
                    
                    # 过滤出方法（通常以动词开头或包含特定模式）
                    for method in method_names:
                        if any(method.startswith(prefix) for prefix in ['show', 'hide', 'refresh', 'test', 'save', 'delete', 'edit', 'create', 'update', 'reset', 'handle']):
                            methods_to_expose.append(method)
                    
                    if methods_to_expose:
                        expose_code = f"\n    // 暴露方法给父组件\n    defineExpose({{\n      {', '.join(methods_to_expose)}\n    }})\n"
                        new_setup = setup_content + expose_code + f"\n    return {{\n{return_content}    }}"
                        content = content.replace(setup_match.group(0), f"setup() {{\n{new_setup}\n  }}")
        
        # 3. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 4. 修复import语句格式
        content = re.sub(r'import\s*{\s*}\s*from', '// import {} from', content)
        
        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🔧 优化Vue组件，修复常见警告...")
    
    fixed_files = []
    
    # 优化系统管理组件
    system_components_dir = Path("apps/web/src/components/system")
    if system_components_dir.exists():
        print(f"\n📁 优化目录: {system_components_dir}")
        
        for vue_file in system_components_dir.glob("*.vue"):
            if fix_vue_component_warnings(vue_file):
                fixed_files.append(vue_file)
                print(f"✅ 已优化: {vue_file.name}")
    
    # 优化主要视图组件
    views_dir = Path("apps/web/src/views")
    if views_dir.exists():
        print(f"\n📁 优化目录: {views_dir}")
        
        # 优化几个主要的组件
        main_views = ['SystemManagement.vue', 'GraphVisualization.vue', 'DictionaryManagement.vue']
        
        for view_name in main_views:
            view_file = views_dir / view_name
            if view_file.exists():
                if fix_vue_component_warnings(view_file):
                    fixed_files.append(view_file)
                    print(f"✅ 已优化: {view_name}")
    
    print(f"\n🎯 优化完成！共优化了 {len(fixed_files)} 个文件")
    
    if fixed_files:
        print("\n📋 已优化的文件:")
        for file in fixed_files:
            print(f"  - {file}")
    
    print("\n💡 建议的后续优化:")
    print("  1. 检查控制台是否还有Vue警告")
    print("  2. 确保所有组件的方法都正确暴露")
    print("  3. 移除未使用的导入和变量")
    print("  4. 使用Vue DevTools检查组件状态")

if __name__ == "__main__":
    main()
