# 最新试玩下载 / Latest previews

三个最新版放在同一个分支 **level3-dev** 的这个文件夹中：

| 想怎么玩 | 下载 | 解压后打开 |
| --- | --- | --- |
| 从 Level 1 接着玩 Level 2 | [两关连玩最新版](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Full-game-play.zip?raw=true) | **Gaming-the-System.html** |
| 只试玩 Level 1 | [Level 1 独立最新版](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level1-play.zip?raw=true) | **Level1.html** |
| 直接试玩 Level 2 | [Level 2 独立最新版](https://github.com/suojin311-creator/gamingthesystem_game/blob/level3-dev/play/Level2-play.zip?raw=true) | **Level2.html** |

1. 登录有此仓库访问权限的 GitHub 账号。
2. 点击对应下载链接，下载 ZIP。
3. 解压，再用 Chrome 或 Edge 打开表格中的 HTML 文件。

不需要安装软件或输入命令；下载后可以离线运行。每个 ZIP 里也有英文的
START-HERE.txt 操作说明。仓库是私有的，可以把下载后的 ZIP 直接发给试玩者。

这三个固定文件名都表示当前最新版，后续更新继续使用这些入口。各入口复用
同一套关卡源码。Level 1 单独版停在第一关结尾；连玩版同一位置可以继续到
Level 2。Level 2 直接进入第二关的开场对话。Level 3 目前尚未加入试玩。

关闭或刷新会重新开始；电影片段仍用 placeholder。姓名衔接接口已保留，
独立试玩暂用 Maya，正式开场尚未合并。

旧的 level1-preview 分支已同步，里面的 [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level1-preview/play/Level1-play.zip?raw=true)
也更新为这次的单关最新版。以后优先使用上表统一入口。

文件名含版本号的 ZIP（例如 Level1-play-v7.zip、Level2-play-v6.zip）是历史
存档，保留当时内容；请用上表的固定入口分享最新版。

开发时运行 `npm run package:previews` 会一起生成三个最新包与 `LATEST.json`。
发布前运行 `python tests/release.py` 检查真实 ZIP 的内容和关卡衔接。
