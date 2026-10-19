# 分支与文档地图

这是对当前工作副本全部本地分支的逐项盘点，不是 GitHub 所有未知远端分支的实时列表。每项固定到检查时提交；之后分支可能继续前进。文档存在只说明该版本包含它，不说明内容仍是最新版。

阅读优先级：用户最新要求 → [最新交接](NEXT_AI_HANDOFF.zh-CN.md)与[概念词典](GAME_CONCEPTS.zh-CN.md) → 对应已确认源码 → 当前接口说明 → 历史报告。

## 1. 各分支用途

| 分支 | 检查时提交 | 用途 |
| --- | --- | --- |
| `feature/design-lab-local` | `dea1afe` | 当前独立 Lab 与本次交接文档；继承最新开头＋三关＋Level 1 动画。Lab 尚未连接游戏。 |
| `animation/opening-integration` | `6385649` | 已通过的开头＋三关＋Level 1 动画合并线；没有独立 Lab 目录。 |
| `preview/level1-settlement` | `411353d` | 已通过的独立 Level 1 结算／影片预览；不作为完整三关最新入口。 |
| `level3-dev` | `00c3116` | 较早稳定三关玩法主线；包含 Level 3 最终自由实验规则，但不是最新开头／Level 1 电影合并线。 |
| `level1-preview` | `6068b0e` | 旧发布别名，与 level2-preview、level2-dev 同提交；名字不是完整动画最新版标志。 |
| `level2-preview` | `6068b0e` | 旧发布别名，与 level1-preview、level2-dev 同提交。 |
| `level2-dev` | `6068b0e` | 旧发布别名，与 level1-preview、level2-preview 同提交。 |
| `archive/opening-before-level1-merge-20261020` | `32a91fe` | 用户要求的合并前备份；保留当时开头＋三关和旧可玩包。 |
| `archive/pre-effort-rules-v16` | `69f2bb4` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-level3-feedback-v18` | `25bc397` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-level3-focus-v8` | `24d8028` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-level3-path-v17` | `5d56d4c` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-player-experiments-v15` | `d3075b7` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-relative-effort-v19` | `23d0a01` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-scaffolding-v13` | `d10e09b` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-task-clarity-v14` | `3ffe535` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |
| `archive/pre-visual-redesign-v6` | `90313c7` | 历史变更前快照，仅供回查和差异比较，不作为最新要求来源。 |

## 2. 文档类型怎么用

| 文档 | 用途与注意点 |
| --- | --- |
| NEXT_AI_HANDOFF.zh-CN.md / .docx | 最新完整需求交接；Word 是 Markdown 的便携副本。 |
| GAME_CONCEPTS.zh-CN.md / .docx | 数字、评价、权重、投入、管理层、学生状态等定义与边界。 |
| BRANCH_DOCUMENT_MAP.zh-CN.md | 本文，查各分支实际拥有哪些文档。 |
| ANIMATION_INTEGRATION.md、src/cinematics/README.md | 动画适配架构、入口、真实结束回调；旧阶段范围限制不能覆盖后续用户指令。 |
| OPENING_HANDOFF.md、LEVEL1/2/3_HANDOFF.md、CHAPTER_TRANSITIONS.md | 接口、过渡及数据交接；开头与 Level 1 的部分历史措辞已被后续修改替代。 |
| LEVEL3_NARRATION.md / .docx | 动画组画面与台词制作稿；不是程序逻辑的第二实现。末尾“暂不进 Lab”属当时范围。 |
| EFFORT_RULES.md、LEVEL3_PLAYER_PATH.md、UNASSIGNED_WEIGHTS-v21.md | 当前第三关相对规则、自由路径与空白起步。 |
| LEVEL2_FRAMING.md | 第二关实验假设和清单膨胀铺垫。里面引用的旧 Level 1 按钮／对话不是最终合并版。 |
| LEVEL1_SETTLEMENT_PREVIEW.md | 独立 Level 1 预览工作方式，不能拿预览限制覆盖完整游戏。 |
| MANAGEMENT_SATISFACTION.md | 管理层叙事反馈含义。其 target、reference publication 等历史表述需对照最新源码，见概念词典。 |
| DEVELOPMENT_WORKFLOW.md、REPOSITORY_GUIDE.md、PROJECT_DETAILS.md | 构建与仓库工作方式；实际工作分支以最新任务和基线为准。 |
| PREVIEW_VALIDATION.json、各 VALIDATION*.json、play/*json | 特定源码／打包版本的验证记录与哈希，不是课堂学习成效证明。 |
| design-lab/README.md、README-Windows.txt、START-HERE.html、AGENTS.md | Lab 开发、Windows 操作与范围；只在 Lab 分支存在。 |
| 根目录及子目录 AGENTS.md | 对应阶段工作约定。根文件积累多阶段规定，不表示要同时向所有历史分支发布。 |
| vN 文件、archive 分支文档 | 历史证据；严禁按编号或文件数量推断最新行为。 |

## 3. 各分支实际文档清单

以下读取 Git 树，不切换／合并分支；当前 feature 分支的清单也包含本次新增、随本次提交发布的三份交接文档。列出所有已跟踪 Markdown、Word、文本／HTML 说明，以及 docs/ 内 JSON 等记录。普通源代码及二进制可玩包不列入。清单中的路径是在该分支内的路径，不是保证你当前检出分支也有该文件。

### feature/design-lab-local

当前独立 Lab 与本次交接文档；继承最新开头＋三关＋Level 1 动画。Lab 尚未连接游戏。

检查基线：`dea1afe72a32f2a8a3a48a25922a086aef7b8327`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `design-lab/AGENTS.md`
- `design-lab/README-Windows.txt`
- `design-lab/README.md`
- `design-lab/START-HERE.html`
- `docs/ANIMATION_INTEGRATION.md`
- `docs/BRANCH_DOCUMENT_MAP.zh-CN.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/GAME_CONCEPTS.zh-CN.docx`
- `docs/GAME_CONCEPTS.zh-CN.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL1_SETTLEMENT_PREVIEW.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_NARRATION.docx`
- `docs/LEVEL3_NARRATION.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/NEXT_AI_HANDOFF.zh-CN.docx`
- `docs/NEXT_AI_HANDOFF.zh-CN.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/cinematics/README.md`
- `src/cinematics/level1/README.md`
- `src/cinematics/opening/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### animation/opening-integration

已通过的开头＋三关＋Level 1 动画合并线；没有独立 Lab 目录。

检查基线：`63856491e62c52d5a9bdb176ea738abbe6c6c9c7`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/ANIMATION_INTEGRATION.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL1_SETTLEMENT_PREVIEW.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_NARRATION.docx`
- `docs/LEVEL3_NARRATION.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/cinematics/README.md`
- `src/cinematics/level1/README.md`
- `src/cinematics/opening/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### preview/level1-settlement

已通过的独立 Level 1 结算／影片预览；不作为完整三关最新入口。

检查基线：`411353dd3ef6103b20faa4debe9075b94f46e199`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/ANIMATION_INTEGRATION.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL1_SETTLEMENT_PREVIEW.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_NARRATION.docx`
- `docs/LEVEL3_NARRATION.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/cinematics/README.md`
- `src/cinematics/opening/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### level3-dev

较早稳定三关玩法主线；包含 Level 3 最终自由实验规则，但不是最新开头／Level 1 电影合并线。

检查基线：`00c311682268ab8593d0733a4163b50ee41cd663`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/ANIMATION_INTEGRATION.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_NARRATION.docx`
- `docs/LEVEL3_NARRATION.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/cinematics/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### level1-preview

旧发布别名，与 level2-preview、level2-dev 同提交；名字不是完整动画最新版标志。

检查基线：`6068b0efe68c91f2835b65d0a79e9c2c685d04f3`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### level2-preview

旧发布别名，与 level1-preview、level2-dev 同提交。

检查基线：`6068b0efe68c91f2835b65d0a79e9c2c685d04f3`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### level2-dev

旧发布别名，与 level1-preview、level2-preview 同提交。

检查基线：`6068b0efe68c91f2835b65d0a79e9c2c685d04f3`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/opening-before-level1-merge-20261020

用户要求的合并前备份；保留当时开头＋三关和旧可玩包。

检查基线：`32a91fe4bfb1cb193040410c846ebc165f8b9d5d`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/ANIMATION_INTEGRATION.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_FRAMING.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_NARRATION.docx`
- `docs/LEVEL3_NARRATION.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/PROJECT_DETAILS.md`
- `docs/README.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/UNASSIGNED_WEIGHTS-v21.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/cinematics/README.md`
- `src/cinematics/opening/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/DOWNLOAD_BUNDLE_VALIDATION-v22.json`
- `docs/DOWNLOAD_BUNDLE_VALIDATION.json`
- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION-v7.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v20.json`
- `docs/LEVEL3_VALIDATION-v21.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-effort-rules-v16

历史快照，按用途回查；不要以此重做最新版。

检查基线：`69f2bb4906a6d6c85442686180e49dc6a0800291`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-level3-feedback-v18

历史快照，按用途回查；不要以此重做最新版。

检查基线：`25bc397aec1bad90158f318d1a0efbfd6a953509`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-level3-focus-v8

历史快照，按用途回查；不要以此重做最新版。

检查基线：`24d80282b83afd65ba4600f5d2fa4c2718a3f8d4`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-level3-path-v17

历史快照，按用途回查；不要以此重做最新版。

检查基线：`5d56d4cbb763b039b4a8a7a4c3bceb7932f303b2`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-player-experiments-v15

历史快照，按用途回查；不要以此重做最新版。

检查基线：`d3075b72950e8bf9a0f693d15cf37b95440cfe7d`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-relative-effort-v19

历史快照，按用途回查；不要以此重做最新版。

检查基线：`23d0a010c24c578532410b66359c396827213469`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/EFFORT_RULES.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FEEDBACK-v19.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/LEVEL3_PLAYER_PATH.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/PLAYER_EXPERIMENTS.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TASK_CLARITY.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v15.json`
- `docs/LEVEL3_VALIDATION-v16.json`
- `docs/LEVEL3_VALIDATION-v17.json`
- `docs/LEVEL3_VALIDATION-v18.json`
- `docs/LEVEL3_VALIDATION-v19.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-scaffolding-v13

历史快照，按用途回查；不要以此重做最新版。

检查基线：`d10e09bc7a34cae462ea594bce09f4fc8671f593`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-task-clarity-v14

历史快照，按用途回查；不要以此重做最新版。

检查基线：`3ffe53588ef599673228b9156c4af975c5aabd68`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/CHAPTER_TRANSITIONS.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEARNING_OPTIMIZATIONS.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_FOCUS.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/SCAFFOLDING.md`
- `docs/TYPOGRAPHY.md`
- `docs/VISUAL_PLAY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v10.json`
- `docs/LEVEL3_VALIDATION-v11.json`
- `docs/LEVEL3_VALIDATION-v12.json`
- `docs/LEVEL3_VALIDATION-v13.json`
- `docs/LEVEL3_VALIDATION-v14.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/LEVEL3_VALIDATION-v7.json`
- `docs/LEVEL3_VALIDATION-v8.json`
- `docs/LEVEL3_VALIDATION-v9.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

### archive/pre-visual-redesign-v6

历史快照，按用途回查；不要以此重做最新版。

检查基线：`90313c79ca1b91d3b9015870944256b43cafaf4d`。

**说明／制作文档：**

- `AGENTS.md`
- `README.md`
- `docs/DIALOGUE_REVIEW.md`
- `docs/LEVEL1_HANDOFF.md`
- `docs/LEVEL2_HANDOFF.md`
- `docs/LEVEL2_NARRATIVE_AUDIT.md`
- `docs/LEVEL3_HANDOFF.md`
- `docs/MANAGEMENT_SATISFACTION.md`
- `docs/OPENING_HANDOFF.md`
- `docs/REPOSITORY_GUIDE.md`
- `docs/TYPOGRAPHY.md`
- `play/README.md`
- `src/levels/level1/README.md`
- `src/levels/level2/README.md`
- `src/levels/level3/README.md`
- `src/shared/README.md`

**验证／记录文件：**

- `docs/LEVEL2_VALIDATION-v2.json`
- `docs/LEVEL2_VALIDATION-v3.json`
- `docs/LEVEL2_VALIDATION-v4.json`
- `docs/LEVEL2_VALIDATION-v5.json`
- `docs/LEVEL2_VALIDATION-v6.json`
- `docs/LEVEL2_VALIDATION.json`
- `docs/LEVEL3_VALIDATION-v1.json`
- `docs/LEVEL3_VALIDATION-v2.json`
- `docs/LEVEL3_VALIDATION-v3.json`
- `docs/LEVEL3_VALIDATION-v4.json`
- `docs/LEVEL3_VALIDATION-v5.json`
- `docs/LEVEL3_VALIDATION-v6.json`
- `docs/PREVIEW_VALIDATION.json`
- `docs/SOURCE_LAYOUT_VALIDATION.json`

## 4. 给下一位 AI 的最短阅读路线

1. 当前 Lab 分支：先看 NEXT_AI_HANDOFF、GAME_CONCEPTS、本地图；然后 Lab README。
2. 开头或 Level 1 合并：看 opening-integration 基线、最新交接对应章节、LevelOneExperience 与电影适配层，再查旧 handoff 的接口。
3. Level 2／3 动画：看最新交接、对应 Level handoff；第三关再看最新 narration 和 weights／experiments。
4. 查旧行为：到对应 archive 固定提交读取，标成历史，不复制回最新版。
5. 不用逐个切换分支读同一文档。可用 git show 分支:路径，只在确实不同／需要时比较，减少重复同步与构建。
