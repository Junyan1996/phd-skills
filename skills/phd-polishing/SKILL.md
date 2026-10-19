---
name: phd-polishing
description: "Polish or translate existing academic prose while preserving scientific meaning, uncertainty and terminology; also repair supplied LaTeX layout. Use for 论文润色、学术中英改写与排版; creating missing results belongs to manuscript drafting."
metadata:
  version: "1.0.0"
---

# 学术润色与排版

先从材料判断用户需要语言修订、论证重构、中英翻译还是排版；沿用明确的输出语言和修改幅度。只润色一段时不扩展为整篇问卷。

## 语言与论证

先识别该节任务和段落主张，再处理句子。优先修复缺少指代、逻辑跳跃、论点顺序、重复与不必要抽象；保持证据强度、否定词、限定词和适用范围。

保留数值、单位、统计术语、基因/物种名、引文键和图号；发现冲突标明待核，不能悄悄改数或把“相关/提示/可能”升级为“导致/证明”。不把显著性改写成生物学重要性。

中文转英文以实际意义为准，建立简短术语对应；不能通过补充原文未给的机制、结果或引用让句子更顺。保留作者声音，不套用固定Nature语气，不保证录用或“去AI检测”。

交付可直接使用的修订文；实质性重构或意义可能变化时给精简的修改理由与作者确认项。用户要求对照/修订模式时保留对应关系，不必解释每个标点。

## LaTeX布局分流

排版任务读[布局检查](references/latex-layout.md)，跳过语言风格流程。先编译、查看日志与实际页面，再按根因调整；修改后重新编译及逐页检查。不要仅凭 `.tex` 宣称分页修复，也不要靠删正文或改变科学图内容解决布局。
