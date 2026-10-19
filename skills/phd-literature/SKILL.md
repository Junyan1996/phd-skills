---
name: phd-literature
description: "Search and synthesize biology/genetics literature with documented coverage, study-level deduplication and source-grounded comparisons. Use for 文献检索、研究现状、叙述性/范围/系统综述; citation-only checks belong to citation work."
metadata:
  version: "1.0.0"
---

# 文献检索与综合

先确定问题、对象、产物与综述类型。开题背景默认针对问题的叙述性综合；只有执行相应检索、筛选与评估后才能称系统综述。

## 检索与记录

- 按领域组合互补来源：PubMed等论文库、预印本、引文追踪，以及基因组/数据仓库和方法原始文档。一个数据库或排名网页结果不能证明检索穷尽。
- 拆成概念词块，同义词用OR、必要概念用AND；先试检已知相关文献，再调整物种/表型/方法词，不把所有技术名强制AND。
- 保存日期、数据库/平台、逐字查询、字段/过滤、结果数、导出文件、筛选范围与访问失败。仅报告实际执行的搜索，当前新颖性判断应更新检索。
- 元数据核对DOI/PMID/登录号、标题、作者、版本和状态；摘要支持的判断不能写成全文核验。

## 去重、筛选与综合

先去重检索记录，再连接预印本、期刊版及同一研究的多个报告；同一队列/数据重复使用要单列。DOI不同不一定是独立研究，组装/软件版本不等同论文数。

建表：`study_id, report_id, identifier, version, question, system, n_and_unit, design, method, main_evidence, limitations, locator, eligibility_reason`。

按问题/证据主题比较共识、冲突与不可比较项，不逐篇堆摘要。数值比较需口径、单位、数据集和评估条件一致。最接近工作矩阵应能说明本项目支持什么差异；无命中只能写“在本次边界内未找到”。

系统/范围综述按适用规范记录标准、筛选和排除理由；独立筛选与分歧解决按协议执行并披露实际人员。分别报告records/reports/studies；PRISMA数字只能由记录汇总，缺失不可补造。量化合并前判断设计与效应量可比性；本技能不把简单平均当meta分析。

交付综合正文、检索日志、纳入表和局限；参考文献应可定位。若用户只要简短背景，按比例缩小产物。模板或PDF生成能力缺失时先交付完整文本，不虚称已生成文件。
