# 来源与迁移说明

2026-10-18：根据用户现有技能快照整理为独立的 `phd-*` 集合。此处“优化”指在新集合中重写和调整；原安装文件夹保持原样，避免破坏已有调用和个人设置。不是将原整套脚本和资源改名复制。

| 已审阅来源 | 新技能/去向 | 主要调整 |
|---|---|---|
| t2t-proposal | phd-proposal | 推广至生物遗传硕博；T2T检查保留为按需参考；移除个人学校附件和本机runtime |
| scientific-problem-selection | phd-topic | 按当前决策进入；保留风险、依赖与早期检验思想；去掉固定周数、成功概率和固定问答 |
| hypothesis-generation | phd-hypothesis | 观察—假说—预测分开；资源、关联、预测、机制分流；不强迫资源项目造机制 |
| literature-review | phd-literature | 保留记录/报告/研究区分及真实筛选计数；不依赖付费CLI或AI配图 |
| nature-academic-search | phd-literature / phd-citation | 多来源检索与混合文件证据；不宣称预置连接器存在 |
| nature-writing | phd-writing / phd-proposal | 论文与开题分别调用，语言和学校/期刊选择由用户任务决定 |
| nature-polishing | phd-polishing | 论证先于措辞、保留证据强度；LaTeX独立分流；移除刊系强制风格 |
| nature-citation | phd-citation | 默认通用学术范围；身份、论点支持和格式分别核验 |
| nature-data | phd-data | 适配一般期刊与真实访问路径；不编登录号，不将FAIR等同全部开放 |
| nature-figure | phd-figure | 保留数据完整性、最终尺寸和多面板视觉检查；不复制个人配色、后端记忆、API设置和专用审计脚本 |
| nature-paper2ppt | phd-slides | 同时支持开题/答辩与读文汇报；实际PPTX和全部页面视觉检查 |
| nature-reader | phd-reader | 保留全文覆盖与图表定位；明确只有链接时的版权边界与OCR不确定性 |
| nature-reviewer | phd-reviewer | 面向实际学科/期刊/开题；去掉默认恰好三位Nature审稿人的固定格式 |
| nature-response | phd-response | 逐条账本与真实修订定位；计划与已完成分开，允许有证据的不同意 |
| objective-pubmed | phd-pubmed | 保留已确认PMID、开发/留出边界与验证后修订；增加按研究分组防泄漏；不捆绑原CLI |
| 跨阶段工作流需求 | phd-workflow | 新增轻量状态续接与能力路由，不要求全量安装或自动委派 |
| 生信通用化需求 | phd-bioinformatics | 新增输入契约、设计可识别性、各分析类型陷阱与执行状态区分 |

`markitdown` 的格式提取经验用于“提取后回看原件”这一通用要求；本集合没有分发其实现或锁定其版本。文档、PDF、幻灯片等工具按运行环境实际能力使用，不打包Codex系统/插件技能。

本次没有把来源中未核实的论文、商业服务、模型ID、期刊数字限制或个人偏好当作通用事实。原来存在的高级专用脚本仍可由用户继续单独使用；新集合不声称具有同等专用自动化实现。后续迁移具体脚本需单独核对依赖、许可和行为。

技能之间无必需的跨目录资源引用，安装一个文件夹即可得到该技能的说明及随附材料。`phd-workflow`对其他技能的调用是可选路由，不是假装已加载的隐式依赖。
