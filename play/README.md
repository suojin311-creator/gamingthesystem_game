# 最新试玩下载 / Latest downloads

## 推荐：一个 ZIP 包含所有版本

**[Gaming-the-System-complete.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Gaming-the-System-complete.zip?raw=true)**

解压整个压缩包，用 Chrome 或 Edge 打开 **START-HERE.html** 选择版本。也可以直接打开下面的 HTML。包内有中英文 `START-HERE.txt`，无需安装软件，下载后可离线使用。

```text
START-HERE.html                     版本选择入口
START-HERE.txt                      中英文说明
Full-game/Gaming-the-System.html    完整三关：Level 1 → 2 → 3
Level1/Level1.html                  单独 Level 1
Level2/Level2.html                  单独 Level 2
Level3/Level3.html                  单独 Level 3
```

所有版本包含已确认的 Level 2 实验铺垫和过渡、Level 3 未分配开局与自由实验路径。完整三关版会传递实际选择；三个独立关卡停在各自关卡末尾。

## 分别下载

| 版本 | 下载 | 解压后打开 |
| --- | --- | --- |
| 完整三关 | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| 单独 Level 1 | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | Level1.html |
| 单独 Level 2 | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | Level2.html |
| 单独 Level 3 | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-play.zip?raw=true) | Level3.html |

原先的 [Level 3＋完整三关双版本包](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level3-and-Full-game-play.zip?raw=true) 继续保留并同步更新。

## 更新与历史

最新版统一位于 **level3-dev**，四个预览/开发分支同步发布。上述固定文件名始终指向最新版；文件名带版本号的 ZIP、旧报告与标签是历史记录，保持原样。

`npm run package:previews` 一次更新全部六个 ZIP；`python3 tests/release.py` 验证实际文件、版本选择入口和三关衔接。校验值在 [LATEST.json](LATEST.json)。

关闭或刷新会开始新游戏；正式开场及成片尚未合并，剧情仍为 placeholder。
