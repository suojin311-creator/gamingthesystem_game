# 最新接力：整合音频与课堂预览（2026-10-20）

当前工作分支：`animation/opening-integration`。稳定别名未移动。

- 已合入认可的 ending 问题：两行居中，learning 浅金、numbers 珊瑚橙，关键词放大。
- 三关动画共用配乐；关键操作有音效。音乐与音效独立音量、总静音、暂停与后台静音。
- 完整游戏接入本地 Design Lab：`/game` → ending 按钮 → `/`，主持页 `/host`。
- Lab 题目：**What is one change you would make to help Alex learn more deeply?**
- 只展示别人的反思；投票无倒计时，选完自动下一张；排名静态 12 秒；问题各 4 秒；
  最后自动揭示 Goodhart。保留既有渐入与转场。Agree/Disagree 共用同一个中性确认音。
- 交付 `play/Gaming-the-System-classroom.zip`。解压运行 `Start-Gaming-the-System.exe`。
  主持页有 Open the game、Preview music & sounds，试听页可直接跳到各关。
- 常规六个 HTML ZIP 统一更新。单机 HTML 的课堂按钮会提示使用本地课堂程序。
- 使用同网络课堂，无云托管、订阅或运行时外部素材下载。

完整 ending 合入、音频添加前的 GitHub 备份：
`archive/full-game-approved-ending-before-audio-20261020`（`04445a5`）。
更早的完整版备份：`archive/full-game-before-audio-20261020`（`33a10e9`）。
独立 Lab 基线保留于 `feature/design-lab-local`（`4c9217e`）；独立 ending 预览分支保留。
当前 Lab 是从该基线引入本分支的目录，并未合入其旧游戏代码。

实现与验证：`docs/AUDIO_DESIGN.md`、`docs/PREVIEW_VALIDATION.json`、
`design-lab/VALIDATION.json`、`play/CLASSROOM_PREVIEW.json`。
音频原始生成脚本 `scripts/render_score.py`，不含外部采样。根目录四个构建可复用
影片缓存；课堂构建需先 lab:build，然后将 dist/index.html 用 gzip（mtime=0）嵌入
`design-lab/web/game.html.gz`，再运行 design-lab/package.py。
真实 Go 工具链由 DESIGN_LAB_GO 指定；此环境为 `/tmp/codex-go/go/bin/go`。

浏览器及本地服务已在 Linux 验证；Windows x64 包检查 PE 和全部嵌入素材，
不能声称做过真实 Windows 启动测试。历史截图和旧 validation 不代表当前版本。
