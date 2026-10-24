# 已确认：三关自动进入并同步正式包

用户已批准本次关卡介绍和老师称呼调整进入正式游戏。六个常规游戏 ZIP 与
Gaming-the-System-classroom.zip 随本次发布更新；独立 Design Lab 未改动。
三关介绍页动画结束后停留两个可见秒并自动进入，老师台词不再直接称呼 Alex。
前面的开头副标题和 ending 两句文案仍是独立未确认预览，不随此发布合并。
正式包检查包含真实 ZIP 的关卡衔接及两个独立客户端通过非回环 HTTP 完整运行。
详情与当前校验值见 play/LATEST.json、play/CLASSROOM_PREVIEW.json 和 docs/PREVIEW_VALIDATION.json。

# 当前：三关介绍页自动进入预览

三关共享 ChapterTransition 现在在最后一段对话入场动画结束后，停留两个可见秒，
自动执行原 onStart；进入按钮已移除，减少动态效果及后台暂停已处理。
老师直接称呼 Alex 的台词在源数据与公共对话/电影字幕渲染层统一去掉；
学生身份标签及第三人称报告保留。Level 2/3 部分老师式提问也改为泛指。
只交付 `play/Chapter-auto-entry-preview.mp4`，示例为 Level 2，未重打游戏或课堂 ZIP。
三关、携带指标、减少动画、后台暂停等八项验证与时间记录在
`play/CHAPTER_AUTO_ENTRY_REVIEW.json`。原电影镜头未在此预览中播放；
Level 1/2 字幕适配器从固定原版重新编译到已有缓存，供下次完整构建使用。
入口、构建与录制命令见 `scripts/chapter-review/README.md`。
前面的 opening/ending 文案预览仍待确认，不能擅自合入本次源代码修改。

# 最新接力：整合音频与课堂预览（2026-10-20）

当前修复（2026-10-21）：用户报告两台浏览器/手机经分享链接玩游戏时动画切换变背景色。
真实局域网 HTTP 复现为 `crypto.randomUUID is not a function`；localhost 没有此问题。
四个电影适配器现在使用 `shared/utils/cinematicRunId.ts` 的 getRandomValues 随机标识，
保持发送窗口与 run token 双重校验。六个常规游戏包及合并课堂包随修复更新，独立 Lab 无变化。
回归脚本 `tests/classroom_lan.py` 必须传非回环 HTTP 地址，启动两个独立 Chromium 进程，
一套桌面、一套手机触控视口，实际完成开头、三关、ending 与同一 Lab 的加入。
不能将手机模拟或 Linux 服务验证描述为在真实手机/Safari/Windows 上测试。

恢复连接后已确认 `d5d26fb9b99ae5d16c980d65540f2b902a63b863` 已上传到 GitHub。
按用户顺序，先交付 `Full-game-play.zip`；其次独立 `Design-Lab-local.zip`；
最后 `Gaming-the-System-classroom.zip`。第 1 和第 3 份复用已校验的 d5d26fb 文件。
独立 Lab 用 `python3 design-lab/package.py --standalone` 构建，主持页直接分享 `/`，
不含游戏，也不显示游戏/游戏试听入口。最新 Go 编译器位于
`/workspace/.cache/gts-go/go/bin/go`，旧 `/tmp` 工具链已随恢复消失。
三份使用方式见 `play/DELIVERY_GUIDE.zh-CN.md`。

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
