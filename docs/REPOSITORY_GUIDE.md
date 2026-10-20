# GitHub 使用说明

> 当前开头＋Level 1／2 动画＋三关整合版在 `animation/opening-integration`，最新入口见 [play/README.md](../play/README.md)。
> Level 2 接入前完整版本保存在 `archive/before-level2-animation-integration-20261020`（`762ce7e`）。
> 下方 `level3-dev` 与预览别名说明属于保留的稳定游戏线，不是最新动画整合版。

统一在 **level3-dev** 分支中保留完整项目，以及各关独立试玩和多关连玩
的最新版。每关有自己的源码文件夹；不同试玩入口复用同一套源码。

## 最新试玩入口

优先下载 [全部版本总 ZIP](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Gaming-the-System-complete.zip?raw=true)。解压后打开 START-HERE.html，可进入完整三关或三个独立关卡，包内另有中英文说明。

| 要找的内容 | 下载 | 解压后打开 |
| --- | --- | --- |
| Level 1＋2＋3 连玩 | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| Level 1 单独试玩 | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | Level1.html |
| Level 2 单独试玩 | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | Level2.html |
| Level 3 单独试玩 | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-play.zip?raw=true) | Level3.html |

以后更新时一起替换总包、四个独立/完整包及原双版本包，分享入口保持不变。旧版带版本号的
ZIP 留作历史记录，不再当作最新版入口。仓库为私有；试玩者没有 GitHub
访问权限时，可以直接把下载后的 ZIP 发给他们。

Level 1 单独包已补齐后来制作 Level 2 时对 Level 1 的改进：学生行为警示、
更早出现的对白、Alex 的双气泡和不同 emoji、精简后的预测页面等。连玩版
现已接通第三关；Level 1、Level 2 的独立包仍停在各自关卡末尾。正式开场与成片尚未合并。

## 源码位置

| 内容 | 入口 |
| --- | --- |
| 当前开发项目 | [level3-dev](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev) |
| Level 1 源码 | [src/levels/level1](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level1) |
| Level 2 源码 | [src/levels/level2](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level2) |
| Level 3 源码 | [src/levels/level3](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level3) |
| 共用模块 | [src/shared](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/shared) |
| 成片动画与素材接入 | [src/cinematics](../src/cinematics/README.md) |
| 动画场景与回调对照 | [动画接入说明](ANIMATION_INTEGRATION.md) |
| 全部试玩包及说明 | [play](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/play) |

```text
src/
  Gameplay.tsx       各关之间的衔接和姓名传递
  cinematics/        后续导入的成片动画和素材
  levels/
    level1/          第一关
    level2/          第二关
    level3/          第三关
  shared/            各关共用的对话、图标、声音等
  assets/            图片素材
docs/                衔接、开发和验证说明
play/                各关独立与多关连玩的最新包，以及历史存档
scripts/             统一打包命令
```

## 分支与更新方式

- **level3-dev**：当前统一开发入口，后续修改在这里继续。
- **level1-preview**：已同步到这次发布，旧分支里的单关 Level 1 也能下载最新版。
- **level2-preview**：已同步到这次发布，提供同样的最新单关和连玩包。
- **level2-dev**：保留此前开发历史，本次也同步；后续开发使用 level3-dev。

日常只在 level3-dev 保存进度，不必为每次修改更新 ZIP 或同步其他分支。
准备交付试玩版本时，四个分支再指向同一次经过验证的发布。仓库当前默认
分支为 level1-preview，显示最近发布；日常开发分支可以领先它。
历史版本通过带版本号的 ZIP 或
Git 提交记录查找，v6 原始提交仍是 `336c59f`。

日常使用 Vite 调试当前关卡；正式发包时使用 `npm run package:previews`，
只做一次类型检查，再重建四个入口及全部六个 ZIP。`play/LATEST.json` 记录最近打包的源码及
文件校验值。发布前用 `python tests/release.py` 验证实际包的内容与衔接。
完整命令和按改动选择检查的方法见 [开发流程](DEVELOPMENT_WORKFLOW.md)。

Level 3 已可试玩：选出三个重点、分配并逐项确认 100% 权重、观察反应，
再根据实际观察自由调整；两次后可以比较，第三次可选，不强制平均或不同均衡程度。首次权重显示未分配，由玩家拖动后生成。
剧情和最终理论揭示仍为 placeholder；Design Lab 继续预留。
