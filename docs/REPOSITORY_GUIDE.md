# GitHub 使用说明

统一在 **level3-dev** 分支中保留完整项目，以及各关独立试玩和多关连玩
的最新版。每关有自己的源码文件夹；不同试玩入口复用同一套源码。

## 最新试玩入口

| 要找的内容 | 下载 | 解压后打开 |
| --- | --- | --- |
| Level 1＋2＋3 连玩 | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| Level 1 单独试玩 | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | Level1.html |
| Level 2 单独试玩 | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | Level2.html |
| Level 3 单独试玩 | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-play.zip?raw=true) | Level3.html |

以后更新时替换这四个固定文件名的包，分享入口保持不变。旧版带版本号的
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
| 全部试玩包及说明 | [play](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/play) |

```text
src/
  Gameplay.tsx       各关之间的衔接和姓名传递
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

本次四个分支指向同一次发布。分支本身不会自动同步；每次发布已认可的
修改时，要一起重新打包并更新预览分支。历史版本通过带版本号的 ZIP 或
Git 提交记录查找，v6 原始提交仍是 `336c59f`。

开发时使用 `npm run package:previews` 一次重建连玩、Level 1 独立和
Level 2 / Level 3 独立四个包，避免只更新其中一个。`play/LATEST.json` 记录源码及
文件校验值。发布前用 `python tests/release.py` 验证实际包的内容与衔接。

Level 3 已可试玩：选出三个重点、分配并逐项确认 100% 权重、观察反应，
再根据第一次结果做平衡或对照测试。两次均衡程度不同的结果并排比较。
剧情和最终理论揭示仍为 placeholder；Design Lab 继续预留。
