# Ending 独立动画预览

下载 `play/Ending-animation-preview.zip`，完整解压后打开 `START-HERE.html`。
影片保持完整的 16:9 构图，最后的 Design Lab 任务入口页铺满视口并适配窄屏文字；
不强制调用浏览器的全屏权限。
左下角「预览控制」可暂停、拖动、重播或跳到 Design Lab 入口。

已确认的 ending 现已接入游戏：点击 Watch Alex’s response 直接全视口播放，
替换默认 comparison/theory 占位链，最后停留在入口页；不再提前揭示 Goodhart。
六个正式游戏 ZIP 统一更新。独立审阅 ZIP 保留为已确认版本；Level 3B 没有导入。
游戏传入实际两次/三次试验，并在完整流程中保留 Level 1 的实际 metric。
单独进入 Level 3 时，早期关卡回忆只作通用示意，Level 3 使用真实试验。

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
  开头身份居中放在字幕正上方，透明字幕、描边和阴影沿用现有 Level 3A。
  回忆后的反思句移至画面中央并去掉 You；0.6 秒淡入，随后配合办公室压暗渐隐。
- 镜头共用 `cinematic-dissolve.mjs` 的约半秒叠化，隐藏页面暂停。
  回忆后回到办公室立即显示 You「Am I improving learning, or just improving the numbers?」。
  之后逐渐压暗并衔接 Design Lab 入口。入口改为全视口时，对整张旧画面连同黑边
  做 0.65 秒叠化，避免构图比例直接跳变。
- Level 3 回忆下方改为「The weights changed. Learning still came second.」，
  明确学习被放到次要位置，不宣称所有真实试验的 effort 都发生改变。
- 删除办公室里虚构的全绿结果面板。最后不再使用孤立的格言式总结和短横线，
  改成明确的 Design Lab 任务入口：
  - NEXT · DESIGN LAB
  - Share what real / learning looks like.
  - ENTER DESIGN LAB →
  用户最新要求删除两段说明文字（游戏经历关联及 reflection/read/vote 步骤）。
  Ending 不出现 Goodhart 名称或引文，也不再进入同伴额外的 recap / handoff 画面。
- 背景恢复较早版本的深色办公室，撤回用户拒绝的全屏灰绿处理。
  最后一页以办公室场景和渐暗背景承托右侧任务文字，标题使用 Georgia、暖白
  `#fff5e3`，入口标识和按钮沿用开场字体。保留标题与行动按钮的简洁层级，
  不增加抽象装饰。移动窄屏使用完整视口及可读字号。
  标题与按钮同时挂载、共同淡入，避免按钮晚出现使文字重新居中上移。
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
检查实际 ZIP 的删减文案、居中反思句、按钮、七种窗口布局、
桌面/竖屏实时叠化、共同淡入、布局稳定、重播和离线资源。

交付目录需要安装与 lockfile 一致的依赖。影片、素材和控件都内嵌进单一 HTML，
无需联网或安装；没有原始音频，保持静音。

验证直接读取实际 ZIP：检查办公室开头、三种历史的真实表现、短动作、无 metric 标题、布局、软转场、
最终停留和不跳转的按钮、窄屏适配、重播及隐藏页暂停。按改动选择相关检查，
按用户要求不重复完整游戏路径。
包哈希和固定来源记录于 `play/ENDING_ANIMATION_PREVIEW.json`；
本次定向结果附于 `docs/PREVIEW_VALIDATION.json` 的 `endingPreview`，
其中原游戏验证仍对应未变化的六个游戏包。

## 游戏接入验证

`npm run package:previews` 统一生成六包；
`python3 tests/ending_integration_release.py` 验证实际包、两次非平均试验、
默认 comparison → 全视口 ending、真实任务、无审阅控件及最终停留。
Design Lab 仍在 `feature/design-lab-local` 单独维护，未连接课堂地址。
