---
name: phd-pubmed
description: "Develop and audit objectively derived PubMed Boolean strategies using confirmed relevant PMIDs, development term mining and held-out retrieval checks. Use for PMID种子检索策略、候选词证据与留出验证; not for answering the review question or all-domain discovery."
metadata:
  version: "1.0.0"
---

# 基于PMID证据开发PubMed策略

交付检索式与验证记录，不代替综述结论。用户只有普通主题时可先做常规检索；“客观开发/留出验证”模式需已确认相关/纳入研究PMID集合。候选综述、相似文章和检索命中不能自动升级为准金标准。

1. 确认自然语言问题与种子来源，规范化去重PMID，核对记录身份、范围及版本；保留排除理由。用户仅给布尔式时，不能把它当候选词频证据。
2. 在调词前固定开发/验证集合和拆分规则，按研究分组避免同一研究多个报告跨集合泄漏。种子太少时明确验证不稳定或不可用，不以一个命中证明检索全面。
3. 只用开发集挖掘标题/摘要词与MeSH，记录覆盖率、背景频率、词义及概念角色。阈值应写明出处/理由；候选通过阈值也不自动纳入，不能把通用统计词或check tags当主题词。
4. 构建概念块：同义词OR，必要概念AND；核对当前PubMed字段、词组、截词、MeSH树与自动映射。执行时查NCBI官方帮助及实际返回，不假定支持任意搜索语法。
5. 先用开发集调试并记录漏检；策略固定后只做一次保留集检查。验证后修改标成“验证后修订”，若无新留出集不得继续称独立验证。
6. 保存逐字策略、检索日期、接口/平台、结果数、候选词取舍、开发及验证检出PMID、漏检理由与访问限制。

报告相对于已确认集合的检出率及其分母；它不是全库真实召回率，也不是精确率。种子可能带有选择偏倚，纳入研究PMID不代表所有相关研究。

可用当前环境中的PubMed工具、官方接口或用户导出记录；本技能不捆绑或虚构原 `objective-pubmed` 的CLI。不能联网时可做术语/语法草案并标记未执行；普通生物遗传查新还应补论文、数据和软件来源，PubMed不是全领域覆盖。
