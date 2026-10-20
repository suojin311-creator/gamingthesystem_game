# 100 metric：从同伴原版重新剪辑的独立预览

本轮只交付 `play/Level2-100metrics-preview.zip`。完整解压后打开 `START-HERE.html`。
现有完整游戏、Level 3 包、Level 2 接入代码及此前的全部片段预览包保持不变。

来源为 `Mg614/gaming-the-system` 的 `feature/cinematic-level2-consequences`，
固定提交 `c8c1c83456c4e67cf627df399bfb67b3a9792adb`；原目录与素材保持只读。
本轮直接使用原版 `Level2ConsequencesSequence`、ChecklistSystem 和人物表演，
独立适配放在 `scripts/metric100-preview/`，不沿用之前的 100 metric 成片裁剪。

- 从原片 hundred 段 0.25 秒的 Criterion 66 落笔特写开始。
- 保留后续原版 Coverage map 与完成过程，纸面标题、计数、证据便笺、
  E1/E2/E3、criteria 条目、gaps 与页脚全部保留。
- 全程移除纸面之外的 LEVEL 02 / MORE METRICS、100 REQUIREMENTS、
  Close the remaining gaps、Level 2 · cinematic candidate 等标题及角标节点。
- 原版无字幕的 perfect 人物停顿不再播放；纸面完成后直接进入 reflection 对话画面，
  进入后 1 秒显示第一句。转场叠化期间计时继续，不额外延后字幕。
- 保留原版最后两句 You 台词；第一句保留完整阅读时间和同一表情，
  第二句与新的表情一起叠化进入，沿用现有约 220 词/分钟的阅读规则。
- 字幕透明、描边及阴影沿用已确认标准；You 暖金色 `#ffe2a3`，
  Alex 淡蓝色 `#cceeff`，身份居中放在字幕正上方。保留老师台词斜体。
- 最后一句结束即停止并停留在该画面，不进入 priority、优先级卡或其他尾页。
  左下角提供暂停、重播与进度工具；没有额外片内文字。原素材无音频。

构建与定向验证：

```sh
LEVEL2_ANIMATION_SOURCE=/absolute/path/to/pinned-original \
node scripts/metric100-preview/build.mjs
python3 tests/metric100_preview.py
```

浏览器直接读取实际 ZIP，检查起播的 criteria 66、完整纸面、清除角标、
实播转场中的 1 秒字幕延迟、字幕视觉、最后停留与重播；不重复完整游戏路径。
`play/LEVEL2_100METRICS_PREVIEW.json` 记录来源、构建与包哈希。
本次结果见同目录的独立验证记录 `docs/METRIC100_PREVIEW_VALIDATION.json`。
