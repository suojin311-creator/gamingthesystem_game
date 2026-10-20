# 动画合并：当前接入说明

本页是接下来动画合并的起点。已确认的玩法保留在 `src/levels/`；完成的动画代码和所需素材放入 [src/cinematics/](../src/cinematics/README.md)。日常预览与正式发包使用 [开发流程](DEVELOPMENT_WORKFLOW.md)。

Ending 现有[独立动画审阅包](ENDING_ANIMATION_PREVIEW.md)：通用开头不预设平均权重，
只回顾真实试验；全屏布局，理论揭示后停留并展示暂不跳转的 Design Lab 按钮。
尚未替换游戏的 comparison/theory placeholder。

当前 `animation/opening-integration` 分支已接入开场：`FullGame` 先显示
`src/cinematics/opening/Opening.tsx`，完成三名学生观察后，返回办公室显示两句思考，再进入与后续关卡共用样式的
Level 1 过渡页。Choose a metric 后，用已确认姓名挂载 Gameplay。邮件和下一名
未观察学生用无圆框的发光箭头引导，三个人像图标显示完成状态。镜头和场景切换
等待实际动画完成，办公室镜头在黑场遮罩下复位。点击邮件后取消第二次镜头放大，
改为独立阅读窗淡入，按钮出现即可使用；标题与办公室思考衔接到第一关的指标选择。开场样式限于 `.opening-scene`，不覆盖关卡按钮和字体。
稳定 `level3-dev` 与预览分支保留原游戏版；本分支的包供动画衔接审阅。

Level 3A 已接入每次 `level3.weights` 的三项实际表现，严格读取当前游戏给出的
effort，不采用同伴可能不同的权重阈值；不使用 Level 3B。数字页、无关切镜与
独立人像已裁剪，当前指标名显示在左上角。合并前的 Level 2 版本备份于
`archive/before-level3a-integration-20261020`（`2411baa`）。见 [Level 3A](LEVEL3A_ANIMATION.md)。
Level 1／2／3A 内部换景现共用短叠化，替代反复的黑幕切换。

Level 2 也已按用户要求接入原有三项、六项和最终清单 placeholder。
只保留所需片段，不插入同伴额外的增长或优先级页；三项从 Alex 完成要求的
第一句开始。字幕身份统一为 Alex／You，并保留 checklist 原有条目文字；颜色、阅读时间及遮罩转场沿用 Level 1。
结果页移除师生复盘聊天，保留现有观察和两张状态卡，不增加说明文字。
合并前源码和六个游戏包已校验备份到
`archive/before-level2-animation-integration-20261020`（`762ce7e`）。
构建、裁剪与验证说明见 [Level 2 动画](LEVEL2_ANIMATION_PREVIEW.md)。

Level 1 已按用户确认的独立预览合入默认 Gameplay：`LevelOneExperience`
复用唯一的 LevelOne、正式 iframe 动画及结果核算页。完整游戏核算页进入
Level 2；单独 Level 1 保留 Try another metric。开场、关卡操作对话、动画
老师标签和祝贺邮件均读取开场确认的同一个姓名。开场与 Level 1 共用
`src/shared/data/cinematicPalette.js`：老师暖金色，Alex／学生浅蓝色。
合并前的完整源码及试玩包保存于 `archive/opening-before-level1-merge-20261020`
（`32a91fe4bfb1cb193040410c846ebc165f8b9d5d`）。

### Level 1 动画构建

同伴原文件保持只读。首次或动画源码变化后，使用已固定的
`Mg614/gaming-the-system@1bdd0c442c4b345b3bd37d6f541742d4e55c732f`
交付目录，先在该目录按其 lockfile 安装依赖，再运行：

```sh
LEVEL1_ANIMATION_SOURCE=/absolute/path/to/partner-checkout npm run cinematic:prepare
```

产物仅写入本仓库被忽略的 `node_modules/.cache/level1-cinematic/`。
后续 dev/build/package 命令自动校验并复用缓存；相关脚本或字幕配色变化时
要求重新构建，避免旧影片混入新版本。也可用 LEVEL1_CINEMATIC_HTML 指向
由当前脚本刚生成的影片 HTML。最终所有游戏 HTML 都内嵌影片，可离线运行。

## 先接真实交付，再接已有接口

接到成片源码时，先确认其入口、素材引用、依赖以及真正的结束事件，再做适配。保留同伴已经完成的脚本和同伴互动，不另外编写一套剧情、重复开场或新增操作页。

开场保留现有姓名输入。真正结束时挂载 `<Gameplay playerName={playerName} />`，使用已确认姓名；三关运行期间保持 Gameplay 挂载，避免关卡状态被动画反复重建。

课堂动画通过 `Gameplay` 已有的三个 renderer 替换完整 placeholder：

```tsx
<Gameplay
  playerName={playerName}
  renderLevelOneCinematic={(request, complete) => (
    <LevelOneAnimation request={request} onComplete={complete} />
  )}
  renderLevelTwoCinematic={(request, complete) => (
    <LevelTwoAnimation request={request} onComplete={complete} />
  )}
  renderLevelThreeCinematic={(request, complete) => (
    <LevelThreeAnimation request={request} onComplete={complete} />
  )}
/>
```

上面是接口的用法示例。默认 Level 1／2 已通过 `LevelOneCinematic`／`LevelTwoCinematic` 接入真实成片，相应 renderer 仍可用于覆盖；`LevelThreeAnimation` 仍代表后续交付的适配组件。renderer 得到真实 `request` 和当前场景的 `complete`。只在场景实际结束时调用 `complete()`；不要用猜测时长推进，也不要在动画外再播放一份 placeholder。

## 场景对照

| 位置 | 现有请求或镜头 ID | 动画需要读取 |
| --- | --- | --- |
| 开场 → Level 1 | 开场真实结束回调 | 开场确认的 `playerName` |
| Level 1 | `level1.prep`、`level1.part`、`level1.focus`、`level1.discuss`、`level1.reflect`、`level1.peer` | `metricId`、`playerName` |
| Level 2 三项 | `level2.three.visible`、`level2.three.quality`、`level2.three.mixed` | 实际 `selectedMetricIds`、`branch`、`playerName` |
| Level 2 六项 | `level2.six` | 原来的三项选择，以及 `metricCount: 6` |
| Level 2 一百项结尾 | `level2.checklist` | 原来的三项选择，以及 `metricCount: 100` |
| Level 3 每轮观察 | 总请求 `level3.weights`；内有三个 `level3.<metricId>.<low/medium/high>` 镜头 | 当前 `shots` 的指标、权重和 effort；实际历史 `runs` |
| Alex's response | `level3.compare` | 两次或三次真实 `runs`，不要求出现平均分配 |
| Goodhart's theory reveal | `theory.reveal` | 同一姓名、实际实验历史；预览在这里结束 |

Level 2 的10和25项是游戏侧现有连续增长过程，不是新增课堂场景请求。不要为了动画合并再添加三次点击或新剧情。

## 玩法与动画各自负责什么

- 游戏负责 metric 选择、权重规则、真实实验记录和关卡状态；动画读取请求，不重新计算一套 effort。
- 动画负责同伴已经写好的画面、对白和结束信号；尽量局部组织样式和素材引用，接入时检查是否影响其他关卡。
- Level 2 的选择继续传到 Level 3，允许玩家修改。不要通过重挂整场游戏来切换动画。
- 检查已有 Sound off 对接入后的音乐/音效是否仍有效；动画卸载时结束其自身播放。
- 不新增 Design Lab 跳转。第三关不强制平均，不虚构没有测试过的参考结果。

## 每次只合并一个边界

先接开场到 Level 1；再按 Level 1、Level 2、Level 3 的真实场景交付逐步替换。每接好一类，就在对应 Vite 入口验证姓名、选项、真实结束回调、重播、静音和相关尺寸。通过后保存开发分支；到需要整体试玩时再统一发包。

需要字段细节时再读 [开场接口](OPENING_HANDOFF.md)、[Level 1](LEVEL1_HANDOFF.md)、[Level 2](LEVEL2_HANDOFF.md)、[Level 3](LEVEL3_HANDOFF.md)。旧说明里的特定 App/beat 名称要对照最终交付源码使用，本页不假定成片仍采用旧文件结构。
