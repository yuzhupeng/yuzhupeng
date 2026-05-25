 
 
 

![Image](https://pbs.twimg.com/media/HI901fSbcAAdHFY?format=jpg&name=medium)

 
Claude Code CLI 命令大全：60 个原生命令一次讲清，照着用就行

 

 
> 一篇给 Claude Code 新手的命令速查教程。这也是我自己的学习笔记。

你刚装好 Claude Code，进了终端，闪着光标的 > 提示符摆在那里，你大概会有这几个困惑：

-   一启动是 sonnet，我想用 opus 怎么换？
    
-   对话长了卡得要死，听说有 /compact 但不知道什么时候该按
    
-   AI 一通操作把我项目改崩了，能不能撤回去？
    
-   CLAUDE.md 是啥？为啥每个教程都让我写一份？
    
-   想让 AI 自己跑测试、跑构建，怎么不用每次点确认？
    

这些问题对应的命令都在下面。先把官方那张「全命令表」翻译成人话，再挑出最常用的几组教你怎么搭着用。

## 把这张图收藏好，命令直接对照查

下面这张是这篇文章的精华——把 60+ 个命令、按类别、配上场景说明、密密麻麻铺在一张图里。看不清就放大看，需要哪条命令看一眼就找到。后续我会针对个别详细讲，比如agent 创建员工等。

[

![Image](https://pbs.twimg.com/media/HI909qqbgAAnOsN?format=jpg&name=large)





](/gaoqian2580/article/2057994075186622633/media/2057992157504700416)

## 

装一下，登录，开干

[

![](https://pbs.twimg.com/profile_images/2052192798347239425/nVtT6QZd_x96.jpg)

](/gaoqian2580)

AI搞钱研究院

@gaoqian2580

·

[May 16](/gaoqian2580/status/2055506999211885045)

![Article cover image](https://pbs.twimg.com/media/HIael9xaAAEJTar?format=jpg&name=medium)

Article  文章

Mac纯国内网络无翻墙｜Claude CLI 保姆级安装使用教程（全程国内镜像、零代理）

我是搞钱研究院 前几天买了电脑，开始装了Claude code ，遇到了一些坑 总结了一下 现在能搜到的教程都不能用，要么是要设置代理，要么就是很慢 用这个教程可以丝滑解决 适用设备：全部Mac设备（Intel芯片 + Apple...

5

9

9

[

3.1K



](/gaoqian2580/status/2055506999211885045/analytics)

## 

  

记一句话就行：消息开头敲 /，会弹出所有可用命令，继续打字会自动过滤。

```text

> /comp

/compact Free up context by summarizing the conversation

/config Open the Settings interface

```

命令只在消息最开头才生效。前面有别的字，AI 就当成普通文本读了。

命令带参数的写法很自然：

```text

/model opus

/effort high

/btw 这个项目的 Node 版本要求是几？

```

下面按 8 个大类把命令铺开。每类先讲场景，再列命令。

[

![Image](https://pbs.twimg.com/media/HI92WxEaIAAVgSj?format=jpg&name=medium)





](/gaoqian2580/article/2057994075186622633/media/2057993688232632320)

## 

一、会话与上下文：省 Token 防串戏

Claude 的回答质量，70% 取决于它"看到"的上下文。这一类命令就是控制它能看到什么、看到多少。

/clear 清空当前对话

写完一个 Bug 修复，准备开新功能，第一件事是 /clear。

旧任务的所有讨论会被一笔勾销，AI 不会再被前面的代码思路带偏。它的别名是 /reset 和 /new，记哪个都行。

注意：/clear 不会动你的 CLAUDE.md 和已加载的 skills，那些是项目级记忆。被清掉的只是当前这一通对话。

/compact 压一压，腾空间

长对话快撑不住的时候，比 /clear 温和的选择是 /compact。

它会把前面 N 轮对话提炼成一份精简的"技术摘要"，把 Token 占用打回原形，关键信息还在。

```text

/compact 重点保留我们对认证模块的设计决策

```

带个 focus instruction，让它知道哪部分不能丢。

什么时候按？看下面这个命令——

/context 看看上下文吃了多少

输入 /context，Claude 会用一张彩色网格告诉你：

-   系统提示占多少
    
-   skills 占多少
    
-   历史对话占多少
    
-   还有多少富余
    

一旦看到接近 80%，就该 /compact 了。这是经验法则，也是防止 AI 突然"失忆"的关键。

/resume 接回历史会话

昨天写到一半的活，今天回来继续。

```text

/resume

```

不带参数，开个交互式选择器；带 ID 或会话名也行。背景会话（/background 推到后台的那种）也会列在里面，标着 bg。

它的别名是 /continue。

/branch 开个平行宇宙

主线对话很顺，但你想试一个激进重构，又怕翻车。这时候用 /branch：

```text

/branch 试试用 Zustand 替换 Redux

```

分支出去，主线原封不动。实验失败 /resume 回主线就行。别名 /fork。

/btw 顺嘴问一句

正在做核心业务，突然想问"这个依赖最新版是几"。

```text

/btw axios 最新稳定版本是多少

```

进入主线上下文。本质上是给主线对话开了个临时通话，不污染主对话的记忆。

/rewind 时光倒流

最关键的"撤销键"。

```text

/rewind

```

到之前任意一个检查点。特别适合 AI 一连改了 8 个文件、跑起来全崩、你也忘了到底改了啥的时候。

别名 /checkpoint 和 /undo。

这一类还有

-   /rename \[新名字\] — 给会话改名，方便 /resume 时认
    
-   /export \[filename\] — 把对话导出成纯文本，归档或者复盘
    
-   /recap — 一句话总结当前进度
    
-   /goal `<condition>` — 设个目标，AI 会跨多轮一直推进直到达成
    
-   /focus — 全屏模式下只显示最后一次问答，看着清爽
    

## 

二、代码开发：从规划到验证一条龙

这一类是干活时按得最多的。

/plan 先想后做

跨多个文件的大改动，先 /plan 再说：

```text

/plan 把所有 axios 调用改成 fetch，统一错误处理

```

你列出受影响的文件、改动顺序、潜在风险，完全不动代码。你点头确认后再退出规划模式去执行。

省下的不是时间，是返工。

/diff 看看到底改了啥

```text

/diff

```

弹出一个交互式 diff 浏览器，左右键切换是看 git 整体 diff 还是看 AI 单轮的改动，上下键浏览文件。比你打开 VS Code 看 diff 还快。

/review、/code-review、/security-review 三道关

提交前的标准动作：

-   /review \[PR\] — 本地代码评审，挑 Bug 和坏味道
    
-   /code-review — 专扫正确性 Bug，可以用 effort 级别调强度（/code-review high）
    
-   /security-review — 安全审计，找注入、硬编码密钥、权限漏洞
    

老版本里的 /simplify 已经合并进 /code-review 了，旧名字还能用，知道就好。

/run 和 /verify 让 AI 真跑起来验证

AI 写完代码说"应该好了"，你心里没底。让它真启动一下：

```text

/run

```

它会读你的 package.json、Makefile 之类的，把 App 跑起来，自己驱动它看一眼是不是真生效。

/verify 更进一步：构建、运行、观察结果，不靠测试和类型检查兜底，直接看 App 的真实表现。

如果你的项目启动姿势复杂（要数据库、要 env、要前端编译），先跑一次 /run-skill-generator，它会把启动配方记成一个项目级 skill 存到 .claude/skills/run-`<name>`/，以后 /run 和 /verify 都按这个配方来。每个项目跑一次就行。

/add-dir 临时加目录

工作中突然要参考另一个仓库的代码：

```text

/add-dir ~/code/another-project

```

当前会话就能读那个目录里的文件了。/clear 不会清这个加进来的目录，要清得用 /permissions 里的工作目录管理。

/copy 复制上一条回答

最后一条 AI 回复有代码块？敲 /copy，弹出一个选择器，可以挑单个代码块或全部内容复制到剪贴板。

要复制再上一条？/copy 2，倒数第二条。在选择器里按 w 还能直接写到文件里，SSH 远程开发时特别好用。

## 

三、智能体与并发：让 AI 自己组队干

下面这一类是 Claude Code 的"高阶玩法"，初学者可以先扫一眼，知道有这功能就行，需要时回来查。

  

/batch 大任务拆并行小队

  

```text

/batch 把 src/ 下所有 React class 组件迁移成函数组件

```

它会先研究代码库，给你一份执行计划。你点确认后，每个小任务在独立的 git worktree 里并行跑，每个跑完开一个 PR。

需要项目是 git 仓库。一个早上跑完一个跨 30 个文件的迁移，没夸张。

/agents 管子智能体

子智能体（subagent）是 Claude Code 的多角色系统：你可以预定义好几个专项 agent（比如"测试专家"、"安全专家"、"重构专家"），主线对话遇到对应任务时，主 Claude 把活派给它们。

  

```text

/agents

```

打开管理面板、新建 agent、改 agent 的工具权限。

/tasks 看后台跑啥呢

后台任务列表。/batch 派出去的子任务、/background 推到后台的会话、/loop 在循环跑的活，全在这里。/bashes 是它的别名。

/background 把整个会话踢到后台

  

```text

/background 继续跑测试，跑完发我通知

```

腾出来给你干别的。后面用 claude agents 命令在终端外查它的状态，或者 /resume 拉回前台。别名 /bg。

/loop 定时循环

  

```text

/loop 5m 检查部署状态，部署完了告诉我

```

每 5 分钟跑一次。不指定 interval，Claude 会自己控节奏。也可以把循环里要做的事写在 .claude/loop.md，命令什么都不带就执行那份。别名 /proactive。

/schedule 云端例行任务

  

```text

/schedule

```

Claude 会跟你聊天式地一步步配置一个云端例行任务：每周一早上 9 点扫一次依赖更新、每天午夜跑一次安全审计……跑在 Anthropic 的云上，不占你本地资源。别名 /routines。

这一类还有

-   /autofix-pr \[prompt\] — 监听当前分支的 PR，CI 挂了或评审有意见就自动修。需要 gh CLI
    
-   /teleport — 把网页版
    
    [claude.ai](//claude.ai)
    
    上的会话拉进当前终端继续聊。别名 /tp
    
-   /remote-control — 反过来，把当前本地会话开放给
    
    [claude.ai](//claude.ai)
    
    远程接管。别名 /rc
    
-   /ultraplan `<prompt>` — 在云端 sandbox 起一个深度规划任务，浏览器审阅后再打回终端执行
    
-   /ultrareview \[PR\] — 多 agent 深度评审，包含 3 次免费配额（Pro/Max）
    
-   /stop — 附在后台会话时停掉它（要保留 transcript 用 /exit 脱离即可）
    

## 

四、模型与算力：在速度和深度之间挑一个

/model 切模型

```text

/model opus

/model sonnet

/model haiku

```

不带参数会开选择器。普通搬砖、改个 Bug、写测试用 sonnet 就够；遇到逻辑绕的算法、跨多文件的架构题，切 opus。

选择器里在某行按 d，可以把这个模型设成新会话默认。

/effort 思考强度

```text

/effort high

```

可选 low / medium / high / xhigh / max，越往上 AI 越深度思考，但响应更慢、Token 更贵。auto 会重置为模型默认。

不带参数会弹出一个交互式滑块，左右键调，回车确认。改完立刻生效，不用等当前回答跑完。

/fast 极速流

```text

/fast on

```

牺牲一些复杂推理换响应速度。。聊设计、聊架构不要开；写脚手架、改 boilerplate 时开着挺爽。

/config 设置面板

  

```text

/config

```

主题、默认模型、输出风格、编辑器模式（包括 Vim 模式）都在这里。/settings 是它的别名。

注意：老版本里有个独立的 /vim 命令，新版本已经合并到 /config → Editor mode，找不到 /vim 不要慌。

/output-style 输出风格

  

```text

/output-style

```

让 AI 回答得更简短直接，或者更详尽冗长。看场景选。

## 

五、项目记忆：让 AI 记住你的规范

这一类是 Claude Code 的灵魂，也是新手最容易忽略的。

/init 给项目一份记忆

第一次进项目，先跑这个：

  

```text

/init

```

生成一份 CLAUDE.md。这份文件每次启动 Claude Code 都会自动加载，里面写的是：

-   项目用什么语言、什么框架
    
-   怎么编译、怎么测试、怎么 lint
    
-   有没有特殊约束（不要引入新依赖 / 不要动某些目录）
    
-   团队规范（命名风格、commit 信息格式、分支策略）
    

写得越具体，AI 越听话。

/memory 编辑记忆文件

```text

/memory

```

直接打开 CLAUDE.md 编辑。也能在这里管理"自动记忆"——Claude 会从对话里抽取它觉得有价值的事实自动追加进来，你能看着、删着、改着。

实操技巧：每次发现 AI 又踩了同一个坑，立刻 /memory 把这条规则加进去。下次它就记住了。

/skills 看技能、管技能

```text

/skills

```

列出当前会话能用的所有 skill：用户级的、项目级的、插件带的。按 t 按 token 占用排序，按空格隐藏不想让 AI 看到的，按回车保存。

如果你不知道什么是 Claude Skill，可以看看这篇 Skills 入门。

这一类还有

-   /insights — 分析你的开发会话，找出高频摩擦点和架构演进规律。复盘神器
    
-   /team-onboarding — 从你近 30 天的使用历史，生成一份团队新人入职指南
    
-   /fewer-permission-prompts — 扫历史，自动给你常用的只读 Bash 命令和 MCP 工具加白名单，少弹窗
    
-   /claude-api — 载入 Claude API SDK 的参考文档，还能 /claude-api migrate 自动升级旧代码到新模型
    
-   /powerup — 交互式小课程 + 动画演示，挖一些你不知道的功能
    

## 

六、诊断与计费：看花了多少、坏了去哪修

/usage、/cost、/stats 都是同一条

  

```text

/usage

```

订阅用户看：每日额度用了多少、剩多少、连续打卡多少天。

按量付费用户看：当前会话花了多少美元。

/cost 和 /stats 都是它的别名，/stats 默认打开 Stats tab。

/usage-credits 触顶后续命

订阅额度炸了想继续工作？

```text

/usage-credits

```

配置一下，超额后自动按量付费继续。这条命令以前叫 /extra-usage，新版本改名了。

/doctor 环境一键体检

装完发现不工作？升级后行为变怪？

```text

/doctor

```

它会逐项检查 CLI 安装、二进制依赖、Node 运行时、网络连通、配置文件一切是否正常。每项前面有状态图标，按 f 让 AI 自动尝试修复有问题的项。

/status 看当前状态

  

```text

/status

```

打开设置面板的 Status tab：版本号、当前用的模型、登录账号、网络连接质量。AI 在回答中也能直接打开看，不用等当前回答跑完。

这一类还有

-   /debug \[description\] — 开启调试日志，定位某个问题。写明描述能让分析更聚焦
    
-   /heapdump — 写一份 JS 堆快照到桌面，排查内存爆炸
    
-   /release-notes — 交互式查看更新日志，挑版本看
    
-   /help — 最简交互速查表
    

## 

七、权限与扩展：管 AI 能动什么

/permissions 自动放行

最值钱的一条命令之一。

  

```text

/permissions

```

打开权限管理面板。这里你可以：

-   把 git status、npm test、ls \* 这些只读 / 安全命令设成自动放行，再也不用每次点确认
    
-   把 rm -rf 这种危险命令设成永远拒绝
    
-   给具体的 MCP 工具或 skill 单独配权限
    

第一周配一次，整个使用体验直接起飞。别名 /allowed-tools。

懒得手动配？跑 /fewer-permission-prompts，它从历史里找你常用的只读命令，自动给你列一份白名单写到 .claude/settings.json。

/sandbox 沙盒隔离

```text

/sandbox

```

开/关沙盒模式。开启后 AI 的代码执行被严格限制，碰不到宿主机文件系统外的东西。给陌生项目跑实验代码时建议开。

/mcp 管 MCP 服务器

  

```text

/mcp

```

MCP 是模型上下文协议，用来挂外部数据库、本地知识库、第三方工具到 Claude。这条命令管所有 MCP 服务器的连接、OAuth 鉴权、状态检查。

/hooks 看生命周期钩子

  

```text

/hooks

```

查看当前配的工具事件 hooks。Hooks 能在文件保存、prompt 提交、工具调用前后等节点插入自动化逻辑（跑 lint、跑测试、发通知）。

/plugin 管插件

  

```text

/plugin

```

Claude Code 支持插件机制，插件能打包 skills、MCP 服务器、hooks 一起分发。这条命令管插件的安装、启用、禁用。配套的还有 /reload-plugins 不用重启就重载所有插件。

## 

八、账号、界面、个性化：一次配完管很久

这些大都是装好的第一周配一次，之后基本不动：

-   /login / /logout — 登录登出 Anthropic 账号
    
-   /theme — 配色主题，包含 dark / light / 色盲友好（daltonized）/ ANSI 等
    
-   /color \[color|default\] — 单独改提示符底条颜色，支持 red / blue / green / yellow / purple / orange / pink / cyan
    
-   /terminal-setup — 一键配好 Shift+Enter 这种键位。VS Code、Cursor、Windsurf、Alacritty、Zed 用户必跑
    
-   /keybindings — 直接编辑键位配置文件
    
-   /statusline — 配状态栏，描述一下你想要什么效果，AI 帮你生成
    
-   /scroll-speed — 调鼠标滚轮速度，全屏模式专用
    
-   /chrome — 在 Chrome 里配 Claude
    
-   /ide — 管 IDE 集成的状态
    
-   /feedback \[report\] — 提 Bug 或反馈，自动附会话上下文（脱敏）。别名 /bug 和 /share
    
-   /exit — 退出。在附在后台会话时，它只是脱离不停止。别名 /quit 和 /bye
    

## 

还没进交互模式时，CLI 也有几个常用 flag

不进交互模式，从普通终端直接发命令也很高频：

```text

# 接着上次最后一个会话继续

claude -c

claude --continue

  

# 单次任务，跑完就退

claude -p "扫一遍 src/ 里有没有重复的工具函数"

  

# 给文件喂进去让 AI 处理

cat logs.txt | claude -p "找出最严重的 5 条错误"

  

# 升级到最新版

claude update

```

  

  

## 

几条最值钱的高频组合

知道命令是一回事，会搭配才是另一回事。下面这几组是我自己天天在用的：

进新项目 = /init + /memory + /permissions

新项目第一天，三条命令配完，整周顺畅。/init 让 AI 知道项目长啥样，/memory 写清楚团队规范，/permissions 把常用命令免签。

大重构 = /plan + /effort high + /model opus

跨多文件的活，先用强算力规划，确认方案再切回 sonnet 写代码。算力花在刀刃上。

长对话 = /context + /compact + /rewind

看占用、压一压、出错回滚。三连让你不必整天提心吊胆"AI 是不是又忘了上下文"。

提交前 = /code-review + /security-review + /diff

正确性、安全、改动范围三道关，比手动 review 快多了。

一改全崩 = /rewind

不要一行行去撤。一键回到刚才那个还能跑的检查点，重新开。

## 

写在最后

Claude Code 的命令多，但你不用一次记住。先把下面这 10 条记熟，覆盖 80% 的日常场景：

```text

/init 进新项目第一条

/memory 改项目记忆

/clear 开新任务前清场

/compact 上下文快爆了压一压

/plan 大改动先规划

/diff 看 AI 改了啥

/review 提交前检查

/rewind 改崩了一键还原

/model 切模型

/permissions 配自动放行

```

剩下的等用到了再回来翻速查图。命令不是越多越好，是用熟几个关键的才好。这也是我自己的学习笔记。

祝你少弹窗、不返工、改不崩。

看到这里的朋友，觉得有用可以点个关注，后续会持续更新 AI 实用教程，搞钱干货。

有任何配置问题、使用问题，都可以在评论区留言，我看到都会一一回复！

Want to publish your own Article?  
想发表自己的文章吗？

[Upgrade to Premium  
升级至高级版](/i/premium_sign_up)

[9:16 AM · May 23, 2026](/gaoqian2580/status/2057994075186622633)

·

[

20.8K

Views](/gaoqian2580/status/2057994075186622633/analytics)

52

49

177

241

Relevant  
相关的

[View quotes  
查看报价](/gaoqian2580/status/2057994075186622633/quotes)
