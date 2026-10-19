---
name: phd-workflow
description: "Coordinate and resume multi-stage biology/genetics research work across topic choice, evidence, analysis, writing and revision. Use for 科研工作流、跨阶段项目推进与续接; for a single clear task use the relevant specialist skill directly."
metadata:
  version: "1.0.0"
---

# 科研任务协调与续接

先读取已有文件、用户决策和状态，再判断当前阶段与本次交付。不要因项目完整就每次重新做选题或把全部技能都加载。

按需要选择可用子技能：开题→`phd-proposal`；选题→`phd-topic`；文献→`phd-literature`；假说/设计→`phd-hypothesis`；生信→`phd-bioinformatics`；起草/润色→`phd-writing`/`phd-polishing`；引文/数据→`phd-citation`/`phd-data`；图/汇报→`phd-figure`/`phd-slides`；精读→`phd-reader`；预审/返修→`phd-reviewer`/`phd-response`；PMID留出检索→`phd-pubmed`。

这些名称是可选能力，不证明已安装。实际使用时读对应SKILL.md；若不存在，直接完成当前范围内的工作并说明工具/信息限制，不强迫安装整个集合。本技能不要求跨文件夹共享资源，单独安装仍可协调任务。

## 最小项目状态

维护与任务规模相称的 `status.md`，内容包括：

- 当前问题/交付、研究系统与学位期限（如适用）。
- 已接受决策及其理由；何种新证据会改变决策。
- 输入和证据位置、文件版本；已完成与尚未执行的步骤。
- 未决事实/阻碍、影响范围、负责人或所需输入。
- 下一行动及验收条件。

大项目可另有来源、主张—证据、目标—方法和风险表；不为短任务制造空文件。跨步骤保留同一来源ID、样本单位、术语和版本，不从上一阶段摘要反推不存在的原始证据。

将任务分成有实际依赖的阶段：可独立完成的整理继续做，缺少关键输入的分析暂停在该依赖处。用户补充信息时更新既有决策，不丢弃已完成产物。只有核验对应文件/输出后才把阶段记为完成；“代码已写”“分析已运行”“结果已验证”分别记录。

遵守本次任务授权范围，不自动委派、发消息、购买服务、上传数据或提交计算。交付当前有用结果、重要限制与清楚的下一步；只有用户明确要求安排提醒时才创建自动任务。
