# 最新试玩下载 / Latest downloads

## 最新合并版：开头＋三关

[Gaming-the-System-complete.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Gaming-the-System-complete.zip?raw=true)：解压后打开 **START-HERE.html**，选择 **Play the full game**。也包含三个单独关卡。

已合入确认的 Level 1 操作页、六种结局动画与核算页，并从核算页继续 Level 2。开头和 Level 1 使用相同师生字幕颜色；开头填写的名字自动用于操作对话、动画老师标签和邮件称呼，并继续传到后两关。

[合并前完整版本备份](https://github.com/suojin311-creator/gamingthesystem_game/blob/archive/opening-before-level1-merge-20261020/play/Gaming-the-System-complete.zip?raw=true)保存了旧开头＋三关和各独立关卡；源码保存在同名备份分支，提交为 `32a91fe`。稳定游戏分支和已确认的独立 Level 1 预览分支未被覆盖。

## 已确认的独立 Level 1 预览（合并前）

[Level1-settlement-preview.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/preview/level1-settlement/play/Level1-settlement-preview.zip?raw=true)：解压后打开 **START-HERE.html**，选择新版或原版对照。新版包含完整六选一操作、考核标准及第一次／第二次考核的班级达标百分比、按阅读速度调整的对应结局动画（直接衔接完整邮件，移除 common ending），以及沿用原状态卡文案的结果核算页。动画自动播放，隐藏播放条和时间显示；结果页已去掉 Target 和管理方底部文字。邮件完整显示后 2 秒出现老师首句，最后一句使用 I；核算页保持管理方结果静态，只强调学生负面结局。结果页可换一个指标。

这是合并前保存的独立预览；其确认内容已接入上方完整版，同伴仓库未被修改。说明见 [LEVEL1_SETTLEMENT_PREVIEW.md](../docs/LEVEL1_SETTLEMENT_PREVIEW.md)，校验见 [LEVEL1_SETTLEMENT_PREVIEW.json](LEVEL1_SETTLEMENT_PREVIEW.json)。


## 合并前 Level 1 原版动画预览

[Level1-animation-preview.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Level1-animation-preview.zip?raw=true)：解压整个 ZIP，打开 **START-HERE.html** 选择六种 metric 结局，进入后点击播放器的 **▶**。页面上方 **Branch** 可以切换结局，**Sequence** 可以单独查看片段。无需安装或联网。

这是同伴 `feature/cinematic-level1-consequences` 分支的独立预览。只在外部打包配置中开启现有预览入口，没有改动同伴仓库或源码，也没有接入游戏。校验信息见 [LEVEL1_ANIMATION_PREVIEW.json](LEVEL1_ANIMATION_PREVIEW.json)。

## 合并前原版开场存档

[Opening-animation-preview.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Opening-animation-preview.zip?raw=true)：解压后用 Chrome 或 Edge 打开 **Opening.html**，建议电脑横屏。按本次上传的原版源码打包，供合并前观看；校验信息见 [OPENING_PREVIEW.json](OPENING_PREVIEW.json)。

## 动画分支审阅：一个 ZIP 包含所有版本

**[Gaming-the-System-complete.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Gaming-the-System-complete.zip?raw=true)**

解压整个压缩包，用 Chrome 或 Edge 打开 **START-HERE.html** 选择版本。也可以直接打开下面的 HTML。包内有中英文 `START-HERE.txt`，无需安装软件，下载后可离线使用。

```text
START-HERE.html                     版本选择入口
START-HERE.txt                      中英文说明
Full-game/Gaming-the-System.html    开场 → Level 1 → 2 → 3
Level1/Level1.html                  单独 Level 1
Level2/Level2.html                  单独 Level 2
Level3/Level3.html                  单独 Level 3
```

所有版本包含已确认的 Level 2 实验铺垫和过渡、Level 3 未分配开局与自由实验路径。完整三关版会传递实际选择；三个独立关卡停在各自关卡末尾。

## 分别下载

| 版本 | 下载 | 解压后打开 |
| --- | --- | --- |
| 完整三关 | [Full-game-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Full-game-play.zip?raw=true) | Gaming-the-System.html |
| 单独 Level 1 | [Level1-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Level1-play.zip?raw=true) | Level1.html |
| 单独 Level 2 | [Level2-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Level2-play.zip?raw=true) | Level2.html |
| 单独 Level 3 | [Level3-play.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Level3-play.zip?raw=true) | Level3.html |

原先的 [Level 3＋完整三关双版本包](https://github.com/suojin311-creator/gamingthesystem_game/blob/animation/opening-integration/play/Level3-and-Full-game-play.zip?raw=true) 继续保留并同步更新。

## 更新与历史

本分支的动画审阅版位于 **animation/opening-integration**；稳定游戏与预览分支保留已确认版本。上述固定文件名始终指向最新版；文件名带版本号的 ZIP、旧报告与标签是历史记录，保持原样。

`npm run package:previews` 一次更新全部六个 ZIP；`python3 tests/release.py` 验证实际文件、版本选择入口和三关衔接。校验值在 [LATEST.json](LATEST.json)。

关闭或刷新会开始新游戏；完整版已接入开场；后续课堂与结尾成片仍为 placeholder。
