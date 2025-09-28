// Mock API 数据和响应
export const mockData = {
  // 系统状态
  systemStatus: {
    success: true,
    data: {
      currentVersion: 'v1.2.3',
      totalRules: 156,
      totalPrompts: 89,
      totalScenarios: 23,
      totalAgents: 12,
      systemHealth: {
        cpu: { value: 45, status: 'normal' },
        memory: { value: 68, status: 'normal' },
        disk: { value: 32, status: 'normal' },
        network: { value: 12, status: 'normal' }
      },
      uptime: '15天 8小时 32分钟',
      lastUpdate: '2024-01-20 15:30:00'
    }
  },

  // 规则列表
  rules: {
    success: true,
    data: [
      {
        rule_id: 'RULE_001',
        name: '产品名称标准化',
        type: 'document_parsing',
        priority: 'high',
        description: '统一产品名称格式，去除特殊字符',
        logic: 'CLEAN(TRIM(product_name))',
        error_message: '产品名称格式不符合规范',
        status: 'active',
        created_at: '2024-01-15 10:30:00',
        updated_at: '2024-01-20 14:25:00'
      },
      {
        rule_id: 'RULE_002',
        name: '质量等级映射',
        type: 'data_normalization',
        priority: 'medium',
        description: '将不同来源的质量等级统一为标准格式',
        logic: 'MAP(quality_level, quality_mapping_table)',
        error_message: '质量等级映射失败',
        status: 'active',
        created_at: '2024-01-16 09:15:00',
        updated_at: '2024-01-18 16:40:00'
      },
      {
        rule_id: 'RULE_003',
        name: '供应商信息验证',
        type: 'data_validation',
        priority: 'high',
        description: '验证供应商信息的完整性和准确性',
        logic: 'VALIDATE(supplier_info, supplier_schema)',
        error_message: '供应商信息验证失败',
        status: 'inactive',
        created_at: '2024-01-17 14:20:00',
        updated_at: '2024-01-19 11:10:00'
      }
    ]
  },

  // Prompt列表
  prompts: {
    success: true,
    data: [
      {
        id: 'PROMPT_001',
        name: '实体抽取提示词',
        category: 'entity_extraction',
        content: '请从以下文本中提取产品实体信息，包括产品名称、型号、规格等...',
        variables: ['text', 'entity_types'],
        status: 'active',
        usage_count: 1250,
        created_at: '2024-01-10 09:00:00'
      },
      {
        id: 'PROMPT_002',
        name: '关系识别提示词',
        category: 'relation_extraction',
        content: '分析文本中实体之间的关系，识别产品与供应商、产品与组件之间的关联...',
        variables: ['entities', 'context'],
        status: 'active',
        usage_count: 890,
        created_at: '2024-01-12 14:30:00'
      }
    ]
  },

  // 场景列表
  scenarios: {
    success: true,
    data: [
      {
        id: 'SCENARIO_001',
        name: '产品质量分析',
        description: '分析产品质量数据，识别质量问题和改进机会',
        category: 'quality_analysis',
        steps: [
          { order: 1, action: 'data_collection', description: '收集产品质量数据' },
          { order: 2, action: 'data_processing', description: '数据清洗和标准化' },
          { order: 3, action: 'analysis', description: '质量分析和问题识别' }
        ],
        status: 'active',
        usage_count: 45,
        created_at: '2024-01-08 11:20:00'
      }
    ]
  },

  // 版本列表
  versions: {
    success: true,
    data: [
      {
        version: 'v1.2.3',
        type: 'patch',
        description: '修复若干bug，优化性能',
        changes: [
          { type: 'fix', description: '修复规则执行异常问题' },
          { type: 'improvement', description: '优化数据处理性能' }
        ],
        release_date: '2024-01-20 10:00:00',
        status: 'current'
      },
      {
        version: 'v1.2.2',
        type: 'patch',
        description: '安全更新和bug修复',
        changes: [
          { type: 'security', description: '修复安全漏洞' },
          { type: 'fix', description: '修复数据导入问题' }
        ],
        release_date: '2024-01-15 15:30:00',
        status: 'released'
      }
    ]
  }
}

// Mock API 响应函数
export const mockApi = {
  // 模拟网络延迟
  delay: (ms = 500) => new Promise(resolve => setTimeout(resolve, ms)),

  // 系统状态
  async getSystemStatus() {
    await this.delay()
    return mockData.systemStatus
  },

  // 规则管理
  async getRules() {
    await this.delay()
    return mockData.rules
  },

  async createRule(rule) {
    await this.delay()
    return { success: true, message: '规则创建成功', data: { ...rule, rule_id: `RULE_${Date.now()}` } }
  },

  async updateRule(ruleId, rule) {
    await this.delay()
    return { success: true, message: '规则更新成功', data: rule }
  },

  async deleteRule(ruleId) {
    await this.delay()
    return { success: true, message: '规则删除成功' }
  },

  async testRule(testData) {
    await this.delay()
    return {
      success: true,
      data: {
        result: 'passed',
        output: '测试通过',
        execution_time: '0.25s'
      }
    }
  },

  // Prompt管理
  async getPrompts() {
    await this.delay()
    return mockData.prompts
  },

  // 场景管理
  async getScenarios() {
    await this.delay()
    return mockData.scenarios
  },

  // 版本管理
  async getVersions() {
    await this.delay()
    return mockData.versions
  },

  async publishVersion(versionData) {
    await this.delay()
    return { success: true, message: '版本发布成功' }
  },

  // 图谱可视化数据
  async getGraphVisualizationData() {
    await this.delay()
    return {
      success: true,
      data: {
        nodes: [
          {
            id: 'product_001',
            name: '智能手机X1',
            category: 'product',
            value: 100,
            symbolSize: 60,
            properties: {
              type: '电子产品',
              brand: 'TechCorp',
              model: 'X1-Pro',
              quality_score: 95
            }
          },
          {
            id: 'component_001',
            name: 'A15处理器',
            category: 'component',
            value: 80,
            symbolSize: 45,
            properties: {
              type: '处理器',
              manufacturer: 'ChipMaker',
              performance: '高性能',
              power_consumption: '低功耗'
            }
          },
          {
            id: 'supplier_001',
            name: '华强电子',
            category: 'supplier',
            value: 70,
            symbolSize: 40,
            properties: {
              type: '供应商',
              location: '深圳',
              rating: 'A级',
              cooperation_years: 5
            }
          },
          {
            id: 'material_001',
            name: '铝合金外壳',
            category: 'material',
            value: 60,
            symbolSize: 35,
            properties: {
              type: '材料',
              grade: '6061-T6',
              strength: '高强度',
              weight: '轻量化'
            }
          },
          {
            id: 'quality_001',
            name: '质量检测报告',
            category: 'quality',
            value: 50,
            symbolSize: 30,
            properties: {
              type: '质量文档',
              test_date: '2024-01-20',
              result: '合格',
              score: 98
            }
          }
        ],
        links: [
          {
            source: 'product_001',
            target: 'component_001',
            relation: '包含',
            value: 10
          },
          {
            source: 'component_001',
            target: 'supplier_001',
            relation: '供应',
            value: 8
          },
          {
            source: 'product_001',
            target: 'material_001',
            relation: '使用',
            value: 6
          },
          {
            source: 'material_001',
            target: 'supplier_001',
            relation: '供应',
            value: 7
          },
          {
            source: 'product_001',
            target: 'quality_001',
            relation: '检测',
            value: 9
          }
        ],
        categories: [
          { name: 'product', itemStyle: { color: '#5470c6' } },
          { name: 'component', itemStyle: { color: '#91cc75' } },
          { name: 'supplier', itemStyle: { color: '#fac858' } },
          { name: 'material', itemStyle: { color: '#ee6666' } },
          { name: 'quality', itemStyle: { color: '#73c0de' } }
        ]
      }
    }
  },

  // 获取实时图谱统计
  async getRealGraphStats() {
    await this.delay()
    return {
      success: true,
      data: {
        total_nodes: 1250,
        total_relations: 3420,
        node_types: {
          product: 156,
          component: 423,
          supplier: 89,
          material: 234,
          quality: 348
        },
        last_update: '2024-01-20 15:30:00'
      }
    }
  },

  // 获取图谱统计
  async getGraphStats() {
    await this.delay()
    return {
      success: true,
      data: {
        total_entities: 1250,
        total_relations: 3420,
        entity_types: {
          product: 156,
          component: 423,
          supplier: 89,
          material: 234,
          quality: 348
        },
        relation_types: {
          contains: 890,
          supplies: 567,
          uses: 432,
          tests: 234,
          produces: 189
        }
      }
    }
  },

  // 获取文件列表
  async getFiles() {
    await this.delay()
    return {
      success: true,
      data: [
        {
          filename: 'product_specs.xlsx',
          size: '2.5MB',
          upload_time: '2024-01-20 14:30:00',
          status: 'processed'
        },
        {
          filename: 'supplier_info.csv',
          size: '1.2MB',
          upload_time: '2024-01-20 13:15:00',
          status: 'processed'
        },
        {
          filename: 'quality_reports.pdf',
          size: '5.8MB',
          upload_time: '2024-01-20 12:00:00',
          status: 'pending'
        }
      ]
    }
  },

  // 健康检查
  async healthCheck() {
    await this.delay(200)
    return {
      success: true,
      status: 'healthy',
      timestamp: new Date().toISOString()
    }
  },

  // 词典管理
  async getDictionary(params = {}) {
    await this.delay()
    return {
      success: true,
      data: {
        entries: [
          {
            term: '智能手机',
            category: '电子产品',
            sub_category: '通信设备',
            aliases: ['手机', '移动电话', 'smartphone'],
            tags: ['电子', '通信', '移动'],
            description: '具有智能操作系统的移动通信设备',
            source: '产品规格书',
            status: 'active'
          },
          {
            term: 'CPU',
            category: '硬件组件',
            sub_category: '处理器',
            aliases: ['中央处理器', '处理器', 'Central Processing Unit'],
            tags: ['硬件', '计算', '芯片'],
            description: '计算机的中央处理单元，负责执行指令和运算',
            source: '技术文档',
            status: 'active'
          },
          {
            term: '质量检测',
            category: '测试流程',
            sub_category: '质量保证',
            aliases: ['QA', '质检', '品质检验'],
            tags: ['质量', '测试', '检验'],
            description: '对产品质量进行检验和测试的过程',
            source: '质量手册',
            status: 'active'
          },
          {
            term: '供应商',
            category: '业务实体',
            sub_category: '合作伙伴',
            aliases: ['供货商', '厂商', 'supplier'],
            tags: ['供应链', '合作', '采购'],
            description: '为企业提供原材料、零部件或服务的外部组织',
            source: '供应商管理系统',
            status: 'active'
          },
          {
            term: '铝合金',
            category: '材料',
            sub_category: '金属材料',
            aliases: ['铝材', 'aluminum alloy'],
            tags: ['材料', '金属', '轻量化'],
            description: '以铝为主要成分的合金材料，具有轻质高强的特点',
            source: '材料规格书',
            status: 'active'
          }
        ],
        total: 5,
        page: 1,
        page_size: params.page_size || 20
      }
    }
  }
}
