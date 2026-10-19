---
name: phd-citation
description: "Find and verify references that support specific academic claims, reconcile citations and export bibliographic records. Use for 补引用、引文核对、参考文献去重与BibTeX/RIS; broad research synthesis belongs to literature review."
metadata:
  version: "1.0.0"
---

# 引文支持与参考文献

先识别任务是找支持、核验现有引用，还是格式/文件管理。按用户指定的学科、年份、语种和期刊范围检索；没有限制时不默认Nature/CNS白名单。

将复合句拆成可核查主张，查原始研究或适当的方法/资源来源。标题相似与DOI有效都不代表支持论点。分别核查：

1. **身份**：标题、作者、年份、刊物、DOI/PMID/登录号、版本是否对应；预印本、正式版、勘误与撤稿状态。
2. **支持**：该研究的对象、样本、设计、方法、结果与被引用主张是否匹配；记录页/节/图/表或可定位原文。
3. **边界**：只见摘要/元数据、访问失败、外推、矛盾证据或不充分支持；不能标成全文确认。
4. **呈现**：实际学校附件或目标期刊当前要求；模板缺失时先给完整元数据并标明格式待核。

支持表字段：`claim_id, claim, reference_id, support_status, source_locator, scope_mismatch, access_level, action`。状态可用支持/部分支持/不支持/无法评估；部分支持时优先收窄正文，不以堆叠引用掩盖。

先按标识符去重，再核对标题—作者—年份；保留不同版本的关联和必要区分。BibTeX键稳定且不冲突，RIS字段逐条对应真实记录，不编卷期页码、DOI或链接。仅做文件转换时无需额外添加参考文献。

正文编号/作者年与文末逐项双向核对；引用顺序改变后重新编号。对Zotero等写入只在用户授权该库及操作时执行，生成本地导入文件可先完成。交付核验记录、可用引用和未决项，不把软件引用当成生物学证据。
