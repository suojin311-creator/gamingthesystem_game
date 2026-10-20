# Level 3A 接入与审阅

当前动画分支将同伴的 **Level 3A** 接入每次权重观察的 `level3.weights`。
只使用 `Mg614/gaming-the-system` 的 `feature/cinematic-level3-metric-adaptations`，
固定提交 `ba9f81ee619c14b3342104228cdd2a5cc2bc2b3b`。同伴源码及素材保持只读。
**不使用 Level 3B**；`level3.compare` 和 `theory.reveal` 保留现有占位内容。

## 合并前备份

`archive/before-level3a-integration-20261020` 保存合并了 Level 2 的完整游戏与源码，
提交 `2411baa78192d764d07a8d3952ebb5d4f02a878c`。推送前已按当时 LATEST.json
核对六个游戏 ZIP 的 SHA-256。更早的备份和稳定游戏分支保持原样。

## 结局与动画对应

游戏的 `effortAt` 和 `cinematicRequest` 继续是规则来源；影片不读取百分比重新分档。
`request.shots` 的 prep／part／focus／discuss／reflect／peer 分别映射为同伴正式指标 ID；
low／medium／high 直接映射为 Low／Medium／High，顺序完全保留。
这包含 49/26/25、45/45/10、接近分配和逐级差异等情况；不是按旧版绝对阈值匹配。
字幕读取游戏当前 `weightedSceneReply`，中等表现仍保留达标后停止的含义。

`src/cinematics/level3/LevelThreeCinematic.tsx` 只负责接入与真实完成消息；
iframe 的来源、runId 和一次性回调共同防止重播或旧消息误推进。
游戏保留原两次实验、可选第三次、真实结果记录、比较和理论入口。

## 镜头与视觉

- 直接播放三个实际任务片段，移除带权重数字的开头／结尾纸面页。
- 移除用户拒绝的单独 Alex 人像；高专注使用对应指标板中的实际任务画面。
- 讨论从 Alex 本人的表现开始，跳过女孩侧脸。参与移除同学反应、反复手部特写；
  其余指标从任务动作开始，删除空场及重复建立镜头。
- 保留能说明表现差异的阅读、勾选、书写、回复、讨论提示等动作。
- 左上角显示当前指标的完整名称，随三个片段更新；不添加权重或状态编号。
- Alex 标签与字幕为 `#cceeff`；老师身份使用 You 与 `#ffe2a3`。当前保留的任务
  台词都是 Alex 的发言，不为补标签另加老师旁白。字幕透明、细描边与阴影沿用共同配色。
- 三段之间使用约半秒叠化；必要的任务内画面变化使用更短叠化。旧画面冻结后淡出，
  新画面先解码；隐藏页面暂停时钟，减少动态效果时直接切换。
- Level 1 的课堂→办公室、Level 2 内部镜头也使用同一叠化工具；未重剪它们的内容。

## 构建与 ZIP

```sh
LEVEL3_ANIMATION_SOURCE=/absolute/path/to/level3a-delivery npm run cinematic:prepare
node node_modules/vite/bin/vite.js build --config scripts/level3-animation-preview.config.mjs --outDir /tmp/gts-level3a-preview --emptyOutDir
python3 scripts/package_level3_animation_preview.py /tmp/gts-level3a-preview
npm run package:previews
```

首次构建 Level 1／2 缓存仍按各自接入说明提供原交付位置。
下载 `play/Level3A-animation-preview.zip`，解压后打开 START-HERE.html；
两组三项指标与四种真实权重模式可暂停、重播和拖进度。
该包与游戏嵌入同一影片；完整游戏仍为 `play/Full-game-play.zip`。
没有音频素材，影片保持静音。

完整版本总包的各关入口共享 Full-game/Gaming-the-System.html，避免重复内嵌影片
超过 GitHub 的单文件限制；保持解压后的文件夹在一起。单独关卡 ZIP 仍含独立 HTML。

## 有针对性的验证

- `tests/level3_animation_mapping.mjs`：全部 4,851 种合法分配、所有三项组合及顺序，
  18 个状态映射、剪辑窗口和阅读时间。
- `tests/level3_animation_preview.py`：真实游戏请求覆盖 18 种表现，检查起始／中段／末尾、
  数字与杂镜头移除、标题、蓝色字幕、叠化、隐藏页和一次完成。
- `tests/cinematic_dissolves.py`：直接检查 Level 1／2 改动的转场及反思字幕。
- 当前 ZIP、单关接入和共享入口检查记录在 PREVIEW_VALIDATION.json。
  按用户要求不重复整条开场→三关流程；早期全路径报告只保留为历史依据。
