# 已确认的 Ending → Design Lab 文案

本表记录用户确认的跨阶段文案。本次只实现 ending；Design Lab 的写作题、
第一反问与最终引文尚待在独立的 `feature/design-lab-local` 分支更新。

|位置|确认英文|
|---|---|
|Ending 开头 · You|Maybe it’s not just about finding the perfect weights…|
|LEVEL 1 回忆|One metric became the target.|
|LEVEL 2 回忆|More metrics became a checklist.|
|LEVEL 3 回忆|The weights changed. Learning still came second.|
|回到办公室 · You|Am I improving learning, or just improving the numbers?|
|Ending 入口标识|NEXT · DESIGN LAB|
|Ending 入口主标题|Share what real / learning looks like.|
|连接游戏经历|You’ve seen how numbers shaped Alex’s choices.|
|下一步具体任务|Now write a short reflection, then read and vote on your classmates’ ideas.|
|Ending 按钮|ENTER DESIGN LAB →|
|Design Lab 写作题|How would you know Alex is really learning?|
|排名后第一问|Did the most flowers mean the deepest thinking?|
|排名后第二问|Did knowing there would be a ranking change what you wrote?|
|Design Lab 最终标题|Goodhart’s Law|
|Design Lab 最终引文|When a measure becomes a target, it ceases to be a good measure.|

斜线表示标题换行，不显示斜线字符。中文解释不放进动画。
最新入口页替代了用户认为意义不明的「When the number becomes the goal…」总结页，
用游戏关联和明确任务说明继续前进的目的；移除原来的短横线装饰。

Ending 不显示 Goodhart 名称或上述理论引文，不提前增加一次写作疑问。
这个疑问直接作为 Design Lab 的写作题，替代旧题
「What do we reward too much—and what deserves more?」，题目下不增加解释小字。

Design Lab 的匿名展示、投票和最终排名事前说明保留；玩家经历活动后，
依次讨论作品受欢迎与思考质量、排名对自己的写作的影响，再揭示理论。
最终引文使用用户指定的通俗表述，不采用旧版的 1975 长句。

Design Lab 当前实现位于 `feature/design-lab-local` 的
`design-lab/src/App.tsx`；核对版本为
`0db8d3d1941d701ae6a3235649f0f83ea028011c`。它仍是独立的本地课堂活动，
尚未与 ending 按钮连接；此次动画 ZIP 里的按钮保持展示入口。
