# Gaming the System

三个关卡均可试玩。完整三关版与各关独立版复用同一套已确认玩法。

## 一次下载全部版本

**[下载完整试玩 ZIP：完整三关＋三个单独关卡](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Gaming-the-System-complete.zip?raw=true)**

解压整个 ZIP，用 Chrome 或 Edge 打开 **START-HERE.html**，再选择要玩的版本。下载后可离线运行，不需要安装软件。

| 版本 | 也可以直接打开 |
| --- | --- |
| 完整三关：Level 1 → 2 → 3 | `Full-game/Gaming-the-System.html` |
| 单独 Level 1 | `Level1/Level1.html` |
| 单独 Level 2 | `Level2/Level2.html` |
| 单独 Level 3 | `Level3/Level3.html` |

包内另有中英文 `START-HERE.txt`。仓库为私有；可以把 ZIP 直接发给没有仓库访问权限的试玩者。

需要分别下载时，请使用 [play/ 最新下载说明](play/README.md)。

## 当前版本

- Level 2 包含六项指标后的实验问题、Test more metrics、连续 10 → 25 → 100 增长，以及追分行为的结果呼应。
- Level 3 首次权重从 **— / — / —** 开始，由玩家操作生成分配；两次后可比较，第三次可选，不要求平均。
- 完整版保留关卡衔接、姓名和声音设置，以及 Level 2 选择到 Level 3 的可修改预选。
- 正式开场及成片尚未合并，剧情使用 placeholder；预览停在理论揭示，Design Lab 仍预留。刷新或重新打开会开始新游戏。

## 查找项目内容

| 内容 | 位置 |
| --- | --- |
| 所有最新试玩包 | [play/](play/README.md) |
| 开发、衔接与验证文档 | [docs/](docs/README.md) |
| 详细玩法及开发说明 | [项目说明](docs/PROJECT_DETAILS.md) |
| GitHub 分支与文件说明 | [仓库使用说明](docs/REPOSITORY_GUIDE.md) |
| 各关源码 | [Level 1](src/levels/level1/) · [Level 2](src/levels/level2/) · [Level 3](src/levels/level3/) |
| 共享模块 | [src/shared/](src/shared/) |
| 动画接入位置与场景对照 | [src/cinematics/](src/cinematics/README.md) · [接入说明](docs/ANIMATION_INTEGRATION.md) |
| 日常开发与正式发包 | [开发流程](docs/DEVELOPMENT_WORKFLOW.md) |

## 开发与发布

当前统一开发分支为 **level3-dev**。日常只保存开发进度、调试当前关卡和做相关检查；需要交付试玩包时才完整打包，并同步 level1-preview、level2-preview 和 level2-dev。历史 ZIP、标签和版本化验证报告保留。

日常开发（依赖安装说明见 [项目说明](docs/PROJECT_DETAILS.md)）：

```sh
npm run dev
npm run dev:level3
npm run check
```

准备交付时：

```sh
npm run package:previews
npm run test:release
```

使用 Node.js 20.19+、22.12+ 或更新版本，以及 Python 3。统一打包只做一次类型检查，再构建四个入口、生成六个包；`play/LATEST.json` 记录最近一次打包的校验值。具体检查按 [开发流程](docs/DEVELOPMENT_WORKFLOW.md) 选择。
