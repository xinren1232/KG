#!/usr/bin/env python3
"""
智能问答助手集成示例
演示如何将知识图谱接入问答系统
"""
import requests
from typing import List, Dict, Optional
import re

class KnowledgeGraphQA:
    """基于知识图谱的问答助手"""
    
    def __init__(self, api_base_url: str = "http://47.108.152.16:8000"):
        self.api_base_url = api_base_url
        self.dictionary = self._load_dictionary()
    
    def _load_dictionary(self) -> List[Dict]:
        """加载词典数据"""
        try:
            response = requests.get(f"{self.api_base_url}/kg/dictionary")
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('entries', [])
            return []
        except Exception as e:
            print(f"加载词典失败: {e}")
            return []
    
    def extract_keywords(self, question: str) -> List[str]:
        """从问题中提取关键词"""
        keywords = []
        
        # 遍历词典，查找匹配的术语
        for entry in self.dictionary:
            term = entry.get('term', '')
            aliases = entry.get('aliases', [])
            
            # 检查术语是否在问题中
            if term in question:
                keywords.append(term)
            
            # 检查别名是否在问题中
            for alias in aliases:
                if alias in question:
                    keywords.append(term)
                    break
        
        return list(set(keywords))  # 去重
    
    def classify_intent(self, question: str) -> str:
        """识别问题意图"""
        # 术语解释类
        if any(word in question for word in ['是什么', '什么是', '定义', '解释', '含义']):
            return 'term_explanation'
        
        # 症状诊断类
        if any(word in question for word in ['原因', '为什么', '怎么回事', '导致']):
            return 'symptom_diagnosis'
        
        # 解决方案类
        if any(word in question for word in ['怎么办', '如何解决', '解决方法', '对策']):
            return 'solution_query'
        
        # 测试流程类
        if any(word in question for word in ['如何测试', '测试方法', '测试流程', '怎么测']):
            return 'test_procedure'
        
        # 组件问题类
        if any(word in question for word in ['常见问题', '有哪些问题', '问题列表']):
            return 'component_issues'
        
        return 'general_query'
    
    def answer_term_explanation(self, term: str) -> str:
        """回答术语解释问题"""
        for entry in self.dictionary:
            if entry.get('term') == term:
                aliases = ', '.join(entry.get('aliases', [])[:3])
                description = entry.get('description', '暂无描述')
                category = entry.get('category', '未分类')
                tags = ', '.join(entry.get('tags', [])[:5])
                
                answer = f"**{term}**\n\n"
                answer += f"📂 分类: {category}\n"
                if aliases:
                    answer += f"🏷️ 别名: {aliases}\n"
                if tags:
                    answer += f"🔖 标签: {tags}\n"
                answer += f"\n📝 定义:\n{description}"
                
                return answer
        
        return f"抱歉，我没有找到关于'{term}'的信息。"
    
    def answer_symptom_diagnosis(self, symptom: str) -> str:
        """回答症状诊断问题"""
        # 查找症状相关信息
        symptom_info = None
        for entry in self.dictionary:
            if entry.get('term') == symptom and entry.get('category') == 'Symptom':
                symptom_info = entry
                break
        
        if not symptom_info:
            return f"抱歉，我没有找到关于'{symptom}'的症状信息。"
        
        answer = f"**{symptom}** 症状分析\n\n"
        answer += f"📝 症状描述:\n{symptom_info.get('description', '暂无描述')}\n\n"
        
        # 查找可能的相关组件
        tags = symptom_info.get('tags', [])
        if tags:
            answer += f"🔍 相关领域: {', '.join(tags[:5])}\n\n"
        
        answer += "💡 建议:\n"
        answer += "1. 检查相关硬件组件是否正常\n"
        answer += "2. 查看系统日志获取更多信息\n"
        answer += "3. 运行相关测试用例进行诊断\n"
        
        return answer
    
    def answer_test_procedure(self, component: str) -> str:
        """回答测试流程问题"""
        # 查找相关测试用例
        test_cases = []
        for entry in self.dictionary:
            if entry.get('category') == 'TestCase':
                term = entry.get('term', '')
                desc = entry.get('description', '')
                if component in term or component in desc:
                    test_cases.append(entry)
        
        if not test_cases:
            return f"抱歉，我没有找到关于'{component}'的测试流程。"
        
        answer = f"**{component}** 测试流程\n\n"
        answer += f"找到 {len(test_cases)} 个相关测试用例:\n\n"
        
        for i, tc in enumerate(test_cases[:5], 1):
            answer += f"{i}. **{tc.get('term')}**\n"
            answer += f"   {tc.get('description', '暂无描述')}\n"
            tags = tc.get('tags', [])
            if tags:
                answer += f"   标签: {', '.join(tags[:3])}\n"
            answer += "\n"
        
        if len(test_cases) > 5:
            answer += f"... 还有 {len(test_cases) - 5} 个测试用例\n"
        
        return answer
    
    def answer_component_issues(self, component: str) -> str:
        """回答组件常见问题"""
        # 查找相关症状
        symptoms = []
        for entry in self.dictionary:
            if entry.get('category') == 'Symptom':
                desc = entry.get('description', '')
                tags = ' '.join(entry.get('tags', []))
                if component in desc or component in tags:
                    symptoms.append(entry)
        
        if not symptoms:
            return f"抱歉，我没有找到关于'{component}'的常见问题。"
        
        answer = f"**{component}** 常见问题\n\n"
        answer += f"找到 {len(symptoms)} 个相关问题:\n\n"
        
        for i, symptom in enumerate(symptoms[:10], 1):
            answer += f"{i}. **{symptom.get('term')}**\n"
            answer += f"   {symptom.get('description', '暂无描述')}\n\n"
        
        if len(symptoms) > 10:
            answer += f"... 还有 {len(symptoms) - 10} 个问题\n"
        
        return answer
    
    def answer_question(self, question: str) -> str:
        """回答用户问题"""
        print(f"\n❓ 问题: {question}")
        
        # 1. 提取关键词
        keywords = self.extract_keywords(question)
        print(f"🔍 提取关键词: {keywords}")
        
        if not keywords:
            return "抱歉，我无法理解您的问题。请尝试使用更具体的术语。"
        
        # 2. 识别意图
        intent = self.classify_intent(question)
        print(f"🎯 识别意图: {intent}")
        
        # 3. 根据意图回答
        main_keyword = keywords[0]
        
        if intent == 'term_explanation':
            return self.answer_term_explanation(main_keyword)
        elif intent == 'symptom_diagnosis':
            return self.answer_symptom_diagnosis(main_keyword)
        elif intent == 'test_procedure':
            return self.answer_test_procedure(main_keyword)
        elif intent == 'component_issues':
            return self.answer_component_issues(main_keyword)
        else:
            # 默认返回术语解释
            return self.answer_term_explanation(main_keyword)


def demo():
    """演示问答功能"""
    print("=" * 80)
    print("🤖 手机研发质量智能问答助手 - 演示")
    print("=" * 80)
    
    # 初始化问答系统（直接使用本地词典）
    print("📂 加载本地词典数据...")
    import json
    with open('api/data/dictionary.json', 'r', encoding='utf-8') as f:
        dictionary_data = json.load(f)

    qa = KnowledgeGraphQA()
    qa.dictionary = dictionary_data
    
    print(f"✅ 已加载 {len(qa.dictionary)} 条术语\n")
    
    # 测试问题
    test_questions = [
        "AQL是什么？",
        "BTB连接器是什么？",
        "黑屏是什么原因？",
        "对焦失败怎么办？",
        "如何测试屏幕？",
        "摄像头有哪些常见问题？",
        "FPC是什么？",
        "SMT工艺有哪些测试方法？"
    ]
    
    for question in test_questions:
        answer = qa.answer_question(question)
        print(f"\n💬 回答:\n{answer}")
        print("\n" + "-" * 80)


if __name__ == "__main__":
    demo()
