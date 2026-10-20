# 开发与发包分开

## 日常只处理正在修改的部分

当前动画分支已将确认的 Level 1／2 接入开头＋三关。首次运行先按
[动画接入说明](ANIMATION_INTEGRATION.md#level-1-动画构建)准备只读交付和本地影片缓存。
`npm run dev`、build 和 package 命令会校验并复用缓存；影片脚本或配色变化后
用对应的 LEVEL1_ANIMATION_SOURCE／LEVEL2_ANIMATION_SOURCE 重新 prepare。
Level 2 的来源、placeholder 裁剪、备份与结果页标准见 [Level 2 动画说明](LEVEL2_ANIMATION_PREVIEW.md)。
当前整包发布仅更新动画分支，不同步稳定分支。

统一在 **level3-dev** 开发。已经推送的提交可作为合并前基线，不必为每次小改动另建存档标签。

本次按用户要求，动画修改和衔接单独放在 **animation/opening-integration**。
动画审阅包也在该分支生成、验证和发布，只推送该分支，不同步稳定游戏分支。

| 工作 | 命令或检查 |
| --- | --- |
| 动画分支：开场后接三关；游戏分支：直接三关 | `npm run dev` |
| 单独调试某一关 | `npm run dev:level1`、`dev:level2` 或 `dev:level3` |
| TypeScript 检查 | `npm run check` |
| 关卡、姓名、场景结束回调的既有接入契约 | 先启动 Vite，再运行 `npm run test:integration` |
| 修改 effort/分配规则时 | `node --experimental-strip-types tests/level3_rules.mjs`，再检查相关玩家路径 |
| 准备完整试玩交付 | `npm run package:previews`，随后 `npm run test:release` |

Vite 会直接显示当前源文件的修改；调对白、动画和样式时不需要反复生成离线 HTML 和 ZIP。若已有服务器正在运行，继续使用它。

### 按改动选择检查

- 只改说明或目录导航：检查内容和链接，不编译游戏。
- 只改动画画面或时序：检查对应场景、完成回调、声音以及相关尺寸；改了 TypeScript 才需要类型检查。
- 改场景路由、姓名或关卡切换：检查相关接入契约。
- 改权重模型：检查分配规则和受影响的玩家路径。
- 要交付 ZIP：检查真实压缩包和完整关卡衔接。

旧测试有些描述已经移除的玩法。不要为了让旧测试通过而恢复 Restart、强制平均、强制三次等旧行为。正式动画替换 placeholder 后，应相应更新依赖占位文字的浏览器断言；场景请求和结束回调仍按现有契约验证。

## 交付时统一生成全部版本

```sh
npm run package:previews
npm run test:release
```

四个入口仍分别构建，以保持单独关卡与完整游戏的进入/继续行为。新流水线将重复的 TypeScript 检查从四次合并为一次；单独执行 `npm run build:level3` 等命令仍自带类型检查。

一次生成全部六个最新包：四个单独/完整版、原双版本包，以及带版本选择页的全部版本总包。验证通过后继续使用这一组构建，不为说明文字再重建一遍。`play/LATEST.json` 描述最近一次打包的源码和文件校验值，并不表示每个日常开发提交都已发包。

## GitHub 保存与发布

- **普通进度**：提交并推送 `level3-dev`。
- **试玩发布**：在验证实际下载包后，把三个预览兼容分支同步到同一个提交。
- `level1-preview` 目前是仓库默认分支，显示最近发布；`level2-preview` 和 `level2-dev` 保留旧链接。它们无需在日常开发时持续追随。
- 当前验证写入 `PREVIEW_VALIDATION.json`；详细版本报告在正式检查点需要时再保留，不为每处小修改复制一份大报告。

## 仓库体积与存档

当前源码约5MB；本地 `play/` 约206MB，Git 松散对象约1.3GB。这些是当前工作区测量，不等于 GitHub 的实际存储占用。历史 ZIP 已经进入历史；移动或删除当前文件不会自动消除旧对象。

本轮保留历史、标签和旧下载入口。减少日常生成和提交大包，比反复搬移存档更直接。未来动画导入以实际需要的源码和素材为准，不导入另一份 `node_modules`、构建缓存或重复试玩 ZIP。
