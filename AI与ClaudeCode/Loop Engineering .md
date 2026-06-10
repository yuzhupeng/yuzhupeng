
![](https://pbs.twimg.com/profile_images/1634900405724545031/gQgQEpaj_bigger.jpg)


\[译\] Loop 工程

 
 
Loop Engineering 正在取代“你亲自给 agent 写 prompt”这件事。它的核心是：你不再直接 prompt agent，而是设计一个系统，让这个系统去 prompt agent。

这里的 loop，可以理解为一种递归目标：你定义一个目的，然后让 AI 不断迭代，直到任务完成。它大致由五个构建块组成，而 Claude Code 和 Codex 现在都已经具备了这五个能力。

我认为，这可能是我们未来与 coding agent 协作的方式。不过，现在仍然很早期。我对此也保持怀疑，而且你必须非常注意 token 成本，因为不同使用模式下的消耗差异可能非常大，尤其取决于你是 token 富裕还是 token 紧张。你仍然需要某种方式来确保质量不会下降，对“AI slop”的担忧也完全合理。话虽如此，我们还是来看看它到底是什么。

最近有人说：

> 你不应该再去 prompt coding agent 了。你应该设计 loops，让 loops 去 prompt 你的 agents。

类似地，Anthropic 的 Claude Code 负责人也说过：

> 我现在已经不直接 prompt Claude 了。我有一套 loops 在运行，它们会去 prompt Claude，并判断接下来要做什么。我的工作是写 loops。

好，那这些话到底是什么意思？

过去大约两年里，你想让 coding agent 做事，基本方式就是写一个好的 prompt，并提供足够多的上下文。你输入一段内容，阅读它返回的结果，再输入下一段。agent 是一个工具，而你一直握着这个工具，一轮接一轮地操作。

这部分工作某种程度上已经结束了，或者至少有些人认为它正在结束。

现在，你构建的是一个小系统。这个系统会自己发现工作、分发工作、检查工作、记录完成情况，然后决定下一步要做什么。你让这个系统去触发 agents，而不是你亲自触发。

我之前写过一个与它相近的概念：harness。harness 是为单个 agent 构建运行环境，也就是那个构建软件的系统。Loop Engineering 则位于 harness 之上。它有点像 harness，但它会按时间运行，会生成小 helper，并且会自己喂养自己。

让我惊讶的是，这现在已经不再是一个“工具问题”了。

一年前，如果你想做一个 loop，你需要写一堆 bash 脚本，然后长期维护它。那是你自己的东西，也只有你自己能用。

但现在，这些能力已经直接内置在产品里了。Steinberger 列出的能力，几乎可以一一映射到 Codex app；同样，也几乎可以映射到 Claude Code。等你意识到它们的形状其实一样时，你就不再纠结到底该用哪个工具，而是开始设计一种 loop：不管你此刻坐在哪个工具里，它都依然能工作。

一个 loop 需要五样东西，以及一个用来记住状态的地方。先列出来，再逐个映射。

1.  Automations：按计划自动触发，自己做 discovery 和 triage。
    
2.  Worktrees：让两个并行工作的 agents 不会互相踩到对方。
    
3.  Skills：把项目知识写下来，避免 agent 靠猜。
    
4.  Plugins 和 connectors：把 agent 接入你已经在用的工具。
    
5.  Sub-agents：让一个 agent 负责提出想法，另一个 agent 负责检查它。
    

然后第六件事，是 memory。

这个 memory 可以是一个 markdown 文件，也可以是一个 Linear board，或者任何存在于单次 conversation 之外、能够保存“已完成事项”和“下一步事项”的地方。

[

![图像](https://pbs.twimg.com/media/HKVQLyTWsAAkdic?format=png&name=900x900)





](/cellinlab/article/2064144608242679822/media/2064144167630974976)

这听起来简单到不像重要的东西。但它其实是每个 long-running agent 都依赖的同一个技巧。模型在每次运行之间会忘记一切，所以 memory 必须存在磁盘上，而不是只存在 context 里。

agent 会忘记，但 repo 不会。

现在两个产品都已经具备这五项能力。

它们的名字在不同地方略有差异，但能力本质上是一样的。我们一个一个看，因为老实说，细节才决定了一个 loop 是真正能跑起来，还是悄悄到处漏水。

## 

Automations

Automations 是让 loop 成为真正 loop 的东西，而不是只运行一次的任务。

在 Codex app 里，你可以在 Automations 标签页中创建一个 automation。你选择项目、它要运行的 prompt、运行频率，以及它是在你的本地 checkout 上运行，还是在 background worktree 上运行。

那些发现了问题的运行结果，会进入 Triage inbox；那些没有发现问题的运行结果，会自动 archive，这点挺好。

OpenAI 内部会用它们处理一些枯燥工作，比如每日 issue triage、总结 CI failures、写 commit briefings、查找上周有人引入的 bug。

automation 还可以调用 skill。这样你就能让重复任务更可维护。你触发的是一个 skill，而不是把一大墙 nobody will ever update 的指令粘到 schedule 里。

Claude Code 到达同一个目标的方式是 scheduling 和 hooks。

你可以用 /loop 按间隔运行一个 prompt 或 command；你也可以安排一个 cron task；还可以在 agent 生命周期的某些阶段用 hooks 触发 shell commands；如果你希望它在你合上笔记本之后继续运行，也可以把整套东西推到 GitHub Actions。

本质是完全一样的：你定义一个 autonomous task，给它一个 cadence，然后让发现结果来到你面前，而不是由你自己到处检查。

这里还有一个值得了解的 in-session primitive，它更接近本文讨论的核心。

/loop 会按 cadence 反复运行。

/goal 则会一直运行，直到你写下的某个条件真的成立。每一轮之后，一个单独的小模型会检查任务是否完成。也就是说，写代码的 agent 不是给自己打分的那个。

你可以给它一个条件，比如：

> all tests in test/auth pass and lint is clean

然后你就可以离开。

Codex 也有同样的东西，也叫 /goal。它会跨多轮继续工作，直到一个可验证的停止条件成立，并支持 pause、resume 和 clear。

同一个 primitive，两个工具都有。这基本上也是整篇文章反复出现的模式。

所以，这一部分负责把工作浮现出来。loop 的其余部分，则负责对这些工作采取行动。

## 

Worktrees

只要你同时运行不止一个 agent，文件就会开始冲突，这会变成失败点。

两个 agents 同时改同一个文件，本质上和两个工程师同时提交同一段代码一样麻烦，而且他们事先还没沟通过。

git worktree 可以解决这个问题。它是一个独立的 working directory，位于自己的 branch 上，同时共享同一个 repo history。因此，一个 agent 的修改，字面意义上不可能碰到另一个 agent 的 checkout。

Codex 直接内置了 worktree 支持，所以多个 threads 可以同时作用于同一个 repo，而不会互相撞车。

Claude Code 也通过 git worktree 提供了同样的隔离能力。你可以用 \--worktree flag 在独立 checkout 中打开一个 session，也可以在 subagent 上设置 isolation: worktree，让每个 helper 都获得一个新的 checkout，并在结束后自动清理。

我之前写过这件事里“人”的一面：worktrees 可以移除机械层面的冲突，但你仍然是天花板。决定你能同时运行多少 agents 的，不是工具，而是你的 review bandwidth。

## 

Skills

skill 的作用，是让你不用每次 session 都像金鱼一样重新解释同一个项目上下文。

两个工具都使用相同的格式：一个包含 SKILL.md 的文件夹，里面存放 instructions 和 metadata，也可以附带 scripts、references、assets。

Codex 会在你用 $ 或 /skills 调用时运行某个 skill；当你的 task 与 skill description 匹配时，它也可能自动调用。这也是为什么一个紧凑、朴素的 description 比一个聪明但含糊的 description 更有用。

Claude Code 的做法也是一样的，我之前也写过这个模式。

Skills 也是让 intent 不再一遍遍消耗成本的地方。

我曾经说过，agent 每个 session 开始时都是冷启动的。只要你的 intent 里有任何空洞，它就会用一种自信的猜测把洞填上。

skill 就是把这种 intent 写在外部：项目约定、构建步骤、“我们不这么做是因为以前发生过某个事故”等等。你只需要写一次，agent 每次运行时都会读取。

没有 skills，loop 每个周期都要从零重新推导你的整个项目。

有了 skills，它就开始有一点复利效应。

有一点需要区分清楚：skill 是 authoring format，而 plugin 是你分发它的方式。

当你想跨 repo 共享一个 skill，或者把几个 skills 打包在一起时，你会把它们封装成 plugin。

Codex 是这样，Claude Code 也是这样。

## 

Connectors

一个只能看见 filesystem 的 loop，是一个很小的 loop。

Connectors 基于 MCP，可以让 agent 读取你的 issue tracker、查询数据库、调用 staging API、在 Slack 里发消息。

Codex 和 Claude Code 都支持 MCP，所以你为其中一个写的 connector，通常在另一个里也能直接工作。

plugins 还可以把 connectors 和 skills 打包在一起。这样你的队友只要安装你的 setup，而不用凭记忆重建整套东西。

这就是“agent 说：这里是修复方案”和“loop 自己打开 PR、链接 Linear ticket，并在 CI 变绿后 ping 频道”之间的区别。

connectors 是 loop 能够在你真实环境里行动的原因，而不只是告诉你“如果我能做，我会怎么做”。

## 

Sub-agents

在一个 loop 中，最有用的结构性设计，远远是把“写的人”和“检查的人”拆开。

写代码的模型，在给自己的作业打分时太友善了。

一个带有不同 instructions、甚至有时使用不同 model 的第二个 agent，能抓住第一个 agent 自我说服后忽略的问题。

Codex 只有在你要求时才会生成 subagents。它们会并行运行，然后把结果合并回一个答案。

你可以把自己的 agents 定义成 .codex/agents/ 里的 TOML 文件。每个文件包含 name、description、instructions，以及可选的 model 和 reasoning effort。

这样，你的 security reviewer 可以用一个强模型和 high effort，而你的 explorer 可以是某个快速的 read-only agent。

Claude Code 也用 .claude/agents/ 里的 subagents 和 agent teams 做同样的事情，让不同 agents 之间传递工作。

两个工具里常见的拆分方式都是：

一个 agent 负责探索；一个 agent 负责实现；一个 agent 负责根据 spec 验证结果。

我之前已经从两个角度讲过这件事。

它在 loop 中尤其重要的原因是：loop 会在你不盯着看的时候运行。因此，一个你真正信任的 verifier，是你能走开的唯一原因。

当然，subagents 会消耗更多 tokens，因为每一个都要进行自己的 model 和 tool work。所以，要把它们花在“第二意见值得付费”的地方。

这也基本上是 Claude Code 的 /goal 在底层做的事：由一个新的模型判断 loop 是否完成，而不是由完成工作的那个模型来判断。

也就是说，maker 和 checker 的拆分，甚至被应用到了停止条件本身。

## 

把它们组合起来

把这些东西粘在一起，一个单线程任务就会变成一个小型控制面板。

下面是我一直在用的一种形状。

每天早上，一个 automation 会在 repo 上运行。

它的 prompt 会调用一个 triage skill。这个 skill 会读取昨天的 CI failures、open issues、recent commits，然后把 findings 写进一个 markdown 文件，或者写进 Linear board。

对于每个值得处理的 finding，这个 thread 会打开一个隔离的 worktree，并派一个 sub-agent 去 draft fix，再派第二个 sub-agent 根据项目 skills 和现有 tests 去 review 这个 draft。

connectors 让 loop 可以打开 PR，并更新 ticket。

任何 loop 无法处理的事情，都会落到我的 triage inbox。

state file 是整套东西的脊柱。它记住了尝试过什么、什么通过了、还有什么仍然 open。所以第二天早上的运行，可以从今天停止的地方继续。

看看你真正做了什么。

你只设计了一次。

你没有亲自 prompt 其中任何一个步骤。

这就是 Steinberger 那个观点落地后的样子。而且不管是在 Codex 里，还是在 Claude Code 里，这都是同一个 loop，因为这些 pieces 本质上是同样的 pieces。

## 

Loop 改变工作，但不会把你从工作中删除

loop 会改变工作方式，但它不会把你从工作中删除。

而且随着 loop 变得更好，有三个问题会变得更尖锐，而不是更容易。

第一，verification 仍然在你身上。

一个无人值守运行的 loop，也是在无人值守地犯错。

你把 verifier sub-agent 和 maker 拆开的原因，就是为了让 loop 说出的“done”有一点意义。即便如此，“done”也只是一个声明，而不是证明。

我一直重复同一句话：

> 你的工作，是交付你确认过能运行的代码。

第二，如果你放任不管，你的理解仍然会腐烂。

loop 越快地交付那些不是你亲手写的代码，真实存在的系统和你实际理解的系统之间的差距就越大。

一个流畅的 loop 只会让这个差距增长得更快，除非你真的去读它产出的东西。

第三，最舒服的姿势，可能也是最危险的姿势。

当 loop 开始自己运行时，你很容易停止拥有自己的判断，只是接受它给你的任何东西。

我称之为一种危险状态。

当你带着判断力去设计 loop 时，设计 loop 是解药。

当你为了逃避思考而设计 loop 时，它就是加速剂。

同一个动作，会产生相反的结果。

## 

这可能是工作方式演化的预览

我认为，这是我们工作方式即将演化的一次预览。

不过，如果我不亲自 review 代码，或者完全依赖自动化 loops 去修复问题，我的产品质量一定会下降。我很可能会陷入一个持续下滑的螺旋，不断把自己挖进更深的坑里。

话虽如此，去设置你的 loops 吧。

但也不要忘记，直接 prompt 你的 agents 仍然有效。关键在于找到正确的平衡。

loops 也会因为使用者不同而产生完全不同的结果。

两个人可以构建完全一样的 loop，却得到截然相反的结果。

一个人用它在自己深刻理解的工作上跑得更快。

另一个人用它来避免理解工作本身。

loop 不知道这两者之间的区别。

但你知道。

这就是为什么 loop design 比 prompt engineering 更难，而不是更简单。

Cherny 的观点并不是说工作变简单了。

而是杠杆点移动了。

构建 loop。

但要像一个仍然打算做 engineer 的人那样去构建它，而不是像一个只会按下“go”按钮的人。

[![图像](https://pbs.twimg.com/media/HKVQiRWW8AARsja?format=jpg&name=900x900)




 
