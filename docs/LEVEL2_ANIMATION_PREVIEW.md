# Level 2 动画接入、裁剪与预览

当前 `animation/opening-integration` 已按用户要求接入 Level 2，且先备份了修改前的完整版本。只替换原有 placeholder；游戏规则、增长过程与第三关选择仍由游戏负责。

## 最新内容在哪里

- 同伴交付：`Mg614/gaming-the-system` 的 `feature/cinematic-level2-consequences`，固定提交 `c8c1c83456c4e67cf627df399bfb67b3a9792adb`。原文件保持只读。
- 当前完整游戏：本仓库动画分支的 `play/Full-game-play.zip`；全部版本总包为 `play/Gaming-the-System-complete.zip`。包含开头、Level 1／2 动画与三关。
- 动画单独查看：`play/Level2-animation-preview.zip`；与游戏使用同一个影片 HTML，保留片外暂停／重播／进度工具。
- 当前来源、影片与审阅包校验：`play/LEVEL2_ANIMATION_PREVIEW.json`；整包检查与六个游戏 ZIP 的校验：`docs/PREVIEW_VALIDATION.json`、`play/LATEST.json`。

## 合并前备份

在任何本轮修改之前，完整源码与六个游戏 ZIP 已推送到
`archive/before-level2-animation-integration-20261020`，提交 `762ce7edc796a85307bde282e78393e4773e7b10`。
六个包都已按该提交的 LATEST.json 通过 SHA-256 校验。
该分支同时保留上一轮未裁剪的同伴动画预览；恢复时使用该分支的源码和包，不能混用新旧构建。
稳定游戏分支、已确认的独立 Level 1 实验和更早历史存档均保持原样。

## 只播放已有场景槽

| 游戏请求 | 保留片段 | 忽略内容 |
| --- | --- | --- |
| level2.three.visible／quality／mixed | 从 Alex 的 “I’ve completed all three requirements!” 起，保留后面的原对白和表演 | 原开场、全景、指标展示、开头勾选动作 |
| level2.six | 六项观察的原四句对白与所需表演 | expand 横线／点／方框叠加，以及额外扩展提问页 |
| level2.checklist | 短暂满意反应、最终两句老师反思 | 100 项增长动画、SET PRIORITIES／What matters most 页面与三张优先级占位卡 |

不插入独立 10／25／100 增长片、Checking 演示或额外操作页。
现有连续 10 → 25 → 100 仍是游戏流程，最终观察结束后回到原结果页，再由原按钮进入第三关过渡。
电影不计算分支、权重或结果；读取游戏提供的真实请求。

## 与已确认视觉一致

- 片内保留字幕及说话身份（老师统一 **You**、学生 **Alex**），以及 checklist 原有条目文字与分组标题。按用户后续纠正，清单中的文字不属于要删除的叠加说明；三项、六项和 100 项清单均保留。章节角标、候选标识、纸面页眉／页脚、系统报告、优先级文字和扩展横线继续移除。
- 共用 `src/shared/data/cinematicPalette.js`：You 为 `#ffe2a3`，Alex 为 `#cceeff`，标签与字幕同色。老师字幕保留斜体，身份标签正常字形。
- 字幕无底板、无暗色渐变遮罩，用与 Level 1 相同的细描边和阴影；字号 2.15cqw、行高 1.5。
- 英文阅读时间沿用 Level 1 的约 220 词／分钟加停顿，每句至少 2.1 秒。隐藏页面不消耗阅读时间。
- 固定 1.025 倍镜头，保留原动作、眨眼和表情；不反复推镜、不把两张人像叠化。换景先用 0.28 秒实色遮罩盖严，再切画面并等待两帧，之后揭开。最后盖严后才通知游戏完成。
- 100 项最后两句反思在黑幕下同步换字幕和表情。第一句保留完整阅读时间，下一句及其镜头准备好后再揭幕；不在第一句中途为表情变化另开一次黑屏，避免揭幕后仍停留在旧字幕。
- 字体、颜色、动作和样式隔离于 iframe，未改同伴素材字节。当前没有音频素材，保持静音；游戏本身的声音设置与提示继续工作。

## 动画后结果页

三项、六项和最终观察后的老师／Alex 聊天已移除，不新增解释文字。
原有观察内容占上方整行，下方 Management’s view 与 Students 两卡等宽并列；手机上按原顺序上下排列。
沿用现有标题、观察文案、状态与按钮。读完观察内容后释放原下一步操作，完成回调仍一次性报告。
Students 卡片出现观察结果时，使用与 Level 1 相同的红色描边，按每次 0.75 秒闪烁三次后停止；减少动态效果时显示静态描边。
六项的 “Would more metrics help Alex learn?”、6 → ? 图示、Test more metrics，以及原第三关衔接仍在。

## Cover the gaps：玩家手动补齐

三项结果后的 Cover the gaps 直接进入六张指标卡，移除原来的缺口说明中间页和 Add remaining metrics 按钮。
原先选中的三项保持已勾选且不可取消，其余三项由玩家逐个勾选，不再自动 Checking。
全部补齐后 Observe the class 立即启用；取消任一新增项则再次禁用。原三项选择仍原样传给第三关。
Level 2 所有页面移除 Illustrative outcomes，不用其他说明文字替代。

## 构建与复现

已有云任务使用现有 checkout；除非用户要求，不新建 worktree。
Level 1 缓存仍使用其已固定交付，说明见 ANIMATION_INTEGRATION.md。
Level 2 首次构建使用位于游戏仓库外、固定在上述提交的同伴目录：

```sh
cd /absolute/path/to/partner-checkout
npm ci --ignore-scripts --cache /tmp/gaming-level2-preview-npm-cache
npm run typecheck

cd /workspace/gamingthesystem_game
LEVEL2_ANIMATION_SOURCE=/absolute/path/to/partner-checkout npm run cinematic:prepare
npm run package:previews
npm run test:release
```

`node_modules/.cache/level2-cinematic/` 为忽略的校验缓存；源码或配色变化时要求重新 prepare。
`LevelTwoCinematic` 默认替换 LevelTwo 原场景槽，自定义 renderCinematic 仍可替换整个场景。
影片完成消息必须匹配 iframe 来源和当前 runId，旧消息／重复完成不推进游戏。

仅重建独立动画审阅包时，复用相同影片：

```sh
node node_modules/vite/bin/vite.js build --config scripts/level2-animation-preview.config.mjs --outDir /tmp/gts-level2-preview --emptyOutDir
python3 scripts/package_level2_animation_preview.py /tmp/gts-level2-preview /absolute/path/to/partner-checkout
python3 tests/level2_animation_preview.py
python3 tests/level2_animation_results.py
LEVEL2_ANIMATION_SOURCE=/absolute/path/to/partner-checkout node --experimental-strip-types --test tests/level2_animation_pacing.mjs
```

浏览器测试读取真实 ZIP，检查五种片段的全程字幕、颜色、片内文字、遮罩、回调、重播、隐藏页面、减少动态效果及正常速度连播。
发布测试从完整游戏经开头、Level 1、全部 Level 2 阶段到 Level 3；结果页测试另行检查三种结果页的桌面／手机布局。
工具中的大体积内嵌 HTML 可将动作／导航时限提高到 120 秒；保留原断言和真实结束回调。
