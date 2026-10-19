# 动画合并：当前接入说明

本页是接下来动画合并的起点。已确认的玩法保留在 `src/levels/`；完成的动画代码和所需素材放入 [src/cinematics/](../src/cinematics/README.md)。日常预览与正式发包使用 [开发流程](DEVELOPMENT_WORKFLOW.md)。

当前 `animation/opening-integration` 分支已接入开场：`FullGame` 先显示
`src/cinematics/opening/Opening.tsx`，完成三名学生观察并在办公室选择
Choose a metric 后，用已确认姓名挂载 Gameplay。邮件和未观察学生用箭头引导，
三个人像图标显示完成状态。开场样式限于 `.opening-scene`，不覆盖关卡按钮和字体。
稳定 `level3-dev` 与预览分支保留原游戏版；本分支的包供动画衔接审阅。

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

上面是现有接口的用法；三个 Animation 名称代表交付源码的适配组件，尚未创建替代成片。renderer 得到真实 `request` 和当前场景的 `complete`。只在场景实际结束时调用 `complete()`；不要用猜测时长推进，也不要在动画外再播放一份 placeholder。

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
