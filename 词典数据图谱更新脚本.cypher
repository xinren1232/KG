// 词典数据图谱更新脚本
// 生成时间: 2025-09-26T09:43:14.337563
// 数据条数: 1192

CREATE (d:Dictionary {
    id: 'TERM_0001',
    name: 'BTB连接器',
    type: '其他',
    category: 'components',
    aliases: ['板对板连接器;Board-to-Board Connector'],
    tags: ['部件;电气连接'],
    description: '连接主板与副板、显示模组等的重要元件，易出现接触不良、虚焊等故障。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0002',
    name: 'CMF',
    type: '其他',
    category: 'components',
    aliases: ['颜色、材料、表面处理;Color', 'Material', 'Finishing'],
    tags: ['设计;外观'],
    description: '决定手机外观质感的关键，涉及喷涂、阳极氧化、镀膜等工艺。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0003',
    name: 'Dome片',
    type: '其他',
    category: 'components',
    aliases: ['按键弹片;Metal Dome'],
    tags: ['部件;人机交互'],
    description: '提供按键手感的关键金属件，失效会导致按键无反应或手感差。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0004',
    name: 'FPC',
    type: '其他',
    category: 'components',
    aliases: ['柔性电路板;Flexible Printed Circuit'],
    tags: ['部件;电气连接'],
    description: '用于连接空间受限的部件，如摄像头、显示屏，易发生弯折断裂。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0005',
    name: 'FPS',
    type: '其他',
    category: 'components',
    aliases: ['帧率;Frames Per Second'],
    tags: ['性能指标;软件相关'],
    description: '衡量界面或游戏流畅度的关键指标，帧率过低会导致卡顿。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0006',
    name: 'Gap',
    type: '其他',
    category: 'components',
    aliases: ['间隙;面差'],
    tags: ['外观;装配'],
    description: '指手机外壳部件之间的间隙和高度差，是衡量装配精度和美观度的重要指标。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0007',
    name: 'Lens',
    type: '其他',
    category: 'components',
    aliases: ['镜片;Camera Lens'],
    tags: ['部件;影像相关'],
    description: '摄像头的光学镜片，有脏污、划伤、镀膜脱落等不良现象。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0008',
    name: 'LRA',
    type: '其他',
    category: 'components',
    aliases: ['线性谐振执行器;Linear Resonant Actuator'],
    tags: ['部件;人机交互'],
    description: '提供振动反馈的马达，失效或性能不佳会导致振动弱、异响。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0009',
    name: 'OIS',
    type: '其他',
    category: 'components',
    aliases: ['光学防抖;Optical Image Stabilization'],
    tags: ['功能;影像相关'],
    description: '通过镜组或传感器移动补偿手抖，模块不良会导致拍照模糊或异响。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0010',
    name: 'SPK',
    type: '其他',
    category: 'components',
    aliases: ['扬声器;Speaker'],
    tags: ['部件;声学'],
    description: '负责声音外放，常见不良有杂音、破音、无声。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0011',
    name: 'TP',
    type: '其他',
    category: 'components',
    aliases: ['触摸屏;Touch Panel'],
    tags: ['部件;人机交互'],
    description: '负责触控功能，常见故障有失灵、乱点、划线不良。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0012',
    name: 'WLAN',
    type: '其他',
    category: 'components',
    aliases: ['无线局域网;Wireless LAN'],
    tags: ['功能;性能指标'],
    description: '手机Wi-Fi功能，常见问题有连接失败、速率慢、断流。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0013',
    name: '包材',
    type: '其他',
    category: 'components',
    aliases: ['包装材料;Packaging Material'],
    tags: ['物料;外观'],
    description: '指手机零售包装盒、内托等，破损、污渍会影响开箱体验。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0014',
    name: '背光',
    type: '其他',
    category: 'components',
    aliases: ['背光模组;Backlight'],
    tags: ['部件;显示相关'],
    description: '为LCD屏幕提供光源的组件，常见不良有亮度不均、漏光、mura（斑驳）。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0015',
    name: '边框',
    type: '其他',
    category: 'components',
    aliases: ['中框;Middle Frame'],
    tags: ['部件;外观'],
    description: '手机的骨架结构，用于固定内部元件，变形或腐蚀会影响整机强度和气密性。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0016',
    name: '充电口',
    type: '其他',
    category: 'components',
    aliases: ['USB-C接口;Type-C Port'],
    tags: ['部件;电气连接'],
    description: '负责充电和数据传输，常见不良有端口松动、腐蚀、连接不稳定。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0017',
    name: '触点',
    type: '其他',
    category: 'components',
    aliases: ['金手指;Contact Pin'],
    tags: ['部件;电气连接'],
    description: '电池、屏幕等模块上与主板连接的导电触点，氧化或污染会导致接触不良。',
    created_at: '2025-09-26T09:43:14.246487',
    updated_at: '2025-09-26T09:43:14.246487'
});
CREATE (d:Dictionary {
    id: 'TERM_0018',
    name: '电芯',
    type: '其他',
    category: 'components',
    aliases: ['电池芯;Battery Cell'],
    tags: ['部件;安全相关'],
    description: '电池的核心储能部件，其质量直接决定电池的容量、寿命和安全性。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0019',
    name: '飞线',
    type: '其他',
    category: 'components',
    aliases: ['跳线;Jumper Wire'],
    tags: ['部件;PCB'],
    description: '在PCB上用于临时或永久修复电路连接的导线，影响可靠性和美观。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0020',
    name: '盖板',
    type: '其他',
    category: 'components',
    aliases: ['玻璃盖板;Cover Glass'],
    tags: ['部件;外观'],
    description: '保护屏幕和装饰的前盖玻璃，要求高硬度、抗冲击和良好的光学性能。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0021',
    name: '高光',
    type: '其他',
    category: 'components',
    aliases: ['镜面效果;High-Gloss'],
    tags: ['外观;CMF'],
    description: '通过高精度加工得到的镜面般的光泽效果，易出现划伤、橘皮等不良。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0022',
    name: '隔磁片',
    type: '其他',
    category: 'components',
    aliases: ['磁性屏蔽片;Magnetic Shielding Sheet'],
    tags: ['部件;EMC'],
    description: '贴在器件上防止磁场干扰的薄片，粘贴不良或破损会影响无线充电或传感器性能。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0023',
    name: '公差',
    type: '其他',
    category: 'components',
    aliases: ['尺寸公差;Tolerance'],
    tags: ['设计;工艺参数'],
    description: '允许的尺寸变动范围，合理的公差设计是保证装配性和功能的关键。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0024',
    name: '公母座',
    type: '其他',
    category: 'components',
    aliases: ['插头与插座;Connector Pair'],
    tags: ['部件;电气连接'],
    description: '配对的连接器，如USB公座和母座，存在插拔力不良、寿命不足等风险。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0025',
    name: '功耗',
    type: '其他',
    category: 'components',
    aliases: ['功率消耗;Power Consumption'],
    tags: ['硬件相关;软件相关'],
    description: '手机工作时的电能消耗，是衡量续航能力的关键，异常功耗需重点分析。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0026',
    name: '光感',
    type: '其他',
    category: 'components',
    aliases: ['环境光传感器;Ambient Light Sensor'],
    tags: ['部件;传感器'],
    description: '用于自动调节屏幕亮度，被遮挡或失效会导致屏幕亮度调节失常。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0027',
    name: '滚轴',
    type: '其他',
    category: 'components',
    aliases: ['铰链;Hinge'],
    tags: ['部件;可靠性'],
    description: '折叠屏手机的关键部件，负责屏幕弯折，对疲劳寿命和顺滑度要求极高。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0028',
    name: '过孔',
    type: '其他',
    category: 'components',
    aliases: ['导通孔;Via'],
    tags: ['PCB;工艺参数'],
    description: 'PCB上用于连接不同层电路的孔，孔铜不良会导致开路或可靠性问题。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0029',
    name: '焊盘',
    type: '其他',
    category: 'components',
    aliases: ['焊点;Pad'],
    tags: ['PCB;SMT'],
    description: 'PCB上用于焊接元件的金属区域，氧化或污染会导致上锡不良、虚焊。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0030',
    name: '基带',
    type: '其他',
    category: 'components',
    aliases: ['Baseband'],
    tags: ['部件;通信相关'],
    description: '负责移动网络信号处理的芯片组，其软件和硬件故障会导致无服务、通话中断。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0031',
    name: '基板',
    type: '其他',
    category: 'components',
    aliases: ['衬底;Substrate'],
    tags: ['部件;PCB'],
    description: '承载芯片和电路的基底材料，如陶瓷基板、BT基板等。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0032',
    name: '极耳',
    type: '其他',
    category: 'components',
    aliases: ['电池极耳; Battery Tab'],
    tags: ['部件;安全相关'],
    description: '电芯正负极引出的金属带，焊接不良或折断会导致电池无法充电或工作。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0033',
    name: '铰链',
    type: '其他',
    category: 'components',
    aliases: ['转轴;Hinge'],
    tags: ['部件;可靠性'],
    description: '折叠屏手机的核心机构，要求高寿命、顺滑度和稳定性。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0034',
    name: '接地点',
    type: '其他',
    category: 'components',
    aliases: ['接地位置;Grounding Point'],
    tags: ['EMC;PCB'],
    description: 'PCB上用于连接参考电位的点，设计不良会导致EMC问题或信号干扰。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0035',
    name: '金线',
    type: '其他',
    category: 'components',
    aliases: ['键合线;Bonding Wire'],
    tags: ['部件;封装'],
    description: '芯片封装内部连接芯片焊盘和引线框架的细金属线，断裂会导致开路。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0036',
    name: '晶振',
    type: '其他',
    category: 'components',
    aliases: ['晶体振荡器;Crystal Oscillator'],
    tags: ['部件;时钟'],
    description: '提供系统基准时钟信号的元件，失效会导致手机无法开机或功能紊乱。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0037',
    name: '镜座',
    type: '其他',
    category: 'components',
    aliases: ['镜头座;Lens Holder'],
    tags: ['部件;摄像头模组'],
    description: '固定摄像头镜头的结构件，其加工精度和稳定性直接影响成像质量。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0038',
    name: '卡托',
    type: '其他',
    category: 'components',
    aliases: ['SIM卡托;SIM Card Tray'],
    tags: ['部件;外观'],
    description: '承载SIM卡和内存卡的可拆卸部件，存在装配不顺、易脱落等风险。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0039',
    name: '拉拔力',
    type: '其他',
    category: 'components',
    aliases: ['插拔力;Insertion/Extraction Force'],
    tags: ['硬件相关;可靠性'],
    description: '将连接器插入或拔出的力，过小导致接触不良，过大会影响用户体验和寿命。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0040',
    name: '良率',
    type: '其他',
    category: 'components',
    aliases: ['yield'],
    tags: ['制造工艺;质量体系'],
    description: '合格品数量与生产总数量的比率，是衡量制造水平的核心指标。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0041',
    name: '马鞍',
    type: '其他',
    category: 'components',
    aliases: ['中框马鞍区;Middle Frame Saddle'],
    tags: ['部件;设计'],
    description: '手机中框两侧收窄的区域，是结构强度和信号设计的重点区域。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0042',
    name: '盲孔',
    type: '其他',
    category: 'components',
    aliases: ['盲埋孔;Blind Via'],
    tags: ['PCB;设计'],
    description: '仅连接PCB外层和内层，但不穿透整个板的导通孔，用于高密度布线。',
    created_at: '2025-09-26T09:43:14.247490',
    updated_at: '2025-09-26T09:43:14.247490'
});
CREATE (d:Dictionary {
    id: 'TERM_0043',
    name: '门限',
    type: '其他',
    category: 'components',
    aliases: ['阈值;Threshold'],
    tags: ['测试验证;软件相关'],
    description: '触发某种动作或判断合格与否的临界值，如功耗门限、信号强度门限。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0044',
    name: '密封圈',
    type: '其他',
    category: 'components',
    aliases: ['密封胶圈;Sealing Ring'],
    tags: ['部件;可靠性'],
    description: '用于防水设计的橡胶或硅胶圈，其压缩量和弹性决定密封效果。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0045',
    name: '膜厚',
    type: '其他',
    category: 'components',
    aliases: ['涂层厚度;Coating Thickness'],
    tags: ['CMF;制造工艺'],
    description: '喷涂、电镀等表面处理层的厚度，影响外观、手感和性能。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0046',
    name: '摩擦',
    type: '其他',
    category: 'components',
    aliases: ['耐磨性;Abrasion Resistance'],
    tags: ['可靠性;外观'],
    description: '材料表面抵抗刮擦和磨损的能力，通常通过摩擦测试来验证。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0047',
    name: '母排',
    type: '其他',
    category: 'components',
    aliases: ['电池母排;Battery FPC'],
    tags: ['部件;电气连接'],
    description: '连接电池保护板和电芯的柔性电路板，其设计和可靠性至关重要。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0048',
    name: '内阻',
    type: '其他',
    category: 'components',
    aliases: ['内部电阻;Internal Resistance'],
    tags: ['硬件相关;电池'],
    description: '电池本身所具有的电阻，内阻增大会导致输出电压下降和发热。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0049',
    name: '粘附',
    type: '其他',
    category: 'components',
    aliases: ['附着力;Adhesion'],
    tags: ['制造工艺;可靠性'],
    description: '涂层、镀层或胶带与基材之间的结合强度，附着力不足会导致脱落。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0050',
    name: '粘锡',
    type: '其他',
    category: 'components',
    aliases: ['焊盘沾锡;Pad Wetting'],
    tags: ['SMT;制造工艺'],
    description: '熔化的焊锡在焊盘上铺展的能力，是形成良好焊点的基础。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0051',
    name: '扭力',
    type: '其他',
    category: 'components',
    aliases: ['扭矩;Torque'],
    tags: ['工具;结构相关'],
    description: '拧紧螺丝所需的力矩，有规定的标准值，过小或过大都有风险。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0052',
    name: '排线',
    type: '其他',
    category: 'components',
    aliases: ['柔性排线;Flex Cable'],
    tags: ['部件;电气连接'],
    description: '连接主板与屏幕、摄像头等部件的软性线路，弯折过度易断裂。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0053',
    name: '平顺',
    type: '其他',
    category: 'components',
    aliases: ['平整度;Flatness'],
    tags: ['结构相关;外观'],
    description: '表面相对于理想平面的偏差程度，影响装配和美观。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0054',
    name: '气密',
    type: '其他',
    category: 'components',
    aliases: ['气密性;Air Tightness'],
    tags: ['结构相关;可靠性'],
    description: '产品防止气体渗透的能力，是防水防尘设计的关键指标。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0055',
    name: '亲水',
    type: '其他',
    category: 'components',
    aliases: ['亲水性;Hydrophilic'],
    tags: ['CMF;可靠性'],
    description: '材料表面容易被水润湿的特性，与疏水性相对。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0056',
    name: '润湿',
    type: '其他',
    category: 'components',
    aliases: ['焊锡润湿;Solder Wetting'],
    tags: ['SMT;制造工艺'],
    description: '熔融焊锡在金属表面铺展并形成冶金结合的过程，是良好焊接的前提。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0057',
    name: '色牢',
    type: '其他',
    category: 'components',
    aliases: ['颜色牢固度;Color Fastness'],
    tags: ['CMF;可靠性'],
    description: '涂层、油墨等颜色抵抗光照、摩擦、汗液等作用而保持不褪色的能力。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0058',
    name: '上盖',
    type: '其他',
    category: 'components',
    aliases: ['上壳体;Top Case'],
    tags: ['部件;外观'],
    description: '手机的上半部分外壳。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0059',
    name: '上锡',
    type: '其他',
    category: 'components',
    aliases: ['锡膏覆盖;Solder Coverage'],
    tags: ['SMT;制造工艺'],
    description: '焊盘表面被焊锡覆盖的面积比例，是评估焊接质量的重要指标。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0060',
    name: '生耳',
    type: '其他',
    category: 'components',
    aliases: ['表耳;Lug'],
    tags: ['部件;外观'],
    description: '表带上用于连接表壳的突出部分，在手机上可能指类似结构。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0061',
    name: '声腔',
    type: '其他',
    category: 'components',
    aliases: ['扬声器腔体;Speaker Chamber'],
    tags: ['部件;声学'],
    description: '为扬声器提供共振空间的密封结构，其容积和设计对音质影响很大。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0062',
    name: '石磨',
    type: '其他',
    category: 'components',
    aliases: ['石材纹理;Stone Pattern'],
    tags: ['外观;设计'],
    description: '通过工艺模拟天然石材的纹理和质感。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0063',
    name: '时长',
    type: '其他',
    category: 'components',
    aliases: ['持续时间;Duration'],
    tags: ['测试验证;可靠性'],
    description: '某项测试持续的时间或产品某项功能的续航时间。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0064',
    name: '食人鱼',
    type: '其他',
    category: 'components',
    aliases: ['食人鱼LED;Piranha LED'],
    tags: ['部件;显示相关'],
    description: '一种亮度高、视角广的LED，常用作指示灯。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0065',
    name: '硬度',
    type: '其他',
    category: 'components',
    aliases: ['材料硬度;Hardness'],
    tags: ['物料;可靠性'],
    description: '材料抵抗硬物压入其表面的能力，如莫氏硬度、铅笔硬度。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0066',
    name: '有源',
    type: '其他',
    category: 'components',
    aliases: ['有源器件;Active Component'],
    tags: ['部件;电气性能'],
    description: '需要电源才能正常工作的器件，如芯片、晶体管等。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0067',
    name: '原色',
    type: '其他',
    category: 'components',
    aliases: ['基底颜色;Base Color'],
    tags: ['外观;设计'],
    description: '材料本身的颜色，区别于后期处理（如喷涂）的颜色。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0068',
    name: '运放',
    type: '其他',
    category: 'components',
    aliases: ['运算放大器;Operational Amplifier'],
    tags: ['部件;电气性能'],
    description: '用于信号放大的集成电路，其性能影响音频、传感器等信号质量。',
    created_at: '2025-09-26T09:43:14.248489',
    updated_at: '2025-09-26T09:43:14.248489'
});
CREATE (d:Dictionary {
    id: 'TERM_0069',
    name: '增益',
    type: '其他',
    category: 'components',
    aliases: ['天线增益;Antenna Gain'],
    tags: ['硬件相关;通信相关'],
    description: '天线在特定方向上的辐射强度与理想点源天线的比值，影响信号覆盖。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0070',
    name: '沾锡',
    type: '其他',
    category: 'components',
    aliases: ['焊盘沾锡;Pad Wetting'],
    tags: ['SMT;制造工艺'],
    description: '熔化的焊锡在焊盘上铺展的能力，是形成良好焊点的基础。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0071',
    name: '张力',
    type: '其他',
    category: 'components',
    aliases: ['表面张力;Surface Tension'],
    tags: ['制造工艺;物料'],
    description: '液体表面收缩的力，影响锡膏印刷、点胶、涂布等工艺的成型。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0072',
    name: '针脚',
    type: '其他',
    category: 'components',
    aliases: ['元器件引脚;Component Lead'],
    tags: ['部件;SMT'],
    description: '元器件上用于焊接的金属引脚。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0073',
    name: '支架',
    type: '其他',
    category: 'components',
    aliases: ['支撑架;Bracket'],
    tags: ['部件;设计'],
    description: '用于支撑和固定其他部件的结构件。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0074',
    name: '直通',
    type: '其他',
    category: 'components',
    aliases: ['直通率;First Pass Yield'],
    tags: ['制造工艺;质量体系'],
    description: '产品在某一工序一次性通过检验的比率，反映工序能力。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0075',
    name: '纸箱',
    type: '其他',
    category: 'components',
    aliases: ['包装外箱;Carton'],
    tags: ['物料;包装'],
    description: '手机运输和销售的外层纸箱，要求有足够的抗压和抗跌落强度。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0076',
    name: '质心',
    type: '其他',
    category: 'components',
    aliases: ['重心;Center of Gravity'],
    tags: ['结构相关;设计'],
    description: '产品重力的合力作用点，影响握持手感和跌落姿态。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0077',
    name: '中框',
    type: '其他',
    category: 'components',
    aliases: ['手机中框;Middle Frame'],
    tags: ['部件;外观'],
    description: '手机的骨架结构，用于固定内部元件，常见材质为金属或塑料。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0078',
    name: '主摄',
    type: '其他',
    category: 'components',
    aliases: ['主摄像头;Main Camera'],
    tags: ['部件;影像相关'],
    description: '手机多个摄像头中性能最强、最常用的那个摄像头。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0079',
    name: '驻波',
    type: '其他',
    category: 'components',
    aliases: ['驻波比;Standing Wave Ratio'],
    tags: ['硬件相关;通信相关'],
    description: '表征天线与馈线匹配程度的指标，驻波比过大意味着信号反射严重。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0080',
    name: '转轴',
    type: '其他',
    category: 'components',
    aliases: ['铰链;Hinge'],
    tags: ['部件;可靠性'],
    description: '折叠屏手机的关键部件，负责屏幕弯折，对疲劳寿命和顺滑度要求极高。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0081',
    name: '追频',
    type: '其他',
    category: 'components',
    aliases: ['频率追踪;Frequency Tracking'],
    tags: ['无线充电;性能指标'],
    description: '无线充电系统中，根据负载变化动态调整工作频率以保持最佳效率。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0082',
    name: '自拍',
    type: '其他',
    category: 'components',
    aliases: ['前置摄像头;Front Camera'],
    tags: ['部件;影像相关'],
    description: '用于拍摄用户自己的摄像头，位于手机正面。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0083',
    name: '阻焊',
    type: '其他',
    category: 'components',
    aliases: ['阻焊层;Solder Mask'],
    tags: ['PCB;设计'],
    description: '覆盖在PCB铜箔上的绿色或其他颜色的绝缘保护层，防止短路和氧化。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0084',
    name: '座充',
    type: '其他',
    category: 'components',
    aliases: ['座式充电器;Desktop Charger'],
    tags: ['配件;充电'],
    description: '将手机插入底座进行充电的配件。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0085',
    name: '座子',
    type: '其他',
    category: 'components',
    aliases: ['连接器插座;Connector Socket'],
    tags: ['部件;电气连接'],
    description: '固定在PCB上的连接器母端。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0086',
    name: 'SAR',
    type: '其他',
    category: 'components',
    aliases: ['比吸收率;Specific Absorption Rate'],
    tags: ['安全相关;通信相关'],
    description: '**定义**: 人体吸收电磁能量的速率。 **判定口径**: <2.0 W/kg。 **常见场景**: 手机靠近头部。 **排查路径**: 测试实验室验证。 **对策**: 优化射频发射功率，改善天线布局。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0087',
    name: '热容率',
    type: '其他',
    category: 'components',
    aliases: ['体积热容'],
    tags: ['物料;热管理'],
    description: '单位体积材料升高单位温度所需热量，影响局部升温速度。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0088',
    name: '柯伐合金',
    type: '其他',
    category: 'components',
    aliases: ['Kovar'],
    tags: ['物料;硬件相关;封装'],
    description: '一种与玻璃、陶瓷膨胀系数匹配的铁镍钴合金，常用于芯片封装引脚。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0089',
    name: '剪切稀化',
    type: '其他',
    category: 'components',
    aliases: ['假塑性；Shear Thinning'],
    tags: ['物料;制造工艺;点胶'],
    description: '流体的表观粘度随剪切速率增加而降低的特性，如锡膏、胶水，利于印刷和点胶。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0090',
    name: '水接触角',
    type: '其他',
    category: 'components',
    aliases: ['Water Contact Angle'],
    tags: ['CMF;可靠性;测试验证'],
    description: '衡量固体表面疏水性的指标，角度越大越疏水。用于评估涂层效果。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0091',
    name: '迁移数',
    type: '其他',
    category: 'components',
    aliases: ['Transference Number'],
    tags: ['硬件相关;电池'],
    description: '在电池中，某种离子所携带的电流与总电流的比值，反映离子导电效率。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0092',
    name: '离子清洁度',
    type: '其他',
    category: 'components',
    aliases: ['Ionic Cleanliness'],
    tags: ['PCB;可靠性;测试验证'],
    description: '衡量PCB表面离子污染物含量的指标，单位通常为μg NaCl/cm²，影响绝缘电阻。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0093',
    name: '塌落直径',
    type: '其他',
    category: 'components',
    aliases: ['Slump Diameter'],
    tags: ['制造工艺;SMT;锡膏'],
    description: '锡膏印刷后，在预热阶段因流动而扩散的直径变化，用于评估锡膏抗塌陷性能。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0094',
    name: '天线效率',
    type: '其他',
    category: 'components',
    aliases: ['Antenna Efficiency'],
    tags: ['硬件相关;通信相关;测试验证'],
    description: '天线辐射功率与输入功率的比值，是衡量天线性能的核心指标。',
    created_at: '2025-09-26T09:43:14.249486',
    updated_at: '2025-09-26T09:43:14.249486'
});
CREATE (d:Dictionary {
    id: 'TERM_0095',
    name: '焊点IMC',
    type: '其他',
    category: 'components',
    aliases: ['Intermetallic Compound'],
    tags: ['SMT;可靠性;硬件相关'],
    description: '焊料与焊盘金属界面生成的金属间化合物层。适中的IMC厚度是良好焊接的标志，过厚则脆。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0096',
    name: '扬氏模量',
    type: '其他',
    category: 'components',
    aliases: ['弹性模量；Young\'s Modulus'],
    tags: ['物料;结构相关;设计'],
    description: '材料在弹性变形范围内，应力与应变的比值，衡量材料抵抗弹性变形的能力。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0097',
    name: '黑镍',
    type: '其他',
    category: 'components',
    aliases: ['Black Nickel Plating'],
    tags: ['外观;制造工艺;可靠性'],
    description: '一种黑色的镍镀层，用于装饰和消光，耐磨性和耐腐蚀性需关注。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0098',
    name: '断差面',
    type: '其他',
    category: 'components',
    aliases: ['Step Surface'],
    tags: ['设计;外观;制造工艺'],
    description: '两个相邻表面存在高度差而形成的台阶面，需控制断差大小和均匀性。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0099',
    name: '焊盘设计',
    type: '其他',
    category: 'components',
    aliases: ['Pad Design'],
    tags: ['设计;PCB;SMT'],
    description: 'PCB焊盘的形状、尺寸和布局设计，直接影响元件的贴装和焊接质量。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0100',
    name: '引脚共面性',
    type: '其他',
    category: 'components',
    aliases: ['Lead Coplanarity'],
    tags: ['硬件相关;SMT;制造工艺'],
    description: '多引脚元件所有引脚底部形成的平面与理想平面的偏差，影响焊接良率。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0101',
    name: '热阻',
    type: '其他',
    category: 'components',
    aliases: ['Thermal Resistance'],
    tags: ['硬件相关;热管理;可靠性'],
    description: '热量在传递路径上遇到的阻力，衡量器件或材料的散热能力。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0102',
    name: '玻璃转化温度',
    type: '其他',
    category: 'components',
    aliases: ['Glass Transition Temperature', 'Tg'],
    tags: ['物料;PCB;可靠性'],
    description: '聚合物从玻璃态向高弹态转变的温度。PCB基材的Tg影响其耐热性。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0103',
    name: '磁导率',
    type: '其他',
    category: 'components',
    aliases: ['Permeability'],
    tags: ['物料;硬件相关;EMC'],
    description: '衡量材料导磁能力的物理量，用于磁芯和电磁屏蔽材料的选择。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0104',
    name: '导通电阻',
    type: '其他',
    category: 'components',
    aliases: ['On-Resistance'],
    tags: ['硬件相关;电气性能'],
    description: '开关器件（如MOSFET）在导通状态下，源极和漏极之间的电阻。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0105',
    name: '声压级',
    type: '其他',
    category: 'components',
    aliases: ['Sound Pressure Level', 'SPL'],
    tags: ['硬件相关;声学;测试验证'],
    description: '衡量声音强弱的物理量，单位分贝，是扬声器、麦克风的重要指标。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0106',
    name: '绝缘阻抗',
    type: '其他',
    category: 'components',
    aliases: ['Insulation Resistance', 'IR'],
    tags: ['硬件相关;电气性能;可靠性'],
    description: '衡量绝缘材料阻止电流通过的能力，单位通常为欧姆。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0107',
    name: '功耗曲线',
    type: '其他',
    category: 'components',
    aliases: ['Power Consumption Profile'],
    tags: ['软件相关;硬件相关;测试验证'],
    description: '手机在不同工作模式下的功耗随时间变化的曲线。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0108',
    name: '哑光',
    type: '其他',
    category: 'components',
    aliases: ['Matt Finish'],
    tags: ['外观;设计'],
    description: '低光泽度的表面效果，不易留下指纹。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0109',
    name: '火花纹',
    type: '其他',
    category: 'components',
    aliases: ['EDM Texture'],
    tags: ['外观;设计;制造工艺'],
    description: '通过电火花加工在模具上形成的纹理，可转移至塑胶件表面。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0110',
    name: '导通孔孔铜',
    type: '其他',
    category: 'components',
    aliases: ['Via Copper Thickness'],
    tags: ['PCB;制造工艺;可靠性'],
    description: '导通孔内壁铜层的厚度，影响电流承载能力和连接可靠性。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0111',
    name: '胶体流动性',
    type: '其他',
    category: 'components',
    aliases: ['Adhesive Flowability'],
    tags: ['物料;制造工艺;点胶'],
    description: '胶水在受力下的流动能力，影响点胶成型和填充效果。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0112',
    name: '磁饱和',
    type: '其他',
    category: 'components',
    aliases: ['Magnetic Saturation'],
    tags: ['硬件相关;电气性能'],
    description: '磁性材料的磁化强度不随外磁场增强而显著增加的状态。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0113',
    name: '镀层孔隙率',
    type: '其他',
    category: 'components',
    aliases: ['Plating Porosity'],
    tags: ['CMF;可靠性;制造工艺'],
    description: '单位面积镀层中针孔的数量，影响其防护性能。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0114',
    name: '热插拔次数',
    type: '其他',
    category: 'components',
    aliases: ['Hot-plugging Cycles'],
    tags: ['硬件相关;可靠性;测试验证'],
    description: '连接器可承受的带电插拔次数，是衡量其寿命的重要指标。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0115',
    name: '信号完整性',
    type: '其他',
    category: 'components',
    aliases: ['Signal Integrity', 'SI'],
    tags: ['硬件相关;设计;PCB'],
    description: '信号在传输路径上的质量，涉及波形失真、时序、噪声等。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0116',
    name: '水汽敏感等级',
    type: '其他',
    category: 'components',
    aliases: ['Moisture Sensitivity Level', 'MSL'],
    tags: ['硬件相关;物料;SMT'],
    description: '根据IC封装对潮湿的敏感程度进行的分级，决定拆包后的使用时限和烘烤条件。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0117',
    name: '塑封体',
    type: '其他',
    category: 'components',
    aliases: ['Mold Compound'],
    tags: ['物料;半导体;封装'],
    description: '用于封装芯片的环氧树脂塑料材料。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0118',
    name: '翘曲度',
    type: '其他',
    category: 'components',
    aliases: ['Warpage'],
    tags: ['结构相关;制造工艺;可靠性'],
    description: '平面部件相对于理想平面的弯曲或扭曲程度量化值。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0119',
    name: '胶体固化率',
    type: '其他',
    category: 'components',
    aliases: ['Adhesive Cure Rate'],
    tags: ['物料;制造工艺;点胶'],
    description: '胶水在特定条件下固化的速度。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0120',
    name: '射频阻抗',
    type: '其他',
    category: 'components',
    aliases: ['RF Impedance'],
    tags: ['硬件相关;射频相关;PCB'],
    description: '射频传输线的特征阻抗，通常设计为50欧姆以实现阻抗匹配。',
    created_at: '2025-09-26T09:43:14.250486',
    updated_at: '2025-09-26T09:43:14.250486'
});
CREATE (d:Dictionary {
    id: 'TERM_0121',
    name: '胶体Tg点',
    type: '其他',
    category: 'components',
    aliases: ['Adhesive Glass Transition Temperature'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂的玻璃化转变温度，影响其在不同温度下的力学性能。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0122',
    name: '邦定强度',
    type: '其他',
    category: 'components',
    aliases: ['Bonding Strength'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '芯片与基板之间键合（如金线、胶水）的机械强度。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0123',
    name: '模温均匀性',
    type: '其他',
    category: 'components',
    aliases: ['Mold Temperature Uniformity'],
    tags: ['制造工艺;注塑'],
    description: '模具不同区域温度的差异程度，影响产品收缩和尺寸一致性。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0124',
    name: '胶体触变性',
    type: '其他',
    category: 'components',
    aliases: ['Adhesive Thixotropy'],
    tags: ['物料;制造工艺;点胶'],
    description: '胶体在剪切力作用下粘度减小，静置后粘度恢复的特性，利于成型。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0125',
    name: '引脚可焊性',
    type: '其他',
    category: 'components',
    aliases: ['Lead Solderability'],
    tags: ['硬件相关;SMT;物料'],
    description: '元件引脚表面被熔融焊料润湿形成良好焊点的能力。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0126',
    name: '功率密度',
    type: '其他',
    category: 'components',
    aliases: ['Power Density'],
    tags: ['硬件相关;热管理;设计'],
    description: '单位体积或单位面积上消耗的功率，是热设计的关键输入。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0127',
    name: '胶体储存期',
    type: '其他',
    category: 'components',
    aliases: ['Adhesive Shelf Life'],
    tags: ['物料;制造工艺;点胶'],
    description: '胶水在特定储存条件下保持其使用性能的时间。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0128',
    name: 'LDS天线',
    type: '其他',
    category: 'components',
    aliases: ['激光直接成型天线'],
    tags: ['制造工艺;通信相关;设计'],
    description: '利用激光在特定塑料上活化出电路图案，然后化学镀金属形成天线。集成度高，适合复杂三维结构。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0129',
    name: '热界面材料',
    type: '其他',
    category: 'components',
    aliases: ['TIM'],
    tags: ['物料;热管理;可靠性'],
    description: '填充在发热器件与散热器之间，降低接触热阻的材料，如导热硅脂、相变材料、导热垫片。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0130',
    name: '差分信号',
    type: '其他',
    category: 'components',
    aliases: ['差动信号'],
    tags: ['设计;电气性能;通信相关'],
    description: '用一对幅度相等、相位相反的信号来传输信息，抗共模噪声能力强，用于高速接口。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0131',
    name: '邦定Pad设计',
    type: '其他',
    category: 'components',
    aliases: ['焊盘设计'],
    tags: ['设计;半导体;封装'],
    description: '芯片上用于键合的铝焊盘或铜焊盘的尺寸、形状和布局设计。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0132',
    name: '模内装饰薄膜',
    type: '其他',
    category: 'components',
    aliases: ['IML Film'],
    tags: ['物料;制造工艺;CMF'],
    description: '用于IML工艺的已印刷好图案的薄膜基材。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0133',
    name: '邦定Pad金属层',
    type: '其他',
    category: 'components',
    aliases: ['焊盘金属化'],
    tags: ['设计;半导体;封装'],
    description: '芯片键合焊盘上方的金属层（如铝），其厚度和成分影响键合性能。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0134',
    name: '邦定Pad设计',
    type: '其他',
    category: 'components',
    aliases: ['焊盘设计'],
    tags: ['设计;半导体;封装'],
    description: '芯片上用于键合的铝焊盘或铜焊盘的尺寸、形状和布局设计。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0135',
    name: '模内装饰薄膜',
    type: '其他',
    category: 'components',
    aliases: ['IML Film'],
    tags: ['物料;制造工艺;CMF'],
    description: '用于IML工艺的已印刷好图案的薄膜基材。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0136',
    name: '邦定Pad金属层',
    type: '其他',
    category: 'components',
    aliases: ['焊盘金属化'],
    tags: ['设计;半导体;封装'],
    description: '芯片键合焊盘上方的金属层（如铝），其厚度和成分影响键合性能。',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0137',
    name: '氮化铝陶瓷',
    type: '材料',
    category: 'components',
    aliases: ['AlN陶瓷'],
    tags: ['物料;硬件相关;热管理'],
    description: '高导热陶瓷材料用于功率器件封装和散热基板',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0138',
    name: '色饱和度',
    type: '性能指标',
    category: 'components',
    aliases: ['色彩饱和度'],
    tags: ['显示相关;影像相关;性能指标'],
    description: '衡量色彩鲜艳程度的指标饱和度越高颜色越纯',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0139',
    name: '聚酰亚胺薄膜',
    type: '材料',
    category: 'components',
    aliases: ['PI膜'],
    tags: ['物料;FPC;可靠性'],
    description: '耐高温高绝缘的柔性基材广泛用于柔性电路板',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0140',
    name: '导热凝胶',
    type: '材料',
    category: 'components',
    aliases: ['导热泥'],
    tags: ['物料;热管理;可靠性'],
    description: '膏状热界面材料适用于不规则间隙的散热填充可自动流平',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0141',
    name: '液晶聚合物',
    type: '材料',
    category: 'components',
    aliases: ['LCP'],
    tags: ['物料;FPC;高频应用'],
    description: '具有低介电常数和损耗的高分子材料适用于高频柔性电路',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0142',
    name: '铍铜合金',
    type: '材料',
    category: 'components',
    aliases: ['铍铜'],
    tags: ['物料;硬件相关;弹片'],
    description: '高强度高弹性的铜合金常用于制造连接器弹片和屏蔽罩',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0143',
    name: '相位噪声',
    type: '性能指标',
    category: 'components',
    aliases: ['相位抖动'],
    tags: ['射频相关;硬件相关;性能指标'],
    description: '振荡器输出信号相位的随机起伏影响通信系统的信噪比',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0144',
    name: '聚氨酯密封胶',
    type: '材料',
    category: 'components',
    aliases: ['PU胶'],
    tags: ['物料;结构相关;可靠性'],
    description: '具有良好弹性和粘接性的密封材料用于防水和结构粘接',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0145',
    name: '腐蚀电位',
    type: '性能指标',
    category: 'components',
    aliases: ['自腐蚀电位'],
    tags: ['物料;可靠性;CMF'],
    description: '金属在腐蚀介质中不发生外电流时的电极电位反映其热力学腐蚀倾向',
    created_at: '2025-09-26T09:43:14.251492',
    updated_at: '2025-09-26T09:43:14.251492'
});
CREATE (d:Dictionary {
    id: 'TERM_0146',
    name: '聚对苯二甲酸丁二醇酯',
    type: '材料',
    category: 'components',
    aliases: ['PBT'],
    tags: ['物料;结构相关;注塑'],
    description: '耐热电绝缘性好的工程塑料用于连接器和结构件',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0147',
    name: '激光直接成型材料',
    type: '材料',
    category: 'components',
    aliases: ['LDS材料'],
    tags: ['物料;硬件相关;通信相关'],
    description: '含有特殊添加剂的塑料经激光活化后可化学镀金属形成电路',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0148',
    name: '低温共烧陶瓷',
    type: '材料',
    category: 'components',
    aliases: ['LTCC'],
    tags: ['物料;硬件相关;射频相关'],
    description: '可将导体电阻电容等集成于一体的多层陶瓷基板技术',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0149',
    name: '信纳比',
    type: '性能指标',
    category: 'components',
    aliases: ['SINAD'],
    tags: ['硬件相关;测试验证;声学'],
    description: '信号+噪声+失真的总功率与噪声+失真的功率之比衡量音频系统动态性能',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0150',
    name: '聚醚醚酮',
    type: '材料',
    category: 'components',
    aliases: ['PEEK'],
    tags: ['物料;结构相关;可靠性'],
    description: '耐高温耐化学腐蚀机械强度高的特种工程塑料',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0151',
    name: '氰酸酯树脂',
    type: '材料',
    category: 'components',
    aliases: ['氰酸酯'],
    tags: ['物料;PCB;高频应用'],
    description: '具有低介电损耗的高性能树脂用于高频电路板',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0152',
    name: '聚四氟乙烯',
    type: '材料',
    category: 'components',
    aliases: ['PTFE'],
    tags: ['物料;硬件相关;高频应用'],
    description: '介电性能极佳耐化学性强的塑料用于高频电路和绝缘',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0153',
    name: '总谐波失真',
    type: '性能指标',
    category: 'components',
    aliases: ['THD'],
    tags: ['硬件相关;测试验证;声学'],
    description: '谐波总功率与基波功率的比值衡量音频设备非线性失真',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0154',
    name: '玻璃纤维布',
    type: '材料',
    category: 'components',
    aliases: ['玻纤布'],
    tags: ['物料;PCB;制造工艺'],
    description: '用作PCB基板的增强材料提供机械强度和尺寸稳定性',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0155',
    name: '磁性流体',
    type: '材料',
    category: 'components',
    aliases: ['磁液'],
    tags: ['物料;硬件相关;声学'],
    description: '含有纳米磁性颗粒的液体用于扬声器音圈散热和阻尼',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0156',
    name: '误差向量幅度',
    type: '性能指标',
    category: 'components',
    aliases: ['EVM'],
    tags: ['硬件相关;测试验证;通信相关'],
    description: '衡量数字调制信号质量的关键参数表示实际信号点与理想点的偏差',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0157',
    name: '氧化铟锡',
    type: '材料',
    category: 'components',
    aliases: ['ITO'],
    tags: ['物料;硬件相关;显示相关'],
    description: '透明导电薄膜材料用于触摸屏传感器和显示电极',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0158',
    name: '导电布',
    type: '材料',
    category: 'components',
    aliases: ['导电织物'],
    tags: ['物料;EMC;硬件相关'],
    description: '纤维织物表面金属化制成的柔性电磁屏蔽材料',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0159',
    name: '接收灵敏度',
    type: '性能指标',
    category: 'components',
    aliases: ['灵敏度'],
    tags: ['硬件相关;测试验证;通信相关'],
    description: '接收机在满足特定误码率条件下能识别的最小输入信号功率',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0160',
    name: '环氧模塑料',
    type: '材料',
    category: 'components',
    aliases: ['EMC'],
    tags: ['物料;半导体;封装'],
    description: '用于封装芯片的环氧树脂基复合材料提供保护和散热',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0161',
    name: '硅凝胶',
    type: '材料',
    category: 'components',
    aliases: ['硅胶'],
    tags: ['物料;可靠性;封装'],
    description: '柔软透明的硅基凝胶用于芯片的软保护和应力缓冲',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0162',
    name: '发射功率',
    type: '性能指标',
    category: 'components',
    aliases: ['输出功率'],
    tags: ['硬件相关;测试验证;通信相关'],
    description: '发射机天线连接处输出的射频功率需符合法规限值',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0163',
    name: '铝碳化硅',
    type: '材料',
    category: 'components',
    aliases: ['AlSiC'],
    tags: ['物料;硬件相关;热管理'],
    description: '高导热低膨胀的金属基复合材料用于功率器件散热底座',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0164',
    name: '导热相变材料',
    type: '材料',
    category: 'components',
    aliases: ['PCM'],
    tags: ['物料;热管理;可靠性'],
    description: '在特定温度发生相变（固-液）能有效填充界面间隙的导热材料',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0165',
    name: '互调失真',
    type: '性能指标',
    category: 'components',
    aliases: ['IMD'],
    tags: ['硬件相关;测试验证;射频相关'],
    description: '由系统非线性导致两个输入频率产生新频率分量造成的干扰',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0166',
    name: '聚萘二甲酸乙二醇酯',
    type: '材料',
    category: 'components',
    aliases: ['PEN'],
    tags: ['物料;FPC;可靠性'],
    description: '性能介于PET和PI之间的柔性基材耐热性优于PET',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0167',
    name: '电磁屏蔽泡棉',
    type: '材料',
    category: 'components',
    aliases: ['导电泡棉'],
    tags: ['物料;EMC;硬件相关'],
    description: '具有弹性的导电海绵材料用于缝隙的电磁屏蔽',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0168',
    name: '相位裕量',
    type: '性能指标',
    category: 'components',
    aliases: ['相位裕度'],
    tags: ['硬件相关;设计;电气性能'],
    description: '反馈系统稳定性的度量相位裕量越大系统越稳定',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0169',
    name: '聚苯硫醚',
    type: '材料',
    category: 'components',
    aliases: ['PPS'],
    tags: ['物料;结构相关;注塑'],
    description: '耐高温耐化学腐蚀尺寸稳定的工程塑料',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0170',
    name: '热塑性聚氨酯',
    type: '材料',
    category: 'components',
    aliases: ['TPU'],
    tags: ['物料;结构相关;可靠性'],
    description: '具有良好弹性耐磨性和抗撕裂性的塑料用于保护套等',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0171',
    name: '增益平坦度',
    type: '性能指标',
    category: 'components',
    aliases: ['增益平坦性'],
    tags: ['硬件相关;测试验证;射频相关'],
    description: '放大器在工作频带内增益的波动程度',
    created_at: '2025-09-26T09:43:14.252494',
    updated_at: '2025-09-26T09:43:14.252494'
});
CREATE (d:Dictionary {
    id: 'TERM_0172',
    name: '微波复合介质基板',
    type: '材料',
    category: 'components',
    aliases: ['高频板材'],
    tags: ['物料;PCB;射频相关'],
    description: '具有低损耗稳定介电常数的高频电路板专用材料',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0173',
    name: '陶瓷基板',
    type: '材料',
    category: 'components',
    aliases: ['陶瓷电路板'],
    tags: ['物料;硬件相关;热管理'],
    description: '氧化铝氮化铝等陶瓷制成的电路基板绝缘性好导热率高',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0174',
    name: '群延迟',
    type: '性能指标',
    category: 'components',
    aliases: ['群时延'],
    tags: ['硬件相关;测试验证;射频相关'],
    description: '信号不同频率成分通过系统时的时间延迟差异',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0175',
    name: '磁性形状记忆合金',
    type: '材料',
    category: 'components',
    aliases: ['MSMA'],
    tags: ['物料;硬件相关;传感器'],
    description: '在外磁场作用下可产生大应变的新型智能材料',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0176',
    name: 'OLED面板',
    type: '组件',
    category: 'components',
    aliases: ['有机发光二极管显示屏'],
    tags: ['显示相关;硬件相关'],
    description: '像素自发光对比度高色彩鲜艳可柔性的显示面板',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0177',
    name: 'LCD面板',
    type: '组件',
    category: 'components',
    aliases: ['液晶显示屏'],
    tags: ['显示相关;硬件相关'],
    description: '需要背光模组成本较低技术成熟的液晶显示面板',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0178',
    name: '盖板玻璃',
    type: '组件',
    category: 'components',
    aliases: ['Cover Glass;防护玻璃'],
    tags: ['显示相关;结构相关;外观'],
    description: '保护屏幕免受冲击和刮伤的防护玻璃',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0179',
    name: '偏光片',
    type: '组件',
    category: 'components',
    aliases: ['Polarizer'],
    tags: ['显示相关;物料'],
    description: '将自然光转换为偏振光是LCD显示不可或缺的组件',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0180',
    name: '光学胶',
    type: '材料',
    category: 'components',
    aliases: ['OCA'],
    tags: ['显示相关;物料;制造工艺'],
    description: '用于全贴合粘接盖板与触摸屏或显示屏减少反光提升透光率',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0181',
    name: '背光模组',
    type: '组件',
    category: 'components',
    aliases: ['Backlight Unit;BLU'],
    tags: ['显示相关;硬件相关'],
    description: '为LCD提供均匀明亮的面光源的模组',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0182',
    name: '显示驱动芯片',
    type: '组件',
    category: 'components',
    aliases: ['DDI;Display Driver IC'],
    tags: ['显示相关;硬件相关;半导体'],
    description: '接收主机信号驱动显示屏像素点显示图像的芯片',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0183',
    name: '触控报点率',
    type: '性能指标',
    category: 'components',
    aliases: ['Touch Report Rate'],
    tags: ['显示相关;性能指标;人机交互'],
    description: '每秒触摸屏上报坐标的次数影响触控跟手性',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0184',
    name: '屏幕响应时间',
    type: '性能指标',
    category: 'components',
    aliases: ['Response Time'],
    tags: ['显示相关;性能指标'],
    description: '像素从一种颜色切换到另一种颜色所需的时间影响动态画面拖影',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0185',
    name: '对比度',
    type: '性能指标',
    category: 'components',
    aliases: ['Contrast Ratio'],
    tags: ['显示相关;性能指标'],
    description: '屏幕最亮与最暗区域的亮度比值',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0186',
    name: '色域覆盖率',
    type: '性能指标',
    category: 'components',
    aliases: ['Color Gamut Coverage'],
    tags: ['显示相关;性能指标;影像相关'],
    description: '显示屏能显示的颜色范围与标准色域（如sRGB DCI-P3）的比值',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0187',
    name: '图像传感器',
    type: '组件',
    category: 'components',
    aliases: ['Image Sensor;CIS'],
    tags: ['影像相关;硬件相关;半导体'],
    description: '将光信号转换为电信号的核心芯片如CMOS传感器',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0188',
    name: '镜头',
    type: '组件',
    category: 'components',
    aliases: ['Lens'],
    tags: ['影像相关;摄像头模组'],
    description: '光学镜片组负责光线汇聚',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0189',
    name: '音圈马达',
    type: '组件',
    category: 'components',
    aliases: ['VCM'],
    tags: ['影像相关;硬件相关'],
    description: '驱动镜头移动实现对焦的致动器',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0190',
    name: '光学防抖',
    type: '组件',
    category: 'components',
    aliases: ['OIS'],
    tags: ['影像相关;功能;性能指标'],
    description: '通过移动镜组或传感器补偿手抖的技术',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0191',
    name: '红外滤光片',
    type: '组件',
    category: 'components',
    aliases: ['IR Cut Filter'],
    tags: ['影像相关;物料'],
    description: '滤除红外光使成像色彩更接近人眼所见的滤光片',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0192',
    name: '摄像头模组',
    type: '组件',
    category: 'components',
    aliases: ['CCM'],
    tags: ['影像相关;硬件相关'],
    description: '将传感器镜头VCM等封装成一体的功能模块',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0193',
    name: '信噪比',
    type: '性能指标',
    category: 'components',
    aliases: ['SNR'],
    tags: ['影像相关;性能指标'],
    description: '图像信号与噪声的比值衡量图像纯净度',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0194',
    name: '灵敏度',
    type: '性能指标',
    category: 'components',
    aliases: ['Sensitivity'],
    tags: ['影像相关;性能指标'],
    description: '传感器将光信号转换为电信号的效率',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0195',
    name: '动态范围',
    type: '性能指标',
    category: 'components',
    aliases: ['Dynamic Range'],
    tags: ['影像相关;性能指标'],
    description: '传感器能同时捕捉的最亮和最暗细节的范围',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0196',
    name: '镜头畸变',
    type: '性能指标',
    category: 'components',
    aliases: ['Lens Distortion'],
    tags: ['影像相关;性能指标'],
    description: '镜头引起的图像形变如桶形畸变枕形畸变',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0197',
    name: '保护板',
    type: '组件',
    category: 'components',
    aliases: ['BMS;Protection Circuit Module'],
    tags: ['硬件相关;安全相关;电气性能'],
    description: '管理电池的充放电防止过充过放过流短路的保护电路',
    created_at: '2025-09-26T09:43:14.253492',
    updated_at: '2025-09-26T09:43:14.253492'
});
CREATE (d:Dictionary {
    id: 'TERM_0198',
    name: '电池封装膜',
    type: '材料',
    category: 'components',
    aliases: ['Pouch Film'],
    tags: ['物料;硬件相关;安全相关'],
    description: '软包电池的外层铝塑复合膜提供封装和绝缘',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0199',
    name: '负极材料',
    type: '材料',
    category: 'components',
    aliases: ['Anode Material'],
    tags: ['物料;电池;硬件相关'],
    description: '如石墨锂离子在充电时嵌入其中的负极材料',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0200',
    name: '正极材料',
    type: '材料',
    category: 'components',
    aliases: ['Cathode Material'],
    tags: ['物料;电池;硬件相关'],
    description: '如钴酸锂磷酸铁锂锂离子在放电时嵌入其中的正极材料',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0201',
    name: '电解液',
    type: '材料',
    category: 'components',
    aliases: ['Electrolyte'],
    tags: ['物料;电池;安全相关'],
    description: '提供锂离子在正负极之间迁移的通道的液体',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0202',
    name: '隔膜',
    type: '材料',
    category: 'components',
    aliases: ['Separator'],
    tags: ['物料;电池;安全相关'],
    description: '隔离正负极防止短路同时允许离子通过的薄膜',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0203',
    name: '额定容量',
    type: '性能指标',
    category: 'components',
    aliases: ['Rated Capacity'],
    tags: ['硬件相关;性能指标;电池'],
    description: '电池在特定条件下放出的电量单位mAh',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0204',
    name: '能量密度',
    type: '性能指标',
    category: 'components',
    aliases: ['Energy Density'],
    tags: ['硬件相关;性能指标;电池'],
    description: '单位体积或重量储存的能量单位Wh/kg或Wh/L',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0205',
    name: '循环次数',
    type: '性能指标',
    category: 'components',
    aliases: ['Cycle Life'],
    tags: ['硬件相关;性能指标;可靠性'],
    description: '容量衰减到规定值（如80%）时所经历的完整充放电循环次数',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0206',
    name: '印刷电路板',
    type: '组件',
    category: 'components',
    aliases: ['PCB'],
    tags: ['硬件相关;设计'],
    description: '承载和连接电子元件的基板',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0207',
    name: '主芯片',
    type: '组件',
    category: 'components',
    aliases: ['SoC;系统级芯片'],
    tags: ['硬件相关;半导体;设计'],
    description: '集成CPU GPU Modem等核心功能的芯片',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0208',
    name: '内存',
    type: '组件',
    category: 'components',
    aliases: ['RAM'],
    tags: ['硬件相关;半导体'],
    description: '运行内存用于临时存储运行的程序和数据',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0209',
    name: '闪存',
    type: '组件',
    category: 'components',
    aliases: ['Flash;ROM'],
    tags: ['硬件相关;半导体'],
    description: '存储空间用于存放系统应用和用户数据',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0210',
    name: '射频功放',
    type: '组件',
    category: 'components',
    aliases: ['PA'],
    tags: ['硬件相关;射频相关'],
    description: '放大要发射的射频信号的功率放大器',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0211',
    name: '电源管理芯片',
    type: '组件',
    category: 'components',
    aliases: ['PMIC'],
    tags: ['硬件相关;电气性能'],
    description: '管理整机的电源分配充电和功耗的芯片',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0212',
    name: 'PCB板材',
    type: '材料',
    category: 'components',
    aliases: ['Laminate'],
    tags: ['物料;PCB'],
    description: '制造PCB的基板材料如FR-4高频板材',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0213',
    name: '阻焊油墨',
    type: '材料',
    category: 'components',
    aliases: ['Solder Mask'],
    tags: ['物料;PCB'],
    description: '覆盖在铜箔上起绝缘和保护作用的绿色或其他颜色的油墨',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0214',
    name: '电源完整性',
    type: '性能指标',
    category: 'components',
    aliases: ['PI'],
    tags: ['硬件相关;设计;电气性能'],
    description: '供给芯片的电源电压稳定纯净的程度',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0215',
    name: '电磁兼容性',
    type: '性能指标',
    category: 'components',
    aliases: ['EMC'],
    tags: ['硬件相关;设计;测试验证'],
    description: '设备在其电磁环境中能正常工作且不对其他设备构成干扰的能力',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0216',
    name: '天线辐射体',
    type: '组件',
    category: 'components',
    aliases: ['Antenna Radiator'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '天线的核心部分直接负责电磁波的辐射和接收',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0217',
    name: '天线调谐器',
    type: '组件',
    category: 'components',
    aliases: ['Antenna Tuner'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '动态调整天线阻抗匹配以应对手握环境变化带来的失配',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0218',
    name: '射频前端模组',
    type: '组件',
    category: 'components',
    aliases: ['RFFE'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '集成PA LNA开关滤波器等功能的模块',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0219',
    name: '功率放大器',
    type: '组件',
    category: 'components',
    aliases: ['PA'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '放大发射链路的射频信号功率',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0220',
    name: '低噪声放大器',
    type: '组件',
    category: 'components',
    aliases: ['LNA'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '放大接收链路的微弱信号自身引入的噪声极低',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0221',
    name: '双工器',
    type: '组件',
    category: 'components',
    aliases: ['Duplexer'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '在FDD系统中允许发射和接收同时进行并隔离两者信号',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0222',
    name: '开关',
    type: '组件',
    category: 'components',
    aliases: ['Switch'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '在不同天线或频段之间进行切换',
    created_at: '2025-09-26T09:43:14.254492',
    updated_at: '2025-09-26T09:43:14.254492'
});
CREATE (d:Dictionary {
    id: 'TERM_0223',
    name: '滤波器',
    type: '组件',
    category: 'components',
    aliases: ['Filter'],
    tags: ['射频相关;硬件相关;通信相关'],
    description: '滤除带外干扰信号保留所需频带内的信号',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0224',
    name: '天线触点',
    type: '组件',
    category: 'components',
    aliases: ['Antenna Contact'],
    tags: ['射频相关;硬件相关;电气连接'],
    description: '天线辐射体与主板射频电路之间的物理连接点通常为弹片或pogo pin',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0225',
    name: '同轴电缆',
    type: '组件',
    category: 'components',
    aliases: ['Coaxial Cable'],
    tags: ['射频相关;硬件相关;线缆管理'],
    description: '用于传输射频信号具有屏蔽层以防干扰',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0226',
    name: '射频连接器',
    type: '组件',
    category: 'components',
    aliases: ['RF Connector'],
    tags: ['射频相关;硬件相关;电气连接'],
    description: '用于连接射频电缆和PCB如IPEX连接器',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0227',
    name: '净空区',
    type: '组件',
    category: 'components',
    aliases: ['Keep-out Area'],
    tags: ['射频相关;设计;硬件相关'],
    description: '天线周围为保证辐射效率而禁止布置金属器件的区域',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0228',
    name: '总全向灵敏度',
    type: '性能指标',
    category: 'components',
    aliases: ['TIS'],
    tags: ['射频相关;性能指标;通信相关'],
    description: '表征手机在整个空间各个方向上接收微弱信号能力的综合指标',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0229',
    name: '总辐射功率',
    type: '性能指标',
    category: 'components',
    aliases: ['TRP'],
    tags: ['射频相关;性能指标;通信相关'],
    description: '表征手机在整个空间各个方向上辐射功率能力的综合指标',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0230',
    name: '回波损耗',
    type: '性能指标',
    category: 'components',
    aliases: ['Return Loss'],
    tags: ['射频相关;性能指标;通信相关'],
    description: '表示入射功率被反射回来的比例值越大如-10dB表示匹配越好反射越小',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0231',
    name: '驻波比',
    type: '性能指标',
    category: 'components',
    aliases: ['VSWR'],
    tags: ['射频相关;性能指标;通信相关'],
    description: '衡量阻抗匹配程度的另一个常用指标理想值为1:1',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0232',
    name: '扬声器BOX',
    type: '组件',
    category: 'components',
    aliases: ['Speaker Box'],
    tags: ['声学;硬件相关;结构相关'],
    description: '为扬声器单元提供密闭或导向的声学腔体极大影响低频响应和灵敏度',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0233',
    name: '受话器',
    type: '组件',
    category: 'components',
    aliases: ['Receiver'],
    tags: ['声学;硬件相关'],
    description: '用于通话时贴近耳朵听音要求高清晰度',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0234',
    name: '麦克风',
    type: '组件',
    category: 'components',
    aliases: ['Microphone'],
    tags: ['声学;硬件相关'],
    description: '将声音信号转换为电信号有MEMS和ECM等类型',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0235',
    name: '音频编解码器',
    type: '组件',
    category: 'components',
    aliases: ['Audio Codec'],
    tags: ['声学;硬件相关;半导体'],
    description: '负责模拟音频信号与数字音频信号的转换并可能集成音频效果处理',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0236',
    name: '扬声器单元',
    type: '组件',
    category: 'components',
    aliases: ['Speaker Driver'],
    tags: ['声学;硬件相关'],
    description: '将电信号转换为机械振动从而发声的核心部件包含磁路音圈振膜等',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0237',
    name: '声学网布',
    type: '材料',
    category: 'components',
    aliases: ['Acoustic Mesh'],
    tags: ['声学;物料;外观'],
    description: '覆盖在出声孔起到防尘防水具有一定透气性和调节声学阻尼的作用',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0238',
    name: '防水透气膜',
    type: '材料',
    category: 'components',
    aliases: ['Waterproof Breathable Membrane'],
    tags: ['声学;物料;可靠性'],
    description: '允许空气通过以实现声学导通但能阻止液态水侵入',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0239',
    name: '音腔',
    type: '组件',
    category: 'components',
    aliases: ['Acoustic Chamber'],
    tags: ['声学;结构相关;硬件相关'],
    description: '麦克风或受话器背后的密封空间其容积对频响有重要影响',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0240',
    name: '频率响应',
    type: '性能指标',
    category: 'components',
    aliases: ['Frequency Response'],
    tags: ['声学;性能指标'],
    description: '设备输出声压级随频率变化的曲线是衡量音质的基础指标',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0241',
    name: '总谐波失真加噪声',
    type: '性能指标',
    category: 'components',
    aliases: ['THD+N'],
    tags: ['声学;性能指标'],
    description: '衡量音频系统非线性失真和本底噪声的综合指标',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0242',
    name: '灵敏度',
    type: '性能指标',
    category: 'components',
    aliases: ['Sensitivity'],
    tags: ['声学;性能指标'],
    description: '给定输入功率如1mW或电压如1V时在指定距离如10cm产生的声压级',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0243',
    name: '最大声压级',
    type: '性能指标',
    category: 'components',
    aliases: ['Maximum SPL'],
    tags: ['声学;性能指标'],
    description: '扬声器在失真不超过限定值时可输出的最大声音强度',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0244',
    name: '金属中框',
    type: '组件',
    category: 'components',
    aliases: ['Metal Mid-frame'],
    tags: ['结构相关;硬件相关'],
    description: '通常采用铝合金不锈钢等提供整机主要结构强度和散热路径',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0245',
    name: '玻璃后盖',
    type: '组件',
    category: 'components',
    aliases: ['Glass Back Cover'],
    tags: ['结构相关;外观;硬件相关'],
    description: '提供美观质感并支持无线充电需与中框可靠粘接',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0246',
    name: '复合板材后盖',
    type: '组件',
    category: 'components',
    aliases: ['Composite Back Cover'],
    tags: ['结构相关;外观;硬件相关'],
    description: '通过注塑喷涂镀膜等工艺实现类似玻璃的质感成本较低',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0247',
    name: '摄像头装饰件',
    type: '组件',
    category: 'components',
    aliases: ['Camera Deco'],
    tags: ['结构相关;外观;摄像头模组'],
    description: '保护摄像头模组并提升外观层次感常见金属或塑料镀膜',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0248',
    name: 'SIM卡托',
    type: '组件',
    category: 'components',
    aliases: ['SIM Tray'],
    tags: ['结构相关;硬件相关'],
    description: '需保证与中框的配合精度和插拔手感具备防水功能',
    created_at: '2025-09-26T09:43:14.255492',
    updated_at: '2025-09-26T09:43:14.255492'
});
CREATE (d:Dictionary {
    id: 'TERM_0249',
    name: '侧键',
    type: '组件',
    category: 'components',
    aliases: ['Side Key'],
    tags: ['结构相关;硬件相关;人机交互'],
    description: '包括电源键和音量键通常为金属杆状结构通过弹片或Dome片实现触发',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0250',
    name: 'Type-C连接器',
    type: '组件',
    category: 'components',
    aliases: ['USB Type-C Connector'],
    tags: ['结构相关;硬件相关;电气连接'],
    description: '负责充电数据传输和音频输出插拔寿命和防水是关键',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0251',
    name: '泡棉',
    type: '材料',
    category: 'components',
    aliases: ['Foam;Gasket'],
    tags: ['结构相关;物料;EMC'],
    description: '用于填充间隙提供缓冲电磁屏蔽或辅助防水',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0252',
    name: '防水胶',
    type: '材料',
    category: 'components',
    aliases: ['Waterproof Adhesive'],
    tags: ['结构相关;物料;可靠性'],
    description: '用于粘接屏幕后盖与中框形成防水密封圈',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0253',
    name: '均热板',
    type: '组件',
    category: 'components',
    aliases: ['Vapor Chamber'],
    tags: ['热管理;硬件相关;可靠性'],
    description: '利用内部工质相变蒸发-冷凝进行高效二维热传导散热效率高于热管',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0254',
    name: '热管',
    type: '组件',
    category: 'components',
    aliases: ['Heat Pipe'],
    tags: ['热管理;硬件相关;可靠性'],
    description: '利用内部工质相变进行高效一维热传导的封闭管状器件',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0255',
    name: '导热硅脂',
    type: '材料',
    category: 'components',
    aliases: ['Thermal Grease;Thermal Paste'],
    tags: ['热管理;物料;可靠性'],
    description: '填充芯片与散热器之间的微间隙降低接触热阻',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0256',
    name: '导热石墨片',
    type: '材料',
    category: 'components',
    aliases: ['Graphite Sheet'],
    tags: ['热管理;物料;可靠性'],
    description: '具有高面内导热系数用于将热点热量迅速横向扩散',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0257',
    name: '导热凝胶',
    type: '材料',
    category: 'components',
    aliases: ['Thermal Gel'],
    tags: ['热管理;物料;可靠性'],
    description: '具有一定流动性的膏状导热材料适用于不规则或易碎器件',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0258',
    name: '导热相变材料',
    type: '材料',
    category: 'components',
    aliases: ['PCM'],
    tags: ['热管理;物料;可靠性'],
    description: '在特定温度如45-60°C发生固-液相变更好地填充间隙',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0259',
    name: '金属屏蔽罩',
    type: '组件',
    category: 'components',
    aliases: ['Shield Can'],
    tags: ['热管理;硬件相关;EMC'],
    description: '在屏蔽电磁干扰的同时也作为散热片将芯片热量传导出去',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0260',
    name: '散热铜箔',
    type: '材料',
    category: 'components',
    aliases: ['Thermal Copper Foil'],
    tags: ['热管理;物料;PCB'],
    description: '贴在PCB背面或特定区域辅助局部散热',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0261',
    name: '结温',
    type: '性能指标',
    category: 'components',
    aliases: ['Junction Temperature'],
    tags: ['热管理;性能指标;可靠性'],
    description: '芯片半导体结的最高工作温度是热设计的核心限制参数',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0262',
    name: 'MEMS加速度计',
    type: '组件',
    category: 'components',
    aliases: ['Accelerometer'],
    tags: ['传感器;硬件相关;性能指标'],
    description: '测量手机在三个轴上的线性加速度用于计步屏幕旋转等',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0263',
    name: '陀螺仪',
    type: '组件',
    category: 'components',
    aliases: ['Gyroscope'],
    tags: ['传感器;硬件相关;性能指标'],
    description: '测量手机围绕三个轴的旋转角速度用于导航游戏控制等',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0264',
    name: '磁力计',
    type: '组件',
    category: 'components',
    aliases: ['Magnetometer'],
    tags: ['传感器;硬件相关;性能指标'],
    description: '测量环境磁场强度用于电子罗盘方向检测',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0265',
    name: '距离传感器',
    type: '组件',
    category: 'components',
    aliases: ['Proximity Sensor'],
    tags: ['传感器;硬件相关;功能'],
    description: '通常由红外LED和光电二极管组成检测手机与物体的距离用于通话时熄屏',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0266',
    name: '环境光传感器',
    type: '组件',
    category: 'components',
    aliases: ['ALS'],
    tags: ['传感器;硬件相关;功能'],
    description: '检测环境光强度用于自动调节屏幕亮度',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0267',
    name: '气压计',
    type: '组件',
    category: 'components',
    aliases: ['Barometer'],
    tags: ['传感器;硬件相关;性能指标'],
    description: '测量大气压强用于海拔计算天气辅助预测',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0268',
    name: '霍尔传感器',
    type: '组件',
    category: 'components',
    aliases: ['Hall Sensor'],
    tags: ['传感器;硬件相关;功能'],
    description: '检测磁场变化常用于翻盖保护套的智能唤醒功能',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0269',
    name: '指纹传感器',
    type: '组件',
    category: 'components',
    aliases: ['Fingerprint Sensor'],
    tags: ['传感器;硬件相关;安全相关;功能'],
    description: '通过光学电容或超声波方式采集指纹信息用于身份认证',
    created_at: '2025-09-26T09:43:14.256493',
    updated_at: '2025-09-26T09:43:14.256493'
});
CREATE (d:Dictionary {
    id: 'TERM_0270',
    name: '红外发射器',
    type: '组件',
    category: 'components',
    aliases: ['IR Blaster'],
    tags: ['传感器;硬件相关;功能'],
    description: '发射红外信号可遥控电视空调等家电',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0271',
    name: '色温传感器',
    type: '组件',
    category: 'components',
    aliases: ['Color Temperature Sensor'],
    tags: ['传感器;影像相关;功能'],
    description: '检测环境光色温辅助相机白平衡校准',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0272',
    name: '传感器中枢',
    type: '组件',
    category: 'components',
    aliases: ['Sensor Hub'],
    tags: ['传感器;硬件相关;软件相关'],
    description: '低功耗协处理器专门用于处理各类传感器数据降低主芯片功耗',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0273',
    name: '分辨率',
    type: '性能指标',
    category: 'components',
    aliases: ['Resolution'],
    tags: ['传感器;性能指标'],
    description: '传感器能感知到的被测量的最小变化量',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0274',
    name: '量程',
    type: '性能指标',
    category: 'components',
    aliases: ['Full Scale Range'],
    tags: ['传感器;性能指标'],
    description: '传感器能够测量的被测量的最大值与最小值之差',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0275',
    name: '非线性度',
    type: '性能指标',
    category: 'components',
    aliases: ['Non-Linearity'],
    tags: ['传感器;性能指标'],
    description: '传感器实际特性曲线与拟合直线之间的最大偏差',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0276',
    name: '重复性',
    type: '性能指标',
    category: 'components',
    aliases: ['Repeatability'],
    tags: ['传感器;性能指标'],
    description: '在同一条件下多次测量同一被测量其输出值的一致性',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0277',
    name: '无线充电接收线圈',
    type: '组件',
    category: 'components',
    aliases: ['RX Coil'],
    tags: ['充电;硬件相关;功能'],
    description: '内置在手机中接收交变磁场并转化为感应电流',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0278',
    name: '无线充电发射板',
    type: '组件',
    category: 'components',
    aliases: ['TX Pad'],
    tags: ['充电;配件;功能'],
    description: '外部设备产生交变磁场为手机无线充电',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0279',
    name: '电荷泵充电芯片',
    type: '组件',
    category: 'components',
    aliases: ['Charge Pump Charger'],
    tags: ['充电;硬件相关;半导体'],
    description: '采用电容储能方式实现高效大电流充电转换效率远高于传统LDO或Buck',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0280',
    name: '电池电量计',
    type: '组件',
    category: 'components',
    aliases: ['Fuel Gauge'],
    tags: ['充电;硬件相关;半导体'],
    description: '精确估算电池剩余电量和健康状态',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0281',
    name: '过压保护电路',
    type: '组件',
    category: 'components',
    aliases: ['OVP'],
    tags: ['充电;硬件相关;安全相关'],
    description: '防止充电电压过高损坏手机内部器件',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0282',
    name: '过流保护电路',
    type: '组件',
    category: 'components',
    aliases: ['OCP'],
    tags: ['充电;硬件相关;安全相关'],
    description: '防止充电电流或负载电流过大',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0283',
    name: 'USB Type-C接口控制器',
    type: '组件',
    category: 'components',
    aliases: ['Type-C Controller'],
    tags: ['充电;硬件相关;功能'],
    description: '管理Type-C接口的正反插角色切换DRP/SRC/SNK和快充协议',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0284',
    name: '输入电压范围',
    type: '性能指标',
    category: 'components',
    aliases: ['Input Voltage Range'],
    tags: ['充电;性能指标'],
    description: '手机充电电路能正常工作的输入电压范围',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0285',
    name: '充电功率',
    type: '性能指标',
    category: 'components',
    aliases: ['Charging Power'],
    tags: ['充电;性能指标'],
    description: '充电时输入手机的总功率电压×电流单位瓦特',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0286',
    name: '转换效率',
    type: '性能指标',
    category: 'components',
    aliases: ['Conversion Efficiency'],
    tags: ['充电;性能指标'],
    description: '充电电路将输入电能转换为电池化学能的效率',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0287',
    name: '线性马达',
    type: '组件',
    category: 'components',
    aliases: ['LRA'],
    tags: ['硬件相关;人机交互;功能'],
    description: '通过电磁驱动质量块做线性运动提供振动反馈启停快手感清脆',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0288',
    name: '转子马达',
    type: '组件',
    category: 'components',
    aliases: ['Eccentric Rotating Mass Motor'],
    tags: ['硬件相关;人机交互;功能'],
    description: '通过不平衡转子的旋转产生振动成本低但启停慢手感松散',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0289',
    name: '压电陶瓷马达',
    type: '组件',
    category: 'components',
    aliases: ['Piezo Haptic Actuator'],
    tags: ['硬件相关;人机交互;功能'],
    description: '利用压电效应使陶瓷片形变产生振动或触感响应极快可模拟丰富纹理',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0290',
    name: '马达驱动芯片',
    type: '组件',
    category: 'components',
    aliases: ['Haptic Driver IC'],
    tags: ['硬件相关;半导体;功能'],
    description: '提供马达所需的驱动波形和功率放大',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0291',
    name: '马达固定结构',
    type: '组件',
    category: 'components',
    aliases: ['Motor Mounting Structure'],
    tags: ['结构相关;硬件相关;可靠性'],
    description: '确保马达被牢固固定避免额外振动噪音并将振动有效传递至整机',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0292',
    name: '振动加速度',
    type: '性能指标',
    category: 'components',
    aliases: ['Vibration Acceleration'],
    tags: ['性能指标;人机交互'],
    description: '衡量振动强度的物理量通常以重力加速度g的倍数表示',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0293',
    name: '频率响应',
    type: '性能指标',
    category: 'components',
    aliases: ['Frequency Response'],
    tags: ['性能指标;人机交互'],
    description: '马达在不同驱动频率下的振动强度变化曲线',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0294',
    name: '总谐波失真',
    type: '性能指标',
    category: 'components',
    aliases: ['THD'],
    tags: ['性能指标;人机交互'],
    description: '马达振动波形中谐波失真的大小影响振动纯净度',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0295',
    name: '阳极氧化层',
    type: '材料',
    category: 'components',
    aliases: ['Anodized Layer'],
    tags: ['CMF;外观;可靠性'],
    description: '通过电解在铝合金表面生成的坚硬耐腐蚀的氧化铝陶瓷膜可着色',
    created_at: '2025-09-26T09:43:14.257495',
    updated_at: '2025-09-26T09:43:14.257495'
});
CREATE (d:Dictionary {
    id: 'TERM_0296',
    name: 'PVD镀膜',
    type: '材料',
    category: 'components',
    aliases: ['物理气相沉积镀膜'],
    tags: ['CMF;外观;可靠性'],
    description: '在真空环境下通过溅射或蒸发方式在表面沉积金属/化合物薄膜呈现金属光泽色彩',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0297',
    name: 'AF防指纹涂层',
    type: '材料',
    category: 'components',
    aliases: ['抗指纹涂层'],
    tags: ['CMF;外观;用户体验'],
    description: '在玻璃或镀层表面涂覆的疏油疏水涂层减少指纹和污渍附着',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0298',
    name: 'AG防眩光涂层',
    type: '材料',
    category: 'components',
    aliases: ['抗反射涂层'],
    tags: ['CMF;外观;显示相关'],
    description: '在玻璃表面通过化学蚀刻或涂层形成微细粗糙度减少环境光反射',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0299',
    name: '光泽度',
    type: '性能指标',
    category: 'components',
    aliases: ['Gloss'],
    tags: ['CMF;性能指标;外观'],
    description: '表面反射光线的能力用光泽度单位表示',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0300',
    name: '粗糙度',
    type: '性能指标',
    category: 'components',
    aliases: ['Roughness'],
    tags: ['CMF;性能指标;外观'],
    description: '表面具有的较小间距和微小峰谷的不平度常用Ra值表示',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0301',
    name: '颜色坐标',
    type: '性能指标',
    category: 'components',
    aliases: ['Color Coordinate'],
    tags: ['CMF;性能指标;外观'],
    description: '在Lab LCh等色彩空间中表示颜色的具体数值',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0302',
    name: 'Wi-Fi 6E芯片',
    type: '组件',
    category: 'components',
    aliases: ['802.11ax芯片'],
    tags: ['通信相关;硬件相关;功能'],
    description: '支持6GHz频段的Wi-Fi芯片提供更宽的信道和更低的干扰',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0303',
    name: '蓝牙5.3芯片',
    type: '组件',
    category: 'components',
    aliases: ['BT 5.3'],
    tags: ['通信相关;硬件相关;功能'],
    description: '支持LE Audio具有更低的功耗和更好的多设备连接能力',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0304',
    name: '5G调制解调器',
    type: '组件',
    category: 'components',
    aliases: ['5G Modem'],
    tags: ['通信相关;硬件相关;半导体'],
    description: '负责5G NR信号的编码解码支持Sub-6GHz和毫米波频段',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0305',
    name: 'GNSS接收芯片',
    type: '组件',
    category: 'components',
    aliases: ['全球导航卫星系统芯片'],
    tags: ['通信相关;硬件相关;功能'],
    description: '支持GPS GLONASS Galileo BDS等多个卫星系统的定位信号接收',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0306',
    name: 'NFC控制器',
    type: '组件',
    category: 'components',
    aliases: ['近场通信控制器'],
    tags: ['通信相关;硬件相关;功能'],
    description: '实现手机支付门禁模拟标签读写等近距离通信功能',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0307',
    name: 'eSIM',
    type: '组件',
    category: 'components',
    aliases: ['嵌入式SIM卡'],
    tags: ['通信相关;硬件相关;功能'],
    description: '直接焊在主板上的SIM芯片可通过软件切换运营商节省空间',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0308',
    name: '天线调谐开关',
    type: '组件',
    category: 'components',
    aliases: ['Antenna Tuning Switch'],
    tags: ['通信相关;硬件相关;射频相关'],
    description: '根据频率动态切换天线匹配网络优化天线效率',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0309',
    name: '分集天线',
    type: '组件',
    category: 'components',
    aliases: ['Diversity Antenna'],
    tags: ['通信相关;硬件相关;射频相关'],
    description: '接收主天线之外的另一套接收天线通过选择或合并技术改善信号质量',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0310',
    name: 'MIMO天线系统',
    type: '组件',
    category: 'components',
    aliases: ['多输入多输出天线系统'],
    tags: ['通信相关;硬件相关;射频相关'],
    description: '使用多个天线同时收发数据提升信道容量和链路可靠性',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0311',
    name: '射频滤波器',
    type: '组件',
    category: 'components',
    aliases: ['RF Filter'],
    tags: ['通信相关;硬件相关;射频相关'],
    description: '如SAW/BAW滤波器用于滤除特定频段的干扰信号',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0312',
    name: '载波聚合',
    type: '性能指标',
    category: 'components',
    aliases: ['Carrier Aggregation'],
    tags: ['通信相关;性能指标;功能'],
    description: '同时使用多个载波频段进行数据传输提升峰值速率',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0313',
    name: '调制阶数',
    type: '性能指标',
    category: 'components',
    aliases: ['Modulation Order'],
    tags: ['通信相关;性能指标;射频相关'],
    description: '如256QAM表示每个符号携带的比特数阶数越高速率越快抗干扰越差',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0314',
    name: '误码率',
    type: '性能指标',
    category: 'components',
    aliases: ['Bit Error Rate'],
    tags: ['通信相关;性能指标;射频相关'],
    description: '接收端错误比特数与总传输比特数之比',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0315',
    name: '接收灵敏度',
    type: '性能指标',
    category: 'components',
    aliases: ['Receiver Sensitivity'],
    tags: ['通信相关;性能指标;射频相关'],
    description: '接收机在满足特定误码率条件下所能识别的最小信号功率',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0316',
    name: 'USB Type-C接口',
    type: '组件',
    category: 'components',
    aliases: ['USB-C'],
    tags: ['硬件相关;电气连接;功能'],
    description: '支持正反插高速数据传输视频输出和快充的多功能接口',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0317',
    name: '闪电接口',
    type: '组件',
    category: 'components',
    aliases: ['Lightning'],
    tags: ['硬件相关;电气连接;功能'],
    description: 'Apple公司专有的紧凑型接口用于数据传输和充电',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0318',
    name: '3.5mm音频接口',
    type: '组件',
    category: 'components',
    aliases: ['耳机孔'],
    tags: ['硬件相关;声学;功能'],
    description: '模拟音频输出接口逐渐被USB-C或无线音频替代',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0319',
    name: '高清多媒体接口',
    type: '组件',
    category: 'components',
    aliases: ['HDMI'],
    tags: ['硬件相关;功能'],
    description: '用于输出高清视频和音频信号',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0320',
    name: 'DisplayPort接口',
    type: '组件',
    category: 'components',
    aliases: ['DP'],
    tags: ['硬件相关;功能'],
    description: '另一种高清视频输出接口常见于USB-C的Alt Mode中',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0321',
    name: 'pogo pin连接器',
    type: '组件',
    category: 'components',
    aliases: ['弹簧针连接器'],
    tags: ['硬件相关;电气连接;测试验证'],
    description: '用于生产测试治具或手机配件的临时性低插拔次数的连接',
    created_at: '2025-09-26T09:43:14.258494',
    updated_at: '2025-09-26T09:43:14.258494'
});
CREATE (d:Dictionary {
    id: 'TERM_0322',
    name: 'FPC连接器',
    type: '组件',
    category: 'components',
    aliases: ['柔性电路板连接器'],
    tags: ['硬件相关;电气连接;制造工艺'],
    description: '用于连接主板与屏幕摄像头等部件的FPC要求高精度和对位',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0323',
    name: '板对板连接器',
    type: '组件',
    category: 'components',
    aliases: ['BTB Connector'],
    tags: ['硬件相关;电气连接;结构相关'],
    description: '连接主板与副板或其他子板是实现手机堆叠的关键元件',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0324',
    name: 'SIM卡座',
    type: '组件',
    category: 'components',
    aliases: ['SIM Card Connector'],
    tags: ['硬件相关;电气连接;功能'],
    description: '承载Nano-SIM卡或eSIM芯片实现与移动网络的连接',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0325',
    name: '麦克风硅麦',
    type: '组件',
    category: 'components',
    aliases: ['MEMS Microphone'],
    tags: ['硬件相关;声学;电气连接'],
    description: '通过FPC或焊点与主板连接体积小抗干扰性强',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0326',
    name: '接触阻抗',
    type: '性能指标',
    category: 'components',
    aliases: ['Contact Resistance'],
    tags: ['硬件相关;性能指标;电气连接'],
    description: '连接器触点之间的电阻值越小越好',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0327',
    name: '额定电流',
    type: '性能指标',
    category: 'components',
    aliases: ['Rated Current'],
    tags: ['硬件相关;性能指标;电气连接'],
    description: '连接器能够长期安全通过的最大电流值',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0328',
    name: '插拔力',
    type: '性能指标',
    category: 'components',
    aliases: ['Insertion/Extraction Force'],
    tags: ['硬件相关;性能指标;人机交互'],
    description: '将公端插入母座或拔出的力影响用户体验和连接可靠性',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0329',
    name: '多层陶瓷电容',
    type: '组件',
    category: 'components',
    aliases: ['MLCC'],
    tags: ['硬件相关;电气性能;SMT'],
    description: '用量最大的被动元件用于滤波去耦储能等',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0330',
    name: '钽电容',
    type: '组件',
    category: 'components',
    aliases: ['Tantalum Capacitor'],
    tags: ['硬件相关;电气性能;SMT'],
    description: '体积小容值大ESR低但有极性需注意防反接和浪涌',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0331',
    name: '电感',
    type: '组件',
    category: 'components',
    aliases: ['Inductor'],
    tags: ['硬件相关;电气性能;SMT'],
    description: '用于电源滤波储能和LC振荡电路',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0332',
    name: '磁珠',
    type: '组件',
    category: 'components',
    aliases: ['Ferrite Bead'],
    tags: ['硬件相关;电气性能;EMC'],
    description: '抑制高频噪声常用于电源和信号线',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0333',
    name: '晶体振荡器',
    type: '组件',
    category: 'components',
    aliases: ['Crystal Oscillator'],
    tags: ['硬件相关;电气性能;半导体'],
    description: '提供系统基准时钟信号',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0334',
    name: '热敏电阻',
    type: '组件',
    category: 'components',
    aliases: ['NTC/PTC'],
    tags: ['硬件相关;电气性能;传感器'],
    description: '电阻值随温度变化用于温度检测和温度补偿',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0335',
    name: '压敏电阻',
    type: '组件',
    category: 'components',
    aliases: ['Varistor'],
    tags: ['硬件相关;电气性能;安全相关'],
    description: '电压敏感用于过压保护如浪涌',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0336',
    name: 'TVS二极管',
    type: '组件',
    category: 'components',
    aliases: ['瞬态电压抑制二极管'],
    tags: ['硬件相关;电气性能;安全相关'],
    description: '响应速度极快用于防护ESD和EFT等快速瞬态过电压',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0337',
    name: '自恢复保险丝',
    type: '组件',
    category: 'components',
    aliases: ['PTC Resettable Fuse'],
    tags: ['硬件相关;电气性能;安全相关'],
    description: '过流时电阻急剧变大限制电流故障排除后自动恢复',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0338',
    name: 'ESD保护器件',
    type: '组件',
    category: 'components',
    aliases: ['ESD Protection Device'],
    tags: ['硬件相关;电气性能;安全相关;ESD'],
    description: '专门用于防护静电放电的器件通常并联在接口电路上',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0339',
    name: '电容的等效串联电阻',
    type: '性能指标',
    category: 'components',
    aliases: ['ESR'],
    tags: ['硬件相关;性能指标;电气性能'],
    description: '电容等效电路中的串联电阻影响滤波效果和自身发热',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0340',
    name: '电容的等效串联电感',
    type: '性能指标',
    category: 'components',
    aliases: ['ESL'],
    tags: ['硬件相关;性能指标;电气性能'],
    description: '电容引脚和内部结构存在的寄生电感影响高频性能',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0341',
    name: '额定电压',
    type: '性能指标',
    category: 'components',
    aliases: ['Rated Voltage'],
    tags: ['硬件相关;性能指标;电气性能'],
    description: '元件能长期安全工作的最大直流电压或交流电压峰值',
    created_at: '2025-09-26T09:43:14.259494',
    updated_at: '2025-09-26T09:43:14.259494'
});
CREATE (d:Dictionary {
    id: 'TERM_0342',
    name: '工作温度范围',
    type: '性能指标',
    category: 'components',
    aliases: ['Operating Temperature Range'],
    tags: ['硬件相关;性能指标;可靠性'],
    description: '元件能正常工作的环境温度范围',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0343',
    name: '在线测试治具',
    type: '组件',
    category: 'components',
    aliases: ['ICT Fixture'],
    tags: ['制造工艺;测试验证;工具'],
    description: '用于ICT测试通过密集的探针接触PCB测试点进行短路/开路和元件值测试',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0344',
    name: '功能测试治具',
    type: '组件',
    category: 'components',
    aliases: ['FCT Fixture'],
    tags: ['制造工艺;测试验证;工具'],
    description: '模拟整机使用环境为手机供电提供信号输入并检测输出',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0345',
    name: '电池模拟器',
    type: '组件',
    category: 'components',
    aliases: ['Battery Emulator'],
    tags: ['制造工艺;测试验证;工具;充电'],
    description: '在FCT中替代真实电池可精确控制电压和电流并模拟电池特性',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0346',
    name: '自动化测试设备',
    type: '组件',
    category: 'components',
    aliases: ['Automated Test Equipment'],
    tags: ['制造工艺;测试验证;工具;自动化'],
    description: '集成机械手相机传感器和测试模块实现生产线自动上下料和测试',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0347',
    name: '视觉对位系统',
    type: '组件',
    category: 'components',
    aliases: ['Vision Alignment System'],
    tags: ['制造工艺;测试验证;工具;自动化'],
    description: '使用工业相机精确定位产品或元件位置引导自动化设备操作',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0348',
    name: '针床',
    type: '组件',
    category: 'components',
    aliases: ['Bed of Nails'],
    tags: ['制造工艺;测试验证;工具'],
    description: 'ICT治具的核心部分上面布满了用于接触PCB测试点的弹簧探针',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0349',
    name: '射频测试治具',
    type: '组件',
    category: 'components',
    aliases: ['RF Test Fixture'],
    tags: ['制造工艺;测试验证;工具;射频相关'],
    description: '用于校准和测试手机的射频性能通常带有射频连接器和屏蔽腔',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0350',
    name: '声学测试密封腔',
    type: '组件',
    category: 'components',
    aliases: ['Acoustic Test Chamber'],
    tags: ['制造工艺;测试验证;工具;声学'],
    description: '在生产线端提供一个标准的声学环境测试麦克风和受话器的性能',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0351',
    name: '屏幕点亮治具',
    type: '组件',
    category: 'components',
    aliases: ['Display Lighting Fixture'],
    tags: ['制造工艺;测试验证;工具;显示相关'],
    description: '快速连接并点亮屏幕检查显示功能和无坏点',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0352',
    name: '激光打标治具',
    type: '组件',
    category: 'components',
    aliases: ['Laser Marking Fixture'],
    tags: ['制造工艺;工具'],
    description: '精确定位手机确保序列号等信息打在规定位置',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0353',
    name: '治具探针',
    type: '组件',
    category: 'components',
    aliases: ['Test Probe'],
    tags: ['制造工艺;测试验证;工具'],
    description: '治具上直接接触测试点的精密零件要求耐磨导电性好',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0354',
    name: '测试覆盖率',
    type: '性能指标',
    category: 'components',
    aliases: ['Test Coverage'],
    tags: ['制造工艺;测试验证;质量体系'],
    description: '测试用例对产品功能或硬件节点的覆盖程度',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0355',
    name: '直通率',
    type: '性能指标',
    category: 'components',
    aliases: ['First Pass Yield'],
    tags: ['制造工艺;测试验证;质量体系'],
    description: '产品一次性通过某道测试工序的比率',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0356',
    name: '误判率',
    type: '性能指标',
    category: 'components',
    aliases: ['False Call Rate'],
    tags: ['制造工艺;测试验证;质量体系'],
    description: '治具或测试程序将合格品判为不合格的比例',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0357',
    name: '漏判率',
    type: '性能指标',
    category: 'components',
    aliases: ['Escape Rate'],
    tags: ['制造工艺;测试验证;质量体系'],
    description: '治具或测试程序将不合格品判为合格的比例',
    created_at: '2025-09-26T09:43:14.260496',
    updated_at: '2025-09-26T09:43:14.260496'
});
CREATE (d:Dictionary {
    id: 'TERM_0358',
    name: '测试周期时间',
    type: '性能指标',
    category: 'components',
    aliases: ['Test Cycle Time'],
    tags: ['制造工艺;测试验证;效率'],
    description: '完成一次完整测试所需的时间影响生产线节拍',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0359',
    name: '治具维护周期',
    type: '性能指标',
    category: 'components',
    aliases: ['Fixture Maintenance Cycle'],
    tags: ['制造工艺;测试验证;维护'],
    description: '治具需要定期清洁校准或更换磨损件的频率',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0360',
    name: '杨氏模量',
    type: '性能指标',
    category: 'components',
    aliases: ['弹性模量'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料在弹性变形范围内应力与应变的比值表征材料抵抗弹性变形的能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0361',
    name: '屈服强度',
    type: '性能指标',
    category: 'components',
    aliases: ['屈服点'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料开始产生明显塑性变形时的应力值',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0362',
    name: '抗拉强度',
    type: '性能指标',
    category: 'components',
    aliases: ['拉伸强度'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料在断裂前所能承受的最大应力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0363',
    name: '伸长率',
    type: '性能指标',
    category: 'components',
    aliases: ['延伸率'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料断裂时的相对伸长量表征材料塑性变形能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0364',
    name: '冲击韧性',
    type: '性能指标',
    category: 'components',
    aliases: ['冲击强度'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料在冲击载荷作用下吸收塑性变形功和断裂功的能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0365',
    name: '疲劳强度',
    type: '性能指标',
    category: 'components',
    aliases: ['疲劳极限'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料在无限次应力循环下不发生破坏的最大应力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0366',
    name: '蠕变极限',
    type: '性能指标',
    category: 'components',
    aliases: ['蠕变强度'],
    tags: ['物料;结构相关;可靠性'],
    description: '材料在高温长期应力作用下抵抗蠕变变形的能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0367',
    name: '热膨胀系数',
    type: '性能指标',
    category: 'components',
    aliases: ['CTE'],
    tags: ['物料;热管理;可靠性'],
    description: '温度每升高1℃材料长度或体积的相对变化量',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0368',
    name: '热导率',
    type: '性能指标',
    category: 'components',
    aliases: ['导热系数'],
    tags: ['物料;热管理;可靠性'],
    description: '材料传导热量的能力单位W/(m·K)',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0369',
    name: '比热容',
    type: '性能指标',
    category: 'components',
    aliases: ['比热'],
    tags: ['物料;热管理;可靠性'],
    description: '单位质量材料升高单位温度所需的热量',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0370',
    name: '密度',
    type: '性能指标',
    category: 'components',
    aliases: ['体积质量'],
    tags: ['物料;结构相关;设计'],
    description: '单位体积材料的质量',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0371',
    name: '电阻率',
    type: '性能指标',
    category: 'components',
    aliases: ['体积电阻率'],
    tags: ['物料;电气性能;硬件相关'],
    description: '表征材料导电性能的物理量',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0372',
    name: '介电常数',
    type: '性能指标',
    category: 'components',
    aliases: ['电容率'],
    tags: ['物料;电气性能;硬件相关'],
    description: '表征电介质材料极化能力的物理量',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0373',
    name: '介质损耗',
    type: '性能指标',
    category: 'components',
    aliases: ['介电损耗'],
    tags: ['物料;电气性能;硬件相关'],
    description: '电介质在交变电场中能量损耗的大小',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0374',
    name: '耐电弧性',
    type: '性能指标',
    category: 'components',
    aliases: ['抗电弧性'],
    tags: ['物料;电气性能;安全相关'],
    description: '绝缘材料抵抗电弧作用的能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0375',
    name: '耐漏电起痕指数',
    type: '性能指标',
    category: 'components',
    aliases: ['CTI'],
    tags: ['物料;电气性能;安全相关'],
    description: '绝缘材料表面抵抗漏电痕迹的能力',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0376',
    name: '氧指数',
    type: '性能指标',
    category: 'components',
    aliases: ['极限氧指数'],
    tags: ['物料;安全相关;可靠性'],
    description: '材料在氧气和氮气混合气体中维持燃烧所需的最低氧气浓度',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0377',
    name: 'UL94阻燃等级',
    type: '性能指标',
    category: 'components',
    aliases: ['燃烧等级'],
    tags: ['物料;安全相关;可靠性'],
    description: '塑料材料阻燃性能评价标准',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0378',
    name: '玻璃化转变温度',
    type: '性能指标',
    category: 'components',
    aliases: ['Tg'],
    tags: ['物料;可靠性;制造工艺'],
    description: '聚合物从玻璃态向高弹态转变的温度',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0379',
    name: '熔融温度',
    type: '性能指标',
    category: 'components',
    aliases: ['熔点'],
    tags: ['物料;制造工艺;可靠性'],
    description: '晶体材料从固态转变为液态的温度',
    created_at: '2025-09-26T09:43:14.261493',
    updated_at: '2025-09-26T09:43:14.261493'
});
CREATE (d:Dictionary {
    id: 'TERM_0380',
    name: '热变形温度',
    type: '性能指标',
    category: 'components',
    aliases: ['HDT'],
    tags: ['物料;可靠性;制造工艺'],
    description: '塑料在特定负荷下达到规定变形量的温度',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0381',
    name: '维卡软化温度',
    type: '性能指标',
    category: 'components',
    aliases: ['VST'],
    tags: ['物料;可靠性;制造工艺'],
    description: '塑料在特定条件下达到规定压入深度的温度',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0382',
    name: '吸水率',
    type: '性能指标',
    category: 'components',
    aliases: ['吸湿率'],
    tags: ['物料;可靠性;制造工艺'],
    description: '材料浸泡在水中吸收水分的程度',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0383',
    name: '透湿率',
    type: '性能指标',
    category: 'components',
    aliases: ['水蒸气透过率'],
    tags: ['物料;可靠性;制造工艺'],
    description: '材料透过水蒸气的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0384',
    name: '透气率',
    type: '性能指标',
    category: 'components',
    aliases: ['气体透过率'],
    tags: ['物料;可靠性;制造工艺'],
    description: '材料透过氧气等气体的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0385',
    name: '耐化学药品性',
    type: '性能指标',
    category: 'components',
    aliases: ['耐化学品性'],
    tags: ['物料;可靠性;制造工艺'],
    description: '材料抵抗酸碱溶剂等化学药品侵蚀的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0386',
    name: '耐候性',
    type: '性能指标',
    category: 'components',
    aliases: ['耐老化性'],
    tags: ['物料;可靠性;外观'],
    description: '材料抵抗阳光雨水温度等气候条件破坏的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0387',
    name: '耐磨性',
    type: '性能指标',
    category: 'components',
    aliases: ['耐磨损性'],
    tags: ['物料;可靠性;外观'],
    description: '材料抵抗机械磨损的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0388',
    name: '耐刮擦性',
    type: '性能指标',
    category: 'components',
    aliases: ['抗刮擦性'],
    tags: ['物料;可靠性;外观'],
    description: '材料表面抵抗刮擦损伤的能力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0389',
    name: '平均无故障时间',
    type: '性能指标',
    category: 'components',
    aliases: ['MTBF'],
    tags: ['可靠性;性能指标;质量体系'],
    description: '可修复产品相邻两次故障间的平均工作时间',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0390',
    name: '平均修复时间',
    type: '性能指标',
    category: 'components',
    aliases: ['MTTR'],
    tags: ['可靠性;性能指标;质量体系'],
    description: '故障修复所需的平均时间',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0391',
    name: '失效率',
    type: '性能指标',
    category: 'components',
    aliases: ['故障率'],
    tags: ['可靠性;性能指标;质量体系'],
    description: '单位时间内产品发生故障的概率',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0392',
    name: '浴盆曲线',
    type: '性能指标',
    category: 'components',
    aliases: ['故障率曲线'],
    tags: ['可靠性;性能指标;质量体系'],
    description: '产品失效率随时间变化的典型曲线形状',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0393',
    name: 'IP防护等级',
    type: '性能指标',
    category: 'components',
    aliases: ['异物防护等级'],
    tags: ['法规;可靠性;结构相关'],
    description: '针对电气设备防尘防水能力的国际标准等级',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0394',
    name: 'IK防护等级',
    type: '性能指标',
    category: 'components',
    aliases: ['冲击防护等级'],
    tags: ['法规;可靠性;结构相关'],
    description: '针对电气设备外壳抵御外部机械冲击能力的等级',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0395',
    name: '比吸收率',
    type: '性能指标',
    category: 'components',
    aliases: ['SAR'],
    tags: ['法规;安全相关;射频相关'],
    description: '衡量人体吸收电磁辐射能量的速率有严格的法规限值',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0396',
    name: '听力安全',
    type: '性能指标',
    category: 'components',
    aliases: ['声压级限值'],
    tags: ['法规;安全相关;声学'],
    description: '对耳机等音频设备输出声压级的限制以保护听力',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0397',
    name: '激光安全',
    type: '性能指标',
    category: 'components',
    aliases: ['激光辐射安全'],
    tags: ['法规;安全相关;硬件相关'],
    description: '对设备激光辐射强度的安全限制要求',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0398',
    name: '生物相容性',
    type: '性能指标',
    category: 'components',
    aliases: ['皮肤刺激性'],
    tags: ['法规;安全相关;可靠性'],
    description: '与人体接触的材料不引起过敏或刺激反应的要求',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0399',
    name: '碳足迹',
    type: '性能指标',
    category: 'components',
    aliases: ['碳排放量'],
    tags: ['法规;环保;供应链'],
    description: '产品全生命周期温室气体排放量的量化指标',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0400',
    name: 'Hotspot',
    type: '其他',
    category: 'symptoms',
    aliases: ['热点;局部过热'],
    tags: ['硬件相关;可靠性'],
    description: '手机特定区域（如SoC、充电芯片）温度过高，影响用户体验和安全。',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0401',
    name: '暗角',
    type: '其他',
    category: 'symptoms',
    aliases: ['边缘暗影;Shading'],
    tags: ['摄像头模组;影像相关'],
    description: '照片四角出现亮度低于中心的现象，与镜头光学设计或组装有关。',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0402',
    name: '白点',
    type: '其他',
    category: 'symptoms',
    aliases: ['亮点;White Spot'],
    tags: ['硬件相关;显示相关'],
    description: '显示屏上常亮的白色像素点，属于LCD/OLED的坏点的一种。',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0403',
    name: '爆音',
    type: '其他',
    category: 'symptoms',
    aliases: ['破音;Popping Sound'],
    tags: ['硬件相关;声学'],
    description: '扬声器在特定频率下输出失真，产生刺耳的噼啪声。',
    created_at: '2025-09-26T09:43:14.262495',
    updated_at: '2025-09-26T09:43:14.262495'
});
CREATE (d:Dictionary {
    id: 'TERM_0404',
    name: '变砖',
    type: '其他',
    category: 'symptoms',
    aliases: ['无法开机;系统崩溃;Brick'],
    tags: ['软件相关;硬件相关'],
    description: '手机软件系统严重故障，无法正常启动或使用的状态，通常需强制刷机修复。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0405',
    name: '波纹',
    type: '其他',
    category: 'symptoms',
    aliases: ['水波纹;Moire'],
    tags: ['显示相关;影像相关'],
    description: '在拍摄特定条纹图案时，因空间频率混叠产生的干扰波纹。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0406',
    name: '残胶',
    type: '其他',
    category: 'symptoms',
    aliases: ['胶水残留;Glue Residual'],
    tags: ['制造工艺;外观'],
    description: '在点胶或贴合工艺后，多余的胶水残留在产品表面，影响美观和性能。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0407',
    name: '断触',
    type: '其他',
    category: 'symptoms',
    aliases: ['触摸失灵;Touch Failure'],
    tags: ['硬件相关;人机交互'],
    description: '触摸屏局部或全部失去响应，可能与TP本身、FPC连接或软件驱动有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0408',
    name: '断流',
    type: '其他',
    category: 'symptoms',
    aliases: ['网络中断;Network Disconnection'],
    tags: ['硬件相关;软件相关'],
    description: '在使用Wi-Fi或移动数据时，网络连接意外中断又快速恢复的现象。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0409',
    name: '发热',
    type: '其他',
    category: 'symptoms',
    aliases: ['过热;Overheat'],
    tags: ['硬件相关;可靠性'],
    description: '手机在充电、高负载运算或信号差时产生的明显温升，影响手感和安全。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0410',
    name: '发烫',
    type: '其他',
    category: 'symptoms',
    aliases: ['严重发热'],
    tags: ['硬件相关;安全相关'],
    description: '比发热更严重的温度异常，可能预示硬件短路或散热设计缺陷。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0411',
    name: '反白',
    type: '其他',
    category: 'symptoms',
    aliases: ['亮点反转;White Spot Reverse'],
    tags: ['显示相关'],
    description: 'LCD显示屏上出现的异常亮斑，与液晶分子排列异常有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0412',
    name: '飞漆',
    type: '其他',
    category: 'symptoms',
    aliases: ['油漆飞溅;Overspray'],
    tags: ['制造工艺;外观'],
    description: '在喷涂过程中，油漆颗粒溅到非目标区域，造成外观不良。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0413',
    name: '分色',
    type: '其他',
    category: 'symptoms',
    aliases: ['颜色差异;Color Difference'],
    tags: ['外观;CMF'],
    description: '同一部件或相邻部件之间存在肉眼可察觉的颜色不一致。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0414',
    name: '腐蚀',
    type: '其他',
    category: 'symptoms',
    aliases: ['生锈;腐蚀;Corrosion'],
    tags: ['可靠性;外观'],
    description: '金属部件因接触汗液、盐雾等腐蚀性物质而发生的化学变化，影响功能和寿命。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0415',
    name: '干腐',
    type: '其他',
    category: 'symptoms',
    aliases: ['干性腐蚀;Dry Corrosion'],
    tags: ['可靠性;硬件相关'],
    description: '金属在干燥环境下与气体（如氧气）发生化学反应导致的腐蚀。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0416',
    name: '鼓包',
    type: '其他',
    category: 'symptoms',
    aliases: ['电池鼓包;Battery Swelling'],
    tags: ['硬件相关;安全相关'],
    description: '电池内部产生气体导致外壳膨胀，是严重的安全隐患，需立即停用。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0417',
    name: '刮伤',
    type: '其他',
    category: 'symptoms',
    aliases: ['划痕;Scratch'],
    tags: ['外观;可靠性'],
    description: '产品表面因摩擦留下的线性痕迹，影响美观，严重时影响功能。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0418',
    name: '关机',
    type: '其他',
    category: 'symptoms',
    aliases: ['自动关机;Auto Shutdown'],
    tags: ['软件相关;硬件相关'],
    description: '非人为操作导致的手机自动断电，可能与电池、电源管理芯片或系统有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0419',
    name: '龟裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['细微裂纹;Craze Cracks'],
    tags: ['结构相关;可靠性'],
    description: '塑料或涂层表面出现的网状细微裂纹，通常与内应力或老化有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0420',
    name: '黑屏',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏幕不亮;Black Screen'],
    tags: ['显示相关;硬件相关'],
    description: '手机有反应（如振动）但屏幕无任何显示，可能与屏幕、FPC或主板供电有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0421',
    name: '花屏',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏幕花屏;Screen Corruption'],
    tags: ['显示相关;硬件相关'],
    description: '屏幕显示乱码、条纹或色块，通常与显示接口、驱动芯片或内存有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0422',
    name: '划伤',
    type: '其他',
    category: 'symptoms',
    aliases: ['刮伤;Scratch'],
    tags: ['外观;可靠性'],
    description: '产品表面因摩擦留下的线性痕迹，影响美观，严重时影响功能。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0423',
    name: '黄斑',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏幕黄斑;Yellow Spot'],
    tags: ['显示相关'],
    description: 'OLED屏幕局部出现的黄色斑块，可能与封装或材料老化有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0424',
    name: '混光',
    type: '其他',
    category: 'symptoms',
    aliases: ['灯光混合;Light Mixing'],
    tags: ['硬件相关;外观'],
    description: '不同颜色的LED灯光相互干扰，导致光色不纯，常见于指示灯设计。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0425',
    name: '击穿',
    type: '其他',
    category: 'symptoms',
    aliases: ['电压击穿;Breakdown'],
    tags: ['硬件相关;安全相关'],
    description: '元器件因过电压导致绝缘失效而损坏，如电容击穿、ESD击穿。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0426',
    name: '积墨',
    type: '其他',
    category: 'symptoms',
    aliases: ['锡膏堆积;Solder Paste Accumulation'],
    tags: ['SMT;制造工艺'],
    description: '钢网开口堵塞或刮刀压力不当导致锡膏印刷后局部过量，易引起连锡。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0427',
    name: '夹料',
    type: '其他',
    category: 'symptoms',
    aliases: ['材料被夹;Material Pinching'],
    tags: ['制造工艺;结构相关'],
    description: '在装配过程中，线材、FPC等软性材料被外壳或螺丝不当挤压。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0428',
    name: '假电',
    type: '其他',
    category: 'symptoms',
    aliases: ['虚电;False Power'],
    tags: ['硬件相关;软件相关'],
    description: '手机显示电量充足但迅速关机，通常与电池老化、电量计校准不准有关。',
    created_at: '2025-09-26T09:43:14.263493',
    updated_at: '2025-09-26T09:43:14.263493'
});
CREATE (d:Dictionary {
    id: 'TERM_0429',
    name: '假压',
    type: '其他',
    category: 'symptoms',
    aliases: ['虚压;False Pressure'],
    tags: ['制造工艺;结构相关'],
    description: '螺丝未真正拧紧或扭矩失效，导致连接松动，存在可靠性风险。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0430',
    name: '胶印',
    type: '其他',
    category: 'symptoms',
    aliases: ['胶水痕迹;Adhesive Mark'],
    tags: ['外观;制造工艺'],
    description: '胶水溢出或擦拭不净，在产品表面留下可见的痕迹。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0431',
    name: '焦灼',
    type: '其他',
    category: 'symptoms',
    aliases: ['烧焦;Burn Mark'],
    tags: ['硬件相关;可靠性'],
    description: '局部过热导致塑料或PCB碳化变黑，通常为严重故障的表现。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0432',
    name: '接触不良',
    type: '其他',
    category: 'symptoms',
    aliases: ['接触不稳定;Intermittent Contact'],
    tags: ['硬件相关;电气连接'],
    description: '连接器、开关等因氧化、松动或污染导致时通时断的现象。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0433',
    name: '结块',
    type: '其他',
    category: 'symptoms',
    aliases: ['胶水结块;Adhesive Lumping'],
    tags: ['制造工艺;物料'],
    description: '胶水在储存或使用前发生部分固化，形成颗粒，影响点胶效果。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0434',
    name: '卡顿',
    type: '其他',
    category: 'symptoms',
    aliases: ['操作不流畅;Lag'],
    tags: ['软件相关;性能指标'],
    description: '系统或应用响应缓慢，界面动画掉帧，严重影响用户体验。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0435',
    name: '开胶',
    type: '其他',
    category: 'symptoms',
    aliases: ['脱胶;De-lamination'],
    tags: ['结构相关;制造工艺'],
    description: '粘接的部件之间出现分离，如屏幕开胶、电池盖开胶。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0436',
    name: '开裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['破裂;Crack'],
    tags: ['结构相关;可靠性'],
    description: '材料或部件出现裂缝，通常由应力过大、材料脆性或冲击导致。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0437',
    name: '开短路',
    type: '其他',
    category: 'symptoms',
    aliases: ['开路与短路;Open/Short Circuit'],
    tags: ['硬件相关;电气连接'],
    description: '电路两种基本故障模式：开路（断开）和短路（异常连接）。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0438',
    name: '空焊',
    type: '其他',
    category: 'symptoms',
    aliases: ['未上锡;Non-wetting'],
    tags: ['SMT;制造工艺'],
    description: '元器件引脚或焊盘没有与焊锡形成良好的冶金结合。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0439',
    name: '孔偏',
    type: '其他',
    category: 'symptoms',
    aliases: ['钻孔偏移;Drilling Offset'],
    tags: ['PCB;制造工艺'],
    description: 'PCB上的钻孔位置偏离设计中心，可能导致电气连接不良或短路。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0440',
    name: '口哨声',
    type: '其他',
    category: 'symptoms',
    aliases: ['啸叫;Whistling Noise'],
    tags: ['硬件相关;声学'],
    description: '电感、变压器等磁性元件在特定频率下振动产生的噪音。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0441',
    name: '溃缩',
    type: '其他',
    category: 'symptoms',
    aliases: ['压溃变形;Crushing Deformation'],
    tags: ['结构相关;可靠性'],
    description: '材料或结构在压力下发生永久性的压缩变形，失去原有功能。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0442',
    name: '拉丝',
    type: '其他',
    category: 'symptoms',
    aliases: ['材料拉丝;Stringing'],
    tags: ['制造工艺;外观'],
    description: '在点胶或塑料注塑过程中，材料被拉扯成丝状残留物。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0443',
    name: '乐音',
    type: '其他',
    category: 'symptoms',
    aliases: ['异音;Abnormal Sound'],
    tags: ['硬件相关;声学'],
    description: '电机、齿轮等运动部件发出的非预期的、不悦耳的噪音。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0444',
    name: '连锡',
    type: '其他',
    category: 'symptoms',
    aliases: ['锡桥;Solder Bridge'],
    tags: ['SMT;制造工艺'],
    description: '焊锡在相邻的两个焊点之间形成非预期的连接，导致短路。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0445',
    name: '亮斑',
    type: '其他',
    category: 'symptoms',
    aliases: ['亮点;Bright Spot'],
    tags: ['显示相关'],
    description: '显示屏上常亮的像素点或区域，属于显示缺陷。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0446',
    name: '亮线',
    type: '其他',
    category: 'symptoms',
    aliases: ['亮线缺陷;Line Defect'],
    tags: ['显示相关'],
    description: '显示屏上出现的异常亮线，通常与驱动线路或屏幕本身损伤有关。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0447',
    name: '裂纹',
    type: '其他',
    category: 'symptoms',
    aliases: ['裂痕;Crack'],
    tags: ['结构相关;可靠性'],
    description: '材料局部开裂形成的缝隙，可能由应力、疲劳或缺陷引起。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0448',
    name: '漏光',
    type: '其他',
    category: 'symptoms',
    aliases: ['光泄漏;Light Leakage'],
    tags: ['显示相关;硬件相关'],
    description: '屏幕边框处有非预期的光线射出，影响视觉效果和产品档次感。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0449',
    name: '漏液',
    type: '其他',
    category: 'symptoms',
    aliases: ['电池漏液;Liquid Leakage'],
    tags: ['硬件相关;安全相关'],
    description: '电池电解液泄漏，具有腐蚀性且可能引发安全问题，是严重不良。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0450',
    name: '漏码',
    type: '其他',
    category: 'symptoms',
    aliases: ['激光漏打;Missing Laser Marking'],
    tags: ['制造工艺;外观'],
    description: '产品上应有的序列号、Logo等信息未被激光打标或打标不清。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0451',
    name: '漏贴',
    type: '其他',
    category: 'symptoms',
    aliases: ['元件漏贴;Missing Component'],
    tags: ['SMT;制造工艺'],
    description: '贴片机未能将元器件贴装到PCB指定位置上。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0452',
    name: '露白',
    type: '其他',
    category: 'symptoms',
    aliases: ['底色显露;Substrate Exposure'],
    tags: ['外观;CMF'],
    description: '喷涂或镀层厚度不足或不均匀，导致底层材料颜色显露出来。',
    created_at: '2025-09-26T09:43:14.264500',
    updated_at: '2025-09-26T09:43:14.264500'
});
CREATE (d:Dictionary {
    id: 'TERM_0453',
    name: '露铜',
    type: '其他',
    category: 'symptoms',
    aliases: ['铜层暴露;Copper Exposure'],
    tags: ['PCB;可靠性'],
    description: 'PCB表面的阻焊层破损，导致底层铜箔暴露，易氧化和短路。',
    created_at: '2025-09-26T09:43:14.265494',
    updated_at: '2025-09-26T09:43:14.265494'
});
CREATE (d:Dictionary {
    id: 'TERM_0454',
    name: '乱码',
    type: '其他',
    category: 'symptoms',
    aliases: ['显示乱码;Garbled Characters'],
    tags: ['显示相关;软件相关'],
    description: '屏幕显示的文字或符号变成无法识别的代码，可能与软件或内存有关。',
    created_at: '2025-09-26T09:43:14.265494',
    updated_at: '2025-09-26T09:43:14.265494'
});
CREATE (d:Dictionary {
    id: 'TERM_0455',
    name: '麻点',
    type: '其他',
    category: 'symptoms',
    aliases: ['表面凹点;Pitting'],
    tags: ['外观;制造工艺'],
    description: '产品表面出现的细小凹坑，可能与注塑、喷涂或电镀工艺有关。',
    created_at: '2025-09-26T09:43:14.265494',
    updated_at: '2025-09-26T09:43:14.265494'
});
CREATE (d:Dictionary {
    id: 'TERM_0456',
    name: '毛边',
    type: '其他',
    category: 'symptoms',
    aliases: ['毛刺;Burr'],
    tags: ['制造工艺;外观'],
    description: '金属或塑料件加工后边缘留下的多余材料，影响装配和安全。',
    created_at: '2025-09-26T09:43:14.265494',
    updated_at: '2025-09-26T09:43:14.265494'
});
CREATE (d:Dictionary {
    id: 'TERM_0457',
    name: '毛絮',
    type: '其他',
    category: 'symptoms',
    aliases: ['纤维粉尘;Lint'],
    tags: ['制造工艺;外观'],
    description: '环境中或擦拭布上的纤维绒毛附着在产品表面，影响清洁度。',
    created_at: '2025-09-26T09:43:14.265494',
    updated_at: '2025-09-26T09:43:14.265494'
});
CREATE (d:Dictionary {
    id: 'TERM_0458',
    name: '霉斑',
    type: '其他',
    category: 'symptoms',
    aliases: ['发霉;Mildew'],
    tags: ['可靠性;外观'],
    description: '在高温高湿环境下，有机物表面生长的霉菌斑点。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0459',
    name: '米粒',
    type: '其他',
    category: 'symptoms',
    aliases: ['锡珠;Solder Ball'],
    tags: ['SMT;制造工艺'],
    description: '回流焊后散布在PCB上的微小锡球，可能引起短路。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0460',
    name: '模垢',
    type: '其他',
    category: 'symptoms',
    aliases: ['模具污垢;Mold Contamination'],
    tags: ['制造工艺;外观'],
    description: '模具表面的残留物转移到产品上，导致注塑件表面缺陷。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0461',
    name: '模痕',
    type: '其他',
    category: 'symptoms',
    aliases: ['合模线;Parting Line'],
    tags: ['结构相关;外观'],
    description: '注塑件在模具分型面处产生的轻微痕迹，工艺控制可减轻其明显度。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0462',
    name: '难拆',
    type: '其他',
    category: 'symptoms',
    aliases: ['拆卸困难;Difficult Disassembly'],
    tags: ['结构相关;维修'],
    description: '产品设计或组装导致维修时难以拆卸，影响可维修性。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0463',
    name: '尿印',
    type: '其他',
    category: 'symptoms',
    aliases: ['水渍痕;Water Spot'],
    tags: ['外观;制造工艺'],
    description: '清洗或擦拭后留下的水渍或清洗剂痕迹，干燥后形成印迹。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0464',
    name: '凝露',
    type: '其他',
    category: 'symptoms',
    aliases: ['冷凝水;Condensation'],
    tags: ['可靠性;测试验证'],
    description: '当环境温度骤变，手机内部较冷的表面凝结出水珠，可能导致短路。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0465',
    name: '抛料',
    type: '其他',
    category: 'symptoms',
    aliases: ['元件抛料;Component Rejection'],
    tags: ['SMT;制造工艺'],
    description: '贴片机识别元件不合格或取料失败后将其丢弃，影响效率和成本。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0466',
    name: '批锋',
    type: '其他',
    category: 'symptoms',
    aliases: ['毛边;Flash'],
    tags: ['制造工艺;外观'],
    description: '注塑件在模具分型面或顶针处产生的薄边多余料。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0467',
    name: '偏位',
    type: '其他',
    category: 'symptoms',
    aliases: ['位置偏移;Misalignment'],
    tags: ['制造工艺;SMT'],
    description: '元器件贴装位置偏离焊盘中心，可能引起虚焊或短路。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0468',
    name: '漂移',
    type: '其他',
    category: 'symptoms',
    aliases: ['参数漂移;Parameter Drift'],
    tags: ['硬件相关;可靠性'],
    description: '元器件参数（如电阻值、时钟频率）随时间或温度发生缓慢变化。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0469',
    name: '气泡',
    type: '其他',
    category: 'symptoms',
    aliases: ['气泡缺陷;Air Bubble'],
    tags: ['制造工艺;外观'],
    description: '在胶合、贴合或注塑过程中，内部或层间残留的空气泡。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0470',
    name: '翘曲',
    type: '其他',
    category: 'symptoms',
    aliases: ['变形;Warpage'],
    tags: ['结构相关;可靠性'],
    description: '平板状部件（如PCB、电池盖）发生的弯曲或扭曲变形。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0471',
    name: '翘脚',
    type: '其他',
    category: 'symptoms',
    aliases: ['引脚翘起;Lifted Lead'],
    tags: ['SMT;制造工艺'],
    description: '元器件引脚未与焊盘接触而翘起，导致开路。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0472',
    name: '缺胶',
    type: '其他',
    category: 'symptoms',
    aliases: ['胶量不足;Insufficient Adhesive'],
    tags: ['制造工艺;结构相关'],
    description: '点胶量未达到要求，导致粘接强度或密封性能不足。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0473',
    name: '缺口',
    type: '其他',
    category: 'symptoms',
    aliases: ['边缘缺口;Notch'],
    tags: ['结构相关;外观'],
    description: '材料边缘因磕碰或加工不良形成的V形或U形缺损。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0474',
    name: '热损',
    type: '其他',
    category: 'symptoms',
    aliases: ['热损伤;Thermal Damage'],
    tags: ['硬件相关;可靠性'],
    description: '元器件因过热导致的不可逆性能劣化或损坏。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0475',
    name: '熔损',
    type: '其他',
    category: 'symptoms',
    aliases: ['过熔;Solder Melting Loss'],
    tags: ['SMT;制造工艺'],
    description: '过高的温度或过长的加热时间导致焊锡过度流失，焊点不饱满。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0476',
    name: '色差',
    type: '其他',
    category: 'symptoms',
    aliases: ['颜色差异;Color Difference'],
    tags: ['外观;CMF'],
    description: '同一产品不同批次，或同一批次不同部件之间存在颜色差异。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0477',
    name: '沙眼',
    type: '其他',
    category: 'symptoms',
    aliases: ['针孔;Pinhole'],
    tags: ['外观;制造工艺'],
    description: '涂层或镀层表面出现的极其细微的孔洞，如同针尖扎过。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0478',
    name: '闪退',
    type: '其他',
    category: 'symptoms',
    aliases: ['应用崩溃;App Crash'],
    tags: ['软件相关'],
    description: '应用程序在运行过程中突然关闭并返回主界面。',
    created_at: '2025-09-26T09:43:14.265701',
    updated_at: '2025-09-26T09:43:14.265701'
});
CREATE (d:Dictionary {
    id: 'TERM_0479',
    name: '伤盘',
    type: '其他',
    category: 'symptoms',
    aliases: ['焊盘损伤;Pad Damage'],
    tags: ['PCB;维修'],
    description: 'PCB焊盘因过度加热、刮擦或多次焊接而脱落或损坏。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0480',
    name: '失效',
    type: '其他',
    category: 'symptoms',
    aliases: ['功能失效;Failure'],
    tags: ['可靠性'],
    description: '产品失去规定功能的状态。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0481',
    name: '油污',
    type: '其他',
    category: 'symptoms',
    aliases: ['油渍;Oil Stain'],
    tags: ['外观;制造工艺'],
    description: '产品表面沾染的油脂污渍。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0482',
    name: '鱼眼',
    type: '其他',
    category: 'symptoms',
    aliases: ['透镜状缺陷;Fish Eye'],
    tags: ['外观;涂层'],
    description: '涂层表面出现的类似鱼眼的圆形凹坑或凸起。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0483',
    name: '云纹',
    type: '其他',
    category: 'symptoms',
    aliases: ['摩尔纹;Moiré Pattern'],
    tags: ['影像相关'],
    description: '当两个周期性图案（如感光元件像素和景物纹理）重叠时产生的干扰条纹。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0484',
    name: '脏污',
    type: '其他',
    category: 'symptoms',
    aliases: ['同污点'],
    tags: ['外观;制造工艺'],
    description: '产品表面附着的油污、灰尘等异物。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0485',
    name: '噪点',
    type: '其他',
    category: 'symptoms',
    aliases: ['图像噪点;Image Noise'],
    tags: ['影像相关'],
    description: '图像中出现的随机颗粒状干扰，在低光照下尤为明显。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0486',
    name: '自愈',
    type: '其他',
    category: 'symptoms',
    aliases: ['自恢复;Self-recovery'],
    tags: ['软件相关;可靠性'],
    description: '系统发生轻微故障后，能自动恢复正常功能的现象。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0487',
    name: '醉机',
    type: '其他',
    category: 'symptoms',
    aliases: ['系统错乱;System Confusion'],
    tags: ['软件相关'],
    description: '系统行为异常，功能紊乱，但尚未死机或重启，通常需重启恢复。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0488',
    name: '对焦失败',
    type: '其他',
    category: 'symptoms',
    aliases: ['无法对焦;Focus Fail'],
    tags: ['影像相关;摄像头模组'],
    description: '**定义**: 摄像头无法正确锁定焦点。 **判定口径**: AF成功率 <95%。 **常见场景**: 暗光/微距/移动拍摄。 **排查路径**: 检查固件→电机→镜头洁净度。 **对策**: 增加AF日志采集，改善模组洁净管控。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0489',
    name: '死机',
    type: '其他',
    category: 'symptoms',
    aliases: ['系统死机;Hang'],
    tags: ['软件相关;硬件相关'],
    description: '**定义**: 系统停止响应。 **判定口径**: 连续无响应 >30s。 **常见场景**: 高并发任务/内存不足。 **排查路径**: 抓取log→检查内存/CPU占用。 **对策**: 优化系统调度，增加watchdog。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0490',
    name: '电流过大',
    type: '其他',
    category: 'symptoms',
    aliases: ['Over Current'],
    tags: ['硬件相关;电气性能'],
    description: '**定义**: 工作电流超过额定值。 **判定口径**: 电流 >1.5×额定。 **常见场景**: 充电、射频发射。 **排查路径**: 检查供电→替换IC。 **对策**: 增加过流保护，优化电源管理。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0491',
    name: '短路',
    type: '其他',
    category: 'symptoms',
    aliases: ['Short Circuit'],
    tags: ['硬件相关;电气连接'],
    description: '**定义**: 电路异常导通。 **判定口径**: 电阻 <1Ω。 **常见场景**: PCBA调试。 **排查路径**: 热像定位→逐级隔离。 **对策**: 增加保护设计，加强制程防呆。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0492',
    name: '松脱',
    type: '其他',
    category: 'symptoms',
    aliases: ['松动;Loose'],
    tags: ['结构相关;可靠性'],
    description: '**定义**: 螺丝/卡扣失去紧固力。 **判定口径**: 力矩 <70% 标准。 **常见场景**: 跌落/运输。 **排查路径**: 检查扭矩记录。 **对策**: 增加锁附监控，改善螺丝工艺。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0493',
    name: '虚焊',
    type: '其他',
    category: 'symptoms',
    aliases: ['假焊;Cold Solder'],
    tags: ['SMT;制造工艺'],
    description: '**定义**: 焊点不牢固。 **判定口径**: X-Ray 显示空洞 >20%。 **常见场景**: PCBA生产。 **排查路径**: 检查焊膏→回流工艺。 **对策**: 增强锡膏管理，优化工艺窗口。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0494',
    name: '噪音',
    type: '其他',
    category: 'symptoms',
    aliases: ['杂音;Noise'],
    tags: ['声学;硬件相关'],
    description: '**定义**: 通话/播放时出现异常声音。 **判定口径**: SNR <20dB。 **常见场景**: 通话/音频播放。 **排查路径**: 检查麦克风→音频IC。 **对策**: 优化声学设计，改善防尘网。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0495',
    name: '亮度不均',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏幕亮度不均;Brightness Uneven'],
    tags: ['显示相关;影像相关'],
    description: '**定义**: 屏幕不同区域亮度差异。 **判定口径**: ΔL/L >20%。 **常见场景**: 灰阶测试。 **排查路径**: 检查背光模组。 **对策**: 改善背光均匀性设计。',
    created_at: '2025-09-26T09:43:14.266595',
    updated_at: '2025-09-26T09:43:14.266595'
});
CREATE (d:Dictionary {
    id: 'TERM_0496',
    name: '锌合金模垢',
    type: '其他',
    category: 'symptoms',
    aliases: ['锌合金模具沉积物'],
    tags: ['制造工艺;外观'],
    description: '锌合金压铸时，合金元素在模具表面析出形成的污垢，影响铸件表面质量。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0497',
    name: '爬行腐蚀',
    type: '其他',
    category: 'symptoms',
    aliases: ['creep corrosion'],
    tags: ['可靠性;PCB;硬件相关'],
    description: '在含硫气氛中，银等金属表面生成导电性硫化物绒毛，并在电场下延伸生长，导致短路。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0498',
    name: '爆米花效应',
    type: '其他',
    category: 'symptoms',
    aliases: ['popcorning'],
    tags: ['可靠性;SMT;封装'],
    description: '受潮的IC封装在回流焊高温下，内部水分急速汽化导致封装材料开裂。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0499',
    name: '锡须',
    type: '其他',
    category: 'symptoms',
    aliases: ['Tin Whisker'],
    tags: ['可靠性;硬件相关;PCB'],
    description: '纯锡镀层表面自发生长的细长锡晶须，可能引起短路。高铅或合金镀层可抑制。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0500',
    name: '冷焊点',
    type: '其他',
    category: 'symptoms',
    aliases: ['Cold Solder Joint'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '焊点温度不足，焊料未完全熔化，表面粗糙呈灰暗色，连接强度极差。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0501',
    name: '银迁移',
    type: '其他',
    category: 'symptoms',
    aliases: ['Silver Migration'],
    tags: ['可靠性;硬件相关;PCB'],
    description: '在直流电场和湿度作用下，银离子在绝缘体表面迁移析出，导致绝缘下降和短路。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0502',
    name: '电化学迁移',
    type: '其他',
    category: 'symptoms',
    aliases: ['ECM'],
    tags: ['可靠性;PCB;硬件相关'],
    description: '详见前表电糊。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0503',
    name: '缩水痕',
    type: '其他',
    category: 'symptoms',
    aliases: ['Sink Mark'],
    tags: ['制造工艺;注塑;外观'],
    description: '塑胶件在肉厚较大区域因冷却收缩不均而产生的表面凹陷。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0504',
    name: '焊料球',
    type: '其他',
    category: 'symptoms',
    aliases: ['Solder Ball'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '回流焊后，在焊盘周围或器件底部形成的独立小球，是焊接不良的一种。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0505',
    name: '彩虹纹',
    type: '其他',
    category: 'symptoms',
    aliases: ['Newton\'s Rings'],
    tags: ['显示相关;外观;摄像头模组'],
    description: '两层透明材料因微小间隙产生光干涉形成的彩色环状条纹。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0506',
    name: '引脚浮高',
    type: '其他',
    category: 'symptoms',
    aliases: ['Lead Lifting'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '元件引脚未与焊盘接触而翘起，通常发生在维修或应力冲击后。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0507',
    name: '晶振频偏',
    type: '其他',
    category: 'symptoms',
    aliases: ['Crystal Frequency Deviation'],
    tags: ['硬件相关;可靠性;通信相关'],
    description: '晶体振荡器的实际输出频率偏离其标称频率超出允许范围。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0508',
    name: '助焊剂残留',
    type: '其他',
    category: 'symptoms',
    aliases: ['Flux Residue'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '焊接后残留的助焊剂，若具腐蚀性或影响绝缘，需清洗或使用免清洗型。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0509',
    name: '焊点疲劳',
    type: '其他',
    category: 'symptoms',
    aliases: ['Solder Joint Fatigue'],
    tags: ['可靠性;SMT;硬件相关'],
    description: '焊点在温度循环或机械应力下，因热膨胀系数不匹配而产生的裂纹和失效。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0510',
    name: '模内应力',
    type: '其他',
    category: 'symptoms',
    aliases: ['Molded-in Stress'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '塑胶件在注塑成型过程中产生的内应力，是后续变形和开裂的根源。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0511',
    name: '锡瘟',
    type: '其他',
    category: 'symptoms',
    aliases: ['Tin Pest'],
    tags: ['可靠性;物料;硬件相关'],
    description: '纯锡在低温下（<13.2°C）由白锡（β锡）转变为灰锡（α锡）的相变，伴随体积膨胀和粉末化。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0512',
    name: '板翘',
    type: '其他',
    category: 'symptoms',
    aliases: ['Board Warpage'],
    tags: ['PCB;制造工艺;可靠性'],
    description: 'PCB本身的翘曲。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0513',
    name: '电迁移',
    type: '其他',
    category: 'symptoms',
    aliases: ['Electromigration'],
    tags: ['可靠性;硬件相关;半导体'],
    description: '集成电路金属互连线中，在高电流密度下金属原子沿电子流方向迁移，导致导线开路或短路。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0514',
    name: '锡珠飞溅',
    type: '其他',
    category: 'symptoms',
    aliases: ['Solder Ball Splashing'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '回流焊时，因预热不足或助焊剂沸腾导致锡膏中的锡珠飞散到焊盘外。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0515',
    name: '板边毛刺',
    type: '其他',
    category: 'symptoms',
    aliases: ['Board Edge Burr'],
    tags: ['PCB;制造工艺;外观'],
    description: 'PCB分板后边缘产生的突出物。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0516',
    name: '触控失灵',
    type: '其他',
    category: 'symptoms',
    aliases: ['触摸屏无响应;Touch Fail'],
    tags: ['显示相关;人机交互'],
    description: '**定义**: 触摸操作无效或延迟。 **判定口径**: 单点/多点触控测试失败。 **常见场景**: 高湿环境、屏幕贴膜。 **排查路径**: 检查TP模组→固件→驱动IC。 **对策**: 优化算法，改善屏幕贴合。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0517',
    name: '信号弱',
    type: '其他',
    category: 'symptoms',
    aliases: ['信号差;Low Signal'],
    tags: ['通信相关;用户体验'],
    description: '**定义**: 手机在正常网络环境下信号强度不足。 **判定口径**: RSRP < -110dBm。 **常见场景**: 地铁、地下室。 **排查路径**: 检查天线设计→射频通道。 **对策**: 优化天线布局，增加功放。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0518',
    name: '通话掉线',
    type: '其他',
    category: 'symptoms',
    aliases: ['Call Drop'],
    tags: ['通信相关;用户体验'],
    description: '**定义**: 通话过程中意外中断。 **判定口径**: 掉话率 >2%。 **常见场景**: 移动场景、弱覆盖。 **排查路径**: 抓取log→检查协议栈→网络条件。 **对策**: 优化射频功率控制，改善切换策略。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0519',
    name: '充电慢',
    type: '其他',
    category: 'symptoms',
    aliases: ['慢充;Slow Charging'],
    tags: ['电池;硬件相关'],
    description: '**定义**: 充电速率低于设计值。 **判定口径**: 充电电流 < 额定值 70%。 **常见场景**: 使用非原装充电器。 **排查路径**: 检查充电IC→协议识别。 **对策**: 增加兼容性测试，优化协议栈。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0520',
    name: '充不进电',
    type: '其他',
    category: 'symptoms',
    aliases: ['无法充电;Not Charging'],
    tags: ['电池;硬件相关'],
    description: '**定义**: 手机接入电源无法充电。 **判定口径**: 电池电量无上升。 **常见场景**: 接口损坏、过放保护。 **排查路径**: 检查充电口→电池保护板。 **对策**: 增强接口防护，优化BMS策略。',
    created_at: '2025-09-26T09:43:14.267598',
    updated_at: '2025-09-26T09:43:14.267598'
});
CREATE (d:Dictionary {
    id: 'TERM_0521',
    name: '电池发热',
    type: '其他',
    category: 'symptoms',
    aliases: ['充电发烫;Battery Heating'],
    tags: ['电池;安全相关'],
    description: '**定义**: 电池温度异常升高。 **判定口径**: 电池温度 >50℃。 **常见场景**: 快充、边充边玩。 **排查路径**: 检查快充协议→电芯阻抗。 **对策**: 控制快充功率，提升散热。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0522',
    name: '耗电异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['功耗异常;Abnormal Power Drain'],
    tags: ['软件相关;电池'],
    description: '**定义**: 待机/使用时电量消耗过快。 **判定口径**: 待机功耗 >200mW。 **常见场景**: APP后台运行。 **排查路径**: 分析耗电曲线→定位进程。 **对策**: 优化系统调度，限制异常应用。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0523',
    name: '过充',
    type: '其他',
    category: 'symptoms',
    aliases: ['过度充电;Over Charging'],
    tags: ['电池;安全相关'],
    description: '**定义**: 电池电压超过安全上限。 **判定口径**: 电压 >4.35V。 **常见场景**: 充电保护失效。 **排查路径**: 检查BMS→充电IC。 **对策**: 增加保护电路，提升电芯一致性。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0524',
    name: '过放',
    type: '其他',
    category: 'symptoms',
    aliases: ['过度放电;Over Discharging'],
    tags: ['电池;安全相关'],
    description: '**定义**: 电池电压低于安全下限。 **判定口径**: 电压 <3.0V。 **常见场景**: 长时间未充电。 **排查路径**: 检查电池保护板。 **对策**: 增加欠压保护，改善电量计校准。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0525',
    name: '电池膨胀',
    type: '其他',
    category: 'symptoms',
    aliases: ['电芯膨胀;Cell Expansion'],
    tags: ['电池;可靠性'],
    description: '**定义**: 电芯鼓胀导致结构异常。 **判定口径**: 厚度增加 >10%。 **常见场景**: 高温、寿命末期。 **排查路径**: 检查气胀情况。 **对策**: 优化电芯材料，增加气体吸收层。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0526',
    name: '屏幕碎裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏幕破裂;Screen Crack'],
    tags: ['显示相关;结构相关'],
    description: '**定义**: 显示屏出现裂纹/碎裂。 **判定口径**: 裂纹可见。 **常见场景**: 跌落。 **排查路径**: 检查玻璃材质/结构。 **对策**: 使用康宁大猩猩玻璃，优化保护壳设计。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0527',
    name: '屏幕进灰',
    type: '其他',
    category: 'symptoms',
    aliases: ['显示进灰;Dust Inside Screen'],
    tags: ['显示相关;结构相关'],
    description: '**定义**: 屏幕层间进入异物。 **判定口径**: 黑屏下可见颗粒。 **常见场景**: 密封不良。 **排查路径**: 检查密封胶→结构间隙。 **对策**: 改善装配工艺，增加洁净度控制。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0528',
    name: '色偏',
    type: '其他',
    category: 'symptoms',
    aliases: ['显示偏色;Color Shift'],
    tags: ['显示相关;CMF'],
    description: '**定义**: 显示色彩与标准不符。 **判定口径**: ΔE >3。 **常见场景**: 屏幕老化。 **排查路径**: 检查色彩管理→面板一致性。 **对策**: 增加出厂校色，优化算法。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0529',
    name: '残影',
    type: '其他',
    category: 'symptoms',
    aliases: ['烧屏;Image Retention'],
    tags: ['显示相关;可靠性'],
    description: '**定义**: 静态画面残留。 **判定口径**: 静态图像切换后残留 >30s。 **常见场景**: OLED屏。 **排查路径**: 检查驱动算法→面板寿命。 **对策**: 优化像素刷新，增加均匀老化策略。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0530',
    name: '闪烁',
    type: '其他',
    category: 'symptoms',
    aliases: ['屏闪;Flicker'],
    tags: ['显示相关;影像相关'],
    description: '**定义**: 屏幕亮度快速变化。 **判定口径**: PWM频率 <240Hz。 **常见场景**: 低亮度使用。 **排查路径**: 检查驱动IC→调光方案。 **对策**: 提升PWM频率，采用DC调光。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0531',
    name: '模内取向效应',
    type: '其他',
    category: 'symptoms',
    aliases: ['分子取向'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '注塑过程中高分子链沿流动方向排列，导致产品力学性能和热膨胀系数各向异性。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0532',
    name: '信号地弹',
    type: '其他',
    category: 'symptoms',
    aliases: ['地噪声'],
    tags: ['硬件相关;电气性能;设计'],
    description: '多个数字输出同时切换时，因封装电感引起地电位波动，影响输入电平判断。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0533',
    name: '模流纤维取向',
    type: '其他',
    category: 'symptoms',
    aliases: ['纤维排向'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '增强纤维在注塑过程中沿流动方向取向，导致产品强度和热膨胀呈现方向性。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0534',
    name: '邦定cratering',
    type: '其他',
    category: 'symptoms',
    aliases: ['弹坑效应'],
    tags: ['可靠性;半导体;封装'],
    description: '键合过程中过大的超声波能量或压力导致芯片下方的硅材料产生裂纹或崩缺。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0535',
    name: '锡膏印刷偏移',
    type: '其他',
    category: 'symptoms',
    aliases: ['印刷对位偏差'],
    tags: ['制造工艺;SMT'],
    description: '锡膏印刷图形与PCB焊盘之间的位置偏差，需控制在允许范围内。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0536',
    name: '邦定Pad污染',
    type: '其他',
    category: 'symptoms',
    aliases: ['焊盘污染'],
    tags: ['可靠性;半导体;封装'],
    description: '芯片键合焊盘表面存在氧化物、有机物或离子污染，影响键合强度和可靠性。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0537',
    name: '腐蚀疲劳',
    type: '其他',
    category: 'symptoms',
    aliases: ['环境疲劳'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '材料在腐蚀性环境和交变应力共同作用下，疲劳寿命显著降低的现象。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0538',
    name: '模流残余应力',
    type: '其他',
    category: 'symptoms',
    aliases: ['内应力'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '注塑件内部因不均匀冷却和分子取向被冻结而形成的应力，是翘曲和开裂的根源。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0539',
    name: '蠕变',
    type: '其他',
    category: 'symptoms',
    aliases: ['徐变'],
    tags: ['可靠性;结构相关;物料'],
    description: '材料在恒定应力下，应变随时间缓慢增加的现象，影响长期尺寸稳定性。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0540',
    name: '锡膏热坍塌',
    type: '其他',
    category: 'symptoms',
    aliases: ['热塌陷'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '锡膏在回流焊预热阶段，因粘度下降过度而扩散到焊盘之外，可能导致桥连。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0541',
    name: '模流纤维断裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['纤维损伤'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '长纤维增强塑料在注塑过程中，纤维因强剪切力而断裂，降低增强效果。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0542',
    name: '胶体化学老化',
    type: '其他',
    category: 'symptoms',
    aliases: ['化学降解'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂因与环境中化学物质（如臭氧、UV）反应而性能劣化。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0543',
    name: '应力松弛',
    type: '其他',
    category: 'symptoms',
    aliases: ['应力弛豫'],
    tags: ['可靠性;结构相关;物料'],
    description: '材料在保持恒定应变的情况下，其内部应力随时间逐渐减小的现象。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0544',
    name: '模流热残渣',
    type: '其他',
    category: 'symptoms',
    aliases: ['材料降解'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '塑料在料筒或喷嘴中长时间受热，发生分解产生黑点或焦化物。',
    created_at: '2025-09-26T09:43:14.268598',
    updated_at: '2025-09-26T09:43:14.268598'
});
CREATE (d:Dictionary {
    id: 'TERM_0545',
    name: '胶体物理老化',
    type: '其他',
    category: 'symptoms',
    aliases: ['物理老化'],
    tags: ['物料;可靠性;点胶'],
    description: '非晶态聚合物在玻璃化转变温度以下，其体积和 enthalpy 向平衡状态缓慢松弛的过程，导致性能变化。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0546',
    name: '氢致开裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['氢脆'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '金属材料因吸收氢原子而在应力作用下发生脆性断裂的现象。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0547',
    name: '信号地弹',
    type: '其他',
    category: 'symptoms',
    aliases: ['地噪声'],
    tags: ['硬件相关;电气性能;设计'],
    description: '多个数字输出同时切换时，因封装电感引起地电位波动，影响输入电平判断。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0548',
    name: '模流纤维取向',
    type: '其他',
    category: 'symptoms',
    aliases: ['纤维排向'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '增强纤维在注塑过程中沿流动方向取向，导致产品强度和热膨胀呈现方向性。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0549',
    name: '邦定cratering',
    type: '其他',
    category: 'symptoms',
    aliases: ['弹坑效应'],
    tags: ['可靠性;半导体;封装'],
    description: '键合过程中过大的超声波能量或压力导致芯片下方的硅材料产生裂纹或崩缺。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0550',
    name: '锡膏印刷偏移',
    type: '其他',
    category: 'symptoms',
    aliases: ['印刷对位偏差'],
    tags: ['制造工艺;SMT'],
    description: '锡膏印刷图形与PCB焊盘之间的位置偏差，需控制在允许范围内。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0551',
    name: '邦定Pad污染',
    type: '其他',
    category: 'symptoms',
    aliases: ['焊盘污染'],
    tags: ['可靠性;半导体;封装'],
    description: '芯片键合焊盘表面存在氧化物、有机物或离子污染，影响键合强度和可靠性。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0552',
    name: '腐蚀疲劳',
    type: '其他',
    category: 'symptoms',
    aliases: ['环境疲劳'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '材料在腐蚀性环境和交变应力共同作用下，疲劳寿命显著降低的现象。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0553',
    name: '模流残余应力',
    type: '其他',
    category: 'symptoms',
    aliases: ['内应力'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '注塑件内部因不均匀冷却和分子取向被冻结而形成的应力，是翘曲和开裂的根源。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0554',
    name: '蠕变',
    type: '其他',
    category: 'symptoms',
    aliases: ['徐变'],
    tags: ['可靠性;结构相关;物料'],
    description: '材料在恒定应力下，应变随时间缓慢增加的现象，影响长期尺寸稳定性。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0555',
    name: '锡膏热坍塌',
    type: '其他',
    category: 'symptoms',
    aliases: ['热塌陷'],
    tags: ['SMT;制造工艺;可靠性'],
    description: '锡膏在回流焊预热阶段，因粘度下降过度而扩散到焊盘之外，可能导致桥连。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0556',
    name: '模流纤维断裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['纤维损伤'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '长纤维增强塑料在注塑过程中，纤维因强剪切力而断裂，降低增强效果。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0557',
    name: '胶体化学老化',
    type: '其他',
    category: 'symptoms',
    aliases: ['化学降解'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂因与环境中化学物质（如臭氧、UV）反应而性能劣化。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0558',
    name: '应力松弛',
    type: '其他',
    category: 'symptoms',
    aliases: ['应力弛豫'],
    tags: ['可靠性;结构相关;物料'],
    description: '材料在保持恒定应变的情况下，其内部应力随时间逐渐减小的现象。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0559',
    name: '模流热残渣',
    type: '其他',
    category: 'symptoms',
    aliases: ['材料降解'],
    tags: ['制造工艺;注塑;可靠性'],
    description: '塑料在料筒或喷嘴中长时间受热，发生分解产生黑点或焦化物。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0560',
    name: '胶体物理老化',
    type: '其他',
    category: 'symptoms',
    aliases: ['物理老化'],
    tags: ['物料;可靠性;点胶'],
    description: '非晶态聚合物在玻璃化转变温度以下，其体积和enthalpy向平衡状态缓慢松弛的过程，导致性能变化。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0561',
    name: '氢致开裂',
    type: '其他',
    category: 'symptoms',
    aliases: ['氢脆'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '金属材料因吸收氢原子而在应力作用下发生脆性断裂的现象。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0562',
    name: '视频不同步',
    type: '其他',
    category: 'symptoms',
    aliases: ['声画不同步;AV Sync Issue'],
    tags: ['软件相关;影像相关'],
    description: '**定义**: 视频播放时声音和画面不同步。 **判定口径**: 延迟 >200ms。 **常见场景**: 在线播放、通话。 **排查路径**: 检查解码→缓冲机制。 **对策**: 优化同步算法，减少延迟。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0563',
    name: '录像掉帧',
    type: '其他',
    category: 'symptoms',
    aliases: ['视频丢帧;Video Frame Drop'],
    tags: ['影像相关;性能指标'],
    description: '**定义**: 录像过程中丢失帧。 **判定口径**: 丢帧率 >5%。 **常见场景**: 高分辨率录像。 **排查路径**: 检查存储写入速度→ISP负载。 **对策**: 提升存储性能，优化编码。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0564',
    name: '自拍过曝',
    type: '其他',
    category: 'symptoms',
    aliases: ['前摄过曝;Selfie Overexposure'],
    tags: ['影像相关;摄像头模组'],
    description: '**定义**: 前置摄像头拍照曝光过度。 **判定口径**: 过曝面积 >20%。 **常见场景**: 强光自拍。 **排查路径**: 检查AE算法→镜头参数。 **对策**: 优化HDR，增加曝光补偿。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0565',
    name: '夜拍拖影',
    type: '其他',
    category: 'symptoms',
    aliases: ['暗光拖影;Night Smear'],
    tags: ['影像相关;摄像头模组'],
    description: '**定义**: 暗光下拍照出现拖影。 **判定口径**: 拖影长度 >3px。 **常见场景**: 夜景拍照。 **排查路径**: 检查快门速度→OIS。 **对策**: 优化夜景算法，提升防抖性能。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0566',
    name: '电池续航不足',
    type: '其他',
    category: 'symptoms',
    aliases: ['续航差;Poor Battery Life'],
    tags: ['硬件相关;电池'],
    description: '**定义**: 电池使用时间明显不足。 **判定口径**: 实测续航低于标称 20%。 **常见场景**: 高功耗应用。 **排查路径**: 检查电池健康度→功耗分析。 **对策**: 优化系统功耗，改进电池容量。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0567',
    name: '电池过热',
    type: '其他',
    category: 'symptoms',
    aliases: ['电池温度过高;Battery Overheat'],
    tags: ['硬件相关;安全相关'],
    description: '**定义**: 电池在充电或使用时过热。 **判定口径**: 电池温度 >45℃。 **常见场景**: 快充、高负载。 **排查路径**: 检查充电IC→散热设计。 **对策**: 增加温控保护，改善散热。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0568',
    name: '无法充电',
    type: '其他',
    category: 'symptoms',
    aliases: ['充电失败;Charging Fail'],
    tags: ['硬件相关;充电'],
    description: '**定义**: 手机无法进入充电状态。 **判定口径**: 插入充电器无反应。 **常见场景**: 接口损坏。 **排查路径**: 检查尾插→充电IC。 **对策**: 提升接口强度，增加防尘设计。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0569',
    name: '无线充不稳',
    type: '其他',
    category: 'symptoms',
    aliases: ['无线充电中断;Wireless Charging Unstable'],
    tags: ['硬件相关;充电'],
    description: '**定义**: 无线充电过程中频繁中断。 **判定口径**: 中断率 >5%。 **常见场景**: 位置偏移。 **排查路径**: 检查线圈对准→EMC干扰。 **对策**: 优化线圈设计，改善异物检测。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0570',
    name: '快充不生效',
    type: '其他',
    category: 'symptoms',
    aliases: ['快充失败;Fast Charging Fail'],
    tags: ['硬件相关;充电'],
    description: '**定义**: 手机无法进入快充模式。 **判定口径**: 实测功率 <10W。 **常见场景**: 非匹配适配器。 **排查路径**: 检查协议→电路设计。 **对策**: 增强快充兼容性。',
    created_at: '2025-09-26T09:43:14.269596',
    updated_at: '2025-09-26T09:43:14.269596'
});
CREATE (d:Dictionary {
    id: 'TERM_0571',
    name: '待机掉电快',
    type: '其他',
    category: 'symptoms',
    aliases: ['待机耗电大;High Standby Power'],
    tags: ['软件相关;电池'],
    description: '**定义**: 手机在待机时掉电快。 **判定口径**: 待机功耗 >1%/h。 **常见场景**: 应用后台异常。 **排查路径**: 检查系统进程→基带状态。 **对策**: 优化后台管控，降低常驻功耗。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0572',
    name: '电池鼓包',
    type: '其他',
    category: 'symptoms',
    aliases: ['电池膨胀;Battery Swelling'],
    tags: ['硬件相关;安全相关'],
    description: '**定义**: 电池外形鼓起。 **判定口径**: 厚度增加 >10%。 **常见场景**: 长期充电/老化。 **排查路径**: 检查循环次数→气体析出。 **对策**: 严格寿命管控，优化材料。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0573',
    name: '电量显示异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['电量不准;Inaccurate Battery Indicator'],
    tags: ['软件相关;电池'],
    description: '**定义**: 电量显示与实际不符。 **判定口径**: 偏差 >10%。 **常见场景**: 电量跳变。 **排查路径**: 检查计量芯片→软件校准。 **对策**: 增加自学习算法，优化校准机制。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0574',
    name: '自动关机',
    type: '其他',
    category: 'symptoms',
    aliases: ['无故关机;Unexpected Shutdown'],
    tags: ['硬件相关;电池'],
    description: '**定义**: 手机电量充足时自动关机。 **判定口径**: 电量 >20% 突然关机。 **常见场景**: 电池老化/低温。 **排查路径**: 检查电池内阻→PMIC。 **对策**: 增加低温补偿，优化电源管理。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0575',
    name: '自动重启',
    type: '其他',
    category: 'symptoms',
    aliases: ['意外重启;Auto Reboot'],
    tags: ['软件相关;系统稳定性'],
    description: '**定义**: 手机非人为操作重启。 **判定口径**: 重启频率 >1 次/天。 **常见场景**: 系统升级、APP异常。 **排查路径**: 分析log→排查内存/电源。 **对策**: 优化系统稳定性，修复Bug。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0576',
    name: '应用闪退',
    type: '其他',
    category: 'symptoms',
    aliases: ['APP崩溃;App Crash'],
    tags: ['软件相关;用户体验'],
    description: '**定义**: 应用运行中意外关闭。 **判定口径**: 崩溃率 >1%。 **常见场景**: 高内存占用。 **排查路径**: 查看log→内存泄漏。 **对策**: 优化APP，完善异常捕获。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0577',
    name: '系统升级失败',
    type: '其他',
    category: 'symptoms',
    aliases: ['OTA失败;OTA Fail'],
    tags: ['软件相关;系统升级'],
    description: '**定义**: OTA升级无法完成。 **判定口径**: 升级失败率 >1%。 **常见场景**: 网络中断、存储不足。 **排查路径**: 检查下载包→存储空间。 **对策**: 增强断点续传，提示存储清理。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0578',
    name: '恶意重启',
    type: '其他',
    category: 'symptoms',
    aliases: ['Bootloop;Reboot Loop'],
    tags: ['软件相关;系统启动'],
    description: '**定义**: 系统不断重启。 **判定口径**: 启动失败 >3 次。 **常见场景**: 系统损坏、刷机失败。 **排查路径**: 检查启动镜像→硬件异常。 **对策**: 增加恢复模式，优化刷机校验。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0579',
    name: '网络不稳定',
    type: '其他',
    category: 'symptoms',
    aliases: ['信号掉线;Network Unstable'],
    tags: ['通信相关;可靠性'],
    description: '**定义**: 移动网络频繁中断。 **判定口径**: 掉线率 >3%。 **常见场景**: 弱信号。 **排查路径**: 检查基带→天线设计。 **对策**: 优化射频匹配，改进算法。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0580',
    name: '无法通话',
    type: '其他',
    category: 'symptoms',
    aliases: ['语音通话失败;Call Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: 无法接通语音通话。 **判定口径**: 呼叫失败率 >1%。 **常见场景**: 弱信号、运营商限制。 **排查路径**: 检查基带→网络配置。 **对策**: 增强兼容性，优化协议。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0581',
    name: '视频通话卡顿',
    type: '其他',
    category: 'symptoms',
    aliases: ['视频聊天卡顿;Video Call Lag'],
    tags: ['通信相关;用户体验'],
    description: '**定义**: 视频通话过程中画面卡顿。 **判定口径**: FPS <20。 **常见场景**: 网络弱。 **排查路径**: 检查带宽→视频编解码。 **对策**: 优化编解码，支持自适应码率。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0582',
    name: '漫游失败',
    type: '其他',
    category: 'symptoms',
    aliases: ['网络漫游失败;Roaming Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: 手机无法漫游。 **判定口径**: 漫游成功率 <95%。 **常见场景**: 出国、异网。 **排查路径**: 检查SIM配置→运营商策略。 **对策**: 增强兼容性，更新漫游表。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0583',
    name: 'SIM不识别',
    type: '其他',
    category: 'symptoms',
    aliases: ['SIM卡无效;SIM Not Detected'],
    tags: ['硬件相关;通信相关'],
    description: '**定义**: 插入SIM卡无效。 **判定口径**: 检测失败率 >1%。 **常见场景**: 卡托松动、触点脏污。 **排查路径**: 检查SIM座→检测电路。 **对策**: 提升卡座强度，优化接触可靠性。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0584',
    name: '数据漫游异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['数据漫游失败;Data Roaming Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: 数据漫游无法使用。 **判定口径**: 成功率 <95%。 **常见场景**: 国外网络。 **排查路径**: 检查基带配置→运营商兼容性。 **对策**: 增强测试覆盖，优化协议实现。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0585',
    name: '短信收发失败',
    type: '其他',
    category: 'symptoms',
    aliases: ['SMS失败;SMS Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: 短信发送或接收失败。 **判定口径**: 失败率 >1%。 **常见场景**: 弱信号、漫游。 **排查路径**: 检查基带→中心号码。 **对策**: 增强网络兼容性，提示用户检查配置。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0586',
    name: '彩信失败',
    type: '其他',
    category: 'symptoms',
    aliases: ['MMS失败;MMS Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: 彩信发送/接收失败。 **判定口径**: 成功率 <95%。 **常见场景**: 网络不稳定。 **排查路径**: 检查APN配置→运营商支持。 **对策**: 优化配置兼容性。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0587',
    name: 'VoLTE异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['VoLTE不通;VoLTE Fail'],
    tags: ['通信相关;功能'],
    description: '**定义**: VoLTE功能不可用。 **判定口径**: 呼叫成功率 <95%。 **常见场景**: 网络制式切换。 **排查路径**: 检查配置→基带协议。 **对策**: 优化协议栈，增强兼容性。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0588',
    name: '语音识别不准',
    type: '其他',
    category: 'symptoms',
    aliases: ['语音识别错误;ASR Inaccuracy'],
    tags: ['软件相关;人机交互'],
    description: '**定义**: 语音识别准确率低。 **判定口径**: 准确率 <90%。 **常见场景**: 方言、噪音环境。 **排查路径**: 检查算法→语料。 **对策**: 优化模型，增加噪声鲁棒性。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0589',
    name: '语音助手误触发',
    type: '其他',
    category: 'symptoms',
    aliases: ['语音助手误唤醒;Voice Assistant False Trigger'],
    tags: ['软件相关;人机交互'],
    description: '**定义**: 无操作时语音助手被误触发。 **判定口径**: 误触发率 >1%。 **常见场景**: 环境噪声。 **排查路径**: 检查麦克风阵列→关键词算法。 **对策**: 优化关键词模型，增加二次确认。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0590',
    name: '传感器漂移',
    type: '其他',
    category: 'symptoms',
    aliases: ['传感器不准;Sensor Drift'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 传感器数值随时间偏移。 **判定口径**: 偏差 >10%。 **常见场景**: 长时间运行。 **排查路径**: 检查校准机制→温度补偿。 **对策**: 增强校准，优化补偿算法。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0591',
    name: '距离感应失效',
    type: '其他',
    category: 'symptoms',
    aliases: ['距离传感器异常;Proximity Fail'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 通话时距离感应无效。 **判定口径**: 误判率 >5%。 **常见场景**: 贴膜遮挡。 **排查路径**: 检查传感器窗口→算法。 **对策**: 增加窗口透光率，优化算法。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0592',
    name: '陀螺仪异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['Gyro Fail'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 陀螺仪无法正常工作。 **判定口径**: 偏差 >5°。 **常见场景**: 游戏、导航。 **排查路径**: 检查模组→校准。 **对策**: 优化算法，提升防震设计。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0593',
    name: '加速度异常',
    type: '其他',
    category: 'symptoms',
    aliases: ['加速度计失效;Accelerometer Fail'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 加速度计无法正确测量。 **判定口径**: 偏差 >10%。 **常见场景**: 翻转屏幕、计步。 **排查路径**: 检查焊点→校准。 **对策**: 增加自校准，提升可靠性。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0594',
    name: '磁力计不准',
    type: '其他',
    category: 'symptoms',
    aliases: ['电子罗盘异常;Magnetometer Fail'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 磁力计方向偏差大。 **判定口径**: 偏差 >15°。 **常见场景**: 地铁、金属环境。 **排查路径**: 检查磁屏蔽→算法。 **对策**: 优化补偿算法。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0595',
    name: '气压计失效',
    type: '其他',
    category: 'symptoms',
    aliases: ['气压传感器异常;Barometer Fail'],
    tags: ['硬件相关;传感器'],
    description: '**定义**: 气压值不正确。 **判定口径**: 偏差 >5hPa。 **常见场景**: 高度测量。 **排查路径**: 检查传感器→校准。 **对策**: 增加温度补偿，优化算法。',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0596',
    name: '水痕',
    type: '症状',
    category: 'symptoms',
    aliases: ['水渍'],
    tags: ['外观;制造工艺'],
    description: '产品表面因接触水后干燥不均留下的痕迹',
    created_at: '2025-09-26T09:43:14.270594',
    updated_at: '2025-09-26T09:43:14.270594'
});
CREATE (d:Dictionary {
    id: 'TERM_0597',
    name: '点蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['孔蚀'],
    tags: ['可靠性;硬件相关;CMF'],
    description: '金属表面局部发生的剧烈腐蚀形成小而深的孔洞',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0598',
    name: '微动磨损',
    type: '症状',
    category: 'symptoms',
    aliases: ['微振磨损'],
    tags: ['可靠性;硬件相关;结构相关'],
    description: '接触面间小幅度的相对运动导致的磨损常见于连接器',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0599',
    name: '晶间腐蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['晶界腐蚀'],
    tags: ['可靠性;硬件相关;CMF'],
    description: '腐蚀沿金属晶粒边界进行导致材料力学性能严重下降',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0600',
    name: '电偶腐蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['伽凡尼腐蚀'],
    tags: ['可靠性;硬件相关;CMF'],
    description: '两种不同电位的金属在电解质中接触时电位负的金属加速腐蚀',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0601',
    name: '应力腐蚀开裂',
    type: '症状',
    category: 'symptoms',
    aliases: ['SCC'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '材料在拉应力和特定腐蚀介质共同作用下发生的脆性开裂',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0602',
    name: '缝隙腐蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['crevice corrosion'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '在金属与金属或非金属间狭窄缝隙内因环境差异引发的局部腐蚀',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0603',
    name: '疲劳断裂',
    type: '症状',
    category: 'symptoms',
    aliases: ['疲劳失效'],
    tags: ['可靠性;结构相关;硬件相关'],
    description: '材料在交变应力作用下经历一定循环次数后发生的断裂',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0604',
    name: '磨损颗粒',
    type: '症状',
    category: 'symptoms',
    aliases: ['磨屑'],
    tags: ['可靠性;硬件相关;结构相关'],
    description: '因摩擦产生的微小材料颗粒可能造成污染或卡死',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0605',
    name: '电化学腐蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['电解腐蚀'],
    tags: ['可靠性;硬件相关;CMF'],
    description: '在电解质溶液中因电位差形成的原电池效应导致的腐蚀',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0606',
    name: 'Mura缺陷',
    type: '症状',
    category: 'symptoms',
    aliases: ['云斑;显示不均'],
    tags: ['显示相关;异常现象'],
    description: '屏幕亮度或色度不均匀呈现云状或斑块状的缺陷',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0607',
    name: '亮线暗线',
    type: '症状',
    category: 'symptoms',
    aliases: ['Line Defect'],
    tags: ['显示相关;异常现象'],
    description: '屏幕上出现的垂直或水平亮线暗线通常与驱动线路或屏幕损伤有关',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0608',
    name: '亮点暗点',
    type: '症状',
    category: 'symptoms',
    aliases: ['坏点'],
    tags: ['显示相关;异常现象'],
    description: '像素点常亮或不亮属于显示缺陷',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0609',
    name: '偏芯',
    type: '症状',
    category: 'symptoms',
    aliases: ['Lens Tilt;Decentering'],
    tags: ['影像相关;异常现象'],
    description: '镜头光学中心与传感器中心不重合导致成像锐度下降暗角',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0610',
    name: '杂质',
    type: '症状',
    category: 'symptoms',
    aliases: ['Particle Contamination'],
    tags: ['影像相关;异常现象;制造工艺'],
    description: '模组内部有灰尘纤维等异物成像上有黑点',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0611',
    name: '鬼影',
    type: '症状',
    category: 'symptoms',
    aliases: ['Ghosting'],
    tags: ['影像相关;异常现象'],
    description: '强光下图像中出现光源的反射重影与镜头镀膜和结构有关',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0612',
    name: '对焦迟缓',
    type: '症状',
    category: 'symptoms',
    aliases: ['Slow Auto-Focus'],
    tags: ['影像相关;异常现象;性能指标'],
    description: '相机对焦速度慢的问题',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0613',
    name: '解析力不足',
    type: '症状',
    category: 'symptoms',
    aliases: ['Poor Resolution'],
    tags: ['影像相关;异常现象;性能指标'],
    description: '拍摄的照片细节不清边缘模糊',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0614',
    name: '循环寿命短',
    type: '症状',
    category: 'symptoms',
    aliases: ['Short Cycle Life'],
    tags: ['硬件相关;可靠性;异常现象'],
    description: '电池容量随充放电循环次数增加而过快衰减',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0615',
    name: '内阻增大',
    type: '症状',
    category: 'symptoms',
    aliases: ['Increased Internal Resistance'],
    tags: ['硬件相关;性能指标;异常现象'],
    description: '导致电池输出电压下降充电发热严重的现象',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0616',
    name: '开路',
    type: '症状',
    category: 'symptoms',
    aliases: ['Open Circuit'],
    tags: ['硬件相关;电气性能;异常现象'],
    description: '电路断开电流无法通过的故障',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0617',
    name: '元器件立碑',
    type: '症状',
    category: 'symptoms',
    aliases: ['Tombstoning'],
    tags: ['SMT;制造工艺;异常现象'],
    description: '片式元件一端翘起脱离焊盘的贴装缺陷',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0618',
    name: '数据吞吐量低',
    type: '症状',
    category: 'symptoms',
    aliases: ['Low Data Throughput'],
    tags: ['射频相关;异常现象;通信相关'],
    description: '上网速度远低于理论值或预期值',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0619',
    name: '搜网慢',
    type: '症状',
    category: 'symptoms',
    aliases: ['Slow Network Search'],
    tags: ['射频相关;异常现象;通信相关'],
    description: '手机开机或进入新区域后寻找和注册到网络的时间过长',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0620',
    name: 'SAR值超标',
    type: '症状',
    category: 'symptoms',
    aliases: ['SAR Exceedance'],
    tags: ['射频相关;异常现象;安全相关;法规'],
    description: '比吸收率超过法规限值对人体电磁辐射吸收过高',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0621',
    name: '频率误差',
    type: '症状',
    category: 'symptoms',
    aliases: ['Frequency Error'],
    tags: ['射频相关;异常现象;通信相关'],
    description: '发射信号的载波频率偏离标准值',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0622',
    name: '调制频谱超标',
    type: '症状',
    category: 'symptoms',
    aliases: ['Modulation Spectrum Fail'],
    tags: ['射频相关;异常现象;通信相关;EMC'],
    description: '发射信号的调制频谱超出规范模板',
    created_at: '2025-09-26T09:43:14.271594',
    updated_at: '2025-09-26T09:43:14.271594'
});
CREATE (d:Dictionary {
    id: 'TERM_0623',
    name: '切换失败',
    type: '症状',
    category: 'symptoms',
    aliases: ['Handover Failure'],
    tags: ['射频相关;异常现象;通信相关'],
    description: '手机在不同基站或不同制式之间切换时失败',
    created_at: '2025-09-26T09:43:14.272592',
    updated_at: '2025-09-26T09:43:14.272592'
});
CREATE (d:Dictionary {
    id: 'TERM_0624',
    name: '破音',
    type: '症状',
    category: 'symptoms',
    aliases: ['Distortion;Clipping'],
    tags: ['声学;异常现象'],
    description: '扬声器在大功率下因振幅过大或达到物理极限产生的失真声音',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0625',
    name: '杂音',
    type: '症状',
    category: 'symptoms',
    aliases: ['Noise;Hiss'],
    tags: ['声学;异常现象'],
    description: '音频信号中夹杂的非预期白噪声或本底噪声',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0626',
    name: '声音小',
    type: '症状',
    category: 'symptoms',
    aliases: ['Low Sound Pressure Level'],
    tags: ['声学;异常现象;性能指标'],
    description: '输出音量达不到设计规格',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0627',
    name: '频响曲线凹陷',
    type: '症状',
    category: 'symptoms',
    aliases: ['Frequency Response Dip'],
    tags: ['声学;异常现象;性能指标'],
    description: '频率响应曲线在特定频段出现不正常的谷值导致声音发闷或单薄',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0628',
    name: '相位抵消',
    type: '症状',
    category: 'symptoms',
    aliases: ['Phase Cancellation'],
    tags: ['声学;异常现象;性能指标'],
    description: '多个声源如双扬声器发出的声波因相位相反而相互削弱导致声音减弱或怪异',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0629',
    name: '回声',
    type: '症状',
    category: 'symptoms',
    aliases: ['Echo'],
    tags: ['声学;异常现象;软件相关'],
    description: '通话时对方能听到自己说话的回声',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0630',
    name: '断差',
    type: '症状',
    category: 'symptoms',
    aliases: ['Step'],
    tags: ['结构相关;异常现象;外观'],
    description: '相邻部件如屏幕与中框之间存在不应有的高度差',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0631',
    name: '缝隙',
    type: '症状',
    category: 'symptoms',
    aliases: ['Gap'],
    tags: ['结构相关;异常现象;外观'],
    description: '部件之间的间隙不均匀或超出设计范围',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0632',
    name: '松动',
    type: '症状',
    category: 'symptoms',
    aliases: ['Loose;Rattle'],
    tags: ['结构相关;异常现象;可靠性'],
    description: '部件装配不牢固受力或晃动时产生异响或位移',
    created_at: '2025-09-26T09:43:14.272699',
    updated_at: '2025-09-26T09:43:14.272699'
});
CREATE (d:Dictionary {
    id: 'TERM_0633',
    name: '卡扣断裂',
    type: '症状',
    category: 'symptoms',
    aliases: ['Snap-fit Breakage'],
    tags: ['结构相关;异常现象;可靠性'],
    description: '塑料卡扣在装配或使用中断裂导致部件松动',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0634',
    name: '热点',
    type: '症状',
    category: 'symptoms',
    aliases: ['Hot Spot'],
    tags: ['热管理;异常现象;可靠性'],
    description: '手机表面或内部特定区域温度异常偏高',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0635',
    name: '表面温度超标',
    type: '症状',
    category: 'symptoms',
    aliases: ['Surface Temperature Exceedance'],
    tags: ['热管理;异常现象;可靠性;用户体验'],
    description: '手机外壳温度超过安全法规或人体舒适度限值',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0636',
    name: '性能降频',
    type: '症状',
    category: 'symptoms',
    aliases: ['Thermal Throttling'],
    tags: ['热管理;异常现象;软件相关;性能指标'],
    description: '因温度过高系统主动降低芯片频率以控制发热导致卡顿',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0637',
    name: '数据漂移',
    type: '症状',
    category: 'symptoms',
    aliases: ['Data Drift'],
    tags: ['传感器;异常现象;可靠性'],
    description: '传感器输出数据随时间发生缓慢偏移偏离真实值',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0638',
    name: '响应延迟',
    type: '症状',
    category: 'symptoms',
    aliases: ['Response Lag'],
    tags: ['传感器;异常现象;性能指标'],
    description: '传感器检测到物理量变化到输出数据之间存在明显延迟',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0639',
    name: '精度不足',
    type: '症状',
    category: 'symptoms',
    aliases: ['Poor Accuracy'],
    tags: ['传感器;异常现象;性能指标'],
    description: '传感器测量值与真实值之间存在较大系统误差',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0640',
    name: '零点偏移',
    type: '症状',
    category: 'symptoms',
    aliases: ['Zero Offset'],
    tags: ['传感器;异常现象;性能指标'],
    description: '在输入为零时传感器输出不为零',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0641',
    name: '充电发热严重',
    type: '症状',
    category: 'symptoms',
    aliases: ['Excessive Heating During Charging'],
    tags: ['充电;异常现象;热管理;安全相关'],
    description: '充电时手机或充电器温度异常升高',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0642',
    name: '充电速度慢',
    type: '症状',
    category: 'symptoms',
    aliases: ['Slow Charging'],
    tags: ['充电;异常现象;性能指标'],
    description: '实际充电功率远低于标称快充功率',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0643',
    name: '无法快充',
    type: '症状',
    category: 'symptoms',
    aliases: ['Fast Charging Not Working'],
    tags: ['充电;异常现象;功能'],
    description: '手机连接支持快充的充电器后仍以标准5V电压充电',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0644',
    name: '充电中断',
    type: '症状',
    category: 'symptoms',
    aliases: ['Charging Interruption'],
    tags: ['充电;异常现象;可靠性'],
    description: '充电过程中断断续续无法连续充满',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0645',
    name: '无线充电效率低',
    type: '症状',
    category: 'symptoms',
    aliases: ['Low Wireless Charging Efficiency'],
    tags: ['充电;异常现象;性能指标'],
    description: '无线充电时能量损耗大手机发热严重且充电慢',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0646',
    name: '振动微弱',
    type: '症状',
    category: 'symptoms',
    aliases: ['Weak Vibration'],
    tags: ['硬件相关;异常现象;人机交互'],
    description: '振动强度不足用户体验差',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0647',
    name: '振动异响',
    type: '症状',
    category: 'symptoms',
    aliases: ['Abnormal Sound During Vibration'],
    tags: ['硬件相关;异常现象;声学'],
    description: '振动时伴随非预期的吱吱或哒哒声',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0648',
    name: '响应延迟',
    type: '症状',
    category: 'symptoms',
    aliases: ['Response Delay'],
    tags: ['硬件相关;异常现象;性能指标'],
    description: '触控操作与振动反馈之间存在可感知的延迟',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0649',
    name: '余振',
    type: '症状',
    category: 'symptoms',
    aliases: ['After-Shock'],
    tags: ['硬件相关;异常现象;性能指标'],
    description: '驱动信号停止后马达因惯性继续振动',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0650',
    name: '橘皮纹',
    type: '症状',
    category: 'symptoms',
    aliases: ['Orange Peel'],
    tags: ['CMF;异常现象;外观'],
    description: '涂层表面出现类似橘皮的不平整纹理',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0651',
    name: '颗粒感',
    type: '症状',
    category: 'symptoms',
    aliases: ['Graininess'],
    tags: ['CMF;异常现象;外观'],
    description: '涂层表面有可见的微小颗粒',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0652',
    name: '缩水',
    type: '症状',
    category: 'symptoms',
    aliases: ['Sink Mark'],
    tags: ['制造工艺;异常现象;外观'],
    description: '塑胶件在肉厚较大区域因冷却收缩不均导致表面凹陷',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0653',
    name: '熔接痕',
    type: '症状',
    category: 'symptoms',
    aliases: ['Weld Line'],
    tags: ['制造工艺;异常现象;外观;结构相关'],
    description: '两股熔融塑料流前沿相遇时因融合不良形成的线痕强度和外观均有影响',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0654',
    name: '刮花',
    type: '症状',
    category: 'symptoms',
    aliases: ['Scratch'],
    tags: ['外观;异常现象;可靠性'],
    description: '表面因摩擦留下的线性痕迹',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0655',
    name: '信号衰减',
    type: '症状',
    category: 'symptoms',
    aliases: ['Signal Attenuation'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '无线信号在传输过程中强度减弱',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0656',
    name: '数据丢包',
    type: '症状',
    category: 'symptoms',
    aliases: ['Packet Loss'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '网络传输过程中数据包丢失导致语音卡顿或视频缓冲',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0657',
    name: 'ping值高',
    type: '症状',
    category: 'symptoms',
    aliases: ['High Latency'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '网络延迟高影响实时应用如游戏视频通话体验',
    created_at: '2025-09-26T09:43:14.273206',
    updated_at: '2025-09-26T09:43:14.273206'
});
CREATE (d:Dictionary {
    id: 'TERM_0658',
    name: '网络切换失败',
    type: '症状',
    category: 'symptoms',
    aliases: ['Handover Failure'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '在不同基站或不同网络制式如5G/4G间切换时失败',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0659',
    name: 'Wi-Fi断流',
    type: '症状',
    category: 'symptoms',
    aliases: ['Wi-Fi Disconnection'],
    tags: ['通信相关;异常现象;性能指标'],
    description: 'Wi-Fi连接看似正常但数据流量间歇性中断',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0660',
    name: '蓝牙配对不稳定',
    type: '症状',
    category: 'symptoms',
    aliases: ['Bluetooth Pairing Instability'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '蓝牙设备频繁断开连接或需要重新配对',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0661',
    name: 'GPS定位漂移',
    type: '症状',
    category: 'symptoms',
    aliases: ['GPS Drift'],
    tags: ['通信相关;异常现象;性能指标'],
    description: '静止时GPS定位点在一定范围内无规律移动',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0662',
    name: '接口腐蚀',
    type: '症状',
    category: 'symptoms',
    aliases: ['Interface Corrosion'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '接口金属触点因汗液潮湿等环境因素发生氧化或电化学腐蚀',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0663',
    name: '引脚弯曲/断裂',
    type: '症状',
    category: 'symptoms',
    aliases: ['Pin Bent/Broken'],
    tags: ['硬件相关;异常现象;制造工艺'],
    description: '连接器引脚在组装或使用中发生物理损伤',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0664',
    name: '连接器缩PIN',
    type: '症状',
    category: 'symptoms',
    aliases: ['Contact Retraction'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '连接器内部的接触端子回缩导致接触不良',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0665',
    name: '接口松动',
    type: '症状',
    category: 'symptoms',
    aliases: ['Loose Connection'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '接口公母端配合不紧轻微外力即可导致断开',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0666',
    name: '电容容值衰减',
    type: '症状',
    category: 'symptoms',
    aliases: ['Capacitance Derating'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '电容特别是MLCC在直流偏压或高温下实际容值减小',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0667',
    name: '电容失效短路',
    type: '症状',
    category: 'symptoms',
    aliases: ['Capacitor Short Failure'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '电容介质击穿导致两极短路可能引发大电流烧毁',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0668',
    name: '电容失效开路',
    type: '症状',
    category: 'symptoms',
    aliases: ['Capacitor Open Failure'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '电容内部连接断开失去功能',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0669',
    name: '电感饱和',
    type: '症状',
    category: 'symptoms',
    aliases: ['Inductor Saturation'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '电流过大导致电感磁芯磁化饱和电感量急剧下降',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0670',
    name: '元件立碑',
    type: '症状',
    category: 'symptoms',
    aliases: ['Tombstoning'],
    tags: ['硬件相关;异常现象;SMT'],
    description: '片式元件一端翘起另一端焊接在焊盘上',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0671',
    name: '元件裂纹',
    type: '症状',
    category: 'symptoms',
    aliases: ['Component Cracking'],
    tags: ['硬件相关;异常现象;可靠性'],
    description: '特别是MLCC因板弯或热应力导致内部介质产生裂纹',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0672',
    name: '失效模式',
    type: '症状',
    category: 'symptoms',
    aliases: ['故障模式'],
    tags: ['可靠性;质量体系;异常现象'],
    description: '产品失效的具体表现形式如开路短路参数漂移等',
    created_at: '2025-09-26T09:43:14.274217',
    updated_at: '2025-09-26T09:43:14.274217'
});
CREATE (d:Dictionary {
    id: 'TERM_0673',
    name: '失效机理',
    type: '症状',
    category: 'symptoms',
    aliases: ['故障机理'],
    tags: ['可靠性;质量体系;异常现象'],
    description: '导致产品失效的物理化学或其它过程',
    created_at: '2025-09-26T09:43:14.275215',
    updated_at: '2025-09-26T09:43:14.275215'
});
CREATE (d:Dictionary {
    id: 'TERM_0674',
    name: 'AQL',
    type: '其他',
    category: 'countermeasures',
    aliases: ['接收质量限;Acceptable Quality Level'],
    tags: ['测试验证;质量体系'],
    description: '抽样检验的标准，用于来料或出货检验时判定批合格与否。',
    created_at: '2025-09-26T09:43:14.275215',
    updated_at: '2025-09-26T09:43:14.275215'
});
CREATE (d:Dictionary {
    id: 'TERM_0675',
    name: 'CABC',
    type: '其他',
    category: 'countermeasures',
    aliases: ['内容自适应背光控制;Content Adaptive Backlight Control'],
    tags: ['影像相关;功耗优化'],
    description: '根据显示内容自动调节背光以节省功耗，算法不良会导致屏幕闪烁或亮度异常。',
    created_at: '2025-09-26T09:43:14.275215',
    updated_at: '2025-09-26T09:43:14.275215'
});
CREATE (d:Dictionary {
    id: 'TERM_0676',
    name: 'CCD视觉对位',
    type: '其他',
    category: 'countermeasures',
    aliases: ['相机对位;CCD Alignment'],
    tags: ['摄像头模组;SMT'],
    description: '在贴片或模组组装中，使用工业相机进行高精度位置校准的工艺。',
    created_at: '2025-09-26T09:43:14.275215',
    updated_at: '2025-09-26T09:43:14.275215'
});
CREATE (d:Dictionary {
    id: 'TERM_0677',
    name: 'Corner Drop',
    type: '其他',
    category: 'countermeasures',
    aliases: ['角跌落'],
    tags: ['可靠性;结构相关'],
    description: '手机特定角落着地的跌落测试，用于评估结构最脆弱点的强度。',
    created_at: '2025-09-26T09:43:14.275215',
    updated_at: '2025-09-26T09:43:14.275215'
});
CREATE (d:Dictionary {
    id: 'TERM_0678',
    name: 'CPK',
    type: '其他',
    category: 'countermeasures',
    aliases: ['过程能力指数;Process Capability Index'],
    tags: ['制造工艺;质量体系'],
    description: '衡量生产过程稳定满足规格要求的能力，大于1.33表示过程能力良好。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0679',
    name: 'DQA',
    type: '其他',
    category: 'countermeasures',
    aliases: ['设计质量保证;Design Quality Assurance'],
    tags: ['流程相关;项目相关'],
    description: '在研发阶段介入，确保产品设计满足可靠性、可制造性等质量要求的角色。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0680',
    name: 'Drop Test',
    type: '其他',
    category: 'countermeasures',
    aliases: ['跌落测试'],
    tags: ['可靠性;结构相关'],
    description: '模拟手机意外跌落场景，验证整机结构强度、屏幕和电池等部件的可靠性。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0681',
    name: 'DSU',
    type: '其他',
    category: 'countermeasures',
    aliases: ['动态软件更新;Dynamic System Updates'],
    tags: ['项目相关;工具'],
    description: 'Android项目在运行时切换系统镜像的技术，用于软件调试与测试。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0682',
    name: 'ESD',
    type: '其他',
    category: 'countermeasures',
    aliases: ['静电放电;Electro-Static Discharge'],
    tags: ['硬件相关;可靠性'],
    description: '测试手机抵御静电冲击的能力，不合格会导致芯片击穿或功能异常。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0683',
    name: 'FACA',
    type: '其他',
    category: 'countermeasures',
    aliases: ['最终审核纠正措施;Final Audit Corrective Action'],
    tags: ['质量体系;项目相关'],
    description: '在项目量产前，针对开箱审计发现的问题进行闭环管理的流程。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0684',
    name: 'HALT',
    type: '其他',
    category: 'countermeasures',
    aliases: ['高加速寿命测试;Highly Accelerated Life Test'],
    tags: ['可靠性;研发'],
    description: '通过施加高应力快速激发产品潜在缺陷的测试方法，用于设计阶段。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0685',
    name: 'IQC',
    type: '其他',
    category: 'countermeasures',
    aliases: ['来料检验;Incoming Quality Control'],
    tags: ['制造工艺;质量体系'],
    description: '对供应商送达的物料进行检验，确保投入生产的物料符合标准。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0686',
    name: 'MTBF',
    type: '其他',
    category: 'countermeasures',
    aliases: ['平均无故障时间;Mean Time Between Failures'],
    tags: ['可靠性;性能指标'],
    description: '衡量产品可靠性的关键预测指标，通常通过可靠性试验数据计算得出。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0687',
    name: 'PMP',
    type: '其他',
    category: 'countermeasures',
    aliases: ['项目管理计划;Project Management Plan'],
    tags: ['流程相关;组织职责'],
    description: '项目开展的总体指导文件，包含范围、进度、质量、风险等管理计划。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0688',
    name: 'PVT',
    type: '其他',
    category: 'countermeasures',
    aliases: ['生产验证测试;Production Validation Test'],
    tags: ['测试验证;制造工艺'],
    description: '在量产初期进行的测试，验证生产线能否稳定地生产出合格产品。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0689',
    name: 'SMT',
    type: '其他',
    category: 'countermeasures',
    aliases: ['表面贴装技术;Surface Mount Technology'],
    tags: ['硬件相关;PCB'],
    description: '将电子元器件贴装到PCB上的核心工艺，涉及锡膏印刷、贴片、回流焊。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0690',
    name: 'UV胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['紫外线固化胶;Ultraviolet Glue'],
    tags: ['结构相关;粘合剂'],
    description: '用于固定镜头、装饰件等，固化不良会导致脱落或溢胶。',
    created_at: '2025-09-26T09:43:14.276213',
    updated_at: '2025-09-26T09:43:14.276213'
});
CREATE (d:Dictionary {
    id: 'TERM_0691',
    name: 'Vendor',
    type: '其他',
    category: 'countermeasures',
    aliases: ['供应商;Supplier'],
    tags: ['流程相关;项目相关'],
    description: '提供手机零部件或服务的厂商，其质量能力直接影响整机质量。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0692',
    name: '点胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['打胶;Underfill'],
    tags: ['结构相关;工艺参数'],
    description: '在芯片底部填充胶水以增强机械强度和耐热性，胶量、路径是关键参数。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0693',
    name: '点屏',
    type: '其他',
    category: 'countermeasures',
    aliases: ['屏幕点亮;Screen Lighting'],
    tags: ['制造工艺;显示相关'],
    description: '在组装过程中对显示屏进行通电，初步检查显示功能是否正常。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0694',
    name: '点压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['按压测试;Press Test'],
    tags: ['人机交互;可靠性'],
    description: '对手机按键、屏幕等进行反复按压，测试其机械耐久性。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0695',
    name: '钝化',
    type: '其他',
    category: 'countermeasures',
    aliases: ['钝化层;Passivation'],
    tags: ['硬件相关;PCB'],
    description: '在芯片或PCB表面形成保护层，防止腐蚀和短路，损伤会导致可靠性问题。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0696',
    name: '多标签',
    type: '其他',
    category: 'countermeasures',
    aliases: ['标签;Tag'],
    tags: ['项目相关;软件相关'],
    description: '用于对问题、物料或知识进行分类和标记的元数据，便于筛选和管理。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0697',
    name: '防呆',
    type: '其他',
    category: 'countermeasures',
    aliases: ['防错;Poka-Yoke'],
    tags: ['质量体系;工具'],
    description: '设计一种装置或方法，防止操作员出现错误，是提升直通率的关键。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0698',
    name: '分板',
    type: '其他',
    category: 'countermeasures',
    aliases: ['板边切割;Board Cutting'],
    tags: ['PCB;工艺参数'],
    description: '将拼板后的PCB分割成单板，方式不当会导致板边毛刺、裂纹或应力损伤。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0699',
    name: '风枪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热风枪;Hot Air Gun'],
    tags: ['维修;SMT'],
    description: '用于维修时加热焊料或拆焊元件的工具，温度和控制精度是关键。',
    created_at: '2025-09-26T09:43:14.276723',
    updated_at: '2025-09-26T09:43:14.276723'
});
CREATE (d:Dictionary {
    id: 'TERM_0700',
    name: '工装',
    type: '其他',
    category: 'countermeasures',
    aliases: ['夹具;治具;Fixture'],
    tags: ['制造工艺;测试验证'],
    description: '在生产或测试中用于定位和固定产品的装置，其精度直接影响产品一致性。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0701',
    name: '固件',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Firmware'],
    tags: ['部件;功能'],
    description: '写入硬件设备的底层软件，如摄像头固件，版本错误或损坏会导致功能异常。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0702',
    name: '挂机',
    type: '其他',
    category: 'countermeasures',
    aliases: ['待机;Standby'],
    tags: ['软件相关;可靠性'],
    description: '手机在休眠状态下长时间运行，用于测试待机功耗和系统稳定性。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0703',
    name: '过炉',
    type: '其他',
    category: 'countermeasures',
    aliases: ['回流焊;Reflow Soldering'],
    tags: ['SMT;工艺参数'],
    description: 'SMT关键工序，通过加热使锡膏熔化连接元件，温度曲线设置至关重要。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0704',
    name: '焊锡',
    type: '其他',
    category: 'countermeasures',
    aliases: ['锡膏;Solder Paste'],
    tags: ['物料;SMT'],
    description: '用于焊接的合金材料，其成分、颗粒度和活性影响焊接质量。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0705',
    name: '合盖',
    type: '其他',
    category: 'countermeasures',
    aliases: ['闭合状态;Closed State'],
    tags: ['结构相关;可靠性'],
    description: '针对折叠屏手机，测试在闭合状态下的机构稳定性、缝隙和压力。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0706',
    name: '烘烤',
    type: '其他',
    category: 'countermeasures',
    aliases: ['低温烘烤;Baking'],
    tags: ['PCB;工艺参数'],
    description: '对受潮的PCB或元件进行烘干，去除湿气，防止回流焊时出现爆米花现象。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0707',
    name: '红胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['红色胶水;Red Adhesive'],
    tags: ['物料;SMT'],
    description: '一种用于波峰焊前暂时固定元件的胶水，点胶量和固化程度是关键。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0708',
    name: '环测',
    type: '其他',
    category: 'countermeasures',
    aliases: ['环境测试;Environmental Test'],
    tags: ['可靠性'],
    description: '将手机置于高低温、湿热、振动等模拟环境中，验证其适应能力。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0709',
    name: '灰阶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['灰度等级;Gray Scale'],
    tags: ['性能指标;影像相关'],
    description: '表示屏幕从黑到白的亮度层次，层次越多，显示效果越细腻。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0710',
    name: '回流焊',
    type: '其他',
    category: 'countermeasures',
    aliases: ['再流焊;Reflow'],
    tags: ['SMT;工艺参数'],
    description: '通过加热使预涂的锡膏熔化，实现元器件与PCB焊盘连接的工艺。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0711',
    name: '激活',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电池激活;Battery Activation'],
    tags: ['硬件相关;工艺参数'],
    description: '新电池首次充电的特定流程，以稳定其化学性能，但现在多数锂电已不需要。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0712',
    name: '机模',
    type: '其他',
    category: 'countermeasures',
    aliases: ['手机模型;Dummy Model'],
    tags: ['项目相关;结构相关'],
    description: '无功能的手机外观模型，用于早期结构验证、外观评估和营销展示。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0713',
    name: '激光',
    type: '其他',
    category: 'countermeasures',
    aliases: ['激光焊接;Laser Welding'],
    tags: ['工艺参数;结构相关'],
    description: '使用激光能量进行精密焊接，常用于电池盖、内部结构件，热影响区小。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0714',
    name: '夹持',
    type: '其他',
    category: 'countermeasures',
    aliases: ['夹具夹紧;Clamping'],
    tags: ['工艺参数;工装'],
    description: '治具对产品的固定力，过小导致位移，过大可能导致产品变形或压伤。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0715',
    name: '检具',
    type: '其他',
    category: 'countermeasures',
    aliases: ['检验治具;Checking Fixture'],
    tags: ['测试验证;质量体系'],
    description: '专门用于快速检测产品尺寸或装配效果的工装，提升检验效率和一致性。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0716',
    name: '胶厚',
    type: '其他',
    category: 'countermeasures',
    aliases: ['胶水厚度;Adhesive Thickness'],
    tags: ['工艺参数;结构相关'],
    description: '点胶或贴合的胶层厚度，影响粘接强度和密封性能。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0717',
    name: '胶量',
    type: '其他',
    category: 'countermeasures',
    aliases: ['点胶量;Dispensing Volume'],
    tags: ['工艺参数'],
    description: '点胶机每次挤出的胶水体积，是影响粘接效果的关键参数。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0718',
    name: '角胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['角落补强胶;Corner Reinforcement'],
    tags: ['结构相关;工艺参数'],
    description: '在结构件角落点胶以增强局部强度，常用于应对跌落应力。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0719',
    name: '校屏',
    type: '其他',
    category: 'countermeasures',
    aliases: ['屏幕校准;Screen Calibration'],
    tags: ['制造工艺;显示相关'],
    description: '对显示屏的色温、Gamma、均匀性等进行软件校准，保证显示一致性。',
    created_at: '2025-09-26T09:43:14.277730',
    updated_at: '2025-09-26T09:43:14.277730'
});
CREATE (d:Dictionary {
    id: 'TERM_0720',
    name: '解锁',
    type: '其他',
    category: 'countermeasures',
    aliases: ['屏幕解锁;Unlock'],
    tags: ['软件相关;人机交互'],
    description: '测试指纹、人脸、图案等解锁方式的成功率和速度。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0721',
    name: '浸锡',
    type: '其他',
    category: 'countermeasures',
    aliases: ['沾锡;Solder Dipping'],
    tags: ['工艺参数;PCB'],
    description: '将元件引脚浸入熔融焊锡中以实现焊接的工艺。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0722',
    name: '静电袋',
    type: '其他',
    category: 'countermeasures',
    aliases: ['防静电袋;ESD Bag'],
    tags: ['物料;ESD'],
    description: '用于包装和运输对静电敏感的元器件。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0723',
    name: '静电环',
    type: '其他',
    category: 'countermeasures',
    aliases: ['防静电手环;ESD Wrist Strap'],
    tags: ['ESD;制造工艺'],
    description: '操作人员佩戴，将人体静电导入大地，防止损坏电子产品。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0724',
    name: '开口',
    type: '其他',
    category: 'countermeasures',
    aliases: ['钢网开口;Stencil Aperture'],
    tags: ['工具;SMT'],
    description: '钢网上用于让锡膏通过的孔，其尺寸和形状决定了锡膏的印刷量。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0725',
    name: '开炉',
    type: '其他',
    category: 'countermeasures',
    aliases: ['打开回流焊炉;Open Reflow Oven'],
    tags: ['SMT;操作'],
    description: '生产开始或换线时，启动回流焊炉并确认其状态的过程。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0726',
    name: '开模',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模具开启;Mold Opening'],
    tags: ['工具;结构相关'],
    description: '注塑成型中，模具打开以便取出成型产品的动作。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0727',
    name: '开箱',
    type: '其他',
    category: 'countermeasures',
    aliases: ['拆箱;Unboxing'],
    tags: ['质量体系;项目相关'],
    description: '指OBA（开箱审计），模拟客户首次打开产品包装的体验和检查。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0728',
    name: '烤机',
    type: '其他',
    category: 'countermeasures',
    aliases: ['老化测试;Burn-in Test'],
    tags: ['可靠性;硬件相关'],
    description: '让手机在特定条件下长时间运行，以提前暴露早期失效的元器件。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0729',
    name: '磕碰',
    type: '其他',
    category: 'countermeasures',
    aliases: ['撞击;Impact'],
    tags: ['可靠性;外观'],
    description: '模拟产品在日常使用中受到的小范围撞击，评估外壳和内部受损情况。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0730',
    name: '可制造性',
    type: '其他',
    category: 'countermeasures',
    aliases: ['可生产性;Manufacturability'],
    tags: ['设计;制造工艺'],
    description: '产品设计易于高效、低成本、高质量地制造出来的特性。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0731',
    name: '客诉',
    type: '其他',
    category: 'countermeasures',
    aliases: ['客户投诉;Customer Complaint'],
    tags: ['质量体系;项目相关'],
    description: '终端用户或客户对产品质量问题的反馈，是质量改进的重要输入。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0732',
    name: '老化',
    type: '其他',
    category: 'countermeasures',
    aliases: ['老化测试;Aging'],
    tags: ['可靠性'],
    description: '使产品在模拟的或强化的使用条件下运行一段时间，以稳定其性能或筛选缺陷。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0733',
    name: '冷屏',
    type: '其他',
    category: 'countermeasures',
    aliases: ['冷屏点亮;Cold Start Screen'],
    tags: ['显示相关;可靠性'],
    description: '在低温环境下对屏幕进行点亮测试，检查其响应速度和显示效果。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0734',
    name: '料带',
    type: '其他',
    category: 'countermeasures',
    aliases: ['载带;Carrier Tape'],
    tags: ['物料;SMT'],
    description: '用于SMT贴片机供料器上承载元件的塑料带。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0735',
    name: '料号',
    type: '其他',
    category: 'countermeasures',
    aliases: ['物料编号;Part Number'],
    tags: ['物料;项目相关'],
    description: '唯一标识一种物料或部件的编码，是物料管理的基础。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0736',
    name: '美纹纸',
    type: '其他',
    category: 'countermeasures',
    aliases: ['和美胶带;Painter\'s Tape'],
    tags: ['制造工艺;防护'],
    description: '在喷涂或点胶时用于遮蔽不需要处理的区域。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0737',
    name: '模厂',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模具厂;Mold Factory'],
    tags: ['供应链;制造工艺'],
    description: '负责设计和制造注塑模具的供应商。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0738',
    name: '模切',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模具切割;Die Cutting'],
    tags: ['工艺参数;物料'],
    description: '使用模具对泡棉、胶带等材料进行精密冲切成型。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0739',
    name: '模温',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模具温度;Mold Temperature'],
    tags: ['工艺参数;注塑'],
    description: '注塑过程中模具的温度，影响塑料的流动性和产品的成型质量。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0740',
    name: '模流',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模流分析;Mold Flow Analysis'],
    tags: ['设计;制造工艺'],
    description: '通过软件模拟塑料在模具内的流动、保压、冷却过程，预测潜在缺陷。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0741',
    name: '尼龙',
    type: '其他',
    category: 'countermeasures',
    aliases: ['尼龙螺丝;Nylon Screw'],
    tags: ['部件;结构相关'],
    description: '用于绝缘或防松动的塑料螺丝，扭矩控制不当易滑牙或断裂。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0742',
    name: '泡棉',
    type: '其他',
    category: 'countermeasures',
    aliases: ['导电泡棉;Conductive Foam'],
    tags: ['部件;EMC'],
    description: '用于填充缝隙、提供缓冲和电磁屏蔽的多孔材料。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0743',
    name: '喷码',
    type: '其他',
    category: 'countermeasures',
    aliases: ['喷墨打标;Inkjet Marking'],
    tags: ['外观;追溯性'],
    description: '使用喷墨机在产品或标签上打印序列号、生产日期等信息。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0744',
    name: '气吹',
    type: '其他',
    category: 'countermeasures',
    aliases: ['吹气清洁;Air Blowing'],
    tags: ['操作;清洁'],
    description: '使用压缩气体清除产品表面的灰尘或颗粒物。',
    created_at: '2025-09-26T09:43:14.278729',
    updated_at: '2025-09-26T09:43:14.278729'
});
CREATE (d:Dictionary {
    id: 'TERM_0745',
    name: '清尾',
    type: '其他',
    category: 'countermeasures',
    aliases: ['生产线清尾;Line Clearance'],
    tags: ['流程相关;操作'],
    description: '生产订单结束时，清理生产线上的物料和产品，确保下一订单顺利开始。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0746',
    name: '取放',
    type: '其他',
    category: 'countermeasures',
    aliases: ['拾取与放置;Pick and Place'],
    tags: ['SMT;操作'],
    description: '贴片机从供料器取料并贴装到PCB上的基本动作。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0747',
    name: '圈胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['环形点胶;Circular Dispensing'],
    tags: ['工艺参数;结构相关'],
    description: '以环形轨迹点胶，常用于需要密封的圆形区域。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0748',
    name: '确认书',
    type: '其他',
    category: 'countermeasures',
    aliases: ['工程确认书;Engineering Confirmation'],
    tags: ['项目相关;质量体系'],
    description: '对设计变更、样品状态等进行正式确认的文件，作为量产依据。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0749',
    name: '热压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热熔;Heat Staking'],
    tags: ['工艺参数;结构相关'],
    description: '通过加热和压力使塑料柱销变形，从而固定另一个部件。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0750',
    name: '热插拔',
    type: '其他',
    category: 'countermeasures',
    aliases: ['带电插拔;Hot Plug'],
    tags: ['硬件相关;可靠性'],
    description: '在手机开机状态下插入或拔出外设（如U盘），测试接口的耐受性。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0751',
    name: '热风',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热风枪;Hot Air'],
    tags: ['维修;SMT'],
    description: '用于维修焊接的工具，通过喷射热空气来熔化焊锡。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0752',
    name: '人因',
    type: '其他',
    category: 'countermeasures',
    aliases: ['人因工程;Human Factors'],
    tags: ['设计;人机交互'],
    description: '研究人、机器及环境之间相互作用的学科，旨在优化产品易用性和舒适度。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0753',
    name: '入网',
    type: '其他',
    category: 'countermeasures',
    aliases: ['进网许可;Network Access License'],
    tags: ['流程相关;法规'],
    description: '在中国大陆市场销售蜂窝通信设备必须获得的官方认证。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0754',
    name: '三防',
    type: '其他',
    category: 'countermeasures',
    aliases: ['防潮、防霉、防盐雾;Three Proofing'],
    tags: ['可靠性'],
    description: '针对恶劣环境（湿热、霉菌、盐雾）的防护性设计和测试。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0755',
    name: '上料',
    type: '其他',
    category: 'countermeasures',
    aliases: ['物料上料;Loading Material'],
    tags: ['操作;SMT'],
    description: '将料盘安装到贴片机供料器上的操作。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0756',
    name: '设变',
    type: '其他',
    category: 'countermeasures',
    aliases: ['设计变更;Design Change'],
    tags: ['项目相关;质量体系'],
    description: '产品开发过程中对已冻结设计的修改，需要严格的流程控制。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0757',
    name: '射屏',
    type: '其他',
    category: 'countermeasures',
    aliases: ['屏幕投射;Screen Casting'],
    tags: ['软件相关;功能'],
    description: '将手机屏幕内容无线投射到其他显示设备上的功能测试。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0758',
    name: '深色',
    type: '其他',
    category: 'countermeasures',
    aliases: ['暗色模式;Dark Mode'],
    tags: ['功能;显示相关'],
    description: '系统界面以深色为主色调的显示模式，有助于节省OLED屏幕功耗。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0759',
    name: '油墨',
    type: '其他',
    category: 'countermeasures',
    aliases: ['印刷油墨;Printing Ink'],
    tags: ['物料;外观'],
    description: '用于丝印、移印等工艺的着色材料，要求附着力、耐磨性好。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0760',
    name: '预压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['预压力;Preload'],
    tags: ['工艺参数;结构相关'],
    description: '在正式紧固前施加的初始压力，使部件初步就位。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0761',
    name: '原材',
    type: '其他',
    category: 'countermeasures',
    aliases: ['原材料;Raw Material'],
    tags: ['物料'],
    description: '用于生产产品的基本材料，如塑胶粒、金属板材、化学药水等。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0762',
    name: '扎带',
    type: '其他',
    category: 'countermeasures',
    aliases: ['束线带;Cable Tie'],
    tags: ['部件;线缆管理'],
    description: '用于捆扎和固定内部线缆的塑料带。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0763',
    name: '针床',
    type: '其他',
    category: 'countermeasures',
    aliases: ['针床测试架;Bed of Nails Fixture'],
    tags: ['测试验证;ICT'],
    description: '用于在线测试的多针夹具，可同时接触PCB上多个测试点。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0764',
    name: '真空',
    type: '其他',
    category: 'countermeasures',
    aliases: ['真空吸附;Vacuum Suction'],
    tags: ['工艺参数;SMT'],
    description: '贴片机利用真空吸嘴抓取元器件的原理。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0765',
    name: '整机',
    type: '其他',
    category: 'countermeasures',
    aliases: ['完整手机;Complete Unit'],
    tags: ['测试验证;项目相关'],
    description: '指装配完整、可正常工作的手机成品。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0766',
    name: '正压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['正压力;Positive Pressure'],
    tags: ['工艺参数;结构相关'],
    description: '施加于产品表面的压力，如气密性测试时向密封腔体内充气加压。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0767',
    name: '制具',
    type: '其他',
    category: 'countermeasures',
    aliases: ['同治具'],
    tags: ['制造工艺;测试验证'],
    description: '在生产或测试中用于定位和固定产品的装置。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0768',
    name: '治具',
    type: '其他',
    category: 'countermeasures',
    aliases: ['夹具;Fixture'],
    tags: ['制造工艺;测试验证'],
    description: '在生产或测试中用于定位和固定产品的装置，其精度直接影响产品一致性。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0769',
    name: '钟摆',
    type: '其他',
    category: 'countermeasures',
    aliases: ['摆动测试;Pendulum Test'],
    tags: ['可靠性;结构相关'],
    description: '模拟手机在背包或口袋中来回摆动，测试其结构和连接的耐久性。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0770',
    name: '重工',
    type: '其他',
    category: 'countermeasures',
    aliases: ['返工;Rework'],
    tags: ['流程相关;质量体系'],
    description: '对不合格品进行修复处理，使其符合标准要求的活动。',
    created_at: '2025-09-26T09:43:14.279731',
    updated_at: '2025-09-26T09:43:14.279731'
});
CREATE (d:Dictionary {
    id: 'TERM_0771',
    name: '周波',
    type: '其他',
    category: 'countermeasures',
    aliases: ['周波数;Cycle'],
    tags: ['可靠性'],
    description: '重复性测试的次数，如按键测试XX万次。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0772',
    name: '注塑',
    type: '其他',
    category: 'countermeasures',
    aliases: ['注射成型;Injection Molding'],
    tags: ['工艺参数;结构相关'],
    description: '将熔融塑料注入模具腔体，冷却后得到塑料制品的工艺。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0773',
    name: '装框',
    type: '其他',
    category: 'countermeasures',
    aliases: ['安装边框;Bezel Assembly'],
    tags: ['操作;结构相关'],
    description: '将屏幕模组安装到中框或前壳上的工序。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0774',
    name: '资材',
    type: '其他',
    category: 'countermeasures',
    aliases: ['物资材料;Materials'],
    tags: ['供应链;物料'],
    description: '泛指生产所需的各类物料和资源。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0775',
    name: '子料',
    type: '其他',
    category: 'countermeasures',
    aliases: ['子物料;Sub-material'],
    tags: ['物料'],
    description: '构成一个成品或半成品所需的多种物料中的一种。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0776',
    name: '走纸',
    type: '其他',
    category: 'countermeasures',
    aliases: ['标签纸走纸;Label Paper Feeding'],
    tags: ['操作;包装'],
    description: '在自动贴标机上，标签纸卷的正常输送。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0777',
    name: '组包',
    type: '其他',
    category: 'countermeasures',
    aliases: ['包装组装;Packing Assembly'],
    tags: ['操作;包装'],
    description: '将手机、配件、说明书等装入包装盒的最终工序。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0778',
    name: '钻孔',
    type: '其他',
    category: 'countermeasures',
    aliases: ['PCB钻孔;Drilling'],
    tags: ['工艺参数;PCB'],
    description: '在PCB上钻取导通孔、安装孔等，精度要求高。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0779',
    name: '爆破测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['破坏性压力测试'],
    tags: ['可靠性;安全相关;电池'],
    description: '对电池或密封结构施加远超额定值的压力，直至其破坏，以验证最大承受极限。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0780',
    name: '金相分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['显微组织分析'],
    tags: ['可靠性;物料;制造工艺'],
    description: '通过显微镜观察材料的微观组织结构，分析其工艺质量及失效原因。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0781',
    name: '邦定胶',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Underfill；底部填充胶'],
    tags: ['工艺参数;SMT;可靠性'],
    description: '用于BGA/CSP芯片底部填充的环氧树脂胶，通过毛细作用流入，增强焊点可靠性。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0782',
    name: '白噪声测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['White Noise Test'],
    tags: ['可靠性;声学;硬件相关'],
    description: '向扬声器或麦克风输入全频带白噪声，测试其在宽频带下的工作稳定性和可靠性。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0783',
    name: '导通孔塞孔',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Via Plugging'],
    tags: ['工艺参数;PCB'],
    description: '用树脂或油墨填充导通孔，以便在孔上布线和焊接，对平整度要求高。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0784',
    name: '模流平衡',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Flow Balance'],
    tags: ['工艺参数;注塑;设计'],
    description: '注塑时熔料能同时到达并充满模具型腔的各个末端，避免滞流和欠注。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0785',
    name: '点胶轨迹',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Dispensing Path'],
    tags: ['工艺参数;点胶;自动化'],
    description: '点胶机针头运动的路径规划，影响胶水覆盖的准确性和一致性。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0786',
    name: '等离子处理',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Plasma Treatment'],
    tags: ['工艺参数;表面处理'],
    description: '利用等离子体活化材料表面，显著提高其润湿性和粘接附着力。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0787',
    name: '溅射镀膜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Sputtering Coating'],
    tags: ['工艺参数;CMF;硬件相关'],
    description: '在真空环境下用离子轰击靶材，使其原子溅射并沉积到工件表面形成薄膜。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0788',
    name: '模温机',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Mold Temperature Controller'],
    tags: ['制造工艺;注塑'],
    description: '用于精确控制注塑模具温度的设备，对成型质量至关重要。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0789',
    name: '热仿真',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Thermal Simulation'],
    tags: ['设计;热管理;软件相关'],
    description: '通过计算机软件模拟产品在工作状态下的温度分布和热流情况。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0790',
    name: '填胶量',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Encapsulation Volume'],
    tags: ['工艺参数;可靠性;点胶'],
    description: '对芯片进行包封保护时，注入的胶水体积，需确保完全覆盖且无气泡。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0791',
    name: '盐雾测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Salt Spray Test'],
    tags: ['可靠性;CMF;硬件相关'],
    description: '模拟海洋大气环境，测试产品或材料耐腐蚀性能的加速试验方法。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0792',
    name: '模内注塑',
    type: '其他',
    category: 'countermeasures',
    aliases: ['In-Mold Molding', 'IMM'],
    tags: ['工艺参数;结构相关;装饰'],
    description: '将薄膜或织物放入模具内，注塑时塑料将其包覆成一体，实现装饰效果。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0793',
    name: '导通孔背钻',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Back Drilling'],
    tags: ['工艺参数;PCB;设计'],
    description: '钻掉高速PCB板中不需要的导通孔 stub，以减少信号反射，提升信号完整性。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0794',
    name: '贴装压力',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Placement Pressure'],
    tags: ['工艺参数;SMT'],
    description: '贴片机贴装元件时，吸嘴对元件施加的压力。压力过大会损伤元件，过小则贴装不稳。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0795',
    name: '跌落姿态',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Drop Orientation'],
    tags: ['可靠性;结构相关'],
    description: '手机跌落时与冲击面接触的初始角度和部位，对失效模式影响显著。',
    created_at: '2025-09-26T09:43:14.280733',
    updated_at: '2025-09-26T09:43:14.280733'
});
CREATE (d:Dictionary {
    id: 'TERM_0796',
    name: '三综合测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Combined Environmental Test'],
    tags: ['可靠性;硬件相关'],
    description: '同时施加温度、湿度和振动三种应力，更真实模拟恶劣环境的测试。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0797',
    name: 'JEDEC托盘',
    type: '其他',
    category: 'countermeasures',
    aliases: ['JEDEC Tray'],
    tags: ['物料;SMT;制造工艺'],
    description: '标准化尺寸的塑料托盘，用于运输和贴片机供料。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0798',
    name: '模仁',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Mold Insert；模具嵌件'],
    tags: ['制造工艺;注塑'],
    description: '模具中直接形成产品型腔的可更换精密零件。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0799',
    name: '底部填充',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Underfill'],
    tags: ['工艺参数;SMT;可靠性'],
    description: '同邦定胶。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0800',
    name: '金丝键合',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Gold Wire Bonding'],
    tags: ['工艺参数;半导体;封装'],
    description: '使用细金线连接芯片焊盘和封装引脚的内互连技术。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0801',
    name: '电磁仿真',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Electromagnetic Simulation'],
    tags: ['设计;EMC;射频相关'],
    description: '通过计算机软件模拟电磁场的分布和相互作用，用于天线、EMC设计。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0802',
    name: '导通孔阻焊',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Solder Mask over Via', 'SMV'],
    tags: ['工艺参数;PCB'],
    description: '在导通孔上覆盖阻焊层，防止焊锡流入。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0803',
    name: '激光焊',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Laser Welding'],
    tags: ['工艺参数;结构相关;可靠性'],
    description: '利用高能量激光束作为热源进行熔焊的方法，精度高，热影响区小。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0804',
    name: '导通孔树脂塞孔',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Resin Plugged Via'],
    tags: ['工艺参数;PCB'],
    description: '使用树脂填充导通孔，是塞孔的一种方式。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0805',
    name: '热失重',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Thermogravimetric Analysis', 'TGA'],
    tags: ['物料;可靠性;测试验证'],
    description: '测量材料质量随温度升高而发生的变化，用于分析热稳定性、成分等。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0806',
    name: '模流分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Mold Flow Analysis'],
    tags: ['设计;制造工艺;注塑'],
    description: '通过CAE软件模拟塑料在模具中的流动、保压、冷却过程，预测缺陷。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0807',
    name: '真空镀膜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Vacuum Deposition'],
    tags: ['工艺参数;CMF;硬件相关'],
    description: '在真空环境中通过物理或化学方法在工件表面沉积薄膜的技术总称。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0808',
    name: '漏测',
    type: '其他',
    category: 'countermeasures',
    aliases: ['测试遗漏;Missed Test'],
    tags: ['质量体系;测试验证'],
    description: '**定义**: 应检项目未执行。 **判定口径**: 测试覆盖率 <100%。 **常见场景**: 产线OBA/功能测试。 **排查路径**: 审核工艺卡→检查治具。 **对策**: 加强自动化测试和流程审核。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0809',
    name: '频偏',
    type: '其他',
    category: 'countermeasures',
    aliases: ['频率偏移;Frequency Offset'],
    tags: ['通信相关;射频相关'],
    description: '**定义**: 无线发射频率偏离标准值。 **判定口径**: 偏移 >±50ppm。 **常见场景**: OTA测试、极端温度。 **排查路径**: 检查晶振→校准电路。 **对策**: 增加温补电路，改善器件精度。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0810',
    name: '电池续航不足',
    type: '其他',
    category: 'countermeasures',
    aliases: ['续航差;Poor Battery Life'],
    tags: ['硬件相关;电池'],
    description: '**定义**: 单次充电使用时长不足。 **判定口径**: 使用时长低于标称值 20%。 **常见场景**: 高功耗应用。 **排查路径**: 功耗分析→检查电芯容量。 **对策**: 优化系统调度，提升电池能量密度。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0811',
    name: '电池容量衰减',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电池老化;Battery Aging'],
    tags: ['电池;可靠性'],
    description: '**定义**: 电池可用容量下降。 **判定口径**: 循环 500 次后容量 <80%。 **常见场景**: 长期使用。 **排查路径**: 读取电池健康数据。 **对策**: 改善材料体系，增加健康监控。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0812',
    name: '纳米注塑',
    type: '其他',
    category: 'countermeasures',
    aliases: ['NMT'],
    tags: ['工艺参数;结构相关;可靠性'],
    description: '在金属表面通过化学处理形成纳米级微孔，注塑时塑料渗入形成强机械互锁，实现金属与塑料的牢固结合。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0813',
    name: '点胶高度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['针头离板高度'],
    tags: ['工艺参数;点胶;SMT'],
    description: '点胶针头尖端与PCB表面的距离，影响胶点形状和一致性。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0814',
    name: '声学密封性',
    type: '其他',
    category: 'countermeasures',
    aliases: ['声学气密性'],
    tags: ['硬件相关;声学;可靠性'],
    description: '扬声器BOX或麦克风腔体的密封程度，直接影响低频响应和灵敏度。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0815',
    name: '钢板张力',
    type: '其他',
    category: 'countermeasures',
    aliases: ['钢网张力'],
    tags: ['工艺参数;SMT'],
    description: '张紧钢网使其保持平整的力，张力不足会导致印刷时钢网下垂，影响锡膏厚度。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0816',
    name: '离子污染度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['离子洁净度'],
    tags: ['PCB;可靠性;测试验证'],
    description: '单位面积PCB表面可水解离子的当量浓度，常用NaCl当量表示，要求低于特定阈值（如1.56μg/cm²）。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0817',
    name: '焊点推拉力',
    type: '其他',
    category: 'countermeasures',
    aliases: ['焊点强度测试'],
    tags: ['可靠性;SMT;硬件相关'],
    description: '使用推拉力测试仪测量单个焊点所能承受的机械强度，用于工艺验证和失效分析。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0818',
    name: '模流剪切热',
    type: '其他',
    category: 'countermeasures',
    aliases: ['剪切生热'],
    tags: ['工艺参数;注塑;可靠性'],
    description: '塑料熔体在高速流经狭小区域时，因内部分子摩擦产生热量，可能导致材料降解。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0819',
    name: '天线频段',
    type: '其他',
    category: 'countermeasures',
    aliases: ['工作频段'],
    tags: ['硬件相关;通信相关;设计'],
    description: '天线能有效工作的频率范围，需覆盖目标市场的所有通信制式（如LTE Band 1, 3, 5...）。',
    created_at: '2025-09-26T09:43:14.281731',
    updated_at: '2025-09-26T09:43:14.281731'
});
CREATE (d:Dictionary {
    id: 'TERM_0820',
    name: '真空回流焊',
    type: '其他',
    category: 'countermeasures',
    aliases: ['真空炉'],
    tags: ['工艺参数;SMT;可靠性'],
    description: '在真空环境下进行回流焊，能有效消除焊点内部气泡，大幅减少空洞率，提升可靠性。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0821',
    name: '胶体屈服值',
    type: '其他',
    category: 'countermeasures',
    aliases: ['屈服应力'],
    tags: ['物料;制造工艺;点胶'],
    description: '使胶水开始流动所需的最小剪切应力，影响点胶的起始性和抗塌陷性。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0822',
    name: '板级可靠性',
    type: '其他',
    category: 'countermeasures',
    aliases: ['BLR'],
    tags: ['可靠性;硬件相关;PCB'],
    description: '针对装配好的PCB进行的可靠性测试，如温度循环、跌落、弯曲等，评估其在实际应用中的寿命。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0823',
    name: '激光功率密度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['能量密度'],
    tags: ['工艺参数;激光加工'],
    description: '单位面积上的激光能量，决定加工效果（如切割、焊接、打标）的质量和效率。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0824',
    name: '电化学阻抗谱',
    type: '其他',
    category: 'countermeasures',
    aliases: ['EIS'],
    tags: ['硬件相关;电池;可靠性'],
    description: '通过施加小幅交流电信号测量电池阻抗随频率的变化，用于分析电池健康状态和反应机理。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0825',
    name: '模内收缩率',
    type: '其他',
    category: 'countermeasures',
    aliases: ['体积收缩率'],
    tags: ['物料;注塑;设计'],
    description: '塑料从熔融状态冷却到固态时的体积变化率，是模具设计时确定收缩补偿系数的依据。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0826',
    name: '信号眼图',
    type: '其他',
    category: 'countermeasures',
    aliases: ['眼图'],
    tags: ['硬件相关;测试验证;设计'],
    description: '用于评估高速数字信号质量（如MIPI, USB）的图形化方法，眼图张开度越大，信号质量越好。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0827',
    name: '邦定线弧高度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['线弧拱高'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线最高点与芯片表面的垂直距离，需精确控制以避免与盖板干涉或短路。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0828',
    name: '导热系数',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热导率'],
    tags: ['物料;热管理;可靠性'],
    description: '材料传导热量的能力，单位W/(m·K)，是选择散热材料的关键参数。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0829',
    name: '锡膏坍落度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['锡膏流变性'],
    tags: ['物料;SMT;制造工艺'],
    description: '衡量锡膏印刷后保持原有形状、抵抗流动和变形能力的指标。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0830',
    name: '模流平衡分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['流道平衡'],
    tags: ['设计;制造工艺;注塑'],
    description: '通过模拟优化流道系统设计，确保各型腔能同时充满，减少产品间的差异。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0831',
    name: '射频传导骚扰',
    type: '其他',
    category: 'countermeasures',
    aliases: ['射频干扰'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '通过电源线或信号线向外发射的射频噪声，需要满足EMC法规限值。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0832',
    name: '胶体储能模量',
    type: '其他',
    category: 'countermeasures',
    aliases: ['弹性模量'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂在交变应力下弹性变形分量对应的模量，反映其弹性行为。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0833',
    name: '高倍率扫描电镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['SEM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用聚焦电子束扫描样品表面，获得高分辨率形貌图像，用于微观结构观察和失效分析。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0834',
    name: '模内温度传感器',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模温感应器'],
    tags: ['制造工艺;注塑;测试验证'],
    description: '植入模具内部，用于实时监测型腔表面或内部某点温度的设备。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0835',
    name: '信号上升时间',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Rise Time'],
    tags: ['硬件相关;设计;测试验证'],
    description: '数字信号从低电平上升到高电平规定比例所需的时间，是信号完整性的关键参数。',
    created_at: '2025-09-26T09:43:14.282732',
    updated_at: '2025-09-26T09:43:14.282732'
});
CREATE (d:Dictionary {
    id: 'TERM_0836',
    name: '邦定第二点',
    type: '其他',
    category: 'countermeasures',
    aliases: ['stitch bond'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线在引脚或基板焊盘上的连接点，与芯片上的第一点（球焊）相对应。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0837',
    name: '热重分析仪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['TGA'],
    tags: ['测试验证;物料;可靠性'],
    description: '测量样品质量随温度或时间变化关系的仪器，用于分析热稳定性、分解温度等。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0838',
    name: '锡膏印刷性',
    type: '其他',
    category: 'countermeasures',
    aliases: ['印刷适性'],
    tags: ['物料;SMT;制造工艺'],
    description: '锡膏通过钢网开口转移到PCB焊盘上的能力，包括填充性、脱模性等。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0839',
    name: '模流熔接痕强度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['熔合线强度'],
    tags: ['制造工艺;注塑;结构相关'],
    description: '两股熔体前沿相遇形成的熔接痕区域的力学强度，通常低于本体强度。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0840',
    name: '辐射骚扰场强',
    type: '其他',
    category: 'countermeasures',
    aliases: ['辐射发射'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备通过空间向外辐射的电磁噪声场强，需在暗室中测量并满足法规要求。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0841',
    name: '胶体损耗模量',
    type: '其他',
    category: 'countermeasures',
    aliases: ['粘性模量'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂在交变应力下粘性变形分量对应的模量，反映其粘性耗能行为。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0842',
    name: 'X射线荧光光谱',
    type: '其他',
    category: 'countermeasures',
    aliases: ['XRF'],
    tags: ['测试验证;物料;CMF'],
    description: '利用X射线激发样品元素产生特征荧光，进行成分定性定量分析，用于镀层厚度、材料成分检测。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0843',
    name: '模内冷却速率',
    type: '其他',
    category: 'countermeasures',
    aliases: ['冷却速度'],
    tags: ['工艺参数;注塑;可靠性'],
    description: '塑胶件在模具内的冷却速度，影响结晶度、内应力和最终尺寸。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0844',
    name: '阻抗匹配',
    type: '其他',
    category: 'countermeasures',
    aliases: ['阻抗控制'],
    tags: ['硬件相关;射频相关;PCB'],
    description: '使源端、传输线和负载端的阻抗一致，以实现最大功率传输和最小信号反射。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0845',
    name: '邦定球剪切力',
    type: '其他',
    category: 'countermeasures',
    aliases: ['球剪切强度'],
    tags: ['可靠性;半导体;制造工艺'],
    description: '测量将金球焊点从芯片焊盘上剪切下来所需的力，评估键合界面强度。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0846',
    name: '锡膏金属粉末粒径',
    type: '其他',
    category: 'countermeasures',
    aliases: ['锡粉粒度'],
    tags: ['物料;SMT;制造工艺'],
    description: '锡膏中合金粉末的尺寸大小及分布，影响印刷分辨率、塌陷性和焊接效果。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0847',
    name: '模流保压压力',
    type: '其他',
    category: 'countermeasures',
    aliases: ['二次压力'],
    tags: ['工艺参数;注塑'],
    description: '注射完成后，为了补偿塑料收缩而继续施加的压力，对产品尺寸和缩水至关重要。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0848',
    name: '静电放电抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['ESD Immunity'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备抵御静电放电干扰而不出现性能降级或损坏的能力，需满足IEC 61000-4-2等标准。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0849',
    name: '胶体tanδ',
    type: '其他',
    category: 'countermeasures',
    aliases: ['损耗因子'],
    tags: ['物料;电气性能;点胶'],
    description: '损耗模量与储能模量的比值，表征胶粘剂在交变电场中能量损耗的大小。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0850',
    name: '聚焦离子束',
    type: '其他',
    category: 'countermeasures',
    aliases: ['FIB'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '用聚焦的离子束对样品进行纳米级加工、切割和成像，用于芯片电路修改和截面分析。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0851',
    name: '共模抑制比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['CMRR'],
    tags: ['硬件相关;电气性能;测试验证'],
    description: '衡量差分放大器抑制共模信号（干扰）能力的指标。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0852',
    name: '邦定线线径',
    type: '其他',
    category: 'countermeasures',
    aliases: ['金线直径'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合金线的直径，常见有0.8mil, 1.0mil, 1.2mil等，影响电流承载能力和机械强度。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0853',
    name: '热循环寿命',
    type: '其他',
    category: 'countermeasures',
    aliases: ['温度循环寿命'],
    tags: ['可靠性;测试验证;硬件相关'],
    description: '产品在规定的温度循环条件下，直到失效所能承受的循环次数。',
    created_at: '2025-09-26T09:43:14.283731',
    updated_at: '2025-09-26T09:43:14.283731'
});
CREATE (d:Dictionary {
    id: 'TERM_0854',
    name: '锡膏触变指数',
    type: '其他',
    category: 'countermeasures',
    aliases: ['TI值'],
    tags: ['物料;SMT;制造工艺'],
    description: '锡膏在低剪切速率和高剪切速率下的粘度比值，衡量其触变性的恢复能力。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0855',
    name: '模流翘曲预测',
    type: '其他',
    category: 'countermeasures',
    aliases: ['变形分析'],
    tags: ['设计;制造工艺;注塑'],
    description: '通过CAE软件预测注塑件冷却后的翘曲变形趋势，指导模具和产品设计优化。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0856',
    name: '浪涌抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['雷击测试'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备抵御电网开关瞬变或间接雷击引起的高能量瞬态过电压/过电流的能力。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0857',
    name: '胶体体积变化率',
    type: '其他',
    category: 'countermeasures',
    aliases: ['固化体积收缩'],
    tags: ['物料;制造工艺;点胶'],
    description: '胶水从液态到完全固化后体积变化的百分比，影响内应力和接合精度。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0858',
    name: '红外热成像仪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热像仪'],
    tags: ['测试验证;热管理;可靠性'],
    description: '将物体表面的温度分布转换为可视化的热图，用于定位过热点和分析热分布。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0859',
    name: '模内气体辅助',
    type: '其他',
    category: 'countermeasures',
    aliases: ['气辅注塑'],
    tags: ['工艺参数;注塑;设计'],
    description: '向熔融塑料中注入高压氮气，推动塑料填充并形成中空截面，可减少缩水、节省材料。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0860',
    name: '功率循环测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['主动温度循环'],
    tags: ['可靠性;硬件相关;热管理'],
    description: '通过给器件周期性通断电，使其自身发热和冷却，考核其热疲劳寿命。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0861',
    name: '锡膏印刷厚度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['锡厚'],
    tags: ['制造工艺;SMT;测试验证'],
    description: '锡膏印刷后留在PCB焊盘上的厚度，通常用螺旋测微计或3D光学扫描仪测量。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0862',
    name: '电快速瞬变脉冲群',
    type: '其他',
    category: 'countermeasures',
    aliases: ['EFT/Burst'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '模拟继电器触点抖动等产生的成群快速瞬变脉冲干扰，测试设备的抗扰度。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0863',
    name: '胶体玻璃化转变温度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Tg'],
    tags: ['物料;可靠性;点胶'],
    description: '同前，胶粘剂的玻璃化转变温度。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0864',
    name: '超声波扫描显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['SAT'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用超声波探测材料内部缺陷（如分层、空洞）的无损检测方法。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0865',
    name: '模内微发泡',
    type: '其他',
    category: 'countermeasures',
    aliases: ['微孔发泡'],
    tags: ['工艺参数;注塑;结构相关'],
    description: '通过超临界流体在塑料内部产生微米级气泡，减轻重量、减少翘曲和缩水。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0866',
    name: '电源抑制比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['PSRR'],
    tags: ['硬件相关;电气性能;测试验证'],
    description: '衡量电路（如LDO）抑制电源输入端纹波和噪声传递到输出端的能力。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0867',
    name: '机械疲劳寿命',
    type: '其他',
    category: 'countermeasures',
    aliases: ['疲劳强度'],
    tags: ['结构相关;可靠性;测试验证'],
    description: '材料或结构在交变应力作用下发生疲劳断裂前所能承受的应力循环次数。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0868',
    name: '模流冷却分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['冷却系统分析'],
    tags: ['设计;制造工艺;注塑'],
    description: '模拟模具冷却系统的效率，优化水路布局，缩短周期时间并减少热变形。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0869',
    name: '电压跌落与中断',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电压暂降'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '模拟电网电压短时下降或中断，测试设备功能的抗干扰性和恢复能力。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0870',
    name: '胶体热膨胀系数',
    type: '其他',
    category: 'countermeasures',
    aliases: ['CTE'],
    tags: ['物料;结构相关;可靠性'],
    description: '胶粘剂热膨胀系数，与基材匹配可减少热应力。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0871',
    name: 'X射线检测',
    type: '其他',
    category: 'countermeasures',
    aliases: ['AXI'],
    tags: ['测试验证;SMT;制造工艺'],
    description: '自动X射线检测，用于检查BGA、QFN等隐藏焊点的焊接质量，如短路、开路、空洞。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0872',
    name: '模内变模温技术',
    type: '其他',
    category: 'countermeasures',
    aliases: ['快速热循环'],
    tags: ['工艺参数;注塑;CMF'],
    description: '在注塑前快速加热模具，注射后快速冷却，可消除熔接痕、提升表面光泽度。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0873',
    name: '时序分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['信号时序'],
    tags: ['硬件相关;测试验证;软件相关'],
    description: '确保数字系统中相关信号满足建立时间和保持时间的要求，避免时序违规。',
    created_at: '2025-09-26T09:43:14.284731',
    updated_at: '2025-09-26T09:43:14.284731'
});
CREATE (d:Dictionary {
    id: 'TERM_0874',
    name: '锡膏黏度曲线',
    type: '其他',
    category: 'countermeasures',
    aliases: ['流变曲线'],
    tags: ['物料;SMT;制造工艺'],
    description: '锡膏粘度随剪切速率变化的曲线，全面表征其流变特性。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0875',
    name: '谐波电流发射',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电流谐波'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备从电网吸取的电流中除基波外的谐波成分含量，需符合规范以减小对电网污染。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0876',
    name: '胶体固化动力学',
    type: '其他',
    category: 'countermeasures',
    aliases: ['固化反应速率'],
    tags: ['物料;制造工艺;点胶'],
    description: '研究胶粘剂固化反应速度与温度、时间等条件的关系。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0877',
    name: '声学扫描显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['C-SAM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '同超声波扫描显微镜。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0878',
    name: '抖动',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Jitter'],
    tags: ['硬件相关;测试验证;设计'],
    description: '数字信号边沿相对于其理想时间位置的短期偏移，是高速信号完整性的重要参数。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0879',
    name: '邦定线弧形状',
    type: '其他',
    category: 'countermeasures',
    aliases: ['线弧轮廓'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线从芯片到引脚的弧形轨迹，需优化以实现可靠的电气连接和机械稳定性。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0880',
    name: '电压波动抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['闪烁测试'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备对电网电压波动（如由大功率设备启停引起）的抗干扰能力。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0881',
    name: '光学轮廓仪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['白光干涉仪'],
    tags: ['测试验证;制造工艺;外观'],
    description: '用于非接触式测量表面形貌、粗糙度、台阶高度等三维轮廓信息。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0882',
    name: '模内层压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模内贴膜'],
    tags: ['工艺参数;结构相关;CMF'],
    description: '将装饰性或功能性薄膜在注塑过程中与塑胶件复合。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0883',
    name: '误码率',
    type: '其他',
    category: 'countermeasures',
    aliases: ['BER'],
    tags: ['硬件相关;测试验证;通信相关'],
    description: '在数字传输系统中，错误比特数与总传输比特数之比，衡量传输可靠性。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0884',
    name: '锡膏印刷面积比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['面积比'],
    tags: ['设计;SMT;制造工艺'],
    description: '钢网开口面积与孔壁侧面积的比值，经验上大于0.66有利于锡膏释放。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0885',
    name: '工频磁场抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['磁场抗扰度'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备对50/60Hz电源频率磁场干扰的抵抗能力。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0886',
    name: '激光共聚焦显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['CLSM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用激光扫描和针孔技术，获得样品不同深度的光学切片，实现三维成像。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0887',
    name: '模内传感器',
    type: '其他',
    category: 'countermeasures',
    aliases: ['智能模具'],
    tags: ['制造工艺;注塑;测试验证'],
    description: '集成在模具内用于监测压力、温度、位移等参数的传感器总称。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0888',
    name: '信纳比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['SINAD'],
    tags: ['硬件相关;测试验证;声学'],
    description: '信号+噪声+失真的总功率与噪声+失真的功率之比，衡量音频系统的动态性能。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0889',
    name: '邦定线弧长度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['线弧跨度'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线从第一点到第二点的水平投影距离。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0890',
    name: '红外热成像仪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['热像仪'],
    tags: ['测试验证;热管理;可靠性'],
    description: '将物体表面的温度分布转换为可视化的热图，用于定位过热点和分析热分布。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0891',
    name: '模内气体辅助',
    type: '其他',
    category: 'countermeasures',
    aliases: ['气辅注塑'],
    tags: ['工艺参数;注塑;设计'],
    description: '向熔融塑料中注入高压氮气，推动塑料填充并形成中空截面，可减少缩水、节省材料。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0892',
    name: '功率循环测试',
    type: '其他',
    category: 'countermeasures',
    aliases: ['主动温度循环'],
    tags: ['可靠性;硬件相关;热管理'],
    description: '通过给器件周期性通断电，使其自身发热和冷却，考核其热疲劳寿命。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0893',
    name: '锡膏印刷厚度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['锡厚'],
    tags: ['制造工艺;SMT;测试验证'],
    description: '锡膏印刷后留在PCB焊盘上的厚度，通常用螺旋测微计或3D光学扫描仪测量。',
    created_at: '2025-09-26T09:43:14.285732',
    updated_at: '2025-09-26T09:43:14.285732'
});
CREATE (d:Dictionary {
    id: 'TERM_0894',
    name: '电快速瞬变脉冲群',
    type: '其他',
    category: 'countermeasures',
    aliases: ['EFT/Burst'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '模拟继电器触点抖动等产生的成群快速瞬变脉冲干扰，测试设备的抗扰度。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0895',
    name: '胶体玻璃化转变温度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Tg'],
    tags: ['物料;可靠性;点胶'],
    description: '胶粘剂的玻璃化转变温度。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0896',
    name: '超声波扫描显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['SAT'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用超声波探测材料内部缺陷（如分层、空洞）的无损检测方法。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0897',
    name: '模内微发泡',
    type: '其他',
    category: 'countermeasures',
    aliases: ['微孔发泡'],
    tags: ['工艺参数;注塑;结构相关'],
    description: '通过超临界流体在塑料内部产生微米级气泡，减轻重量、减少翘曲和缩水。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0898',
    name: '电源抑制比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['PSRR'],
    tags: ['硬件相关;电气性能;测试验证'],
    description: '衡量电路（如LDO）抑制电源输入端纹波和噪声传递到输出端的能力。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0899',
    name: '机械疲劳寿命',
    type: '其他',
    category: 'countermeasures',
    aliases: ['疲劳强度'],
    tags: ['结构相关;可靠性;测试验证'],
    description: '材料或结构在交变应力作用下发生疲劳断裂前所能承受的应力循环次数。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0900',
    name: '模流冷却分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['冷却系统分析'],
    tags: ['设计;制造工艺;注塑'],
    description: '模拟模具冷却系统的效率，优化水路布局，缩短周期时间并减少热变形。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0901',
    name: '电压跌落与中断',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电压暂降'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '模拟电网电压短时下降或中断，测试设备功能的抗干扰性和恢复能力。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0902',
    name: '胶体热膨胀系数',
    type: '其他',
    category: 'countermeasures',
    aliases: ['CTE'],
    tags: ['物料;结构相关;可靠性'],
    description: '胶粘剂热膨胀系数，与基材匹配可减少热应力。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0903',
    name: 'X射线检测',
    type: '其他',
    category: 'countermeasures',
    aliases: ['AXI'],
    tags: ['测试验证;SMT;制造工艺'],
    description: '自动X射线检测，用于检查BGA、QFN等隐藏焊点的焊接质量，如短路、开路、空洞。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0904',
    name: '模内变模温技术',
    type: '其他',
    category: 'countermeasures',
    aliases: ['快速热循环'],
    tags: ['工艺参数;注塑;CMF'],
    description: '在注塑前快速加热模具，注射后快速冷却，可消除熔接痕、提升表面光泽度。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0905',
    name: '时序分析',
    type: '其他',
    category: 'countermeasures',
    aliases: ['信号时序'],
    tags: ['硬件相关;测试验证;软件相关'],
    description: '确保数字系统中相关信号满足建立时间和保持时间的要求，避免时序违规。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0906',
    name: '锡膏黏度曲线',
    type: '其他',
    category: 'countermeasures',
    aliases: ['流变曲线'],
    tags: ['物料;SMT;制造工艺'],
    description: '锡膏粘度随剪切速率变化的曲线，全面表征其流变特性。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0907',
    name: '谐波电流发射',
    type: '其他',
    category: 'countermeasures',
    aliases: ['电流谐波'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备从电网吸取的电流中除基波外的谐波成分含量，需符合规范以减小对电网污染。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0908',
    name: '胶体固化动力学',
    type: '其他',
    category: 'countermeasures',
    aliases: ['固化反应速率'],
    tags: ['物料;制造工艺;点胶'],
    description: '研究胶粘剂固化反应速度与温度、时间等条件的关系。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0909',
    name: '声学扫描显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['C-SAM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '同超声波扫描显微镜。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0910',
    name: '抖动',
    type: '其他',
    category: 'countermeasures',
    aliases: ['Jitter'],
    tags: ['硬件相关;测试验证;设计'],
    description: '数字信号边沿相对于其理想时间位置的短期偏移，是高速信号完整性的重要参数。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0911',
    name: '邦定线弧形状',
    type: '其他',
    category: 'countermeasures',
    aliases: ['线弧轮廓'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线从芯片到引脚的弧形轨迹，需优化以实现可靠的电气连接和机械稳定性。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0912',
    name: '电压波动抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['闪烁测试'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备对电网电压波动（如由大功率设备启停引起）的抗干扰能力。',
    created_at: '2025-09-26T09:43:14.286738',
    updated_at: '2025-09-26T09:43:14.286738'
});
CREATE (d:Dictionary {
    id: 'TERM_0913',
    name: '光学轮廓仪',
    type: '其他',
    category: 'countermeasures',
    aliases: ['白光干涉仪'],
    tags: ['测试验证;制造工艺;外观'],
    description: '用于非接触式测量表面形貌、粗糙度、台阶高度等三维轮廓信息。',
    created_at: '2025-09-26T09:43:14.287731',
    updated_at: '2025-09-26T09:43:14.287731'
});
CREATE (d:Dictionary {
    id: 'TERM_0914',
    name: '模内层压',
    type: '其他',
    category: 'countermeasures',
    aliases: ['模内贴膜'],
    tags: ['工艺参数;结构相关;CMF'],
    description: '将装饰性或功能性薄膜在注塑过程中与塑胶件复合。',
    created_at: '2025-09-26T09:43:14.287731',
    updated_at: '2025-09-26T09:43:14.287731'
});
CREATE (d:Dictionary {
    id: 'TERM_0915',
    name: '误码率',
    type: '其他',
    category: 'countermeasures',
    aliases: ['BER'],
    tags: ['硬件相关;测试验证;通信相关'],
    description: '在数字传输系统中，错误比特数与总传输比特数之比，衡量传输可靠性。',
    created_at: '2025-09-26T09:43:14.287731',
    updated_at: '2025-09-26T09:43:14.287731'
});
CREATE (d:Dictionary {
    id: 'TERM_0916',
    name: '锡膏印刷面积比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['面积比'],
    tags: ['设计;SMT;制造工艺'],
    description: '钢网开口面积与孔壁侧面积的比值，经验上大于0.66有利于锡膏释放。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0917',
    name: '工频磁场抗扰度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['磁场抗扰度'],
    tags: ['EMC;可靠性;硬件相关'],
    description: '设备对50/60Hz电源频率磁场干扰的抵抗能力。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0918',
    name: '激光共聚焦显微镜',
    type: '其他',
    category: 'countermeasures',
    aliases: ['CLSM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用激光扫描和针孔技术，获得样品不同深度的光学切片，实现三维成像。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0919',
    name: '模内传感器',
    type: '其他',
    category: 'countermeasures',
    aliases: ['智能模具'],
    tags: ['制造工艺;注塑;测试验证'],
    description: '集成在模具内用于监测压力、温度、位移等参数的传感器总称。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0920',
    name: '信纳比',
    type: '其他',
    category: 'countermeasures',
    aliases: ['SINAD'],
    tags: ['硬件相关;测试验证;声学'],
    description: '信号+噪声+失真的总功率与噪声+失真的功率之比，衡量音频系统的动态性能。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0921',
    name: '邦定线弧长度',
    type: '其他',
    category: 'countermeasures',
    aliases: ['线弧跨度'],
    tags: ['工艺参数;半导体;封装'],
    description: '键合线从第一点到第二点的水平投影距离。',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0922',
    name: '供应链审计',
    type: '流程',
    category: 'countermeasures',
    aliases: ['供应商审核'],
    tags: ['质量体系;供应链;组织职责'],
    description: '对供应商的质量体系生产过程及能力进行的系统性检查与评估',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0923',
    name: '产品数据管理工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['PDM工程师'],
    tags: ['组织职责;项目相关;流程相关'],
    description: '负责管理产品全生命周期数据（BOM图纸规格）的工程师',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0924',
    name: '项目质量经理',
    type: '角色',
    category: 'countermeasures',
    aliases: ['PQM'],
    tags: ['组织职责;质量体系;项目相关'],
    description: '负责特定项目内所有质量活动的策划控制和保证的管理人员',
    created_at: '2025-09-26T09:43:14.287933',
    updated_at: '2025-09-26T09:43:14.287933'
});
CREATE (d:Dictionary {
    id: 'TERM_0925',
    name: '环境健康安全工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['EHS工程师'],
    tags: ['组织职责;法规;流程相关'],
    description: '负责确保工作环境符合健康安全及环保法规的专业人员',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0926',
    name: '金相切片',
    type: '工具',
    category: 'countermeasures',
    aliases: ['交叉切片'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '将样品封装研磨抛光后在显微镜下观察内部结构的制样方法',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0927',
    name: '客户质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['CQE'],
    tags: ['组织职责;质量体系;供应链'],
    description: '作为与客户对接的质量窗口处理客户反馈投诉和审核',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0928',
    name: '高低温循环试验箱',
    type: '工具',
    category: 'countermeasures',
    aliases: ['温循箱'],
    tags: ['测试验证;可靠性;硬件相关'],
    description: '可编程控制温度在高温和低温间循环变化的测试设备',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0929',
    name: '生产质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['PQE'],
    tags: ['组织职责;质量体系;制造工艺'],
    description: '负责解决生产线上的质量问题提升直通率和产品质量',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0930',
    name: '可制造性设计评审',
    type: '流程',
    category: 'countermeasures',
    aliases: ['DFM评审'],
    tags: ['设计;制造工艺;质量体系'],
    description: '在产品设计阶段评估其是否易于高效低成本制造的正式评审流程',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0931',
    name: '阳极氧化',
    type: '流程',
    category: 'countermeasures',
    aliases: ['阳极化'],
    tags: ['制造工艺;CMF;可靠性'],
    description: '通过电解在铝材表面生成致密氧化铝膜用于着色耐腐蚀和耐磨',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0932',
    name: '可靠性测试工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['可靠性工程师'],
    tags: ['组织职责;测试验证;可靠性'],
    description: '负责制定和执行产品可靠性测试方案评估产品寿命和失效模式',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0933',
    name: '来料质量检验员',
    type: '角色',
    category: 'countermeasures',
    aliases: ['IQC检验员'],
    tags: ['组织职责;质量体系;制造工艺'],
    description: '负责对供应商来料进行检验和判定的操作人员',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0934',
    name: '模流分析软件',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Moldflow'],
    tags: ['设计;制造工艺;注塑'],
    description: '用于模拟塑料在模具中流动保压冷却过程的CAE软件',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0935',
    name: '失效分析工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['FA工程师'],
    tags: ['组织职责;可靠性;质量体系'],
    description: '负责对失效品进行根因分析定位故障机理并提出改进措施',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0936',
    name: '化学镀镍金',
    type: '流程',
    category: 'countermeasures',
    aliases: ['ENIG'],
    tags: ['制造工艺;PCB;工艺参数'],
    description: '在PCB焊盘上化学沉积镍层和金层的表面处理工艺',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0937',
    name: '体系质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['体系工程师'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '负责建立维护和改进公司质量管理体系（如ISO9001）',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0938',
    name: '离子色谱仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['IC'],
    tags: ['测试验证;物料;可靠性'],
    description: '用于检测样品中离子型杂质（如卤素硫酸根）的种类和含量',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0939',
    name: '射频微波暗室',
    type: '工具',
    category: 'countermeasures',
    aliases: ['电波暗室'],
    tags: ['测试验证;EMC;射频相关'],
    description: '内部覆盖吸波材料用于天线辐射等测试的电磁屏蔽空间',
    created_at: '2025-09-26T09:43:14.288441',
    updated_at: '2025-09-26T09:43:14.288441'
});
CREATE (d:Dictionary {
    id: 'TERM_0940',
    name: '制程质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['IPQC工程师'],
    tags: ['组织职责;质量体系;制造工艺'],
    description: '负责监控和生产过程质量确保工艺参数稳定和产品符合标准',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0941',
    name: '振动控制器',
    type: '工具',
    category: 'countermeasures',
    aliases: ['振动控制仪'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '用于控制振动试验台按预设谱线进行振动的设备',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0942',
    name: '功耗分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['功率分析仪'],
    tags: ['测试验证;硬件相关;性能指标'],
    description: '精确测量设备电压电流功率能耗等电气参数的仪器',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0943',
    name: '材料合规工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['环保工程师'],
    tags: ['组织职责;法规;供应链'],
    description: '确保产品所用材料符合RoHS REACH等环保法规的专业人员',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0944',
    name: 'X射线荧光光谱仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['XRF'],
    tags: ['测试验证;物料;CMF'],
    description: '用于快速无损分析材料元素成分和镀层厚度的仪器',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0945',
    name: '标准化工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['标准工程师'],
    tags: ['组织职责;设计;流程相关'],
    description: '负责制定和维护企业技术标准设计规范等',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0946',
    name: '邦定球剪切测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['球剪切测试'],
    tags: ['测试验证;可靠性;半导体'],
    description: '测量芯片键合球与焊盘界面强度的破坏性测试方法',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0947',
    name: '超声波焊接',
    type: '流程',
    category: 'countermeasures',
    aliases: ['超声焊'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用高频振动能量使塑料或金属局部熔化实现连接',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0948',
    name: '实验室认可工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['实验室工程师'],
    tags: ['组织职责;测试验证;质量体系'],
    description: '负责实验室管理体系（如CNAS）的建立和维护',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0949',
    name: '红外热像仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['热像仪'],
    tags: ['测试验证;热管理;可靠性'],
    description: '将物体表面温度分布转换为可视化热图的设备',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0950',
    name: '扫描电子显微镜',
    type: '工具',
    category: 'countermeasures',
    aliases: ['SEM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '利用电子束扫描样品表面获得高分辨率形貌图像的设备',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0951',
    name: '质量成本分析师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['质量成本会计'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '负责核算和分析预防鉴定内部和外部失败成本',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0952',
    name: '恒温恒湿试验箱',
    type: '工具',
    category: 'countermeasures',
    aliases: ['温湿箱'],
    tags: ['测试验证;可靠性;硬件相关'],
    description: '可精确控制温度和湿度的环境模拟设备',
    created_at: '2025-09-26T09:43:14.289027',
    updated_at: '2025-09-26T09:43:14.289027'
});
CREATE (d:Dictionary {
    id: 'TERM_0953',
    name: '矢量网络分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['VNA'],
    tags: ['测试验证;射频相关;硬件相关'],
    description: '测量器件网络参数（S参数）的精密仪器',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0954',
    name: '供应商开发工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['SDE'],
    tags: ['组织职责;供应链;质量体系'],
    description: '负责寻找评估和引入新供应商并提升现有供应商能力',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0955',
    name: '微弧氧化',
    type: '流程',
    category: 'countermeasures',
    aliases: ['微弧氧化'],
    tags: ['制造工艺;CMF;可靠性'],
    description: '在铝镁钛等金属表面通过高压放电生成陶瓷化氧化层的技术',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0956',
    name: '计量校准工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['计量工程师'],
    tags: ['组织职责;测试验证;质量体系'],
    description: '负责测量设备的定期校准和量值溯源管理',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0957',
    name: '激光测振仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['LDV'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '利用激光多普勒效应非接触测量物体振动速度和位移的设备',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0958',
    name: '能谱仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['EDS/EDX'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '与SEM联用对样品微区进行元素成分定性定量分析',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0959',
    name: '客户满意度经理',
    type: '角色',
    category: 'countermeasures',
    aliases: ['CSM'],
    tags: ['组织职责;质量体系;项目相关'],
    description: '负责监控和提升客户对产品和服务的满意程度',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0960',
    name: '落球冲击测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['球冲击测试'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '用规定重量的钢球从一定高度自由落体冲击样品表面',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0961',
    name: '等离子体清洗',
    type: '流程',
    category: 'countermeasures',
    aliases: ['等离子清洗'],
    tags: ['制造工艺;表面处理;可靠性'],
    description: '利用等离子体活化材料表面去除有机物污染提高粘接性',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0962',
    name: '质量培训师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['质量培训专员'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '负责策划和实施公司范围内的质量意识工具和流程培训',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0963',
    name: '三坐标测量机',
    type: '工具',
    category: 'countermeasures',
    aliases: ['CMM'],
    tags: ['测试验证;结构相关;制造工艺'],
    description: '用于精密测量工件几何尺寸形状和位置公差的高精度设备',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0964',
    name: '原子力显微镜',
    type: '工具',
    category: 'countermeasures',
    aliases: ['AFM'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '通过探测针尖与样品表面的原子力获得纳米级分辨率的三维形貌',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0965',
    name: '项目质量保证',
    type: '角色',
    category: 'countermeasures',
    aliases: ['PQA'],
    tags: ['组织职责;质量体系;项目相关'],
    description: '在项目团队内独立评估过程合规性确保项目按质量要求执行',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0966',
    name: '插拔力测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['插拔寿命测试'],
    tags: ['测试验证;可靠性;硬件相关'],
    description: '测试连接器反复插拔过程中的插入力和拔出力以及寿命次数',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0967',
    name: '化学气相沉积',
    type: '流程',
    category: 'countermeasures',
    aliases: ['CVD'],
    tags: ['制造工艺;半导体;硬件相关'],
    description: '利用气态先驱物在衬底表面发生化学反应并沉积固态薄膜的技术',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0968',
    name: '质量信息系统专员',
    type: '角色',
    category: 'countermeasures',
    aliases: ['QIS专员'],
    tags: ['组织职责;质量体系;软件相关'],
    description: '负责维护和质量数据统计分析软件系统（如SPC QMS）',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0969',
    name: '光谱分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['OSA'],
    tags: ['测试验证;射频相关;硬件相关'],
    description: '测量光信号功率随波长分布关系的仪器',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0970',
    name: '卓越运营经理',
    type: '角色',
    category: 'countermeasures',
    aliases: ['精益经理'],
    tags: ['组织职责;质量体系;制造工艺'],
    description: '推动精益生产六西格玛等持续改进方法提升运营效率和质量',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0971',
    name: '高温存储测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['高温老化'],
    tags: ['测试验证;可靠性;硬件相关'],
    description: '将产品置于高温环境下长时间存储评估其材料和老化的稳定性',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0972',
    name: '物理气相沉积',
    type: '流程',
    category: 'countermeasures',
    aliases: ['PVD'],
    tags: ['制造工艺;CMF;硬件相关'],
    description: '通过物理方法（蒸发溅射）使材料气化并在工件表面沉积成膜',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0973',
    name: '风险管理工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['风险工程师'],
    tags: ['组织职责;质量体系;项目相关'],
    description: '负责识别分析和管控产品开发过程中的技术和管理风险',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0974',
    name: '白光干涉仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['光学轮廓仪'],
    tags: ['测试验证;制造工艺;外观'],
    description: '用于非接触式测量表面形貌粗糙度台阶高度等三维轮廓',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0975',
    name: '二次离子质谱仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['SIMS'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '用离子束溅射样品表面对溅出二次离子进行质谱分析用于痕量元素和深度剖析',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0976',
    name: '质量审计员',
    type: '角色',
    category: 'countermeasures',
    aliases: ['内审员'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '经培训合格负责执行内部质量管理体系审核的人员',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0977',
    name: '弯曲测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['弯折测试'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '对FPC连接线等柔性部件进行反复弯折考核其耐疲劳性',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0978',
    name: '激光焊接',
    type: '流程',
    category: 'countermeasures',
    aliases: ['激光焊'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用高能量密度激光束作为热源进行精密焊接的方法',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0979',
    name: '变更控制委员会',
    type: '角色',
    category: 'countermeasures',
    aliases: ['CCB'],
    tags: ['组织职责;项目相关;流程相关'],
    description: '负责评估和批准产品设计工艺等重要变更的跨部门团队',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0980',
    name: '热阻测试仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['热阻测量系统'],
    tags: ['测试验证;热管理;可靠性'],
    description: '用于测量器件结到环境或结到外壳热阻的专用设备',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0981',
    name: 'X射线衍射仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['XRD'],
    tags: ['测试验证;物料;可靠性'],
    description: '用于分析材料的晶体结构物相组成结晶度等',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0982',
    name: '质量目标管理专员',
    type: '角色',
    category: 'countermeasures',
    aliases: ['质量KPI专员'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '负责制定跟踪和分析公司及部门级质量关键绩效指标',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0983',
    name: '砂尘测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['防尘测试'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '模拟沙尘环境测试产品外壳的防尘能力（IP5X）',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0984',
    name: '选择性焊接',
    type: '流程',
    category: 'countermeasures',
    aliases: ['选择焊'],
    tags: ['制造工艺;PCB;工艺参数'],
    description: '仅对PCB上特定通孔元件进行焊接避免热敏感SMD元件受热',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0985',
    name: '新产品导入质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['NPI QE'],
    tags: ['组织职责;质量体系;项目相关'],
    description: '负责在新产品从研发转向量产阶段的质量策划和验证',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0986',
    name: '泄漏测试仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['检漏仪'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '用于检测产品气密性的设备如压降法氦质谱检漏仪',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0987',
    name: '俄歇电子能谱仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['AES'],
    tags: ['测试验证;可靠性;失效分析'],
    description: '用于表面1-3nm层元素的定性定量和化学状态分析',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0988',
    name: '质量改进小组组长',
    type: '角色',
    category: 'countermeasures',
    aliases: ['QIT Leader'],
    tags: ['组织职责;质量体系;制造工艺'],
    description: '领导跨职能团队针对特定质量问题进行根本原因分析和改进',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0989',
    name: '机械冲击测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['冲击测试'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '模拟产品在运输或使用中受到的剧烈冲击考核结构坚固性',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0990',
    name: '卷对卷加工',
    type: '流程',
    category: 'countermeasures',
    aliases: ['R2R'],
    tags: ['制造工艺;FPC;物料'],
    description: '基材以卷筒形式连续进行多个工序（如曝光蚀刻镀铜）的生产方式',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0991',
    name: '客户投诉处理专员',
    type: '角色',
    category: 'countermeasures',
    aliases: ['客诉专员'],
    tags: ['组织职责;质量体系;供应链'],
    description: '负责接收记录初步分析和跟踪客户投诉的处理进程',
    created_at: '2025-09-26T09:43:14.289537',
    updated_at: '2025-09-26T09:43:14.289537'
});
CREATE (d:Dictionary {
    id: 'TERM_0992',
    name: '绝缘耐压测试仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['耐压测试仪'],
    tags: ['测试验证;安全相关;硬件相关'],
    description: '施加高电压测试产品的绝缘强度是否满足安全规范',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0993',
    name: '动态力学分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['DMA'],
    tags: ['测试验证;物料;可靠性'],
    description: '测量材料在不同温度频率下的动态模量和损耗因子研究粘弹行为',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0994',
    name: '质量成本管理经理',
    type: '角色',
    category: 'countermeasures',
    aliases: ['质量成本经理'],
    tags: ['组织职责;质量体系;流程相关'],
    description: '负责全面策划核算分析和优化质量成本',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0995',
    name: '防水测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['浸水测试'],
    tags: ['测试验证;可靠性;结构相关'],
    description: '将产品浸入规定深度水中一定时间测试其防水等级（IPX7/IPX8）',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0996',
    name: '激光修调',
    type: '流程',
    category: 'countermeasures',
    aliases: ['激光调阻'],
    tags: ['制造工艺;硬件相关;工艺参数'],
    description: '使用激光精确切割调整厚膜或薄膜电阻的阻值',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0997',
    name: '供应商质量改进工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['SQI工程师'],
    tags: ['组织职责;质量体系;供应链'],
    description: '常驻或频繁访问供应商协助其进行质量问题的根本原因分析和持续改进',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0998',
    name: '伽马校正',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Gamma Calibration'],
    tags: ['显示相关;测试验证;制造工艺'],
    description: '调整显示屏的灰阶输出特性使显示亮度与输入信号呈准确的幂函数关系',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_0999',
    name: '色准调试',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Color Calibration'],
    tags: ['显示相关;测试验证;影像相关'],
    description: '调整显示屏色域白平衡等参数使其色彩显示符合标准',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1000',
    name: '亮度均匀性测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Luminance Uniformity Test'],
    tags: ['显示相关;测试验证;性能指标'],
    description: '测量屏幕不同区域的亮度计算均匀性的测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1001',
    name: '色度均匀性测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Chromaticity Uniformity Test'],
    tags: ['显示相关;测试验证;性能指标'],
    description: '测量屏幕不同区域的色坐标偏差的测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1002',
    name: '分光色度计',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Spectrophotometer'],
    tags: ['显示相关;测试验证;影像相关'],
    description: '精确测量屏幕亮度色度等光学参数的仪器',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1003',
    name: '显示测试信号发生器',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Pattern Generator'],
    tags: ['显示相关;测试验证'],
    description: '产生各种标准测试画面（如纯色灰阶棋盘格）的设备',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1004',
    name: '自动光学检测设备',
    type: '工具',
    category: 'countermeasures',
    aliases: ['AOI for Display'],
    tags: ['显示相关;测试验证;制造工艺'],
    description: '用相机自动检测显示屏外观缺陷（Mura坏点等）的设备',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1005',
    name: '显示模块工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Display Module Engineer'],
    tags: ['显示相关;设计;硬件相关'],
    description: '负责显示屏选型光学调试可靠性验证及与整机的匹配',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1006',
    name: '主动对齐',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Active Alignment'],
    tags: ['影像相关;制造工艺;摄像头模组'],
    description: '在通电状态下调整传感器与镜头的相对位置以达到最佳光学性能的组装工艺',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1007',
    name: '标定',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Calibration'],
    tags: ['影像相关;测试验证;制造工艺'],
    description: '对摄像头模块进行参数校正如shading correction AF calibration',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1008',
    name: '调制传递函数测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['MTF Test'],
    tags: ['影像相关;测试验证;性能指标'],
    description: '评价镜头成像分辨率和对比度还原能力的核心光学测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1009',
    name: '色彩还原测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Color Reproduction Test'],
    tags: ['影像相关;测试验证;性能指标'],
    description: '评估摄像头在不同光源下还原被摄物颜色的准确性',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1010',
    name: '影像质量测试卡',
    type: '工具',
    category: 'countermeasures',
    aliases: ['IQ Test Chart'],
    tags: ['影像相关;测试验证'],
    description: '如ISO12233分辨率测试卡24色卡等测试图卡',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1011',
    name: '积分球',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Integrating Sphere'],
    tags: ['影像相关;测试验证'],
    description: '提供均匀稳定的面光源用于摄像头均匀性色差等测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1012',
    name: '影像实验室',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Image Quality Lab'],
    tags: ['影像相关;测试验证;组织职责'],
    description: '配备暗室光源测试设备和软件的专门测试场地',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1013',
    name: '影像质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Image Quality Engineer'],
    tags: ['影像相关;测试验证;设计'],
    description: '负责制定摄像头评测标准进行主观和客观的影像质量评估与调试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1014',
    name: '快充协议',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Quick Charge Protocol'],
    tags: ['硬件相关;充电;软件相关'],
    description: '如QC PD用于协商提高充电功率的通信协议',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1015',
    name: '化成',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Formation'],
    tags: ['制造工艺;电池'],
    description: '电池激活后的首次充放电使其形成稳定的SEI膜的工艺',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1016',
    name: '老化测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Aging Test'],
    tags: ['可靠性;电池;测试验证'],
    description: '模拟电池长期使用后的性能衰减的测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1017',
    name: '针刺测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Nail Penetration Test'],
    tags: ['安全相关;电池;测试验证'],
    description: '模拟电池内部短路检验其安全性能的测试',
    created_at: '2025-09-26T09:43:14.291062',
    updated_at: '2025-09-26T09:43:14.291062'
});
CREATE (d:Dictionary {
    id: 'TERM_1018',
    name: '热滥用测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Thermal Abuse Test'],
    tags: ['安全相关;电池;测试验证'],
    description: '将电池置于高温环境中检验其热稳定性的测试',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1019',
    name: '电池测试系统',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Battery Test System'],
    tags: ['测试验证;电池;硬件相关'],
    description: '可编程充放电设备用于测试电池性能',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1020',
    name: '绝热量热仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Accelerating Rate Calorimeter'],
    tags: ['测试验证;安全相关;电池'],
    description: '测量电池在绝热条件下发生热失控时的放热特性的仪器',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1021',
    name: '电池安全工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Battery Safety Engineer'],
    tags: ['安全相关;硬件相关;可靠性'],
    description: '负责电池安全设计风险评估和失效分析的工程师',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1022',
    name: '表面贴装技术',
    type: '流程',
    category: 'countermeasures',
    aliases: ['SMT'],
    tags: ['制造工艺;SMT;硬件相关'],
    description: '将元件贴装到PCB表面的工艺技术',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1023',
    name: '在线测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['ICT'],
    tags: ['测试验证;硬件相关;制造工艺'],
    description: '通过针床对组装好的PCB进行自动化电气性能测试',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1024',
    name: '功能测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['FCT'],
    tags: ['测试验证;硬件相关;软件相关'],
    description: '模拟整机工作条件测试产品各项功能是否正常',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1025',
    name: '示波器',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Oscilloscope'],
    tags: ['测试验证;电气性能;工具'],
    description: '观察电信号波形随时间变化的仪器',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1026',
    name: '矢量网络分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['VNA'],
    tags: ['测试验证;射频相关;工具'],
    description: '测量射频元器件和电路网络参数的精密仪器',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1027',
    name: '硬件测试工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Hardware Test Engineer'],
    tags: ['测试验证;硬件相关;组织职责'],
    description: '负责制定硬件测试方案执行测试并分析问题的工程师',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1028',
    name: 'PCB布局工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['PCB Layout Engineer'],
    tags: ['设计;硬件相关;组织职责'],
    description: '负责根据原理图进行PCB的元器件布局和走线设计的工程师',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1029',
    name: '天线阻抗匹配',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Antenna Impedance Matching'],
    tags: ['射频相关;设计;测试验证'],
    description: '通过调整匹配电路使天线阻抗与射频前端输出阻抗共轭匹配实现最大功率传输',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1030',
    name: '射频校准',
    type: '流程',
    category: 'countermeasures',
    aliases: ['RF Calibration'],
    tags: ['射频相关;制造工艺;测试验证'],
    description: '在生产线末端对每个手机的发射功率接收增益等射频参数进行校准使其符合标准',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1031',
    name: '综测仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Comprehensive Tester'],
    tags: ['射频相关;测试验证;工具'],
    description: '如Keysight安立公司的仪器可模拟基站进行全面的射频和协议一致性测试',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1032',
    name: '网络分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['VNA'],
    tags: ['射频相关;测试验证;工具'],
    description: '用于测量天线滤波器等无源器件的S参数如回波损耗S11插入损耗S21',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1033',
    name: '微波暗室',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Anechoic Chamber'],
    tags: ['射频相关;测试验证;工具'],
    description: '内部覆盖吸波材料模拟自由空间环境用于测量天线的辐射性能方向图效率等',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1034',
    name: '传导测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Conducted Test'],
    tags: ['射频相关;测试验证;通信相关'],
    description: '通过射频电缆直接连接手机主板和测试仪器排除天线影响测试射频电路的性能',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1035',
    name: 'OTA测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Over-the-Air Test'],
    tags: ['射频相关;测试验证;通信相关'],
    description: '在微波暗室中通过空中接口无线测试整机的辐射功率和接收灵敏度TRP/TIS',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1036',
    name: '射频工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['RF Engineer'],
    tags: ['射频相关;设计;硬件相关'],
    description: '负责射频电路和天线的设计仿真调试和性能优化',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1037',
    name: '天线工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Antenna Engineer'],
    tags: ['射频相关;设计;硬件相关'],
    description: '专注于天线的设计仿真调试以及与整机结构的协同设计',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1038',
    name: '音频调试',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Audio Tuning'],
    tags: ['声学;测试验证;制造工艺'],
    description: '通过软件参数调整扬声器受话器麦克风的EQ增益限幅器等优化音质和响度',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1039',
    name: '声学密封测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Acoustic Seal Test'],
    tags: ['声学;测试验证;可靠性'],
    description: '检测扬声器BOX或麦克风声腔的密封性是否良好',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1040',
    name: '人工嘴',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Artificial Mouth'],
    tags: ['声学;测试验证;工具'],
    description: '用于播放标准测试信号模拟人嘴说话测试麦克风性能',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1041',
    name: '人工耳',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Artificial Ear'],
    tags: ['声学;测试验证;工具'],
    description: '模拟人耳的声学特性用于测量受话器或扬声器在耳道入口处产生的声压',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1042',
    name: '声学分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Audio Analyzer'],
    tags: ['声学;测试验证;工具'],
    description: '如APx系列用于进行高精度的音频参数测量和分析',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1043',
    name: '消声室',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Anechoic Chamber'],
    tags: ['声学;测试验证;工具'],
    description: '房间内壁铺设吸声材料模拟自由声场环境用于精确测量声源的辐射特性',
    created_at: '2025-09-26T09:43:14.292072',
    updated_at: '2025-09-26T09:43:14.292072'
});
CREATE (d:Dictionary {
    id: 'TERM_1044',
    name: '声学工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Acoustic Engineer'],
    tags: ['声学;设计;硬件相关'],
    description: '负责声学器件的选型声学结构设计音质主观客观评价和调试',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1045',
    name: '点胶方案',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Underfill;Potting'],
    tags: ['结构相关;制造工艺;可靠性'],
    description: '在芯片底部或关键部件周围点胶增强机械强度和可靠性',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1046',
    name: '跌落测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Drop Test'],
    tags: ['结构相关;测试验证;可靠性'],
    description: '模拟日常跌落场景验证整机结构强度屏幕抗摔能力',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1047',
    name: '钢球冲击测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Ball Drop Test'],
    tags: ['结构相关;测试验证;可靠性'],
    description: '用特定重量的钢球从一定高度冲击盖板玻璃测试其抗冲击强度',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1048',
    name: '扭压测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Twist and Bend Test'],
    tags: ['结构相关;测试验证;可靠性'],
    description: '对手机进行扭曲和弯曲测试结构抗变形能力',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1049',
    name: '按键寿命测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Key Life Test'],
    tags: ['结构相关;测试验证;可靠性'],
    description: '模拟用户长时间使用测试侧键的按压寿命',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1050',
    name: '连接器插拔力测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Connector Insertion/Extraction Force Test'],
    tags: ['结构相关;测试验证;可靠性'],
    description: '测试连接器的插入力和拔出力以及反复插拔后的性能变化',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1051',
    name: '结构强度仿真',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Structural Simulation'],
    tags: ['结构相关;设计;工具'],
    description: '通过CAE软件如Abaqus模拟手机在跌落静压等工况下的应力分布',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1052',
    name: '模具工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Mold Engineer'],
    tags: ['结构相关;制造工艺;组织职责'],
    description: '负责结构件注塑模具的设计开发和维护',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1053',
    name: '结构工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Mechanical Engineer'],
    tags: ['结构相关;设计;组织职责'],
    description: '负责手机整机结构零部件结构设计以及强度和可靠性验证',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1054',
    name: '热仿真分析',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Thermal Simulation'],
    tags: ['热管理;设计;工具'],
    description: '通过CFD软件如FloTHERM Icepak模拟手机在不同工况下的温度场和气流场',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1055',
    name: '红外热像仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Thermal Imager;IR Camera'],
    tags: ['热管理;测试验证;工具'],
    description: '非接触式测量手机表面温度分布直观定位热点',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1056',
    name: '热电偶',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Thermocouple'],
    tags: ['热管理;测试验证;工具'],
    description: '接触式温度传感器用于精确测量芯片封装表面等特定点的温度',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1057',
    name: '热测试基台',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Thermal Test Chamber'],
    tags: ['热管理;测试验证;工具'],
    description: '可控制环境温度用于测试手机在高温下的散热性能',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1058',
    name: '稳态温度测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Steady-state Temperature Test'],
    tags: ['热管理;测试验证;可靠性'],
    description: '让手机长时间运行高负载任务直至温度达到稳定记录最终温度',
    created_at: '2025-09-26T09:43:14.293070',
    updated_at: '2025-09-26T09:43:14.293070'
});
CREATE (d:Dictionary {
    id: 'TERM_1059',
    name: '瞬态温度测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Transient Temperature Test'],
    tags: ['热管理;测试验证;可靠性'],
    description: '测试手机在突然加载高负载任务时温度随时间上升的曲线',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1060',
    name: '散热工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Thermal Engineer'],
    tags: ['热管理;设计;组织职责'],
    description: '负责手机散热方案的选型设计仿真验证和测试优化',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1061',
    name: '传感器校准',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Sensor Calibration'],
    tags: ['传感器;制造工艺;测试验证'],
    description: '在产线末端对传感器的零点灵敏度交叉轴误差等进行标定确保数据准确',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1062',
    name: '传感器融合',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Sensor Fusion'],
    tags: ['传感器;软件相关;算法'],
    description: '将多个传感器如加速度计陀螺仪磁力计的数据进行算法融合得到更精确的姿态信息',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1063',
    name: '传感器功能测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Sensor Functional Test'],
    tags: ['传感器;测试验证;功能'],
    description: '验证各传感器基本功能是否正常如摇动手机触发相应动作',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1064',
    name: '精度验证测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Accuracy Verification Test'],
    tags: ['传感器;测试验证;性能指标'],
    description: '在受控条件下将传感器读数与更高精度的标准器进行比对',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1065',
    name: '稳定性测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Stability Test'],
    tags: ['传感器;测试验证;可靠性'],
    description: '长时间运行传感器观察其输出数据的稳定性',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1066',
    name: '转台',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Turntable'],
    tags: ['传感器;测试验证;工具'],
    description: '用于精确控制手机旋转角度和速率校准和测试陀螺仪加速度计等',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1067',
    name: '磁屏蔽箱',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Magnetic Shield Box'],
    tags: ['传感器;测试验证;工具'],
    description: '提供无磁或已知磁场的环境用于磁力计的校准和测试',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1068',
    name: '标准光源箱',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Standard Light Booth'],
    tags: ['传感器;测试验证;工具'],
    description: '提供标准色温和照度的光源用于环境光传感器和色温传感器的测试',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1069',
    name: '传感器测试工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Sensor Test Engineer'],
    tags: ['传感器;测试验证;组织职责'],
    description: '负责传感器测试方案的制定自动化测试开发和数据分析',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1070',
    name: '传感器算法工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Sensor Algorithm Engineer'],
    tags: ['传感器;软件相关;算法'],
    description: '负责传感器数据的滤波融合姿态解算等算法的开发和优化',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1071',
    name: '充电协议握手',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Handshake'],
    tags: ['充电;软件相关;硬件相关'],
    description: '手机与充电器通过通信如USB PD QC协商双方支持的电压和电流档位',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1072',
    name: '恒流充电',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Constant Current Charging'],
    tags: ['充电;性能指标'],
    description: '充电电流保持恒定电池电压逐渐上升的阶段',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1073',
    name: '恒压充电',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Constant Voltage Charging'],
    tags: ['充电;性能指标'],
    description: '电池电压达到设定值后充电电压保持恒定电流逐渐减小的阶段',
    created_at: '2025-09-26T09:43:14.294079',
    updated_at: '2025-09-26T09:43:14.294079'
});
CREATE (d:Dictionary {
    id: 'TERM_1074',
    name: '涓流充电',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Trickle Charging'],
    tags: ['充电;性能指标'],
    description: '电池电量极低时先以小电流预充激活电池',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1075',
    name: '充电效率测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Charging Efficiency Test'],
    tags: ['充电;测试验证;性能指标'],
    description: '测量输入手机的电能与充入电池的电能之比计算整体效率',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1076',
    name: '温升测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Temperature Rise Test'],
    tags: ['充电;测试验证;热管理;安全相关'],
    description: '在特定环境温度下进行快充监测手机和充电器关键点的温升曲线',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1077',
    name: '兼容性测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Compatibility Test'],
    tags: ['充电;测试验证;功能'],
    description: '使用不同品牌不同协议的充电器和线缆测试手机能否正常快充',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1078',
    name: '直流电源',
    type: '工具',
    category: 'countermeasures',
    aliases: ['DC Power Supply'],
    tags: ['充电;测试验证;工具'],
    description: '可编程精密电源用于模拟充电器精确控制输出电压和电流',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1079',
    name: '功率分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Power Analyzer'],
    tags: ['充电;测试验证;工具'],
    description: '高精度测量充电过程中的电压电流功率能耗等参数',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1080',
    name: '热成像仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Thermal Imager'],
    tags: ['充电;测试验证;热管理;工具'],
    description: '观察充电时手机内部和充电器的温度分布定位热点',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1081',
    name: '充电系统工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Charging System Engineer'],
    tags: ['充电;设计;硬件相关'],
    description: '负责手机充电架构设计器件选型性能优化和安全性评估',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1082',
    name: '触觉反馈波形',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Haptic Waveform'],
    tags: ['软件相关;人机交互;功能'],
    description: '驱动马达的特定电压-时间曲线决定振动的强度节奏和质感',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1083',
    name: '波形编辑',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Waveform Editing'],
    tags: ['软件相关;人机交互;功能'],
    description: '设计和调试触觉反馈波形以匹配不同的UI交互场景',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1084',
    name: '振动加速度测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Vibration Acceleration Test'],
    tags: ['测试验证;性能指标;人机交互'],
    description: '使用加速度传感器测量马达在特定驱动下的振动加速度G值',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1085',
    name: '启停时间测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Rise/Fall Time Test'],
    tags: ['测试验证;性能指标;人机交互'],
    description: '测量马达从静止达到稳定振幅启动时间和从稳定振幅回到静止停止时间的快慢',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1086',
    name: '音频-触觉同步测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Audio-Haptic Synchronization Test'],
    tags: ['测试验证;性能指标;人机交互'],
    description: '验证游戏或媒体播放中声音效果与触觉反馈是否精准同步',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1087',
    name: '激光测振仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Laser Doppler Vibrometer'],
    tags: ['测试验证;工具'],
    description: '非接触式精确测量物体表面振动速度和位移的设备',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1088',
    name: '加速度传感器',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Accelerometer'],
    tags: ['测试验证;工具'],
    description: '用于接触式测量振动加速度',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1089',
    name: '触觉体验评估师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Haptic UX Evaluator'],
    tags: ['人机交互;组织职责'],
    description: '从用户角度主观评价不同场景下触觉反馈的舒适度和契合度',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1090',
    name: '马达工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Motor Engineer'],
    tags: ['硬件相关;设计;组织职责'],
    description: '负责马达的选型驱动电路设计结构匹配和性能调试',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1091',
    name: 'NCVM不导电真空镀',
    type: '流程',
    category: 'countermeasures',
    aliases: ['非导电真空镀'],
    tags: ['CMF;制造工艺;外观'],
    description: '一种PVD工艺镀膜层不连续不影响内部天线信号传输同时实现金属质感',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1092',
    name: 'IML模内注塑装饰',
    type: '流程',
    category: 'countermeasures',
    aliases: ['模内贴标'],
    tags: ['CMF;制造工艺;结构相关'],
    description: '将印刷好的薄膜放入模具内注塑时与塑胶件结合图案耐磨且具有立体感',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1093',
    name: '高压成型',
    type: '流程',
    category: 'countermeasures',
    aliases: ['High Pressure Forming'],
    tags: ['制造工艺;结构相关'],
    description: '将平面薄膜通过加热加压使其在模具内成型为3D形状用于复杂曲面装饰',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1094',
    name: '耐磨测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Abrasion Resistance Test'],
    tags: ['测试验证;可靠性;外观'],
    description: '使用特定磨料和压力对表面进行摩擦评估其抗刮擦能力如钢丝绒磨擦',
    created_at: '2025-09-26T09:43:14.295080',
    updated_at: '2025-09-26T09:43:14.295080'
});
CREATE (d:Dictionary {
    id: 'TERM_1095',
    name: '附着力测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Adhesion Test'],
    tags: ['测试验证;可靠性;外观'],
    description: '评估涂层与基材结合强度如百格测试胶带拉拔测试',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1096',
    name: '耐汗液测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Perspiration Resistance Test'],
    tags: ['测试验证;可靠性;外观'],
    description: '模拟汗液腐蚀测试涂层耐化学腐蚀性和颜色稳定性',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1097',
    name: '色差仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Colorimeter'],
    tags: ['CMF;测试验证;工具'],
    description: '测量样品颜色坐标的仪器',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1098',
    name: '光泽度计',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Glossmeter'],
    tags: ['CMF;测试验证;工具'],
    description: '测量表面光泽度的仪器',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1099',
    name: '表面轮廓仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Profilometer'],
    tags: ['CMF;测试验证;工具'],
    description: '接触式或非接触式测量表面粗糙度和轮廓形状',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1100',
    name: 'CMF设计师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['CMF Designer'],
    tags: ['CMF;设计;组织职责'],
    description: '负责手机的颜色材质和表面处理工艺的设计与策划',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1101',
    name: '外观质量工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Appearance Quality Engineer'],
    tags: ['外观;质量体系;组织职责'],
    description: '负责制定外观检验标准监控和提升产品外观质量',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1102',
    name: '协议一致性测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Protocol Conformance Test'],
    tags: ['通信相关;测试验证;法规'],
    description: '验证设备的通信协议栈是否符合3GPP等标准组织的规定',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1103',
    name: '网络模拟测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Network Emulation Test'],
    tags: ['通信相关;测试验证;性能指标'],
    description: '使用网络模拟器模拟各种真实网络条件如弱信号高速移动测试设备性能',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1104',
    name: '吞吐量测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Throughput Test'],
    tags: ['通信相关;测试验证;性能指标'],
    description: '测量设备在特定网络条件下的最大上行/下行数据传输速率',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1105',
    name: 'OTA性能测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Over-the-Air Performance Test'],
    tags: ['通信相关;测试验证;射频相关'],
    description: '在微波暗室中测试天线系统的总辐射功率和总全向灵敏度',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1106',
    name: '网络模拟器',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Network Emulator'],
    tags: ['通信相关;测试验证;工具'],
    description: '如Keysight/罗德与施瓦茨的设备可模拟完整的蜂窝网络或Wi-Fi接入点',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1107',
    name: '协议分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Protocol Analyzer'],
    tags: ['通信相关;测试验证;工具'],
    description: '捕获和分析空中接口的信令消息用于深度调试',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1108',
    name: '频谱分析仪',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Spectrum Analyzer'],
    tags: ['通信相关;测试验证;射频相关;工具'],
    description: '测量射频信号的频谱分布用于分析信号质量和干扰',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1109',
    name: '射频测试工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['RF Test Engineer'],
    tags: ['通信相关;测试验证;组织职责'],
    description: '负责无线通信产品的射频性能测试验证和故障分析',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1110',
    name: '协议栈工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Protocol Stack Engineer'],
    tags: ['通信相关;软件相关;组织职责'],
    description: '负责蜂窝或Wi-Fi/蓝牙协议栈的开发集成和优化',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1111',
    name: '连接器耐焊接热测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Solder Heat Resistance Test'],
    tags: ['硬件相关;测试验证;制造工艺'],
    description: '验证连接器本体和端子能否承受回流焊的高温而不变形或性能劣化',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1112',
    name: '连接器保持力测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Retention Force Test'],
    tags: ['硬件相关;测试验证;可靠性'],
    description: '测试FPC或线缆插入连接器后抵抗外力拔出的能力',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1113',
    name: '连接器插拔寿命测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Durability Test'],
    tags: ['硬件相关;测试验证;可靠性'],
    description: '模拟用户多次插拔测试连接器机械寿命和电性能稳定性',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1114',
    name: '连接器选型工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Connector Selection Engineer'],
    tags: ['硬件相关;设计;供应链'],
    description: '负责根据电气机械成本和供应链需求选择合适的连接器',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1115',
    name: '信号完整性工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Signal Integrity Engineer'],
    tags: ['硬件相关;设计;电气性能'],
    description: '负责高速接口如USB 3.0 MIPI的SI仿真和设计确保信号质量',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1116',
    name: '高加速寿命测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['HALT'],
    tags: ['硬件相关;测试验证;可靠性'],
    description: '通过施加高强度的综合应力热振动快速激发产品潜在缺陷',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1117',
    name: '电容纹波电流测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Ripple Current Test'],
    tags: ['硬件相关;测试验证;可靠性'],
    description: '测试电容在额定纹波电流下的温升和寿命',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1118',
    name: 'ESD抗扰度测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['ESD Immunity Test'],
    tags: ['硬件相关;测试验证;安全相关;ESD'],
    description: '依据IEC 61000-4-2标准对设备施加不同等级的静电放电检验其抗干扰能力',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1119',
    name: '浪涌抗扰度测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['Surge Immunity Test'],
    tags: ['硬件相关;测试验证;安全相关'],
    description: '模拟雷击或大功率设备开关引起的瞬态过压/过流',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1120',
    name: 'LCR meter',
    type: '工具',
    category: 'countermeasures',
    aliases: ['电感电容电阻测试仪'],
    tags: ['硬件相关;测试验证;工具'],
    description: '用于精确测量被动元件的参数L C R D Q',
    created_at: '2025-09-26T09:43:14.296083',
    updated_at: '2025-09-26T09:43:14.296083'
});
CREATE (d:Dictionary {
    id: 'TERM_1121',
    name: '被动元件失效分析工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Passive Component FA Engineer'],
    tags: ['硬件相关;可靠性;组织职责'],
    description: '负责对失效的电容电阻电感等进行根因分析',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1122',
    name: '电路保护设计工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Circuit Protection Design Engineer'],
    tags: ['硬件相关;设计;安全相关'],
    description: '负责针对过压过流浪涌ESD等设计保护电路并选型器件',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1123',
    name: '气动压合',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Pneumatic Pressing'],
    tags: ['制造工艺;测试验证;自动化'],
    description: '使用气缸控制治具的合模力和行程确保接触稳定且不损伤产品',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1124',
    name: '治具设计工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Fixture Design Engineer'],
    tags: ['制造工艺;设计;组织职责'],
    description: '负责根据产品设计和测试需求设计测试治具的机械结构和电路',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1125',
    name: '测试工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['Test Engineer'],
    tags: ['制造工艺;测试验证;组织职责'],
    description: '负责制定测试方案开发测试程序优化测试流程和数据分析',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1126',
    name: '微弧氧化',
    type: '流程',
    category: 'countermeasures',
    aliases: ['等离子体电解氧化'],
    tags: ['制造工艺;CMF;可靠性'],
    description: '在铝镁钛等阀金属表面通过高压放电生成陶瓷化氧化层',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1127',
    name: '原子层沉积',
    type: '流程',
    category: 'countermeasures',
    aliases: ['ALD'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '通过交替通入前驱体在基底表面逐层生长薄膜的技术',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1128',
    name: '化学机械抛光',
    type: '流程',
    category: 'countermeasures',
    aliases: ['CMP'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '通过化学腐蚀和机械研磨实现全局平坦化的工艺',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1129',
    name: '深反应离子刻蚀',
    type: '流程',
    category: 'countermeasures',
    aliases: ['DRIE'],
    tags: ['制造工艺;半导体;MEMS'],
    description: '能够实现高深宽比侧壁陡直的三维微结构加工',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1130',
    name: '晶圆级封装',
    type: '流程',
    category: 'countermeasures',
    aliases: ['WLP'],
    tags: ['制造工艺;半导体;封装'],
    description: '在晶圆上完成芯片封装的大部分工序然后切割成单个器件',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1131',
    name: '系统级封装',
    type: '流程',
    category: 'countermeasures',
    aliases: ['SiP'],
    tags: ['制造工艺;半导体;封装'],
    description: '将多个不同功能的芯片和无源器件集成在一个封装内',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1132',
    name: '扇出型封装',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Fan-Out'],
    tags: ['制造工艺;半导体;封装'],
    description: '芯片I/O端口通过再布线层引到芯片外部区域实现更高集成度',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1133',
    name: '微机电系统',
    type: '流程',
    category: 'countermeasures',
    aliases: ['MEMS'],
    tags: ['制造工艺;传感器;硬件相关'],
    description: '利用微加工技术制造微型传感器执行器等器件',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1134',
    name: '纳米压印',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Nanoimprint Lithography'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '通过机械模具复形实现纳米级图形转移的技术',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1135',
    name: '激光退火',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Laser Annealing'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '利用激光瞬间高温完成半导体材料的退火处理',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1136',
    name: '选择性激光熔化',
    type: '流程',
    category: 'countermeasures',
    aliases: ['SLM'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '3D打印技术的一种通过激光完全熔化金属粉末逐层成型',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1137',
    name: '电子束蒸发',
    type: '流程',
    category: 'countermeasures',
    aliases: ['E-Beam Evaporation'],
    tags: ['制造工艺;半导体;可靠性'],
    description: '利用电子束轰击加热蒸发材料在基底上沉积薄膜',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1138',
    name: '磁控溅射',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Magnetron Sputtering'],
    tags: ['制造工艺;CMF;可靠性'],
    description: '利用磁场约束提高等离子体密度实现高速率高质量薄膜沉积',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1139',
    name: '电化学沉积',
    type: '流程',
    category: 'countermeasures',
    aliases: ['电镀'],
    tags: ['制造工艺;PCB;可靠性'],
    description: '通过电解原理在导体表面沉积金属镀层',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1140',
    name: '化学镀',
    type: '流程',
    category: 'countermeasures',
    aliases: ['无电镀'],
    tags: ['制造工艺;PCB;可靠性'],
    description: '通过自催化化学反应在材料表面沉积金属镀层',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1141',
    name: '热等静压',
    type: '流程',
    category: 'countermeasures',
    aliases: ['HIP'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '在高温高压惰性气体环境下对材料进行致密化处理',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1142',
    name: '粉末注射成型',
    type: '流程',
    category: 'countermeasures',
    aliases: ['PIM'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '将金属或陶瓷粉末与粘结剂混合注射成型后脱脂烧结',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1143',
    name: '超精密加工',
    type: '流程',
    category: 'countermeasures',
    aliases: ['超精加工'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '实现纳米级加工精度和表面粗糙度的加工技术',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1144',
    name: '水导激光',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Water Jet Guided Laser'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用细水束引导激光实现无热影响区的高精度加工',
    created_at: '2025-09-26T09:43:14.297087',
    updated_at: '2025-09-26T09:43:14.297087'
});
CREATE (d:Dictionary {
    id: 'TERM_1145',
    name: '飞秒激光加工',
    type: '流程',
    category: 'countermeasures',
    aliases: ['超快激光加工'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用超短脉冲激光进行高精度低热损伤的微加工',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1146',
    name: '冷喷涂',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Cold Spray'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用高速气体加速粉末颗粒通过塑性变形沉积形成涂层',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1147',
    name: '原子扩散焊接',
    type: '流程',
    category: 'countermeasures',
    aliases: ['扩散焊'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '在高温压力下通过原子扩散实现材料间牢固连接',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1148',
    name: '摩擦搅拌焊',
    type: '流程',
    category: 'countermeasures',
    aliases: ['FSW'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '通过高速旋转搅拌头与工件摩擦生热实现材料连接',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1149',
    name: '电子束焊接',
    type: '流程',
    category: 'countermeasures',
    aliases: ['EBW'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '利用高速电子束轰击工件产生热量实现焊接',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1150',
    name: '激光熔覆',
    type: '流程',
    category: 'countermeasures',
    aliases: ['Laser Cladding'],
    tags: ['制造工艺;结构相关;可靠性'],
    description: '通过激光熔化添加材料在基体表面形成冶金结合涂层',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1151',
    name: '失效分析',
    type: '流程',
    category: 'countermeasures',
    aliases: ['故障分析'],
    tags: ['可靠性;质量体系;测试验证'],
    description: '通过一系列技术方法确定失效模式和机理的过程',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1152',
    name: '根因分析',
    type: '流程',
    category: 'countermeasures',
    aliases: ['根本原因分析'],
    tags: ['可靠性;质量体系;测试验证'],
    description: '追溯并确定导致问题发生的最深层原因',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1153',
    name: '鱼骨图',
    type: '工具',
    category: 'countermeasures',
    aliases: ['因果图'],
    tags: ['可靠性;质量体系;工具'],
    description: '用于系统性分析问题所有可能原因的图表工具',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1154',
    name: '8D方法',
    type: '流程',
    category: 'countermeasures',
    aliases: ['8步纠正措施'],
    tags: ['可靠性;质量体系;流程相关'],
    description: '系统化解决质量问题的八步法流程',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1155',
    name: '故障树分析',
    type: '工具',
    category: 'countermeasures',
    aliases: ['FTA'],
    tags: ['可靠性;质量体系;工具'],
    description: '通过逻辑演绎分析系统故障与底层事件关系的分析方法',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1156',
    name: '失效模式与影响分析',
    type: '工具',
    category: 'countermeasures',
    aliases: ['FMEA'],
    tags: ['可靠性;质量体系;工具'],
    description: '系统性识别和预防潜在失效模式的分析方法',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1157',
    name: '故障报告分析和纠正措施系统',
    type: '流程',
    category: 'countermeasures',
    aliases: ['FRACAS'],
    tags: ['可靠性;质量体系;流程相关'],
    description: '闭环的故障数据管理和问题解决系统',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1158',
    name: '加速寿命测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['ALT'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '通过施加高应力在短时间内获得产品寿命信息',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1159',
    name: '高加速寿命测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['HALT'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '通过步进应力快速发现产品设计极限和薄弱环节',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1160',
    name: '高加速应力筛选',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['HASS'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '在生产阶段使用高应力快速剔除有缺陷产品',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1161',
    name: '环境应力筛选',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['ESS'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '通过环境应力激发和剔除早期失效产品',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1162',
    name: '可靠性增长测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['RGT'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '通过测试-改进-再测试循环逐步提高产品可靠性',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1163',
    name: '可靠性鉴定测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['RQT'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '验证产品设计是否满足可靠性要求的测试',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1164',
    name: '可靠性验收测试',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['RAT'],
    tags: ['可靠性;测试验证;质量体系'],
    description: '对批量生产产品进行抽样可靠性验证',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1165',
    name: '威布尔分布',
    type: '工具',
    category: 'countermeasures',
    aliases: ['Weibull分布'],
    tags: ['可靠性;质量体系;工具'],
    description: '常用于可靠性数据分析的概率分布模型',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1166',
    name: '阿伦尼乌斯模型',
    type: '工具',
    category: 'countermeasures',
    aliases: ['温度加速模型'],
    tags: ['可靠性;质量体系;工具'],
    description: '基于化学反应速率理论的温度加速模型',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1167',
    name: '艾林模型',
    type: '工具',
    category: 'countermeasures',
    aliases: ['温度-湿度加速模型'],
    tags: ['可靠性;质量体系;工具'],
    description: '考虑温度和湿度共同作用的加速模型',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1168',
    name: '科芬-曼森关系',
    type: '工具',
    category: 'countermeasures',
    aliases: ['温度循环加速模型'],
    tags: ['可靠性;质量体系;工具'],
    description: '基于疲劳损伤理论的温度循环加速模型',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1169',
    name: '可靠性预计',
    type: '流程',
    category: 'countermeasures',
    aliases: ['可靠性预测'],
    tags: ['可靠性;设计;质量体系'],
    description: '基于元器件失效率数据预测系统可靠性水平',
    created_at: '2025-09-26T09:43:14.298079',
    updated_at: '2025-09-26T09:43:14.298079'
});
CREATE (d:Dictionary {
    id: 'TERM_1170',
    name: '可靠性分配',
    type: '流程',
    category: 'countermeasures',
    aliases: ['可靠性指标分配'],
    tags: ['可靠性;设计;质量体系'],
    description: '将系统可靠性指标合理分配到各分系统和元器件',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1171',
    name: '可靠性设计',
    type: '流程',
    category: 'countermeasures',
    aliases: ['DfR'],
    tags: ['可靠性;设计;质量体系'],
    description: '在产品设计阶段就考虑和融入可靠性要求',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1172',
    name: '失效分析工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['FA工程师'],
    tags: ['可靠性;质量体系;组织职责'],
    description: '负责产品失效分析和技术问题解决的专业人员',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1173',
    name: '可靠性工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['可靠性专家'],
    tags: ['可靠性;质量体系;组织职责'],
    description: '负责可靠性设计测试和管理的专业人员',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1174',
    name: '3C认证',
    type: '流程',
    category: 'countermeasures',
    aliases: ['中国强制性产品认证'],
    tags: ['法规;质量体系;安全相关'],
    description: '中国市场准入的强制性安全认证',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1175',
    name: 'CE标志',
    type: '流程',
    category: 'countermeasures',
    aliases: ['欧洲符合性标志'],
    tags: ['法规;质量体系;安全相关'],
    description: '产品符合欧盟安全健康环保要求的标志',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1176',
    name: 'FCC认证',
    type: '流程',
    category: 'countermeasures',
    aliases: ['美国联邦通信委员会认证'],
    tags: ['法规;质量体系;EMC'],
    description: '美国市场电磁兼容性和射频设备合规性认证',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1177',
    name: 'UL认证',
    type: '流程',
    category: 'countermeasures',
    aliases: ['美国保险商实验室认证'],
    tags: ['法规;质量体系;安全相关'],
    description: '美国产品安全性能认证',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1178',
    name: 'RoHS指令',
    type: '流程',
    category: 'countermeasures',
    aliases: ['有害物质限制指令'],
    tags: ['法规;环保;供应链'],
    description: '限制电子电气产品中使用特定有害物质的欧盟指令',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1179',
    name: 'REACH法规',
    type: '流程',
    category: 'countermeasures',
    aliases: ['化学品注册评估授权和限制法规'],
    tags: ['法规;环保;供应链'],
    description: '欧盟对化学品安全管理的综合性法规',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1180',
    name: 'WEEE指令',
    type: '流程',
    category: 'countermeasures',
    aliases: ['废弃电子电气设备指令'],
    tags: ['法规;环保;供应链'],
    description: '欧盟关于电子电气设备废弃物回收利用的指令',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1181',
    name: '能效标准',
    type: '流程',
    category: 'countermeasures',
    aliases: ['能源效率标准'],
    tags: ['法规;环保;性能指标'],
    description: '对产品能耗和效率要求的强制性标准',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1182',
    name: '射频电磁场辐射抗扰度',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['辐射抗扰度'],
    tags: ['法规;测试验证;EMC'],
    description: 'IEC 61000-4-3标准规定的射频电磁场辐射抗扰度测试',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1183',
    name: '电快速瞬变脉冲群抗扰度',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['EFT抗扰度'],
    tags: ['法规;测试验证;EMC'],
    description: 'IEC 61000-4-4标准规定的电快速瞬变脉冲群抗扰度测试',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1184',
    name: '传导骚扰',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['传导发射'],
    tags: ['法规;测试验证;EMC'],
    description: 'CISPR 32等标准规定的设备通过电源线或信号线向外发射的骚扰',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1185',
    name: '辐射骚扰',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['辐射发射'],
    tags: ['法规;测试验证;EMC'],
    description: 'CISPR 32等标准规定的设备通过空间辐射的电磁骚扰',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1186',
    name: '电压波动和闪烁',
    type: '测试用例',
    category: 'countermeasures',
    aliases: ['闪烁测试'],
    tags: ['法规;测试验证;EMC'],
    description: 'IEC 61000-3-3标准规定的设备对电网电压波动的影响',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1187',
    name: '包装材料要求',
    type: '流程',
    category: 'countermeasures',
    aliases: ['包装环保要求'],
    tags: ['法规;环保;供应链'],
    description: '对产品包装材料的可再生可回收性要求',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1188',
    name: '能效标签',
    type: '流程',
    category: 'countermeasures',
    aliases: ['能源标签'],
    tags: ['法规;环保;性能指标'],
    description: '标示产品能效等级的强制性标签制度',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1189',
    name: '冲突矿产',
    type: '流程',
    category: 'countermeasures',
    aliases: ['冲突矿物'],
    tags: ['法规;环保;供应链'],
    description: '对来自刚果民主共和国等冲突地区矿产的使用限制',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1190',
    name: '数据安全',
    type: '流程',
    category: 'countermeasures',
    aliases: ['信息安全'],
    tags: ['法规;安全相关;软件相关'],
    description: '对用户数据保护和隐私安全的法规要求',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1191',
    name: '网络安全',
    type: '流程',
    category: 'countermeasures',
    aliases: ['网络信息安全'],
    tags: ['法规;安全相关;软件相关'],
    description: '对设备网络连接和安全防护的法规要求',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});
CREATE (d:Dictionary {
    id: 'TERM_1192',
    name: '法规认证工程师',
    type: '角色',
    category: 'countermeasures',
    aliases: ['认证工程师'],
    tags: ['法规;质量体系;组织职责'],
    description: '负责产品全球市场准入认证和法规符合性的专业人员',
    created_at: '2025-09-26T09:43:14.299077',
    updated_at: '2025-09-26T09:43:14.299077'
});