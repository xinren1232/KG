<template>
  <div class="prompts-management">
    <!-- 操作栏 -->
    <div class="action-bar">
      <div class="action-left">
        <h3>Prompt管理</h3>
        <span class="prompt-count">共 {{ filteredPrompts.length }} 个Prompt模板</span>
      </div>
      <div class="action-right">
        <el-button type="primary" @click="showAddDialog">
          <el-icon><Plus /></el-icon>
          新增Prompt
        </el-button>
        <el-button @click="showVersionDialog">
          <el-icon><Clock /></el-icon>
          版本管理
        </el-button>
        <el-button @click="showEvaluationDialog">
          <el-icon><TrendCharts /></el-icon>
          效果评估
        </el-button>
        <el-button @click="exportPrompts">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- Prompt分类过滤 -->
    <div class="category-filter">
      <el-radio-group v-model="activeCategory" @change="handleCategoryChange">
        <el-radio-button label="all">全部 ({{ prompts.length }})</el-radio-button>
        <el-radio-button label="extraction">抽取词典 ({{ getPromptCountByCategory('extraction') }})</el-radio-button>
        <el-radio-button label="construction">信息构建 ({{ getPromptCountByCategory('construction') }})</el-radio-button>
        <el-radio-button label="scenario">场景化 ({{ getPromptCountByCategory('scenario') }})</el-radio-button>
        <el-radio-button label="analysis">分析评估 ({{ getPromptCountByCategory('analysis') }})</el-radio-button>
      </el-radio-group>
    </div>

    <!-- Prompt列表 -->
    <div class="prompts-grid">
      <div
        v-for="prompt in filteredPrompts"
        :key="prompt.id"
        class="prompt-card"
        @click="editPrompt(prompt)"
      >
        <div class="card-header">
          <div class="prompt-info">
            <h4 class="prompt-name">{{ prompt.name }}</h4>
            <span class="prompt-category">{{ prompt.category }}</span>
          </div>
          <div class="card-actions" @click.stop>
            <el-dropdown trigger="click">
              <el-button size="small" text>
                <el-icon><MoreFilled /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editPrompt(prompt)">编辑</el-dropdown-item>
                  <el-dropdown-item @click="testPrompt(prompt)">测试</el-dropdown-item>
                  <el-dropdown-item @click="duplicatePrompt(prompt)">复制</el-dropdown-item>
                  <el-dropdown-item @click="deletePrompt(prompt)" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="card-content">
          <p class="prompt-description">{{ prompt.description }}</p>
          <div class="prompt-preview">
            <pre>{{ getPromptPreview(prompt.template) }}</pre>
          </div>
        </div>
        
        <div class="card-footer">
          <div class="prompt-meta">
            <el-tag size="small" :type="getCategoryColor(prompt.category)">
              {{ prompt.category }}
            </el-tag>
            <el-tag size="small" type="info" v-if="prompt.version">
              v{{ prompt.version }}
            </el-tag>
            <span class="update-time">{{ formatTime(prompt.updated_at) }}</span>
          </div>
          <div class="prompt-stats">
            <span class="usage-count">使用 {{ prompt.usage_count || 0 }} 次</span>
            <span class="success-rate" v-if="prompt.success_rate">
              成功率 {{ prompt.success_rate }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑Prompt对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑Prompt' : '新增Prompt'"
      width="800px"
      @close="resetForm"
    >
      <el-form :model="promptForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="名称" prop="name">
              <el-input v-model="promptForm.name" placeholder="请输入Prompt名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="promptForm.category" placeholder="请选择分类">
                <el-option label="系统提示" value="system" />
                <el-option label="用户提示" value="user" />
                <el-option label="助手提示" value="assistant" />
                <el-option label="工具提示" value="tool" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="promptForm.description"
            type="textarea"
            :rows="2"
            placeholder="请输入Prompt描述"
          />
        </el-form-item>
        
        <el-form-item label="模板内容" prop="template">
          <el-input
            v-model="promptForm.template"
            type="textarea"
            :rows="8"
            placeholder="请输入Prompt模板内容，支持变量 {variable_name}"
          />
        </el-form-item>
        
        <el-form-item label="变量定义" prop="variables">
          <div class="variables-editor">
            <div
              v-for="(variable, index) in promptForm.variables"
              :key="index"
              class="variable-item"
            >
              <el-input
                v-model="variable.name"
                placeholder="变量名"
                style="width: 150px; margin-right: 10px;"
              />
              <el-input
                v-model="variable.description"
                placeholder="变量描述"
                style="flex: 1; margin-right: 10px;"
              />
              <el-button
                size="small"
                type="danger"
                @click="removeVariable(index)"
              >
                删除
              </el-button>
            </div>
            <el-button size="small" @click="addVariable">添加变量</el-button>
          </div>
        </el-form-item>
        
        <el-form-item label="标签">
          <el-tag
            v-for="tag in promptForm.tags"
            :key="tag"
            closable
            @close="removeTag(tag)"
            style="margin-right: 8px;"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="inputVisible"
            ref="inputRef"
            v-model="inputValue"
            size="small"
            style="width: 100px;"
            @keyup.enter="handleInputConfirm"
            @blur="handleInputConfirm"
          />
          <el-button v-else size="small" @click="showInput">+ 新标签</el-button>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePrompt" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- Prompt测试对话框 -->
    <el-dialog v-model="testDialogVisible" title="Prompt测试" width="900px">
      <div class="test-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <h4>变量输入</h4>
            <el-form :model="testVariables" label-width="100px">
              <el-form-item
                v-for="variable in currentPrompt?.variables || []"
                :key="variable.name"
                :label="variable.name"
              >
                <el-input
                  v-model="testVariables[variable.name]"
                  :placeholder="variable.description"
                />
              </el-form-item>
            </el-form>
          </el-col>
          <el-col :span="12">
            <h4>生成结果</h4>
            <div class="test-result">
              <pre>{{ generatedPrompt }}</pre>
            </div>
          </el-col>
        </el-row>
      </div>
      <template #footer>
        <el-button @click="testDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="generatePrompt">生成Prompt</el-button>
      </template>
    </el-dialog>

    <!-- 版本管理对话框 -->
    <el-dialog v-model="versionDialogVisible" title="Prompt版本管理" width="70%">
      <div class="version-management">
        <el-table :data="promptVersions" stripe>
          <el-table-column prop="version" label="版本" width="100" />
          <el-table-column prop="name" label="Prompt名称" min-width="200" />
          <el-table-column prop="changes" label="变更说明" min-width="250" />
          <el-table-column prop="created_at" label="创建时间" width="160" />
          <el-table-column prop="usage_count" label="使用次数" width="100" />
          <el-table-column prop="success_rate" label="成功率" width="100">
            <template #default="{ row }">
              <span v-if="row.success_rate">{{ row.success_rate }}%</span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" @click="compareVersion(row)">对比</el-button>
              <el-button size="small" type="primary" @click="restoreVersion(row)">恢复</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>

    <!-- 效果评估对话框 -->
    <el-dialog v-model="evaluationDialogVisible" title="Prompt效果评估" width="80%">
      <div class="evaluation-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="evaluation-metrics">
              <h4>性能指标</h4>
              <el-row :gutter="16">
                <el-col :span="12">
                  <div class="metric-card">
                    <div class="metric-value">{{ evaluationData.avgResponseTime }}ms</div>
                    <div class="metric-label">平均响应时间</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="metric-card">
                    <div class="metric-value">{{ evaluationData.successRate }}%</div>
                    <div class="metric-label">成功率</div>
                  </div>
                </el-col>
              </el-row>
              <el-row :gutter="16" style="margin-top: 16px;">
                <el-col :span="12">
                  <div class="metric-card">
                    <div class="metric-value">{{ evaluationData.totalUsage }}</div>
                    <div class="metric-label">总使用次数</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="metric-card">
                    <div class="metric-value">{{ evaluationData.userSatisfaction }}</div>
                    <div class="metric-label">用户满意度</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="evaluation-chart">
              <h4>使用趋势</h4>
              <div class="chart-placeholder">
                <p>使用趋势图表区域</p>
                <p>（可集成 ECharts 或其他图表库）</p>
              </div>
            </div>
          </el-col>
        </el-row>

        <el-divider />

        <div class="evaluation-feedback">
          <h4>用户反馈</h4>
          <el-table :data="evaluationData.feedback" stripe>
            <el-table-column prop="user" label="用户" width="120" />
            <el-table-column prop="rating" label="评分" width="100">
              <template #default="{ row }">
                <el-rate v-model="row.rating" disabled show-score />
              </template>
            </el-table-column>
            <el-table-column prop="comment" label="评论" min-width="200" />
            <el-table-column prop="date" label="时间" width="160" />
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import {
  Plus,
  Refresh,
  MoreFilled,
  Clock,
  TrendCharts,
  Download
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'PromptsManagement',
  components: {
    Plus,
    Refresh,
    MoreFilled,
    Clock,
    TrendCharts,
    Download
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const testDialogVisible = ref(false)
    const versionDialogVisible = ref(false)
    const evaluationDialogVisible = ref(false)
    const isEdit = ref(false)
    const prompts = ref([])
    const formRef = ref(null)
    const inputRef = ref(null)
    const inputVisible = ref(false)
    const inputValue = ref('')
    const currentPrompt = ref(null)
    const activeCategory = ref('all')
    const promptVersions = ref([])

    // 评估数据
    const evaluationData = reactive({
      avgResponseTime: 1250,
      successRate: 94.5,
      totalUsage: 1847,
      userSatisfaction: 4.6,
      feedback: [
        { user: '张三', rating: 5, comment: '效果很好，生成的内容很准确', date: '2024-01-20 15:30' },
        { user: '李四', rating: 4, comment: '基本满足需求，偶尔需要调整', date: '2024-01-19 14:20' }
      ]
    })

    // 计算属性
    const filteredPrompts = computed(() => {
      if (activeCategory.value === 'all') {
        return prompts.value
      }
      return prompts.value.filter(prompt => prompt.category === activeCategory.value)
    })

    // 表单数据
    const promptForm = reactive({
      id: '',
      name: '',
      category: '',
      description: '',
      template: '',
      variables: [],
      tags: []
    })

    // 测试变量
    const testVariables = reactive({})

    // 表单验证规则
    const formRules = {
      name: [
        { required: true, message: '请输入Prompt名称', trigger: 'blur' }
      ],
      category: [
        { required: true, message: '请选择分类', trigger: 'change' }
      ],
      template: [
        { required: true, message: '请输入模板内容', trigger: 'blur' }
      ]
    }

    // 计算属性
    const generatedPrompt = computed(() => {
      if (!currentPrompt.value) return ''
      
      let result = currentPrompt.value.template
      for (const [key, value] of Object.entries(testVariables)) {
        result = result.replace(new RegExp(`{${key}}`, 'g'), value || `{${key}}`)
      }
      return result
    })

    // 方法
    const refreshData = async () => {
      loading.value = true
      try {
        // 模拟数据
        prompts.value = [
          {
            id: 'p001',
            name: '系统角色定义',
            category: 'system',
            description: '定义AI助手的基本角色和能力',
            template: '你是一个专业的{domain}专家，具有{experience}年的经验。你的主要职责是{responsibilities}。',
            variables: [
              { name: 'domain', description: '专业领域' },
              { name: 'experience', description: '经验年数' },
              { name: 'responsibilities', description: '主要职责' }
            ],
            tags: ['系统', '角色'],
            usage_count: 25,
            updated_at: '2024-01-20 10:30:00'
          },
          {
            id: 'p002',
            name: '异常分析提示',
            category: 'user',
            description: '用于分析硬件质量异常的提示模板',
            template: '请分析以下异常情况：\n异常描述：{symptom}\n发生组件：{component}\n请提供可能的原因和解决方案。',
            variables: [
              { name: 'symptom', description: '异常症状' },
              { name: 'component', description: '相关组件' }
            ],
            tags: ['分析', '异常'],
            usage_count: 18,
            updated_at: '2024-01-19 15:20:00'
          },
          {
            id: 'p003',
            name: '词典抽取专家',
            category: 'extraction',
            description: '从技术文档中提取专业术语并构建结构化词典',
            template: `# 🎯 手机质量词典抽取专家

## 📋 角色
你是手机研发质量知识图谱构建专家，从技术文档中提取专业术语并构建结构化词典。

## 📥 输入信息
- **待处理文档**：{document_content}
- **目标领域**：手机研发制造与质量管理
- **术语数量要求**：{term_count_requirement}
- **抽取重点**：{extraction_focus}

## 📊 输出格式
严格按照以下表格格式输出：

| 术语 | 别名 | 类别 | 多标签 | 备注 |
|------|------|------|--------|------|

## 🏷️ 字段说明

### 1. 术语 (必填)
标准中文名称，如：BTB连接器、虚焊、FMEA

### 2. 别名 (推荐)
用分号分隔，如：Board-to-Board Connector;板对板连接器

### 3. 类别 (必填) - 8选1
- **Symptom**: 异常现象/故障症状 (信号弱、死机、虚焊)
- **Component**: 硬件组件/电子元件 (BTB连接器、CPU、摄像头)
- **Tool**: 检测工具/测试设备 (示波器、AQL、治具)
- **Process**: 制造工艺/质量流程 (SMT工艺、FMEA、IQC)
- **TestCase**: 测试方法/验证标准 (可靠性测试、功能测试)
- **Metric**: 性能指标/量化参数 (良率、缺陷率、MTBF)
- **Material**: 原材料/化学品 (胶水、泡棉、油墨)
- **Role**: 组织角色/岗位职责 (DQA、IQC、工艺工程师)

### 4. 多标签 (推荐2-5个)
从70个标签中选择，用分号分隔：

**领域标签**: 显示相关、影像相关、声学、射频相关、电池、充电、无线充电、通信相关、安全相关、热管理、时钟、传感器

**工艺标签**: 制造工艺、SMT、注塑、点胶、装配、封装、PCB、EMC、测试验证、失效分析、维修、操作

**质量标签**: 可靠性、ESD、质量体系、性能指标、工艺参数、外观

**生命周期标签**: 设计、硬件相关、软件相关、结构相关、项目相关、流程相关

**材料标签**: 物料、CMF、半导体、电气性能、电气连接、包装

**功能标签**: 功能、人机交互、用户体验、配件

**组织标签**: 组织职责、供应链、工具

**其他标签**: 部件、摄像头模组、ICT、线缆管理、系统稳定性等

### 5. 备注 (推荐)
50-200字，包含：定义+应用场景+重要性

## 🔍 分类速查
- 异常现象？ → Symptom | 物理组件？ → Component
- 检测设备？ → Tool | 工艺流程？ → Process
- 测试方法？ → TestCase | 量化指标？ → Metric
- 原材料？ → Material | 岗位角色？ → Role

## 📚 标准示例
| 术语 | 别名 | 类别 | 多标签 | 备注 |
|------|------|------|--------|------|
| FMEA | 潜在失效模式与后果分析;Failure Mode and Effects Analysis | Process | 质量体系;设计;可靠性;流程相关 | 系统性分析方法，识别设计或生产过程中潜在失效模式，评估后果和风险，制定预防措施。广泛应用于设计阶段和工艺改进。 |
| 虚焊 | 冷焊;假焊;Intermittent Solder Joint | Symptom | SMT;制造工艺;可靠性;电气连接 | 焊点看似连接但电气连接不稳定，时通时断的隐蔽性缺陷。通常因焊接温度不足、焊盘污染导致，是SMT工艺常见质量问题。 |

## 🎯 输出要求
1. 严格按表格格式输出
2. 每个术语占一行
3. 必填：术语、类别
4. 推荐：别名、多标签、备注
5. 质量优先：准确性胜过数量

开始时请先分析文档内容，然后直接输出术语表格。`,
            variables: [
              { name: 'document_content', description: '待处理的技术文档内容' },
              { name: 'term_count_requirement', description: '术语数量要求，如"尽可能多"或具体数字' },
              { name: 'extraction_focus', description: '抽取重点，如"重点关注异常现象"' }
            ],
            tags: ['词典', '抽取', '知识图谱'],
            usage_count: 0,
            updated_at: '2025-09-28 01:15:00',
            version: '2.0',
            success_rate: 95
          },
          {
            id: 'p004',
            name: '词典抽取专家(详细版)',
            category: 'extraction',
            description: '完整版词典抽取prompt，包含详细指导和分类决策树',
            template: `# 🎯 手机研发质量知识图谱词典抽取专家 (详细版)

## 📋 角色定义
你是一个专业的手机研发质量知识图谱构建专家，负责从技术文档中提取专业术语，并按照标准格式构建结构化词典。你具备深厚的手机制造、质量管理、硬件设计等领域专业知识。

## 📥 输入信息
- **待处理文档**：{document_content}
- **目标领域**：手机研发制造与质量管理
- **术语数量要求**：{term_count_requirement}
- **抽取重点**：{extraction_focus}

## 📊 输出格式要求
严格按照以下Markdown表格格式输出：

| 术语 | 别名 | 类别 | 多标签 | 备注 |
|------|------|------|--------|------|

## 🏷️ 字段定义详解

### 1. 术语 (必填)
- **要求**：标准中文名称，作为唯一标识
- **规范**：优先使用行业标准术语，避免口语化表达
- **示例**：BTB连接器、虚焊、FMEA

### 2. 别名 (推荐)
- **格式**：用分号(;)分隔多个别名
- **内容**：英文全称、缩写、同义词、口语化叫法
- **示例**：Board-to-Board Connector;板对板连接器

### 3. 类别 (必填) - 8选1
| 类别 | 中文名称 | 适用范围 | 示例 |
|------|----------|----------|------|
| **Symptom** | 症状/异常现象 | 故障现象、异常表现、问题症状 | 信号弱、死机、充电慢、虚焊 |
| **Component** | 组件/部件 | 硬件组件、电子元件、机械部件 | BTB连接器、CPU、摄像头、电池 |
| **Tool** | 工具/方法 | 检测工具、测试设备、分析方法 | 示波器、AQL、CCD视觉对位 |
| **Process** | 流程/工艺 | 制造工艺、质量流程、操作步骤 | SMT工艺、FMEA、IQC检验 |
| **TestCase** | 测试用例 | 测试方法、验证方案、检验标准 | 可靠性测试、功能测试、老化测试 |
| **Metric** | 性能指标 | 量化指标、性能参数、质量标准 | 良率、缺陷率、MTBF、信噪比 |
| **Material** | 物料/材料 | 原材料、辅料、化学品 | 胶水、泡棉、油墨、涂料 |
| **Role** | 角色/职责 | 组织角色、岗位职责、人员分工 | DQA、IQC、工艺工程师 |

### 4. 多标签 (推荐2-5个)
从以下70个标签中选择，用分号(;)分隔：

#### 🌐 domain (领域标签 - 13个)
显示相关、影像相关、声学、射频相关、电池、充电、无线充电、通信相关、安全相关、热管理、时钟、传感器

#### ⚙️ process (工艺流程标签 - 12个)
制造工艺、SMT、注塑、点胶、装配、封装、PCB、EMC、测试验证、失效分析、维修、操作

#### 🛡️ quality (质量标签 - 6个)
可靠性、ESD、质量体系、性能指标、工艺参数、外观

#### 🔄 lifecycle (生命周期标签 - 6个)
设计、硬件相关、软件相关、结构相关、项目相关、流程相关

#### 🧱 material (材料标签 - 6个)
物料、CMF、半导体、电气性能、电气连接、包装

#### 🎯 function (功能标签 - 4个)
功能、人机交互、用户体验、配件

#### 🏢 organization (组织标签 - 3个)
组织职责、供应链、工具

#### 🔧 other (其他标签 - 20个)
部件、摄像头模组、ICT、线缆管理、系统稳定性、系统升级、系统启动、天线、基带、增益、频段、调制、协议、兼容性、干扰、屏蔽、接地、滤波、匹配、校准、补偿

### 5. 备注 (推荐)
- **内容**：术语的标准定义、应用场景、重要性说明
- **长度**：50-200字，简洁准确
- **要素**：定义+应用场景+重要性/影响

## 💡 分类判断指南

### 🔍 分类决策树
术语性质判断：
├── 是否为异常现象/故障症状？ → Symptom
├── 是否为物理组件/电子元件？ → Component
├── 是否为检测设备/分析方法？ → Tool
├── 是否为工艺流程/操作步骤？ → Process
├── 是否为测试方法/验证标准？ → TestCase
├── 是否为量化指标/性能参数？ → Metric
├── 是否为原材料/化学品？ → Material
└── 是否为岗位角色/组织职责？ → Role

### 📋 快速参考表
| 类别 | 关键词 | 典型前缀/后缀 | 避免混淆 |
|------|--------|---------------|----------|
| **Symptom** | 异常、故障、问题、现象 | 无法、不能、异常、故障 | 非量化描述 |
| **Component** | 器件、模组、部件、元件 | -器、-头、-板、-片 | 有形物理实体 |
| **Tool** | 设备、仪器、工具、治具 | -仪、-器、-机、-台 | 用于检测/制造 |
| **Process** | 工艺、流程、方法、步骤 | -工艺、-流程、-法 | 操作性描述 |
| **TestCase** | 测试、检验、验证、标准 | -测试、-检验、-标准 | 验证性活动 |
| **Metric** | 率、度、值、指标、参数 | -率、-度、-比、-值 | 可量化数值 |
| **Material** | 料、胶、油、膜、粉 | -胶、-油、-料、-膜 | 原始材料 |
| **Role** | 师、员、手、岗、部门 | -师、-员、-手、-岗 | 人员职责 |

## 🔧 特殊处理规则

### 📝 缩写词处理
- **术语字段**：使用缩写形式（如FMEA）
- **别名字段**：包含完整英文全称和中文翻译
- **示例**：FMEA | 潜在失效模式与后果分析;Failure Mode and Effects Analysis

### 🌐 中英文混合处理
- **优先级**：中文术语 > 英文术语 > 中英混合
- **别名补充**：为中文术语补充英文别名，为英文术语补充中文别名
- **示例**：示波器 | Oscilloscope;OSC

### 🔄 重复术语处理
- **合并原则**：保留信息最完整的版本
- **别名整合**：将重复术语的不同表达形式整合为别名
- **避免冗余**：确保最终输出中每个术语唯一

## 📚 标准示例

| 术语 | 别名 | 类别 | 多标签 | 备注 |
|------|------|------|--------|------|
| FMEA | 潜在失效模式与后果分析;Failure Mode and Effects Analysis | Process | 质量体系;设计;可靠性;流程相关 | 系统性的分析方法，用于识别产品设计或生产过程中潜在的失效模式，评估其后果和风险，制定预防措施。广泛应用于设计阶段和工艺改进中。 |
| 虚焊 | 冷焊;假焊;Intermittent Solder Joint | Symptom | SMT;制造工艺;可靠性;电气连接 | 焊点看似连接但电气连接不稳定，时通时断的隐蔽性缺陷。通常因焊接温度不足、焊盘污染或助焊剂失效导致，是SMT工艺中的常见质量问题。 |
| BTB连接器 | Board-to-Board Connector;板对板连接器 | Component | 电气连接;硬件相关;结构相关;部件 | 连接主板与副板、显示模组等的重要电气连接元件。易出现接触不良、虚焊、机械损伤等故障，直接影响设备功能和可靠性。 |
| 示波器 | Oscilloscope;OSC | Tool | 工具;测试验证;电气性能;硬件相关 | 用于观察和分析电信号波形的精密电子测试仪器。在硬件调试、信号完整性分析、EMC测试等环节发挥关键作用，是电子工程师必备工具。 |

## 🎯 输出要求总结

1. **严格按照表格格式输出**，不要添加额外的格式或说明
2. **每个术语占一行**，确保表格结构完整
3. **必填字段**：术语、类别
4. **推荐字段**：别名、多标签、备注
5. **质量优先**：宁可数量少但质量高，不要为了数量牺牲准确性

开始处理文档时，请先简要分析文档内容，然后直接输出标准格式的术语表格。`,
            variables: [
              { name: 'document_content', description: '待处理的技术文档内容' },
              { name: 'term_count_requirement', description: '术语数量要求，如"尽可能多"或具体数字' },
              { name: 'extraction_focus', description: '抽取重点，如"重点关注异常现象"' }
            ],
            tags: ['词典', '抽取', '知识图谱', '详细版'],
            usage_count: 0,
            updated_at: '2025-09-28 01:15:00',
            version: '2.1',
            success_rate: 98
          },
          {
            id: 'p005',
            name: '词典质量检查专家',
            category: 'analysis',
            description: '一体化词典质量检查，涵盖基础规范、内容逻辑、重复冲突、实用价值四大维度',
            template: `# 🔍 词典质量一体化检查专家

## 📋 角色定义
你是手机研发质量词典的专业质检专家，负责对词典数据进行全面的质量检查和评估。你具备深厚的质量管理、技术标准和数据治理专业知识。

## 📥 检查对象
**待检查词典**: {dictionary_content}
**检查重点**: {check_focus}
**质量标准**: {quality_standard}

## 🎯 检查维度

### 1. 📊 基础规范检查
#### 完整性检查
- **必填字段**: 术语、别名、类别、多标签、备注五个字段必须完整
- **格式规范**: 别名和多标签使用英文分号(;)分隔
- **字段长度**: 术语2-15字符，备注20-200字符

#### 分类标准检查
- **8大标准分类**: Symptom, Component, Tool, Process, TestCase, Metric, Material, Role
- **分类准确性**: 类别必须与术语定义高度匹配
- **分类分布**: 检查各分类的数量分布是否合理

### 2. 🧠 内容逻辑检查
#### 准确性验证
- **技术准确性**: 术语定义在技术上准确无误
- **专业性**: 使用标准的行业术语和表达
- **一致性**: 相似术语的描述风格和深度保持一致

#### 关联性检查
- **类别匹配**: 类别与术语定义的高度相关性
- **标签相关**: 多标签必须与术语的应用领域相关
- **描述匹配**: 备注内容与术语的实际含义匹配

### 3. 🔄 重复冲突检查
#### 重复项识别
- **术语重复**: 检查术语名称是否完全相同
- **别名重复**: 检查核心别名是否在不同术语间重复
- **语义重复**: 识别表达不同但含义相同的术语

#### 冲突项检测
- **别名冲突**: 不同术语共享相同或易混淆的别名
- **分类冲突**: 相似术语被分配到不同类别
- **标签冲突**: 相似术语的标签分配不一致

### 4. 💎 实用价值检查
#### 价值评估
- **信息丰富度**: 备注是否提供超出简单定义的有价值信息
- **应用场景**: 是否包含实际应用场景和重要性说明
- **问题导向**: 对于Symptom类，是否说明原因和影响

#### 完善建议
- **缺失信息**: 识别可以补充的有价值信息
- **深度不足**: 指出需要增加技术深度的术语
- **实用性**: 评估术语在实际工作中的实用价值

## 📊 输出格式

### 🚨 基础问题清单 (必须修复)
| 行号 | 术语 | 问题类型 | 具体问题 | 修改建议 |
|------|------|----------|----------|----------|

### ⚠️ 逻辑与优化问题 (建议修复)
| 行号 | 术语 | 问题类型 | 具体问题 | 优化建议 |
|------|------|----------|----------|----------|

### 🔄 重复与冲突检查
- **重复术语**: [列出所有重复的术语对]
- **别名冲突**: [术语A] 与 [术语B] 共享别名 [冲突的别名]
- **语义重复**: [列出语义相同但表达不同的术语组]

### 📈 质量统计分析
- **总词条数**: X条
- **完整性**: X% (X条完整/X条总数)
- **分类分布**: 各类别数量和占比
- **标签使用**: 热门标签和使用频率
- **平均质量分**: X/10分

### 🎯 整体评价与改进建议

#### ✅ 主要优点
1. [词典的主要优势]
2. [数据质量的亮点]
3. [标准化程度的评价]

#### 🔧 关键改进项 (优先级排序)
1. **高优先级**: [最关键的问题和改进建议]
2. **中优先级**: [重要但不紧急的问题]
3. **低优先级**: [优化性质的建议]

#### 📊 质量提升路径
1. **立即修复**: [必须立即解决的问题]
2. **短期改进**: [1-2周内可以完成的优化]
3. **长期完善**: [持续改进的方向]

## 🔍 检查标准参考

### 📋 分类判断标准
- **Symptom**: 异常现象、故障症状、问题表现
- **Component**: 硬件组件、电子元件、物理部件
- **Tool**: 检测工具、测试设备、分析方法
- **Process**: 制造工艺、质量流程、操作步骤
- **TestCase**: 测试方法、验证标准、检验程序
- **Metric**: 性能指标、量化参数、评估标准
- **Material**: 原材料、化学品、辅助材料
- **Role**: 组织角色、岗位职责、人员分工

### 🏷️ 标签体系参考
**领域标签**: 显示相关、影像相关、声学、射频相关、电池、充电等
**工艺标签**: 制造工艺、SMT、注塑、点胶、装配、封装等
**质量标签**: 可靠性、ESD、质量体系、性能指标、外观等
**生命周期标签**: 设计、硬件相关、软件相关、结构相关等

### ✅ 质量评分标准
- **9-10分**: 优秀 - 完全符合标准，信息丰富，实用价值高
- **7-8分**: 良好 - 基本符合标准，信息较完整，有一定价值
- **5-6分**: 一般 - 符合基本要求，信息不够丰富，价值有限
- **3-4分**: 较差 - 存在明显问题，信息不完整，需要改进
- **1-2分**: 很差 - 严重不符合标准，信息错误或缺失严重

## 🎯 检查执行要求

1. **全面性**: 对每个词条进行逐一检查，不遗漏任何问题
2. **准确性**: 基于专业知识和标准进行准确判断
3. **实用性**: 提供具体、可操作的改进建议
4. **优先级**: 明确区分问题的严重程度和修复优先级
5. **建设性**: 不仅指出问题，更要提供解决方案

开始检查时，请先分析词典的整体结构和规模，然后按照上述四个维度进行系统性检查，最后输出完整的质量检查报告。`,
            variables: [
              { name: 'dictionary_content', description: '待检查的词典内容（CSV格式或表格格式）' },
              { name: 'check_focus', description: '检查重点，如"重点检查分类准确性"' },
              { name: 'quality_standard', description: '质量标准要求，如"企业级标准"' }
            ],
            tags: ['质量检查', '数据治理', '词典管理'],
            usage_count: 0,
            updated_at: '2025-09-28 01:55:00',
            version: '1.0',
            success_rate: 96
          }
        ]
      } catch (error) {
        console.error('获取Prompt列表失败:', error)
        ElMessage.error('获取Prompt列表失败')
      } finally {
        loading.value = false
      }
    }

    const showAddDialog = () => {
      isEdit.value = false
      dialogVisible.value = true
      resetForm()
    }

    const editPrompt = (prompt) => {
      isEdit.value = true
      Object.assign(promptForm, {
        ...prompt,
        variables: [...(prompt.variables || [])],
        tags: [...(prompt.tags || [])]
      })
      dialogVisible.value = true
    }

    const resetForm = () => {
      Object.assign(promptForm, {
        id: '',
        name: '',
        category: '',
        description: '',
        template: '',
        variables: [],
        tags: []
      })
      formRef.value?.resetFields()
    }

    const savePrompt = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value?.validate()
        saving.value = true
        
        // 模拟保存
        ElMessage.success(isEdit.value ? 'Prompt更新成功' : 'Prompt创建成功')
        dialogVisible.value = false
        refreshData()
      } catch (error) {
        console.error('保存Prompt失败:', error)
        ElMessage.error('保存Prompt失败')
      } finally {
        saving.value = false
      }
    }

    const deletePrompt = async (prompt) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除Prompt "${prompt.name}" 吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        ElMessage.success('Prompt删除成功')
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除Prompt失败:', error)
          ElMessage.error('删除Prompt失败')
        }
      }
    }

    const testPrompt = (prompt) => {
      currentPrompt.value = prompt
      // 初始化测试变量
      Object.keys(testVariables).forEach(key => {
        delete testVariables[key]
      })
      prompt.variables?.forEach(variable => {
        testVariables[variable.name] = ''
      })
      testDialogVisible.value = true
    }

    const duplicatePrompt = (prompt) => {
      const newPrompt = {
        ...prompt,
        id: '',
        name: prompt.name + ' (副本)',
        usage_count: 0
      }
      editPrompt(newPrompt)
    }

    const generatePrompt = () => {
      // 生成结果已通过计算属性实现
      ElMessage.success('Prompt生成完成')
    }

    // 变量管理
    const addVariable = () => {
      promptForm.variables.push({ name: '', description: '' })
    }

    const removeVariable = (index) => {
      promptForm.variables.splice(index, 1)
    }

    // 标签管理
    const removeTag = (tag) => {
      const index = promptForm.tags.indexOf(tag)
      if (index > -1) {
        promptForm.tags.splice(index, 1)
      }
    }

    const showInput = () => {
      inputVisible.value = true
      nextTick(() => {
        inputRef.value?.focus()
      })
    }

    const handleInputConfirm = () => {
      if (inputValue.value && !promptForm.tags.includes(inputValue.value)) {
        promptForm.tags.push(inputValue.value)
      }
      inputVisible.value = false
      inputValue.value = ''
    }

    // 辅助方法
    const getPromptPreview = (template) => {
      return template.length > 100 ? template.substring(0, 100) + '...' : template
    }

    const getCategoryColor = (category) => {
      const colors = {
        system: 'primary',
        user: 'success',
        assistant: 'warning',
        tool: 'info'
      }
      return colors[category] || 'info'
    }

    const formatTime = (time) => {
      return time ? new Date(time).toLocaleDateString() : ''
    }

    // 新增方法
    const handleCategoryChange = (category) => {
      activeCategory.value = category
    }

    const getPromptCountByCategory = (category) => {
      return prompts.value.filter(prompt => prompt.category === category).length
    }

    const showVersionDialog = () => {
      // 模拟版本数据
      promptVersions.value = [
        {
          version: '1.2',
          name: '词典抽取优化版',
          changes: '优化了实体识别准确率，增加了上下文理解',
          created_at: '2024-01-20 15:30',
          usage_count: 156,
          success_rate: 94.5
        },
        {
          version: '1.1',
          name: '词典抽取基础版',
          changes: '基础的词典信息抽取功能',
          created_at: '2024-01-15 10:20',
          usage_count: 89,
          success_rate: 87.2
        }
      ]
      versionDialogVisible.value = true
    }

    const showEvaluationDialog = () => {
      evaluationDialogVisible.value = true
    }

    const exportPrompts = () => {
      try {
        const data = JSON.stringify(filteredPrompts.value, null, 2)
        const blob = new Blob([data], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `prompts_${activeCategory.value}_${new Date().toISOString().slice(0, 10)}.json`
        link.click()
        window.URL.revokeObjectURL(url)
        ElMessage.success('Prompt导出成功')
      } catch (error) {
        ElMessage.error('Prompt导出失败')
      }
    }

    const compareVersion = (version) => {
      ElMessage.info(`对比版本 ${version.version} 功能开发中...`)
    }

    const restoreVersion = async (version) => {
      try {
        await ElMessageBox.confirm(
          `确定要恢复到版本 ${version.version} 吗？`,
          '确认恢复',
          { type: 'warning' }
        )
        ElMessage.success('版本恢复成功')
        versionDialogVisible.value = false
        refreshData()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('版本恢复失败')
        }
      }
    }

    // 生命周期
    onMounted(() => {
      refreshData()
    })

    return {
      loading,
      saving,
      dialogVisible,
      testDialogVisible,
      versionDialogVisible,
      evaluationDialogVisible,
      isEdit,
      prompts,
      formRef,
      inputRef,
      inputVisible,
      inputValue,
      currentPrompt,
      activeCategory,
      promptVersions,
      evaluationData,
      filteredPrompts,
      promptForm,
      testVariables,
      formRules,
      generatedPrompt,
      refreshData,
      showAddDialog,
      editPrompt,
      resetForm,
      savePrompt,
      deletePrompt,
      testPrompt,
      duplicatePrompt,
      generatePrompt,
      addVariable,
      removeVariable,
      removeTag,
      showInput,
      handleInputConfirm,
      handleCategoryChange,
      getPromptCountByCategory,
      showVersionDialog,
      showEvaluationDialog,
      exportPrompts,
      compareVersion,
      restoreVersion,
      getPromptPreview,
      getCategoryColor,
      formatTime
    }
  }
}
</script>

<style scoped>
.prompts-management {
  height: 100%;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.action-left h3 {
  margin: 0 0 4px 0;
  color: #303133;
}

.prompt-count {
  color: #909399;
  font-size: 14px;
}

.action-right {
  display: flex;
  gap: 12px;
}

/* 分类过滤样式 */
.category-filter {
  margin-bottom: 24px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.category-filter :deep(.el-radio-button__inner) {
  border-radius: 6px;
  margin-right: 8px;
  border: 1px solid #dcdfe6;
  background: white;
  color: #606266;
}

.category-filter :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: #409eff;
  border-color: #409eff;
  color: white;
}

.prompts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.prompt-card {
  background: white;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.prompt-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.prompt-info h4 {
  margin: 0 0 4px 0;
  color: #303133;
  font-size: 16px;
}

.prompt-category {
  color: #909399;
  font-size: 12px;
}

.card-content {
  margin-bottom: 12px;
}

.prompt-description {
  color: #606266;
  font-size: 14px;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.prompt-preview {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 8px;
  font-size: 12px;
  max-height: 80px;
  overflow: hidden;
}

.prompt-preview pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #606266;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f2f5;
}

.prompt-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.update-time {
  color: #909399;
  font-size: 12px;
}

.usage-count {
  color: #909399;
  font-size: 12px;
}

.variables-editor {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 12px;
  background: #fafafa;
}

.variable-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.variable-item:last-child {
  margin-bottom: 0;
}

.test-content {
  max-height: 500px;
  overflow-y: auto;
}

.test-result {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
  min-height: 200px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 版本管理样式 */
.version-management {
  max-height: 500px;
  overflow-y: auto;
}

/* 效果评估样式 */
.evaluation-content {
  max-height: 600px;
  overflow-y: auto;
}

.evaluation-metrics h4,
.evaluation-chart h4,
.evaluation-feedback h4 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 16px;
}

.metric-card {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}

.metric-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 14px;
  color: #909399;
}

.chart-placeholder {
  height: 200px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  border: 2px dashed #dcdfe6;
}

.chart-placeholder p {
  margin: 4px 0;
}
</style>
