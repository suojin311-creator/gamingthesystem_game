# GitHub 使用说明

后续 Level 3 的开发都在 **level3-dev** 分支进行。分支里保留完整项目，
每一关分别放在自己的文件夹中，共用部分放在 shared。

前面制作 Level 2 时，对 Level 1 的后续修改放在 level2-dev 的
`src/levels/level1/` 中，也打包进了 v6 两关试玩包。旧的 level1-preview
没有单独同步，仍保存早期 v7 独立版。分支之间不会自动同步；后续以
level3-dev 下的各关文件夹作为当前整合版本。

## 直接入口

| 要找的内容 | 入口 |
| --- | --- |
| 当前开发项目 | [level3-dev](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev) |
| Level 3 文件夹 | [src/levels/level3](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level3) |
| 当前分支里的 Level 1 源码 | [src/levels/level1](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level1) |
| 当前分支里的 Level 2 源码 | [src/levels/level2](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/levels/level2) |
| 当前分支里的共用模块 | [src/shared](https://github.com/suojin311-creator/gamingthesystem_game/tree/level3-dev/src/shared) |
| 已认可的前两关版本 | [level2-preview](https://github.com/suojin311-creator/gamingthesystem_game/tree/level2-preview) |
| 前两关 v6 试玩包 | [下载 Level2-play-v6.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/level2-preview/play/Level2-play-v6.zip?raw=true) |
| 较早的 Level 1 独立预览 | [level1-preview](https://github.com/suojin311-creator/gamingthesystem_game/tree/level1-preview) |

下载试玩包后，先解压。打开 **Levels1-and-2.html** 可以从 Level 1 玩到
Level 2；打开 **Level2.html** 可以直接进入第二关。Level 3 目前只有开发
位置，尚未加入试玩。

## 分支各自做什么

- **level1-preview**：保存较早的 Level 1 单关版本。
- **level2-preview**：保存这次认可的前两关 v6，对应提交 `336c59f`。
- **level2-dev**：保留之前制作 Level 2 的开发记录。
- **level3-dev**：从 v6 接着开发，包含前两关和 Level 3 的文件夹。

在 GitHub 仓库页面，点击左上方的分支名称，下拉选择 **level3-dev**，
就能看到当前开发内容。也可以直接使用上表里的链接。

## 文件放在哪里

```text
src/
  Gameplay.tsx       负责各关之间的衔接和姓名传递
  levels/
    level1/          第一关
    level2/          第二关
    level3/          第三关，当前已预留
  shared/            各关共用的对话、图标、声音等
  assets/            图片素材
docs/                游戏衔接与开发说明
play/                可下载的试玩包
```

制作第三关时，在 level3-dev 中继续使用现有的前两关和共用模块。第三关
完成后，再接通 Level 2 结尾的按钮，并加入第三关试玩入口。旧试玩包的
文件名和位置继续保留，因此之前聊天里的下载链接仍然有效。
