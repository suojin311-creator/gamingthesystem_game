# Gaming the System：下一位 AI 合并交接说明

本说明汇总用户多轮修改后的最终要求，并对照当前已确认源码核验。用途是继续合并游戏与动画，不是重新设计已通过的玩法。最新明确要求优先于旧文档；下文特别标出的待接入内容，不代表已经完成。

配套文档：**[分支与文档地图](BRANCH_DOCUMENT_MAP.zh-CN.md)**列出每个现存分支的文档；**[游戏概念与界面元素词典](GAME_CONCEPTS.zh-CN.md)**统一数字、标准、权重、投入与观察证据的含义。

## 1. 先认准版本，避免从旧版本继续

仓库：<https://github.com/suojin311-creator/gamingthesystem_game>

| 用途 | 分支 | 已确认基线提交 |
| --- | --- | --- |
| 开头＋三个 Level，已接入 Level 1 六种结局动画 | `animation/opening-integration` | `63856491e62c52d5a9bdb176ea738abbe6c6c9c7` |
| 独立本地 Design Lab；同时继承上行全部游戏源码 | `feature/design-lab-local` | `33d93d25a412d2086bb676217844cb1f796402f0` |
| 合并新版 Level 1 之前的开头＋三关备份 | `archive/opening-before-level1-merge-20261020` | `32a91fe4bfb1cb193040410c846ebc165f8b9d5d` |
| 已通过的独立 Level 1 预览 | `preview/level1-settlement` | `411353dd3ef6103b20faa4debe9075b94f46e199` |

**用户已认可目前 Design Lab。游戏与 Lab 尚未接通；Level 2、3 正式动画尚未接入。** 不要把占位场景误认为完成的动画。

建议后续在新合并分支继续，保留以上基线。Design Lab 分支已经包含游戏基线，不要再把整套游戏重复复制进去。仓库默认分支及旧 `level1-preview`、`level2-preview`、`level2-dev` 名称不表示最新合并版。

同伴仓库 <https://github.com/Mg614/gaming-the-system> **只读**。用户明确要求不要修改她的任何文件。已接入的 Level 1 原始交付固定在 `1bdd0c442c4b345b3bd37d6f541742d4e55c732f`；自己的改动放本仓库适配层。以后有新交付，要先确认版本，不要直接拿同伴 main 覆盖已修改的动画。

## 2. 全局不能丢失的要求

- 一个 Level 只有一套玩法实现，完整游戏和独立预览复用。动画负责呈现真实选择，不能另外计算指标、权重、effort 或编造玩家没做过的实验。
- 开头填写的教师姓名自动带入操作界面与动画。不要再次输入，不要硬编码 Maya；Alex 的名字保持 Alex。Lab 匿名，不接收游戏姓名。
- 老师字幕暖金色 `#ffe2a3`，Alex／学生字幕浅蓝色 `#cceeff`，用暗描边／小阴影保证可读。不要用底部一整片淡黑色遮罩承托字幕。
- 主要操作按钮保持统一陶土红色、浅色文字与箭头，位置沿用对应关卡原来位置。不能无故挪动按钮或改成另一套视觉语言。
- 节奏适合阅读和正常反应：避免过慢等待，也避免突然瞬移。镜头先稳定再出对白；过场结束依据实际事件回调，不能单靠猜时长。
- 不向玩家展示调试选项、动画时间／播放进度条、分支选择器或内部场景编号。已删除的 Replay animation 不要恢复。
- 游戏进度仅在当前页面内存中存在。误退出／刷新不恢复游戏，不新增账号、云端存档或自动保存。
- 不擅自修改已确认脚本、补写动画或增加新玩法。缺交付先明确缺哪段，不用占位图伪装完成。
- 用户主要通过下载 ZIP 试玩。实际界面更新交付时要有对应可玩 ZIP，不能只更新源码；本次交接文档不改变可玩包。

## 3. 开头动画：最新版

### 3.1 标题、入口与姓名

标题下副标题是：**Do better numbers mean better learning?**

保留姓名输入；已删除 **You'll be making the decisions from here.**，不要放回来。

**TAKE YOUR SEAT →** 与 **BACK TO OFFICE →** 要醒目且统一：实心陶土红 `#ad5840`、浅色文字、清晰边框／箭头，正常点击面积，不再是背景上的弱文字。此要求不意味着要顺便重做 START GAME。

### 3.2 邮件与三个学生的引导

- Urgent email 出现时有清晰的发光箭头，提示可以点；箭头外不加圆圈。
- 点邮件后不再做第二次 zoom in；固定尺寸阅读层在最终字号呈现，简短切换。已实现普通约 300ms、减少动态模式约 100ms。
- VISIT CLASSROOM 一直明亮、立即可用，不等待旁白全部播放才解锁。
- 学生场景提示：**Come closer to take a look at the students.**，字号足够明显。
- 不给学生画圈。一次只在下一个未观察学生上方给箭头；玩家仍可自行选择任何学生。
- 有三个小完成标记，明确必须看完三人才能回办公室。不是只写 Look around 后让玩家猜。
- 学生观察时镜头连续移动、停稳再读台词。当前参考：对焦约 900ms、回应约 1700ms、返回约 850ms；不是把全部动作压成瞬间切图。

### 3.3 回办公室到 Level 1 的铺垫

心理活动依次建立动机：

1. **They’re here, but they’re not really engaged.**
2. **Management wants measurable results. / I need a sign I can track.**
3. 进入独立的 Level 1 过渡：**Which sign would tell me the most?**，再由 Choose a metric 进入操作。

不要恢复孤立的 What should I measure first，也不要回办公室一按就直接跳完全不同风格的操作页。

## 4. Level 1：六选一、评分含义与动画结算

### 4.1 指标与评分究竟是什么

六项：Pre-class Preparation、In-class Participation、On-task Focus、In-class Discussion Quality、Learning Reflection Quality、Online Peer Response Quality。

**分数表示：班级中符合玩家所选指标评价标准的学生比例。** 比较第一次和第二次 assessment。它不是实际学习质量分数，不是老师得分，也不是 Alex 学会了多少。分数提高与教室里学生追逐得分行为可以同时发生，后续 Observe 正是检查这种差别。

每项具体标准读取 `src/levels/level1/metrics.ts` 的 `assessmentCriteria`，不要只给模糊数值。

### 4.2 最新操作文案和布局

| 位置 | 最终要求 |
| --- | --- |
| 顶部阶段 | Choose → Predict → Evaluate → Observe；不增加 Results |
| 选择页主问题 | What will count in the next assessment? |
| 评分页标题 | Assessment results. |
| 数字含义标签 | **Percentage of students meeting the criteria** |
| 两次数据标签 | First assessment / Second assessment |
| 评分操作 | View assessment results；保持原来右侧位置 |
| 进入观察 | Look behind the result |

以下文字已要求删除，不要恢复：

- At the second assessment。
- This metric now counts towards students’ marks.
- How will students respond when this counts towards their marks?（可保留表单无障碍名称，不显示该行。）
- 结果页 Target 标记、目标刻度和 target-met 标题。
- Management’s view 底部说明文字。

评分展示仍保留原有数字／能量条从 before 升到 after 的动态。不要把“结算卡静态”的要求误用到前面的 Evaluate。

### 4.3 六种结局动画

- 玩家实际选择哪一项，只播放该项后果。动画放原 placeholder 的区域，属于 Observe。
- 删除 **common ending** 片段；保留所选后果及办公室邮件／老师心理活动的收束。
- 不显示底部六指标菜单、内部预览按钮、播放进度条、时间和 Replay animation。
- 不频繁 zoom in／zoom out，不做复杂慢消融。镜头切换用短暂完整遮挡，再显示下一幅稳定画面，保证前一幅彻底退出。
- **修过的 bug 不能复发：Alex 教室画面不应半透明叠到办公室邮件后面。** 始终只有一个不透明主镜头；切换按实际结束事件处理。
- 邮件内容一起出现，不逐行揭示；删除绿色 Selected metric／TARGET ACHIEVED 区块，不像正常邮件。
- 邮件称呼使用玩家姓名；老师字幕和角色标签同步姓名。
- 邮件真正显示后 **等 2 秒**出第一句：**The number looks great... but something still feels wrong.** number 单数。
- 收束思考：**What if I measured more than one?** 用 I，不用 we。
- 对话字幕按全局金色／蓝色区分，取消底部黑色阴影带。

### 4.4 动画后的结算页

这是对结果的核算与强调，不重复演一遍师生交流。

- 保留原标题 **Management’s view**、**Students**，原有满意状态和学生行为文案。不要改为 Measured result／Classroom result。
- 调整原有内容排列，使它像关卡结算；删除老师—Alex 复盘聊天和原来的整块 IN THE CLASSROOM 解释面板。
- 不再显示 **What changed?**。
- Students 卡片保留小型笔记本／所选 metric 插图，避免大面积空白；不要恢复全宽旧面板。
- **最终要求：结算 Management’s view 静态，Students 卡片边框做轻微负面强调闪动。** 此项覆盖早先“管理条先上升，然后再出学生结果”的提议。
- Management’s view 底部说明不显示。Continue to Level 2 按原操作区位置和统一主按钮风格出现。
- 独立 Level 1 预览用 Try another metric，不能误带完整游戏跳转。

## 5. Level 2：从三个指标到清单膨胀

- 沿用玩家选过的指标与教师姓名，不能悄悄重置。
- 过程是 3 项 → 6 项 → 10 → 25 → 100。不是新增一套玩家逐个输入 100 项的玩法。
- 六项观察后，明确提出 **Would more metrics help Alex learn?**，配非交互的 **6 → ?** 小纸张示意；不能把关键假设仅藏在老师台词里。
- 玩家明确点击 **Test more metrics** 后，10 → 25 → 100 连续推进，不要求三次重复点击。
- 推进标题 **Testing more metrics.**，最终观察标题 **More metrics. Still chasing marks.**
- 已确认节奏：可见停留约 3.5 秒、提前约 0.7 秒翻纸；页面隐藏暂停推进。计数、清单与纸张持续挂载，避免闪烁重置。到 100 等玩家 Observe the class。
- 指标多了不等于真实学习更好；不能新增虚构学习得分或声称“所有多指标都无效”。
- Level 2 各阶段的 Students 文案以该关 data.ts 为准（详见概念词典）。进入 Level 3 后，无低投入项时显示 **Stops when the criteria are met.**，承接“达标成为目标”的问题；不要把这句话强行替换第二关全部阶段。
- Continue to Level 3 保持统一陶土红色主按钮。不要恢复截图里的浅色次级按钮。
- **Level 2 正式动画仍待接入**。接入前读 `src/levels/level2/` 与场景请求接口，不用旧故事覆盖上述已确认流程。

## 6. Level 3：最终权重实验逻辑

### 6.1 玩家实际路径

1. 完整版继承 Level 2 三项，允许更改；独立第三关自己选三项。
2. 第一次进入权重页，三项显示 **—**，滑条初始位置 0，但尚未分配；不预设 33/33/34，不给玩家“正确答案”暗示。
3. 移动任意滑条后创建合法分配：正整数、每项至少 1、总计 100。逐项确认后运行。
4. 公布真实权重，点 Observe the class 才看该轮课堂。
5. 第二次保留上一轮真实权重与观察，提出对应问题，玩家自行调整。
6. **完成两次真实观察就能比较并继续结尾**；第三次是可选。可取消第三次返回比较，最多三次，不造出第四次。

不能强迫玩家操作出平均分配，不能要求依次做“一高两低”“两高一低”，不能插入系统参考实验冒充玩家试过。改了数值但 effort 没变也是合法结果；完全重复已观察权重才拒绝。

Reset：第一次尚无观察时回未分配；之后回上一次实际观察，不是每次清零或平均。确认／锁定机制保留；截图里每卡 Confirm weight 并非 bug，用户已澄清误会。

### 6.2 effort 不是固定百分比档位

每项同时与另外两项比较，差距 **≤10 个百分点（含 10）视为相近**；超过 10 才算更高或更低。比较结果中：更高次数多于更低 → Intense；更低更多 → Minimum；两者相同 → Steady。

| 分配 | 三项 effort | 用意 |
| --- | --- | --- |
| 49 / 26 / 25 | Intense / Minimum / Minimum | 一高两低 |
| 49 / 27 / 24 | Intense / Minimum / Minimum | 不存在 24/25 绝对断崖 |
| 45 / 45 / 10 | Intense / Intense / Minimum | 两高一低 |
| 65 / 24 / 11 | Intense / Steady / Minimum | 渐变高、中、低 |
| 34 / 33 / 33 | Steady / Steady / Steady | 相近，不要求绝对平均 |
| 40 / 30 / 30 | Steady / Steady / Steady | 恰好 10 的边界算相近 |
| 40 / 31 / 29 | Intense / Steady / Minimum | 40 与 29 差 11，跨相对边界 |

这是游戏的定性设计模型，不是 Goodhart 定律推导的科学阈值，也不是学习收益。动画直接读取 `effortAt` 已算出的请求，不得按绝对 25%／67% 再划一次档。

滑条调整保留其他未锁定项的相对比例，保留锁定项与总计 100；不要把剩余项无条件重置平均。

### 6.3 主问题、Hint 与 Students view：完整分支

三者必须读取同一真实历史。按以下顺序判断，特别注意第三次“前两轮 effort 全没变”的优先级。

| 编辑时点与真实情况 | 主问题 | Need a hint? 内容 | Students / Last observation |
| --- | --- | --- | --- |
| 第一次，无历史 | How would you split the 100%? | Move any slider to start. Confirm your weights, then watch Alex. | 没有虚构上一轮 |
| 第二次，上轮至少一项 Minimum，包括一高两低、两高一低、渐变组合 | Can you bring more attention to [实际低投入项名称]? | Give a neglected task more weight. Watch what happens to the others. | Low-weight areas get less attention. |
| 第二次，上轮没有 Minimum，三项 Steady | All three got attention. Has that solved the problem? | Try a different split. Does Alex still stop once the criteria are met? | Stops when the criteria are met. |
| 可选第三次，前两轮各项 effort 都未变，优先于其余分支 | Alex’s effort stayed the same. What could you change? | Make a bigger change to the shares. Does Alex’s effort change this time? | 按上轮是否含 Minimum 显示对应状态 |
| 可选第三次，effort 变过，上轮仍有 Minimum | [实际低投入项名称] gets/get little attention. What could you change? | Give a neglected task more weight. Can you avoid neglecting another? | Low-weight areas get less attention. |
| 可选第三次，effort 变过，上轮没有 Minimum | The effort changed. Did the stopping point? | Try another split. Does Alex still stop when the criteria are met? | Stops when the criteria are met. |

实际源码：`src/levels/level3/experiments.ts`、`ExperimentPrompt.tsx`、`data.ts`。低投入名称自动从上一轮取出；不要写死 Preparation，也不要遗漏两高一低。

投入分布与停止动机是两条线：三项 Steady 可以表示注意更均衡，但仍达标就停；不能表演成“完美权重解决学习”。有 Minimum 的任务在停止序列里不能全部打勾。

旧 **Follow the evidence** 小标题、**100% allocated** 彩色总条和旧泛泛提示不恢复。Hint 可折叠，桌面尽量简短，但不要用 nowrap 导致小屏裁切。

### 6.4 比较、对白和动画接口

- 比较只列真正完成的两次／三次。First result／Same effort／More effort／Less effort 相对紧前一轮同一 metric 的 effort，不拿权重变化冒充投入变化。
- 不再要求每轮先选择抽象实验 aim，不设最终 keep/rethink 强制判断。legacy intent／decision 字段存在不代表需要恢复界面。
- Guide 是四步控件说明：Next／Back／Skip／Esc，不替玩家移动滑条或演示固定配比。
- 后续场景直接读取 `LevelThreeCinematicRequest`：真实 `runs` 和当前三项 `shots`，包含 metricId、weight、effort、sceneId。
- 同一指标同一 effort 再出现时使用对应第 2／3 句，避免原句机械重复；同一轮重播不改变台词。详细 6×3 档、每档 3 句在 `docs/LEVEL3_NARRATION.md` 与同名 Word，不在此重复抄录。
- 结尾按真实历史分两种：effort 变过，或所有试验 effort 一直相同。共同指向“仍按评分要求工作并停止”，不能说玩家试过不存在的平均分配。
- 理论闪回使用玩家真实经历；不庆祝找到完美权重。
- **Level 3 正式动画尚未接入**。已有 narration 的末尾“到预览结束、不去 Lab”是当时范围限定；未来接 Lab 时需更新这一处，并设计理论揭示与 Lab 收尾的重复程度，不能把历史限制当成永远禁止接入。

## 7. Design Lab：已认可的独立版本

### 7.1 课堂与费用

- 电脑课堂使用，最多 **20 名学生＋1 名老师＝21 人**。老师也可以玩，主持控制页另开标签，不算第二个参与者。
- 优先本地：老师 Windows 10/11 x64，双击 **Start-Design-Lab.exe**，自动打开控制页，把同一局域网的网址发给同学；学生只用浏览器。
- 不安装 Node／Python 给老师，不收费、不接付费云服务、不绑卡，不因人数自动计费。学校隔离局域网是连通性问题，不等于必须花钱。
- 用户不想要创建房间／输入房间码等流程。程序内部会话标识不应变成新的玩家操作。
- 最终希望游戏结束自然进入 Lab，但当前独立保存，**尚未合并**。不要现在就声称全流程已打通。
- 不同步游戏记录、姓名、指标、权重。Lab 匿名记录在老师进程内存里，关闭清空；自己的 Lab 标签页可保留不透明会话 ID，这不等于保存游戏进度。

### 7.2 环节、文字与时间

1. 等待老师开始。提前告知：**Your reflection will be shared anonymously.** / **Everyone will vote, and a ranking will follow.** 需要让玩家知道之后会展示和排名，最终反问才成立。
2. 写作 **90 秒固定**，不延长。最终题目：**What is one change you would make to help Alex learn more deeply?**（最新确认文案，覆盖旧题）。去掉 Join the audience 按钮。 题目下不要小字提示、长模板或额外写作任务。当前认可原型限制 240 字符。
3. 匿名展示 Reflection 01…；编号随机一次后固定，不公开姓名。
4. 仅两个反应：鲜花 **Agree**、炸弹 **Disagree**。只说明二选一；不加泼水或其他反应，不解释“选择后不能改”，实现上单次不可修改。
5. 每位参与者只看其他作者的作品；展示**没有倒计时**，未选择就留在当前作品，选择后短暂反馈并自动进入下一份，不再有 Next 按钮。
6. 服务端个人队列跳过本人作品，界面和 API 都不会向作者展示自己的卡片。各人独立推进；提前看完进入等候。
7. 21 人都投稿时每位作者看 20 份；展示阶段无全局截止时间，所有人选择完成后进入排名。主持大屏显示进度。
8. 只按**鲜花数**排名，炸弹不扣分；**写作前不说明仅鲜花计分**。并列相邻，共享名次（当前 1、2、2、4），同分内部顺序随机固定。排名只读，不能点击互动。
9. 排行榜静态停留 **12 秒**，移除高光扫动、自动滚动和扫描音效；可手动滚动查看。
10. 排名留在背景，画面中央依次出现：
   - **Did the most flowers mean the deepest thinking?**
   - **Did knowing there would be a ranking change what you wrote?**
11. 两问各展示 **4 秒**，持续保留同一排行榜背景，柔和淡出淡入后揭示 Goodhart’s Law，无需老师点击继续；不是再让学生写一轮。
12. 最后 Goodhart 半身像、标题和短句分层缓慢进入，强调理论重点；短句不加双引号。留思考空间，不加长篇总结、测试或作业。

最终短句：**When a measure becomes a target, it ceases to be a good measure.**
用户已确认使用这句通俗表述，覆盖旧版 1975 长引文要求；不将它标成 1975 年原文。
现有人像 `design-lab/public/goodhart.png` 是 AI 绘制的编辑插画，不是历史照片。
Ending 已在 `animation/opening-integration` 接入正式游戏，Lab 仍在本分支单独发包，未连接 ending 按钮。

用户明确去掉专门防捣乱设计，不要再加反作弊、审核、复杂账号或惩罚流程。单次投票、不能自投等基本交互保持。

### 7.3 技术现状与尚未验证部分

- Go 标准库本地服务，内嵌 React 页面和图片，Windows 单 EXE；运行时不依赖外部字体／CDN／付费服务。
- 当前 `/` 学生、`/host` 老师、`/display` 投影。未来接游戏要明确路径方案，防止根路径把游戏覆盖；`/game`、`/lab` 只是可选设计，尚未确认最终路径。
- 核心：`design-lab/main.go`、`design-lab/session.go`、`design-lab/src/App.tsx`、`design-lab/src/useClassroom.ts`；API 见源码。投票和阶段时钟由服务端管理，不靠每台电脑各自决定排名。
- 当前已做服务端测试、21 个独立浏览器上下文流程、Windows 交叉编译检查。**还没在真实 Windows 机器双击运行，也没验证学校实际网络与 21 台实体电脑。** 不能把浏览器模拟说成课堂实测。
- 最终合并应保留免费、本地和匿名规则；同时处理退出游戏不保存、游戏结束进 Lab、老师等待全班的实际衔接。不应为了方便把游戏记录提交到 Lab。

## 8. 合并落点与交付方式

### 8.1 优先阅读的代码

| 领域 | 路径 |
| --- | --- |
| 开场到游戏 | `src/FullGame.tsx` |
| 三关连接及动画注入 | `src/Gameplay.tsx` |
| Level 1 共用流程／电影 | `src/levels/level1/LevelOneExperience.tsx`、`src/cinematics/level1/LevelOneCinematic.tsx` |
| Level 1 自有覆盖／组装 | `scripts/level1-settlement/` |
| 六项共用名称／Level 1 评价标准与数值 | `src/shared/data/metrics.ts`、`src/levels/level1/metrics.ts` |
| Level 2 场景与请求 | `src/levels/level2/` |
| Level 3 规则、提示、电影请求 | `src/levels/level3/weights.ts`、`experiments.ts`、`data.ts` |
| Level 3 制作对白 | `docs/LEVEL3_NARRATION.md`、`docs/LEVEL3_NARRATION.docx` |
| 统一字幕色 | `src/shared/data/cinematicPalette.js` |
| Lab | `design-lab/README.md`、`design-lab/AGENTS.md` |

`onDesignLab` 虽然已有预留传递，但 Level 3 并未真正完成调用。最后 `theory.reveal` 仍是 End of preview 占位，不能只以“有 prop”就判定接通。

### 8.2 构建和效率

- 按需使用 Vite 预览，不要每调一个字幕都重建所有 ZIP 或同步全部分支。
- 游戏 `npm run cinematic:prepare` 使用本机 `node_modules/.cache/level1-cinematic/` 缓存。新环境缓存／外部原片可能不存在；用 `LEVEL1_ANIMATION_SOURCE=/真实路径 npm run cinematic:prepare` 指向固定同伴源码。缺缓存不是删动画或改回 placeholder 的理由。
- 游戏 TypeScript 改动跑 `npm run check`，再跑与本次改动相关的行为检查。正式交付执行 `npm run package:previews`、`npm run test:release`，同步六个固定游戏 ZIP；别只换其中一个。
- 六包：Level1-play、Level2-play、Level3-play、Full-game-play、Level3-and-Full-game-play、Gaming-the-System-complete，均在 `play/`。
- Lab 独立命令 `npm run lab:check`、`npm run lab:build`、`npm run lab:package`，不应为文案微调去重打游戏六包。
- Go 需真实编译器；当前环境可用 `/workspace/.tools/design-lab-go/go/bin/go`，也可通过 `DESIGN_LAB_GO` 指定。新环境按 README 检查，不能假定绝对路径一直存在。
- 完整游戏目前是自包含 HTML，文件较大。最终本地服务如需分离资源、缓存与按需加载，要保持既有规则及离线包能玩；21 人课堂应做加载验证。
- 大改或合并前留已推送基线；不改历史包、不强推、不为整理而重写历史。仅更新实际工作的分支。

### 8.3 合并后最低验收

- 开头三学生必看、箭头醒目，邮件不顿挫缩放；姓名含中文／英文时贯穿游戏和动画。
- Level 1 六项各自对应正确影片；评分语义明确；邮件两秒出老师思考；无绿色块、旧聊天、进度条及 Alex 残影。
- Evaluate 数值仍动，结算管理卡静态、学生卡强调；按钮位置与四步导航不变。
- Level 2 的明确假设及 10→25→100 节奏保留，过渡不是直接跳原始控件。
- Level 3 覆盖一高两低、两高一低、渐变、相近非平均、权重变但 effort 不变；只做两轮也能完成。影片、Hint、Students、比较表不能互相矛盾。
- 动画只结束一次、完成回调只触发一次；重播／隐藏标签／减少动态模式不导致重复推进或黑屏。
- Lab 最多 21 人，展示排除本人且无倒计时、选择后自动下一份、提前完成等待、匿名与投票不可修改、12 秒静态排名、两问及分层理论揭示按规定工作。
- 游戏误退出不保存，不向 Lab 同步游戏信息；真实 Windows 启动与课堂网络需另外实测。

## 9. 已作废／容易误恢复的旧方案

| 历史方案 | 最新状态 |
| --- | --- |
| Level 3 默认平均，必须试出平均，固定三轮 | 未分配起步；平均可不出现；两轮可结束，第三轮可选 |
| effort 固定 25%／67% 档 | 全三项相对比较，10 点相近容差 |
| Hint 只覆盖一高两低 | 用真实低投入列表，覆盖两高一低与全部其他合法组合 |
| Level 1 common ending、师生结算聊天、额外 Results 阶段 | 删除；动画属 Observe，结算不再重复对话 |
| 结算 Management 动态上升后才出 Students | 后来改成 Management 静态，Students 边框强调；Evaluate 的原始动态保留 |
| 邮件逐行出字、绿色指标／达标块、长时间后才出老师字幕 | 邮件一起显示、去绿色块、真实显示 2 秒后出思考 |
| Lab 反应无明确含义，或鲜花／泼水／炸弹三种 | 仅鲜花同意、炸弹不同意 |
| 展示自己的作品、计时跳过未选内容 | 每人只看别人；未选择不前进，选择后自动下一份，全员结束后统一排名 |
| 专门防捣乱和复杂房间加入 | 用户要求去掉；不新增这些流程 |
| 给玩家长时间写作、再写结尾反思 | 固定 90 秒短写；结尾只看两问和 Goodhart |
| 必须付费线上托管／新增云同步 | 免费本地优先，Windows 主机＋学生浏览器 |
| 理论后永远不得跳 Lab | 旧文件当时只做到预览；最终目标是游戏接 Lab，目前尚未合并 |

旧 `AGENTS.md`、Level handoff、版本报告包含阶段性分支约定和文案，尤其旧 Level 1 Target／Run evaluation／对话与旧 Level 3 强制路径。**读它们了解接口，不要机械恢复历史要求。** 继续工作时结合用户的新任务更新工作分支约定，不在保存的基线上直接覆盖。

## 10. 可直接转发给下一位 AI 的任务说明

> 请先读 docs/NEXT_AI_HANDOFF.zh-CN.md，并核对固定基线。已通过的开头＋三关＋Level 1 动画在 6385649，独立 Lab 在 33d93d2 且已继承游戏。接下来的合并不要重做已确认玩法，也不要修改同伴仓库。先列出现有动画交付能覆盖哪些真实 scene 请求，缺什么；在新的合并分支做适配，保留原始基线。尤其保留姓名同步、三关评分语义、Level 3 相对 effort 与自由两／三轮路径，以及 Lab 免费本地／匿名／只展示别人作品且投票不计时的规则。用户后续指示决定具体先合哪段；别把尚未接入的片段说成完成。完成可见改动要给可玩 ZIP，并说明实测范围。

## 11. 固定版本下载

- [已通过完整游戏总包（含完整与三个独立关卡）](https://github.com/suojin311-creator/gamingthesystem_game/blob/63856491e62c52d5a9bdb176ea738abbe6c6c9c7/play/Gaming-the-System-complete.zip?raw=true)
- [仅完整游戏包](https://github.com/suojin311-creator/gamingthesystem_game/blob/63856491e62c52d5a9bdb176ea738abbe6c6c9c7/play/Full-game-play.zip?raw=true)
- [已通过的独立 Design Lab Windows 包](https://github.com/suojin311-creator/gamingthesystem_game/blob/33d93d25a412d2086bb676217844cb1f796402f0/play/Design-Lab-local.zip?raw=true)
- [合并新版 Level 1 之前的备份总包](https://github.com/suojin311-creator/gamingthesystem_game/blob/32a91fe4bfb1cb193040410c846ebc165f8b9d5d/play/Gaming-the-System-complete.zip?raw=true)

本说明不改变现有游戏、动画或 Lab 可玩文件。文中的“已验证”描述已有版本的验证记录，不表示本次交接又执行了一遍课堂实测。
