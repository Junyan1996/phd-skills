# phd-skills

面向生物学、遗传学和生物信息学硕博生的科研技能集合：从选题、开题和研究设计，到论文写作、配图、汇报与返修。

**每个 `skills/phd-*` 都是独立技能文件夹。** `phd-skills` 是集合名，不需要一次加载全部技能。默认遵从用户语言、实际数据和学校/目标期刊要求；不默认 Nature 风格，不保证覆盖所有生物学分支。

## 技能目录

| 子技能 | 适用任务 | 核心产物 |
|---|---|---|
| [phd-proposal](skills/phd-proposal/SKILL.md) | 硕博开题、研究计划、多文件整合 | 可追溯的开题稿、目标—方法表、风险与进度 |
| [phd-topic](skills/phd-topic/SKILL.md) | 选题、项目卡住、方向取舍 | 问题简报、最接近工作差异、最小可行性检验 |
| [phd-literature](skills/phd-literature/SKILL.md) | 文献检索、研究现状、综述 | 检索日志、研究—报告映射、主题综合 |
| [phd-hypothesis](skills/phd-hypothesis/SKILL.md) | 假说、研究问题、实验设计 | 竞争解释、区分性预测、设计与分析计划 |
| [phd-bioinformatics](skills/phd-bioinformatics/SKILL.md) | 生信分析设计、流程实现、排错 | 输入契约、可复现流程、质控与验证记录 |
| [phd-writing](skills/phd-writing/SKILL.md) | 从结果/笔记撰写论文 | 论证主线、分节稿、证据缺口 |
| [phd-polishing](skills/phd-polishing/SKILL.md) | 学术润色、中英改写、LaTeX排版 | 保留原意的修订稿、实质修改说明 |
| [phd-citation](skills/phd-citation/SKILL.md) | 补引用、引文核验、参考文献管理 | 论点支持表、核验后的 BibTeX/RIS |
| [phd-data](skills/phd-data/SKILL.md) | 数据/代码可用性、仓库与元数据规划 | 数据清单、共享路径、可用性声明 |
| [phd-figure](skills/phd-figure/SKILL.md) | 科研绘图、多面板图、机制示意图 | 可编辑源文件、导出图、图例、视觉检查 |
| [phd-reader](skills/phd-reader/SKILL.md) | 论文精读、对照翻译、图表解读 | 带原文定位的读本、术语表、覆盖记录 |
| [phd-slides](skills/phd-slides/SKILL.md) | 文献汇报、组会、开题/答辩PPT | 实际 PPTX、讲稿、来源记录 |
| [phd-reviewer](skills/phd-reviewer/SKILL.md) | 开题预审、投稿前审稿 | 按证据定位的问题、优先级与修订建议 |
| [phd-response](skills/phd-response/SKILL.md) | 审稿回复、返修、意见冲突 | 逐点回复、修订映射、待办 |
| [phd-pubmed](skills/phd-pubmed/SKILL.md) | 用已确认PMID开发并验证PubMed策略 | 候选词表、布尔式、留出验证记录 |
| [phd-workflow](skills/phd-workflow/SKILL.md) | 跨阶段科研任务、项目续接 | 轻量状态、三文件计划、独立任务目录与证据续接 |

## 开始使用

将一个或多个完整的 `skills/phd-*` 文件夹放入支持 `SKILL.md` 的工具的技能目录。Codex 的常规用户目录为 `~/.codex/skills`；其他工具请按其说明配置。不要只复制 `SKILL.md`，配套 references/assets/scripts 也需要保留。

```bash
git clone https://github.com/Junyan1996/phd-skills.git
cd phd-skills
python scripts/install.py --list
python scripts/install.py --skill phd-proposal --skill phd-writing
# 安装全部：python scripts/install.py --all
```

安装器默认写入 `$CODEX_HOME/skills`，未设置时写入 `~/.codex/skills`；也可传 `--dest PATH`。已有同名文件夹时整次安装退出，绝不覆盖；可先使用 `--dry-run`。安装只复制文本与脚本，不安装软件、不运行分析、不修改原有 `nature-*` 等技能。

调用例子：

```text
用 $phd-proposal 帮我做玉米耐旱遗传机制的硕士开题。
已有120份材料的重测序和两环境表型，先检查研究问题与数据是否匹配。

用 $phd-bioinformatics 审核我的RNA-seq方案，特别检查生物学重复、批次和差异分析设计。

用 $phd-writing 根据我提供的图表和统计输出写Results，不补造缺失结果。

用 $phd-workflow 接续这个项目，读取已有状态，只推进尚未完成的阶段。
```

`phd-workflow` 1.1 支持两种规模：普通续接沿用 `status.md`；长项目在 `.phd-workflow/<task-id>/` 中分开保存 `task_plan.md`（计划）、`findings.md`（证据）和 `progress.md`（执行记录）。同一项目多个任务明确指定ID，不按“最近修改”猜任务。没有自动循环或每次工具调用重复加载计划的钩子。

```text
用 $phd-workflow 管理任务 goat-proposal。
先比较 papers 文件夹中已提供的论文，在 .phd-workflow/goat-proposal/ 保存计划、发现和进度。
下次继续时先恢复该任务，只推进尚未完成的工作；重要新证据可以修订旧决定。
```

完整示例见[首次使用与续接](skills/phd-workflow/references/examples.md)。可选的标准库工具只初始化新任务/提供只读预览：

```bash
python skills/phd-workflow/scripts/state.py init --project-root ./my-research --task-id goat-proposal --title 山羊基因组开题
python skills/phd-workflow/scripts/state.py show --project-root ./my-research --task-id goat-proposal
```

示例中的项目目录必须已存在；已有任务直接恢复，不重新初始化。此版本借鉴了planning-with-files的文件分工并针对科研重写，不要求同时安装两个技能。

开题资料夹可选初始化（Python标准库，无网络）：

```bash
python skills/phd-proposal/scripts/init_project.py ./my-proposal
```

适用于动物/植物/微生物遗传、群体与数量遗传、功能基因组、多组学和基因组资源等常见方向。临床决策、具体高风险实验操作、测序采购与集群提交需要单独的专业判断及实际任务授权。技能提供研究辅助，不代替导师、伦理审查或真实实验。

## 设计与验证

从原有 T2T 开题工作流推广，审阅并重写了现有科研技能的可迁移部分；[迁移与来源说明](docs/MIGRATION.md)记录对应关系。新技能不依赖原机的 `_shared`、`nature-shared`、固定解释器路径、个人配色或特定连接器。不捆绑原有整套脚本、付费图像服务或期刊原文。

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

结构检查和脚本测试不能证明学术结论正确；使用时仍要核验原始文献、统计设计和渲染后的文档。示例与验收情境见 [使用情境](docs/SCENARIOS.md)。授权范围见 [LICENSE](LICENSE) 与 [来源声明](THIRD_PARTY_NOTICES.md)。
