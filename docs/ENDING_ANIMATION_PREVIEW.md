# Ending 独立动画预览

下载 `play/Ending-animation-preview.zip`，完整解压后打开 `START-HERE.html`。
影片进入即占满浏览器视口，保持完整的 16:9 构图；不强制调用浏览器的全屏权限。
左下角「预览控制」可暂停、拖动、重播或跳到理论揭示。

本次仅交付独立动画审阅包，未替换当前完整游戏中的 comparison/theory placeholder，
六个正式游戏 ZIP 保持不变。Level 3B 没有导入。

## 已确认的适配

- 开头不再展示固定的 uneven / near-equal 对照，不预设玩家测试过平均分配，
  也不宣称 effort 一定变得平均或发生变化。
- 开头直接淡入办公室，You「Maybe it’s not just about finding the perfect weights…」。
  移除重复问答，不再冻结单个任务画面约 11 秒。
- 三关各保留一个短动作：Level 1 的任务操作、Level 2 的最后一次清单勾选、
  Level 3 最后一次真实试验中的最后一个任务。三段各 2.1 秒，加叠化约 8 秒；
  移除后面再次叠放三张画面的重复展示。
  `src/cinematics/ending/input.ts` 调用当前游戏的 `cinematicRequest` 和 `weightedSceneReply`，
  影片只读取它提供的 shot，不按同伴的阈值重新推断表现。
- 预览提供三种示例历史：没有 near-even 且 effort 改变、没有 near-even 且 effort 不变、
  三次真实试验。它们是审阅样例，不会被添加到玩家的游戏历史里。
- 复用已有任务、清单和办公室素材，不使用被拒绝的单独 Alex 人像、女孩侧脸、
  同学反应等杂镜头。整个 ending 都不显示左上角 metric 名称；Level 3A 本身仍保留。
- You 与字幕同为暖金色 `#ffe2a3`。本次 ending 没有 Alex 的重复对白。
  身份居中放在字幕正上方，透明字幕、描边和阴影沿用现有 Level 3A。
- 镜头共用 `cinematic-dissolve.mjs` 的约半秒叠化，隐藏页面暂停。
  回忆后回到办公室立即显示 You「Am I improving learning, or just improving the numbers?」。
  之后逐渐压暗并揭示理论，不保留无对白的建立镜头。
- Level 3 回忆下方改为「The weights changed. Learning still came second.」，
  明确学习被放到次要位置，不宣称所有真实试验的 effort 都发生改变。
- 删除办公室里虚构的全绿结果面板。最终停留在两行通俗反思：
  「When the number becomes the goal, / learning can get left behind.」。
  Ending 不出现 Goodhart 名称或引文，也不再进入后续 recap / handoff 画面。
- 背景恢复较早版本的深色办公室，撤回用户拒绝的全屏灰绿处理。
  最后两行反思采用开场办公室旁白的 Georgia、暖白 `#fff5e3`，
  以斜体文字和按钮之间的留白建立层级，不使用理论标题或金色发光。
- 用户最新要求覆盖了早先「不制作 Design Lab 按钮」的约定：
  现在直接导入开场 `styles.css`，使用 TAKE YOUR SEAT / BACK TO OFFICE 的同一个
  `opening-action` 砖红色按钮，暂为 `aria-disabled` 的展示入口，
  不发送 handoff，不挂载或跳转到现有 Design Lab。
- 按钮文字为 ENTER DESIGN LAB。已采纳的 Design Lab 后续文案单独记录于
  [衔接文案](ENDING_DESIGN_LAB_COPY.md)：入口写作题替换为
  「How would you know Alex is really learning?」，最后才揭示 Goodhart，
  使用短句「When a measure becomes a target, it ceases to be a good measure.」。
  本次只修改 ending，未改动独立的 `feature/design-lab-local`。

## 固定来源与构建

同伴 ending：`Mg614/gaming-the-system`，
`feature/cinematic-ending-theory-reveal`，
`e467998dfb07abc028e4e0fcb5567006e4eaa07d`。
实际任务素材：已接入的 Level 3A，
`ba9f81ee619c14b3342104228cdd2a5cc2bc2b3b`。
两个交付目录都保持只读；局部适配在本仓库构建时执行。

```sh
ENDING_ANIMATION_SOURCE=/absolute/path/to/ending-delivery \
LEVEL3_ANIMATION_SOURCE=/absolute/path/to/level3a-delivery \
npm run package:ending-preview
npm run check
python3 tests/ending_preview.py
```

只调整结尾文案/排版时可运行 `python3 tests/ending_preview.py --closing-only`，
检查实际 ZIP 的 Level 3 文案、最终两行文字、按钮、不同窗口尺寸和离线资源。

交付目录需要安装与 lockfile 一致的依赖。影片、素材和控件都内嵌进单一 HTML，
无需联网或安装；没有原始音频，保持静音。

验证直接读取实际 ZIP：检查办公室开头、三种历史的真实表现、短动作、无 metric 标题、布局、软转场、
最终停留和不跳转的按钮、窄屏适配、重播及隐藏页暂停。按改动选择相关检查，
按用户要求不重复完整游戏路径。
包哈希和固定来源记录于 `play/ENDING_ANIMATION_PREVIEW.json`；
本次定向结果附于 `docs/PREVIEW_VALIDATION.json` 的 `endingPreview`，
其中原游戏验证仍对应未变化的六个游戏包。
