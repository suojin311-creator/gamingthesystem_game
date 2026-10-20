# Design Lab · 本地课堂版

原独立版本保存在 `feature/design-lab-local`；当前分支已接入三关游戏，并加入统一音乐和音效。完整课堂预览使用 `play/Gaming-the-System-classroom.zip`，启动方式见 `README-Windows.txt`。游戏位于 `/game`，ending 按钮进入同一课堂的 Lab。
它由老师的 Windows 电脑临时提供网页；学生仅需浏览器。同一局域网可互通即可运行，
无需云服务器、账号、Python、Node.js 或订阅，也没有按人数收费的服务。

## 下载与启动（老师）

下载 [Design-Lab-local.zip](https://github.com/suojin311-creator/gamingthesystem_game/blob/feature/design-lab-local/play/Design-Lab-local.zip?raw=true)。

1. **先完整解压**，双击 `Start-Design-Lab.exe`。支持 Windows 10/11 64 位。
2. 浏览器会自动打开主持页。启动程序的窗口保持打开。
3. 主持页右侧显示可分享给同学的网址。老师电脑和同学电脑需要处于可互通的网络。
4. 如老师也参与，点击 **Join as a participant**，在新标签页作答。主持页本身不占参与名额。
5. 等大家加入后，点击 **Start writing**。
6. 固定 90 秒写作后自动进入展示，只看别人写的内容；没有投票倒计时。选择鲜花／炸弹后，短暂反馈并自动进入下一份。
7. 提前完成的人等候。全员选择完成后，显示同一份静态排行榜，停留 12 秒，可手动滚动查看。
8. 随后两个反问各展示 4 秒并柔和转场，自动进入 **Goodhart’s Law**；人物、标题和正文分层淡入。
9. 下课点击 **Close classroom**。程序退出，本次数据随之清空。

首次启动若 Windows 防火墙询问，请允许该程序在课堂使用的网络上接收连接。
不要在活动期间关闭启动程序窗口、让老师电脑休眠或断网。

## 一个人先检查界面

主持页点击 **Join as a participant**，即可自己走一遍写作和收尾。
只有一个投稿者时没有别人的作品可展示，会直接进入排行榜。
要预览二选一展示，请用另一个浏览器或隐私窗口打开参与者链接并提交另一份作品。
同一个参与者标签页刷新会恢复当前 Lab 状态；新活动需要关闭程序后重新启动。

## 课堂网络自测

先启动程序，在另一台电脑输入主持页分享的网址。
能看到 Design Lab 等候页，并让主持页的加入人数增加，即已完成实际连通测试。
如老师电脑可访问、其他电脑不行，检查地址、防火墙及校园网络隔离。
主机有多张网卡时，可展开 **Other local addresses**，选择当前课堂网络的地址。
还需在正式课堂使用的网络上完成一次测试；云开发环境不能验证校园网。

## 已确认的规则

- 最多按 20 位学生＋1 位老师使用设计；主持页面不额外算人。
- 写作题目：**What is one change you would make to help Alex learn more deeply?** 无题目下方小字。
- 最多 240 字符，支持中文与英文。
- 开始前说明匿名展示、投票及最终排名，不说明计分细节。
- 只有 **Agree（鲜花）／Disagree（炸弹）**；只接受第一次选择。
- 展示中只出现其他作者的作品；作者本人不会收到自己的卡片。21 人都投稿时每人看 20 份。
- 展示不设个人或全班倒计时，未选择就留在当前作品。选择后记录单次不可修改的票，约 0.45 秒反馈后自动下一份；没有 Next 按钮。
- 各人独立推进；提前完成的人等候，直到全员完成后统一进入排名。
- 鲜花数降序；同分并列相邻，采用 1、2、2、4 这样的名次，组内沿用一次随机顺序。
- 排名在展示结束时冻结，静态停留 12 秒；移除高光滑动与扫描音效，可以手动滚动列表。
- 删除写作页的 Join the audience 按钮。
- 第一问：Did the most flowers mean the deepest thinking?
- 第二问：Did knowing there would be a ranking change what you wrote?
- 两问各 4 秒，自动依次切换并进入 Goodhart；服务统一维护截止时间。
- 排行榜作为两个问题的连续背景，问题柔和淡出淡入，避免切换时闪回排行榜。
- Goodhart 理论页以更缓慢的分层动画进入，原图提前加载；引文不加双引号。系统减少动态效果时即时呈现。
- 不收集姓名、不连接游戏数据，不将活动内容写入文件或第三方服务。进程关闭后清空。
- 不增加防捣乱、审核或排行榜互动功能。主持操作只在老师电脑上开放。

## 技术与开发

前端复用仓库已有 React / TypeScript / Framer Motion，单独使用 Vite 构建。
Go 服务只依赖标准库，嵌入全部前端和插画，交叉编译成 Windows 单文件程序。
HTTP 监听局域网；主持页 `/host`，参与者页 `/`，投影页 `/display`。
所有阶段、截止时间、锁定的选择和最终排名由本地服务管理；浏览器按自己的进度显示作品。

```sh
# 仓库根目录；首次需要 Node.js 与 npm ci
npm run lab:build

# 使用真正的 Go 1.22+ 工具链
cd design-lab
go test -race ./...
go build -o build/design-lab-local .
./build/design-lab-local --no-browser --port 3000

# 另一终端在仓库根目录运行，按需热更新前端
npm run lab:dev

# 发布独立 Windows ZIP（在仓库根目录）
npm run lab:package
```

如果系统的 `go` 不是 Go 编译器，可通过 `DESIGN_LAB_GO` 指定真实路径。
源码、启动器构建和测试都与原游戏隔离；不需要重建游戏动画或原来的六个 ZIP。

浏览器验证：`python3 design-lab/tests/browser.py --scenario all`。
测试缩短写作时间，并真实等待超过旧的 10 秒，检查未选择的卡片保持不动。
Go 时钟测试覆盖 90 秒写作、无截止时间的展示、12 秒排名和两问各 4 秒；
浏览器另查自己作品始终不出现、选择后自动推进与渐入渐出过渡。
测试中使用同源码的 Linux 服务；Windows 产物另做 PE 架构和嵌入资源校验。
不能将 Linux 测试描述为已经在 Windows 实机运行；发布前后仍需用老师电脑实际启动一次。

## 结尾素材

半身像是为本项目生成的插画，非历史照片。按用户确认使用简短表述：
“When a measure becomes a target, it ceases to be a good measure.”
不再展示 1975 年长引文或将该简短表述标为 1975 年原文。
Ending 的正式游戏接入保存在 `animation/opening-integration`；
本分支的课堂程序已连接 ending 按钮；原独立版本与旧 ZIP 保留在原分支。

## 界面预览

![主持页](docs/00-host.png)
![写作](docs/02-writing.png)
![匿名投票](docs/03-voting.png)
![Goodhart 结尾](docs/06-closing.png)
