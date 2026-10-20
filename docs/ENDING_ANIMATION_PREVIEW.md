# Ending 独立动画预览

下载 `play/Ending-animation-preview.zip`，完整解压后打开 `START-HERE.html`。
影片进入即占满浏览器视口，保持完整的 16:9 构图；不强制调用浏览器的全屏权限。
左下角「预览控制」可暂停、拖动、重播或跳到理论揭示。

本次仅交付独立动画审阅包，未替换当前完整游戏中的 comparison/theory placeholder，
六个正式游戏 ZIP 保持不变。Level 3B 没有导入。

## 已确认的适配

- 开头不再展示固定的 uneven / near-equal 对照，不预设玩家测试过平均分配，
  也不宣称 effort 一定变得平均或发生变化。
- 通用对白为 You「Did changing the weights change why you were working?」、
  Alex「I was still working out what earns marks.」、
  You「Maybe it’s not just about finding the perfect weights…」。
- 开头复用最后一次实际试验的最后一个任务；Level 3 闪回依次复用该轮三个实际任务。
  `src/cinematics/ending/input.ts` 调用当前游戏的 `cinematicRequest` 和 `weightedSceneReply`，
  影片只读取它提供的 shot，不按同伴的阈值重新推断表现。
- 预览提供三种示例历史：没有 near-even 且 effort 改变、没有 near-even 且 effort 不变、
  三次真实试验。它们是审阅样例，不会被添加到玩家的游戏历史里。
- 复用已有任务、清单和办公室素材，不使用被拒绝的单独 Alex 人像、女孩侧脸、
  同学反应等杂镜头。任务左上角显示实际指标名称。
- You 与字幕同为暖金色 `#ffe2a3`；Alex 与字幕同为浅蓝色 `#cceeff`。
  身份居中放在字幕正上方，透明字幕、描边和阴影沿用现有 Level 3A。
- 镜头共用 `cinematic-dissolve.mjs` 的约半秒叠化，隐藏页面暂停。
  办公室切入后立即开始问题，不保留原先四秒的无对白等待。
- 删除办公室里虚构的全绿结果面板。最终停留在 Goodhart’s Law，
  引文在逗号后明确换行，字号放大；不再进入后续 recap / handoff 画面。
- 用户最新要求覆盖了早先「不制作 Design Lab 按钮」的约定：
  现在在理论画面下方浮现醒目的金色按钮，暂为 `aria-disabled` 的展示入口，
  不发送 handoff，不挂载或跳转到现有 Design Lab。

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

交付目录需要安装与 lockfile 一致的依赖。影片、素材和控件都内嵌进单一 HTML，
无需联网或安装；没有原始音频，保持静音。

验证直接读取实际 ZIP：检查三种历史的匹配、字幕及身份、布局、软转场、
最终停留和不跳转的按钮、窄屏适配、重播及隐藏页暂停。按用户要求不重复完整游戏路径。
包哈希和固定来源记录于 `play/ENDING_ANIMATION_PREVIEW.json`；
本次定向结果附于 `docs/PREVIEW_VALIDATION.json` 的 `endingPreview`，
其中原游戏验证仍对应未变化的六个游戏包。
