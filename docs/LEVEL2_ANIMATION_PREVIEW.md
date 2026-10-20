# Level 2 同伴动画：合并前独立预览

这是供用户先看动画的独立候选版，尚未接入现有游戏。先审阅动画，再根据用户反馈决定接入调整。

## 最新内容在哪里

- 同伴源码：`Mg614/gaming-the-system` 的 `feature/cinematic-level2-consequences`。
- 本次固定提交：`c8c1c83456c4e67cf627df399bfb67b3a9792adb`。
- 同伴最新说明：该提交的 `docs/cinematics/CIN02_CHARACTER_CANDIDATE.md`；`CIN02_INTERIM.md` 是较早状态。
- 下载：本仓库 `animation/opening-integration` 分支的 `play/Level2-animation-preview.zip`。
- 来源、文件校验与当前验证：`play/LEVEL2_ANIMATION_PREVIEW.json`。
- 现有开头＋Level 1 动画＋三关完整版仍使用 `play/Full-game-play.zip` 或 `play/Gaming-the-System-complete.zip`，本次未替换。

## 怎么看

解压整个 ZIP，用 Chrome 或 Edge 打开 **START-HERE.html**，先选 **完整串联 / Full chain**。
它顺序演示三项、六项、10、25、100 项与结尾。原预览提供暂停、重播、进度条和 1×／2×／4×，建议先用 1× 看节奏。

入口还包括 Visible／Quality／Mixed 三种三项分支、Six、10、25、100＋结尾、只看结尾以及 Checking 勾选动作。
完整串联模拟游戏之间的交接，不是已合入的游戏流程。当前交付没有音频素材，因此保持静音；未生成替代音频或图像。

## 原动画与导出的边界

同伴的源码、对白、镜头、动作、时长、图片和 lockfile 都保留原样，不向同伴仓库写入。
外部 Vite 配置仅在构建内存中把原 `Level2DevPreview` 设为独立入口，并将原 Opening 链接改为返回本地选择页。
所有运行素材内嵌到单个 `Level2-animation.html`，下载后无需网络和安装工具。

这个预览独立打包，不执行正常四入口／六 ZIP 的游戏发布流水线，不覆盖已确认游戏、Level 1 独立实验或历史包。

## 复现导出

使用固定在上述提交的同伴只读目录，位于游戏仓库外。Node.js 24 可运行以下命令：

```sh
cd /absolute/path/to/partner-checkout
npm ci --ignore-scripts --cache /tmp/gaming-level2-preview-npm-cache
npm run typecheck
node --experimental-strip-types --test tests/cinematics/level2.test.ts

cd /workspace/gamingthesystem_game
LEVEL2_ANIMATION_SOURCE=/absolute/path/to/partner-checkout \
  node /absolute/path/to/partner-checkout/node_modules/vite/bin/vite.js build \
  --config scripts/level2-animation-preview.config.mjs \
  --outDir /tmp/gts-level2-preview --emptyOutDir
python3 scripts/package_level2_animation_preview.py /tmp/gts-level2-preview /absolute/path/to/partner-checkout
python3 tests/level2_animation_preview.py
```

打包脚本校验固定提交和未修改的同伴文件，并记录全部原文件的组合校验值。
浏览器验证读取真实 ZIP，在断网状态下检查入口、原控制、各片段完成通知和一遍正常速度串联；输出在忽略的 `test-results/`。
人工画面、阅读节奏与动画品质仍由用户审阅。本次独立预览通过不代表正式游戏接入已完成。

## 后续合并时保留的边界

按当前 `ANIMATION_INTEGRATION.md` 和 `LEVEL2_HANDOFF.md` 接收真实三项分支、六项和最终场景请求。
同伴预览中的 `three`／`six`／`10`／`25`／`100` 是展示分段，不能直接据此改变游戏协议或插入额外操作。
现有游戏的 10 → 25 → 100 连续增长仍由游戏负责；预览中的优先级页也不能覆盖 Level 3 的真实选择和规则。
未来接入必须保留玩家姓名、声音设置、Level 2 原始三项选择、真实结束回调与一次性完成约束。
