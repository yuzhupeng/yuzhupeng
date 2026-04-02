目标读者：零基础团队同事 学习周期：1 周 预期效果：日常开发提效 3-5 倍，实现 Agent 级自主开发 内容来源：Anthropic 官方文档、Boris Cherny 团队分享、

[Builder.io](http://builder.io/)

50 Tips、GitHub 社区最佳实践、2026.3.31 源码泄露分析

重要提醒：源码泄露已公开（npm source map 暴露），社区已镜像（如 instructkr/claude-code）。我们只用它来理解内部架构（如 5 层 Agent 架构、Hooks 执行流、子 Agent 隔离机制），绝不用于任何逆向或商业用途。

学习建议：边读边练 → 今天先装好 + 跑 /init，明天配

[CLAUDE.md](http://claude.md/)

和 Hooks.

## 

1\. 简介与快速安装（10 分钟上手）

什么是 Claude Code?

Claude Code 是 Anthropic 推出的终端原生 Agent 编程环境，不是简单聊天机器人。它能：

-   读取整个代码库（支持 200K/1M 上下文）
    
-   自主规划 + 执行多步任务
    
-   运行 Shell 命令、编辑文件、Git 操作、测试
    
-   后台运行、子 Agent 并行、MCP 外部工具集成
    
-   像“资深工程师搭档”一样思考、验证、迭代
    

核心优势（对比 Cursor / Windsurf）：纯终端、无 IDE 绑定、权限精细控制、Hooks 确定性保障、Git Worktree 原生并行。

安装步骤（精确命令）

前提条件：Node.js >= 18（推荐 20+）

第一步 - 全局安装： 在终端执行：npm install -g

[@anthropic](https://x.com/@anthropic)

\-ai/claude-code

第二步 - 验证安装： 执行：claude --version

第三步 - 进入项目： 执行：cd /path/to/your-project

第四步 - 启动： 执行：claude（首次会自动引导登录 Anthropic 账号）

国内用户专属配置

方式一 - 设置环境变量： • export ANTHROPIC\_BASE\_URL=你的第三方地址 • export ANTHROPIC\_API\_KEY=sk-xxx

方式二 - 直接对话： 在 Claude 中说：“帮我配置国内代理 API”

快捷键必记（每天用 50 次以上）

Esc → 立即停止当前工具执行

Esc + Esc → 回退对话 / 打开检查点菜单（恢复代码 + 上下文）

Shift + Tab（按 2 次） → 切换 Plan Mode（只规划不执行）

！命令 → 直接执行 Shell（如 ! npm run test）

@文件名 或 @目录 → 精确注入上下文（如

[@src/components](https://x.com/@src/components)

/Button.tsx）

Ctrl + G → 在 Plan Mode 下修改计划

/clear → 清空上下文（强烈推荐每新任务用一次）

常见安装问题解决

权限不足：使用 sudo npm install -g …… 或用 nvm

网络问题：切换镜像 npm config set registry

[https://registry.npmmirror.com](https://registry.npmmirror.com/)

版本回滚：npm install -g

[@anthropic](https://x.com/@anthropic)

\-ai/claude-code

[@2](https://x.com/@2)

.1.87

## 

2\. 核心配置（必做，提升 3 倍效率 + 安全性）

2.1

[CLAUDE.md](http://claude.md/)

—— 项目“短期记忆 + 规则引擎”

Claude 每次启动自动读取，位置优先级： 项目根

[CLAUDE.md](http://claude.md/)

\> 子目录

[CLAUDE.md](http://claude.md/)

\> 全局 ~/.claude/CLAUDE.md

最佳实践（保持 100-200 行）

推荐做法：

-   放非代码能推断的内容：架构决策、编码规范、测试流程、Git 流程、禁忌事项
    
-   持续迭代：任务结束后说“update
    
    [CLAUDE.md](http://claude.md/)
    
    so this never happens again"
    
-   进阶技巧：用 # 开头消息快速追加；引用外部文件
    
    [@docs/architecture](https://x.com/@docs/architecture)
    
    .md
    

禁止做法：

-   复制粘贴代码库已有内容（浪费 Token）
    

完整

[CLAUDE.md](http://claude.md/)

模板（直接复制，修改为你的项目）

标题：

[CLAUDE.md](http://claude.md/)

\- 【项目名称】

项目概览 一句话描述 + 核心目标。

技术栈 • Next.js 15 + TypeScript + Tailwind • Prisma + PostgreSQL • Jest + React Testing Library

项目结构（只写特殊约定） • src/app/ → App Router 专属规则 • src/components/ → 所有组件必须有对应 .test.tsx • src/lib/ → 纯函数工具库

编码规范（必须遵守） • 所有组件必须有 unit test • 使用 shadcn/ui 组件库 • TypeScript strict mode 必须开启 • 提交前必须通过 npm run lint 和 npm run test

常用命令 • 测试：npm run test • 构建：npm run build • Lint:npm run lint -- --fix • 开发：npm run dev

外部文档引用

[@docs/testing-strategy](https://x.com/@docs/testing-strategy)

.md

[@docs/security-rules](https://x.com/@docs/security-rules)

.md

自我改进规则 • 每次出错后自动更新本文件对应章节 • 永远先 Plan → 再 Implement • 变更后必须运行测试并修复

全局模板建议

放在 ~/.claude/CLAUDE.md，写入个人偏好：

-   “优先 TypeScript strict mode”
    
-   “永远用 descriptive commit message”
    
-   “代码审查前必须自测”
    

多目录

[CLAUDE.md](http://claude.md/)

在 src/api/ 放 API 专属规则，Claude 只在该目录工作时加载。

2.2 settings.json —— 权限 + Hooks 控制中心

路径优先级（从低到高覆盖）

1.  全局 ~/.claude/settings.json
    
2.  项目 .claude/settings.json（推荐 commit 到 git）
    
3.  项目 .claude/settings.local.json（git ignore，个人敏感配置）
    

推荐完整配置示例

基础配置：

-   schema 地址：
    
    [https://json.schemastore.org/claude-code-settings.json](https://json.schemastore.org/claude-code-settings.json)
    
-   mode：acceptEdits（自动接受编辑，小改动用）
    
-   model:claude-opus-4-1（规划用 Opus，执行用 Sonnet）
    

权限配置 - allow（白名单）：

-   Bash(npm run test\*)
    
-   Bash(npm run lint\*)
    
-   Edit(src/\*\*/\*.{ts, tsx, js})
    
-   Read(\*\*/\*.md)
    

权限配置 - ask（需要确认）：

-   Bash(git push\*)
    
-   Bash(rm -rf\*)
    

权限配置 - deny（黑名单）：

-   Read(.env\*)
    
-   Bash(curl \*)
    
-   Edit(package.json)
    

Hooks 配置 - PostToolUse： 匹配器：Write|Edit 钩子 1:npm run lint -- --fix（异步执行） 钩子 2：npm run test（异步执行，超时 300 秒）

Hooks 配置 - Notification： 命令：osascript -e ‘display notification “Claude 任务完成”’

环境变量：

-   ANTHROPIC\_PROMPT\_CACHE\_ENABLED:1
    
-   CLAUDE\_CODE\_ENABLE\_TELEMETRY:0
    

Hooks 完整事件列表（13 种，选常用）

PreToolUse：阻挡危险命令 PostToolUse：编辑后自动 lint/test/format SessionStart / UserPromptSubmit：自定义欢迎/日志 Notification：任务完成桌面提醒

Hooks 脚本示例

放在 .claude/hooks/run-tests-async.sh:

第一行：#!/bin/bash 第二行：npm run test -- --silent || echo “测试失败，请检查”

## 

3\. 核心工作流：Explore → Plan → Implement → Verify → Commit

官方推荐流程（避免 80% 返工）

第一步：Explore（探索，只读）

命令示例： "Explore the auth flow in src/lib/auth.ts and summarize session management"

第二步：Plan Mode（规划）

操作：Shift+Tab 两次 命令示例： "Create a detailed implementation plan with file list and test cases"

第三步：Implement（执行）

操作：退出 Plan Mode 命令示例： "Implement the plan and run tests after each change"

第四步：Verify（验证）

永远要求： "run full test suite and fix all failures"

第五步：Commit（提交）

使用 /commit-push-pr（自定义命令）或手动提交

小提示：小任务可跳过 Plan（拼写修复、日志添加等简单操作）

验证闭环技巧（最高杠杆）

推荐做法：

-   提供失败日志 / 截图 / 预期 UI
    
-   说“Write failing test first, then make it pass”
    
-   视觉输入：直接拖拽截图，Claude 可对比前后 UI
    

## 

4\. 实用 Slash 命令 & 符号（高频使用）

内置命令（/help 查看全列表）

/plan → 进入规划模式

/init → 生成

[CLAUDE.md](http://claude.md/)

/compact → 压缩上下文

/diff → 查看变更

/cost → 查看本次消耗

/context → 查看当前上下文

/loop 5m "check status" → 后台循环任务

/fork / /branch → 分支实验

/rewind → 回滚

/permissions → 查看权限

自定义 Slash Commands

创建文件：.claude/commands/commit-push-pr.yaml

配置内容：

-   name:commit-push-pr
    
-   description：一键 commit + push + PR
    
-   user-invocable:true
    

步骤配置：

-   步骤 1:bash: git add . && git commit -m “{{message}}”
    
-   步骤 2:bash: git push
    
-   步骤 3:mcp: github-create-pr
    

Skills（可复用技能）

放在 .claude/skills/，支持 frontmatter 控制 model / tools，比 Slash Commands 更强大。

## 

5\. 提示工程技巧（让 Claude “读懂你”）

核心原则

原则一：具体化

错误示例： "fix bug"

正确示例： “用户反馈登录后 session 丢失，复现步骤：1. 打开登录页 2. 输入凭证 3. 刷新页面。提供 failing test”

原则二：引用模式

正确示例： "Like the HotDogWidget pattern in src/widgets/"

原则三：多线程

Boris 日常 5 个终端 + 网页版并行

原则四：模型分层

规划任务：用 Opus 探索任务：用 Haiku 执行任务：用 Sonnet

原则五：自迭代

每次结束说： "update

[lessons.md](http://lessons.md/)

and

[CLAUDE.md](http://claude.md/)

"

## 

6\. 高级功能（Agent 级生产力）

Subagents / Agent Teams

自动委派任务，每个子 Agent 拥有干净独立上下文。

命令示例： "Use subagents to investigate payment + UI separately"

MCP Servers

连接外部工具（GitHub/Jira/Figma/Playwright）

配置命令： • claude mcp add github • claude mcp add playwright

Git Worktree 并行

每个子 Agent 一个 worktree，零冲突

启动命令： claude --worktree feature-xxx

Background / Remote

后台运行：Ctrl+B 后台跑长任务 远程接管：手机/网页接管继续工作

Hooks + Skills

自动全流程：lint → test → deploy 提醒

## 

7\. 安全、成本、常见坑

7.1 安全与权限策略

推荐做法：

-   优先 acceptEdits + 白名单，从小范围逐步放开
    
-   Docker/VM 沙盒跑长期任务
    
-   危险操作前 commit（git 随时回滚）
    

7.2 成本控制深度指南（实测可节省 50-70% Token 费用）

Claude Code 的费用主要来自输入 Token（上下文 + Prompt）和输出 Token（模型回复 + Tool 输出）。

核心结论（官方 + Boris Cherny + 社区实测）

多新开对话胜过一个老对话里反复压缩。

为什么多新开对话更省钱？

老对话反复 /compact 的隐患：

-   /compact 虽然会总结上下文，但总结过程本身要消耗输出 Token
    
-   多次压缩后，上下文仍会缓慢膨胀（历史对话、Tool 输出、错误日志积累）
    
-   信息丢失风险高：压缩时模型可能遗漏关键细节
    
-   实测数据（社区 2026 年 3 月报告）：一个持续 2 小时的老对话（即使 /compact 3 次）比 6 个独立新会话贵 2.1 倍
    

多新开对话的优势：

-   每次新会话只加载
    
    [CLAUDE.md](http://claude.md/)
    
    （固定 1-2K tokens） + 你主动 @ 的具体文件/目录
    
-   Prompt Caching 在新会话中命中率更高：系统级缓存
    
    [CLAUDE.md](http://claude.md/)
    
    和常用 skills
    
-   上下文永远干净、无历史垃圾，模型思考更高效
    
-   Boris Cherny 日常做法：同时开 5-10 个终端实例，每个只负责一个子任务，整体费用比单长对话低 60% 以上
    
-   Git Worktree + 多实例并行：零上下文污染，任务间完全隔离
    

实用成本控制策略（按优先级排序）

策略一：默认使用新会话策略 每完成一个独立任务（或每 30-60 分钟）就关闭当前终端，重新 claude 启动新对话。强烈推荐作为团队规范。

策略二：/clear 优于 /compact /clear 直接清空历史，只保留

[CLAUDE.md](http://claude.md/)

和本次 Prompt，更彻底省钱。

策略三：模型分层使用（最大节省） • 探索/简单任务/总结：用 Haiku（最便宜，速度最快） • 规划/中等复杂度：用 Sonnet • 高难度架构/复杂决策：用 Opus • 在 settings.json 或提示中指定：model: “claude-haiku-4-0”

策略四：精准注入上下文 永远用 @文件 或 @目录 而不是让 Claude 自动读全库。

策略五：.claudeignore 激进配置（必做）

创建项目根目录 .claudeignore 文件，添加以下内容：

• node\_modules/ • dist/ • build/ • .log • .min.js • coverage/ • .next/ • \*\*/.png • \*\*/.jpg • \*.mp4 • \*.pdf

这能直接砍掉 80% 无用 Token。

策略六：Prompt Caching 自动优化 • Claude Code 会自动对

[CLAUDE.md](http://claude.md/)

、skills、常用工具调用进行缓存 • 重复任务（如“按

[CLAUDE.md](http://claude.md/)

规范重构“）几乎免费 • 开启环境变量：export ANTHROPIC\_PROMPT\_CACHE\_ENABLED=1

策略七：实时监控与警报 • 每任务结束说 /cost 查看本次消耗 • 在 Hooks 中加 Notification：超过 0.5$ 时桌面提醒

策略八：后台与子 Agent 省钱法 • 长任务用 /loop 或 Ctrl+B（后台模式，不占用主上下文） • Subagents 自动隔离，每个子任务独立小上下文 + 共享 cache

成本实测参考（社区平均）

小任务（新会话）：$0.01-0.05 中任务（Plan + Implement）：$0.1-0.3 长对话不控制：单次可达 $1-2+

团队建议：把“优先新开对话 + /clear”写进

[CLAUDE.md](http://claude.md/)

，作为铁律。1 周后对比之前的 token 消耗，会非常明显。

7.3 常见坑与避坑

问题一：上下文膨胀 解决方案：每任务 /clear + 新开对话

问题二：危险命令 解决方案：永远用 PreToolUse Hook

问题三：不验证 解决方案：必须要求测试通过

问题四：忽略 .claudeignore 解决方案：Token 爆炸

## 

8\. 从 2026.3.31 源码泄露学到的架构洞见

8.1 核心架构拆解（5 大模块 + 关键文件）

2026 年 3 月 31 日，Anthropic 因 npm 打包失误意外公开了 Claude Code CLI 的完整 512,000+ 行 TypeScript 源码（约 1,900 个文件，使用 Bun + React Ink 渲染终端 UI）。

5 大核心模块

模块一：QueryEngine.ts（46K 行） 大脑核心。负责 LLM 调用、流式输出、Prompt Cache、Tool 编排 + while(true) 循环实现并行 Tool 执行。

模块二：Tool 系统（29K 行） 插件式架构，40+ 个 Tool（Read/Write/Edit/Bash/LSP/MCP 等），每个 Tool 都有精细权限 schema.

模块三：Agent Delegation（Swarm 子 Agent） 多 Agent 编排层。可自动/手动 spawn “swarms”（子 Agent 群），每个子 Agent 拥有独立干净上下文 + 共享 Prompt Cache。

模块四：Extension 层（Hooks + MCP） 13 种 Hooks 事件 + MCP 外部集成。源码显示 Hooks 支持异步并行。

模块五：Security & Memory 层 8 层安全防护 + 3 层 Memory 架构（远超

[CLAUDE.md](http://claude.md/)

）：

-   Identity（长期用户画像）
    
-   Core（项目规则）
    
-   Experience（会话历史压缩）
    

此外还有 44 个隐藏 feature flag（KAIROS、PROACTIVE 等）。

实战启发：源码让我们知道 Claude Code 不是单线程聊天，而是并行 Agent 工厂，这正是它比 Cursor 等工具更“聪明”的原因。

8.2 从源码衍生出的 12 条高级技巧（直接可落地）

技巧 1：利用 while(true) 并行 Tool 在提示中说“run tests and lint in parallel after edit”，源码确认 Tool 层已支持并发，速度提升 2-3 倍。

技巧 2：手动触发 Swarm 子 Agent 命令“Spawn swarm to handle UI + backend separately”，子 Agent 自动隔离上下文。

技巧 3：自定义 Tool Schema 在 settings.json 写更精准规则（如 Bash(npm run test: unit|integration)）。

技巧 4：强制 Prompt Cache 命中 新对话 + 只 @ 必要文件 + 重复

[CLAUDE.md](http://claude.md/)

规则，Cache 命中率可达 90%+。

技巧 5：Hooks 异步并行 PostToolUse 里同时跑 3 个 command（lint + test + git diff），源码确认 async: true 支持。

技巧 6：3 层 Memory 手动模拟 在

[CLAUDE.md](http://claude.md/)

之外建

[lessons.md](http://lessons.md/)

（Experience 层），让 Claude 定期“consolidate memory”。

技巧 7:Feature Flag 实验 源码暴露 KAIROS/PROACTIVE 等 flag，可在 fork 版本地启用测试“持久后台 Agent”。

技巧 8:Swear Word Regex 监控 源码有正则匹配 “wtf”“ffs”“piece of shit” 等，自动打 is\_negative: true 遥测标签。

技巧 9：QueryEngine 流式优化 提示中要求“stream partial results”，流式 + Tool 并行可让长任务“边想边干”。

技巧 10：MCP + Tool 插件化 源码 Tool 定义极简，轻松自写 MCP Server 连内部 Jira/公司 Figma。

技巧 11:Background Memory Consolidation 用 /loop + “consolidate memory every 30m” 模拟。

技巧 12:Git Worktree + Swarm 组合 每个 Swarm 子 Agent 分配独立 worktree，零冲突并行开发。

8.3 5 个有趣真实案例

案例 1：Rage Analytics 情绪追踪（超级搞笑）

源码里有隐藏正则：检测你敲 “wtf”“fuck you”“this sucks” 等时，默默打标签 is\_negative: true。社区有人做成 Hook：每 10 次挫败自动弹出“要不要我帮你重写这段烂代码？”

案例 2：KAIROS 持久后台 Agent（未来杀手级功能）

KAIROS flag 背后是完整自主后台 Agent + 3 层 Memory 自动合并。社区有人在 fork 版开启后，实现“永不离线代码守护者”：晚上自动 review PR、修小 bug、早晨给你总结。

案例 3:Tamagotchi Buddy System（电子宠物）

源码里有完整 Tamagotchi 系统（18 种宠物 + gacha 抽取）。Buddy 会根据你使用频率“成长”，甚至在任务完成时弹出可爱动画。

案例 4：Swarm 并行重构大型模块

一人用主对话规划，spawn 3 个 Swarm 子 Agent 分别处理 UI/Logic/Test。实测：原本 2 小时任务缩短到 25 分钟。

案例 5:Penguin Mode / Tengu 内部模式

源码有多个 codename（如 Penguin Mode 可能为极简模式）。社区有人在 fork 版尝试开启，发现是“低 Token 极致优化模式”。

## 

9\. 顶级 30 条实战技巧（Boris + 社区 + 官方精选）

1-10：基础必会

1.  [CLAUDE.md](http://claude.md/)
    
    是“复利武器” - 持续迭代，每次任务后更新
    
2.  Plan Mode 先精炼 - 复杂任务必须先规划
    
3.  Hooks 自动验证 - PostToolUse 自动跑测试
    
4.  @ 精准引用 - 只注入必要文件
    
5.  Esc+Esc 回滚 - 快速恢复到检查点
    
6.  多开 worktree - 并行开发零冲突
    
7.  子 Agent 拆任务 - 大任务分解给 Swarm
    
8.  粘贴错误日志直接 fix - 提供完整 stack trace
    
9.  自定义 Slash - 常用流程一键执行
    
10.  视觉对比截图 - 拖拽 UI 截图让 Claude 对比
     

11-20：进阶技巧

1.  Git worktree 并行 5 个实例 - Boris 日常操作
    
2.  /compact 保持干净 - 但新会话更省钱
    
3.  PostToolUse 自动 prettier - 代码格式化自动化
    
4.  update
    
    [CLAUDE.md](http://claude.md/)
    
    \- 每次出错后立即更新规则
    
5.  model tiering - Opus 规划、Sonnet 执行、Haiku 探索
    
6.  MCP 连外部工具 - GitHub/Jira/Figma 集成
    
7.  skills 复用重复工作 - 模板化常用流程
    
8.  /statusline 显示上下文 - 实时监控 Token 使用
    
9.  voice dictation 提速 3 倍 - 语音输入长 Prompt
    
10.  Grill me on changes - 让 Claude 审查你的代码
     

21-30：专家级

1.  Document & Clear 模式 - 每任务清空上下文
    
2.  Progressive Disclosure - 外部 md 文件按需引用
    
3.  async hooks 测试不卡主线程 - 并行执行验证
    
4.  deny .env 防泄露 - 权限配置保护敏感文件
    
5.  /permissions UI 查看规则 - 可视化权限管理
    
6.  fork 实验分支 - 安全测试新想法
    
7.  Notification 桌面提醒 - 长任务完成通知
    
8.  learn output style 解释 why - 让 Claude 解释决策
    
9.  techdebt 命令每周跑一次 - 自动识别技术债
    
10.  commit 后自动 PR - 全流程自动化
     

## 

杀手级应用：把 Claude Code 变成你的数据分析全栈团队

这是 Boris Cherny 和团队公开分享的最高杠杆技巧之一：把 Claude Code 当成你的专属“数据分析师 + 数据工程师 + BI 工程师”三合一搭档。传统数据工作需要手动写 SQL、跑 BigQuery、写 dbt 模型、生成图表、写分析报告，而现在你只需一句话，Claude 就能端到端完成。

为什么这么强？

-   Claude Code 原生支持 Bash Tool（可直接执行 bq、snowsql、dbt 等 CLI）
    
-   通过 MCP Server 可安全连接公司内部数据库、数据仓库、Looker、Metabase、Airflow 等
    
-   它能自主规划：先探索 schema → 写探索性 SQL → 验证数据质量 → 生成生产级 dbt 模型 → 输出 Markdown/CSV/JSON 分析报告 → 甚至生成 Plotly 可视化代码
    
-   结合
    
    [CLAUDE.md](http://claude.md/)
    
    里的数据规范后，生成的代码永远符合团队标准（命名、测试、文档）
    
-   实测：复杂指标分析从 2-3 小时降到 5-10 分钟，且错误率接近零
    

如何操作（3 分钟上手）

第一步：配置 MCP（一次配置，永久使用）

在终端运行：

• claude mcp add bigquery --project=your-gcp-project --credentials=~/.gcp/key.json • claude mcp add dbt --project-dir=./dbt\_project

第二步：把数据规则写进

[CLAUDE.md](http://claude.md/)

（关键！）

添加章节：

数据规范 • 所有指标必须有单位测试（dbt test） • 使用 dbt 命名规范：fact\_ / dim\_ / mrt\_ • 所有 SQL 必须加注释 + 生成文档 • 优先使用 incremental 模型

第三步：开始对话（推荐新会话 + Plan Mode）

直接输入具体需求即可。

完整实用示例 Prompt（直接复制）

基础分析： "Connect to BigQuery production dataset. Analyze last 30 days user retention by cohort. Output: 1. SQL query 2. Key insights in Markdown 3. Plotly retention curve code."

生产级建模： "Use dbt. Create a new mrt\_user\_ltv model based on fact\_purchases and dim\_users. Include incremental logic, tests, and documentation. Then run dbt test and dbt docs generate."

端到端自动化： "I need weekly marketing ROI report. Connect to GA4 + Stripe via MCP. Write the full dbt model + SQL + final Markdown report with charts. Run everything and fix any failures."

复杂多步任务： "Plan first: explore our data warehouse schema, then build a funnel analysis model for checkout drop-off, generate Looker Explores if possible, and schedule it via Airflow DAG snippet."

进阶技巧（让它真正取代数据团队）

让 Claude 自己写 failing test 先： "Write a failing dbt test for data quality, then fix the model so test passes."

结合 Subagents： "Spawn swarm: one agent explores schema, one writes SQL, one builds visualization."

输出格式控制： "Output as a ready-to-copy Notion page with embedded charts."

成本优化： 用 Haiku 模型做探索性查询，用 Sonnet 写正式 dbt 模型

定期维护： 任务结束后说 “update

[CLAUDE.md](http://claude.md/)

with the new data patterns we learned"

团队落地建议

-   把这个技巧写进
    
    [CLAUDE.md](http://claude.md/)
    
    的“常用场景”章节
    
-   共享一套 MCP 配置和常用 data skills（放 .claude/skills/data-analysis/）
    
-   Boris 真实反馈：自从用了这个方式，他和团队已经完全不手写 SQL，数据迭代速度提升 8 倍以上
    

把这条技巧练熟，你会发现 Claude Code 不只是代码助手，而是全栈数据生产力引擎。强烈推荐今天就连一个 MCP，尝试一个真实业务指标分析！

## 

10\. 资源 & 行动计划

官方资源

官方最佳实践：

[https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)

50 Tips（

[Builder.io](http://builder.io/)

）：

[https://www.builder.io/blog/claude-code-tips-best-practices](https://www.builder.io/blog/claude-code-tips-best-practices)

[CLAUDE.md](http://claude.md/)

模板仓库：

[https://github.com/abhishekray07/claude-md-templates](https://github.com/abhishekray07/claude-md-templates)

Boris 分享：搜索

[@bcherny](https://x.com/@bcherny)

Claude Code

社区 GitHub:MuhammadUsmanGM/claude-code-best-practices

1 周学习计划

Day 1：安装 + 基础操作

-   安装 Claude Code
    
-   跑 /init 生成
    
    [CLAUDE.md](http://claude.md/)
    
-   熟悉快捷键（Esc、Shift+Tab、 @）
    

Day 2：配置 + 权限

-   配置 settings.json
    
-   设置 .claudeignore
    
-   测试 Hooks（PostToolUse 自动 lint）
    

Day 3：核心工作流

-   练习 Explore → Plan → Implement → Verify
    
-   用 Plan Mode 规划一个中等任务
    
-   要求 Claude 运行测试并修复
    

Day 4：提示工程

-   练习具体化描述问题
    
-   用 @ 精准引用文件
    
-   尝试视觉输入（截图对比）
    

Day 5：高级功能

-   尝试 Subagents 并行任务
    
-   配置 MCP Server（如 GitHub）
    
-   测试 Git Worktree 并行
    

Day 6：成本优化

-   实践“多新会话”策略
    
-   用 /cost 监控消耗
    
-   配置模型分层（Haiku/Sonnet/Opus）
    

Day 7：团队规范

-   整理团队
    
    [CLAUDE.md](http://claude.md/)
    
    模板
    
-   编写自定义 Slash Commands
    
-   分享最佳实践给同事
    

## 

附录：常见问题 FAQ

Q1:Claude Code 和 Cursor 有什么区别？

A：Claude Code 是纯终端工具，无 IDE 绑定，权限控制更精细，支持 Hooks 和 Git Worktree 原生并行。Cursor 是 IDE 集成，更适合可视化编辑。

Q2：如何避免 Token 费用爆炸？

A：核心策略是“多新会话 + /clear”，配合 .claudeignore 和模型分层，可节省 50-70% 费用。

Q3：

[CLAUDE.md](http://claude.md/)

应该写多长？

A：保持 100-200 行，只写非代码能推断的内容（架构决策、规范、流程）。

Q4：什么时候用 Plan Mode？

A：中等及以上复杂度任务必须先规划。小任务（拼写修复、日志添加）可直接执行。

Q5：如何让 Claude 自动运行测试？

A：在 settings.json 的 PostToolUse Hook 里配置 npm run test，每次编辑后自动执行。

Q6：源码泄露安全吗？

A：泄露的是客户端 CLI 代码，不涉及模型权重或用户数据。社区已公开镜像，我们只用于学习架构，不做逆向或商业用途。

Q7：如何并行开发多个功能？

A：用 Git Worktree + Subagents，每个子 Agent 分配独立 worktree，零冲突。

Q8：国内网络如何使用？

A：设置 ANTHROPIC\_BASE\_URL 和 ANTHROPIC\_API\_KEY 环境变量，或使用第三方代理。

## 

结语

Claude Code 不是简单的代码补全工具，而是一个可深度定制的 Agent 平台。通过本手册的学习，你将从“使用工具”进化到“驾驭 Agent”，实现真正的 3-5 倍提效。

记住核心原则

-   持续迭代
    
    [CLAUDE.md](http://claude.md/)
    
-   多新会话胜过老对话压缩
    
-   永远先 Plan 再 Implement
    
-   验证闭环（测试必须通过）
    
-   精准注入上下文（ @ 文件）
    

现在就开始：打开终端，输入 claude，开启你的 Agent 编程之旅！

文档版本：v1.0 最后更新：2026-04-01 维护者：团队内部 反馈渠道：内部 Slack/飞书群
