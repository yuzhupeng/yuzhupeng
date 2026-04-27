[

![Image](https://pbs.twimg.com/media/HB2sKVsbkAAHfKR?format=jpg&name=small)





](/jungeAGI/article/2025968331644420288/media/2025964701008760832)

OpenViking×OpenClaw:7 个 Agent不再是陌生人,token暴降 90%

2

15

57

[

14K



](/jungeAGI/status/2025968331644420288/analytics)

我在 OpenClaw 上跑了 7 个 Agent。

一个大总管，一个写代码的，一个写文章的，一个搞增长的，还有法务、财务、教学。

听起来 NB 吧？全自动AI团队，分工明确，各司其职。

但用了几周了，我快疯了。

## 

它们活得像七个陌生人

真实场景。

我跟大总管说："帮我安排一篇关于多Agent协作的文章。"

它问我："请问你的写作风格是什么？目标读者是谁？"

兄弟。我。昨天。刚。告诉过你。

你是不是金鱼转世。。。

更离谱的是——

开发助理刚帮我修好了飞书 webhook 的配置问题。我转头让内容助理写篇复盘。

它说："什么配置问题？能详细说说吗？"

你俩在同一台服务器上跑着啊！隔壁房间的事你都不知道？？

我当时的心情：🙂（假笑）

## 

每次重新介绍自己，都是在烧钱

你以为只是麻烦？不，还费钱。

我算了一笔账：

[

![Image](https://pbs.twimg.com/media/HB2stZ1bUAEJPOl?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025965303415656449)

一个月下来。。。光是"自我介绍"就烧掉一大坨。

咱就是说，这不是助理在工作，这是我在工作——重复给7个人做入职培训。

## 

字节开源了个东西，把我点醒了

字节跳动最近开源了一个项目叫 OpenViking。

GitHub 地址：

[github.com/volcengine/OpenViking](http://github.com/volcengine/OpenViking)

它的核心思路特别简单——

把 Agent 的记忆当文件系统来管理。

啥意思？

你打开电脑找文件的时候，会把硬盘里所有文件内容全读一遍吗？

不会吧。你先看文件夹名，找到目标文件夹，再打开具体文件。

Agent 读记忆也该这样。

但现在大多数 Agent 的做法是：每次启动，把记忆文件从头到尾全部读一遍。

100 行的时候没感觉。8000 行的时候，token 哗哗地烧。

家有矿也不是这个烧法。

## 

L0 / L1 / L2：三层按需加载

OpenViking 把记忆分成三层：

[

![Image](https://pbs.twimg.com/media/HB2s6vnbcAAKegM?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025965532600823808)

每次启动只读 L0。100 个 token，就知道记忆里有啥。

需要具体信息？读 L1 摘要。确认了？才读 L2 全文。

从"每次全读"变成"按需读取"。

我实测，日常对话 token 消耗直接降 10 倍。

不是省一点点，是断崖式下降。

## 

P0 / P1 / P2：给记忆加保质期

光分层还不够。记忆会越来越多。

OpenViking 的另一招——给记忆打"保质期"：

[

![Image](https://pbs.twimg.com/media/HB2tFCabAAAXzGQ?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025965709445234688)

P0 永远不删。P1 过期归档。P2 到期清理。

就像人的记忆——重要的事记得牢，琐碎的事会淡忘。但去翻笔记还能找回来。

[

![Image](https://pbs.twimg.com/media/HB2vSrHbAAA8Avr?format=jpg&name=small)





](/jungeAGI/article/2025968331644420288/media/2025968142732951552)

## 

我的真实改造：给 OpenClaw 多 Agent 装上共享大脑

说了这么多原理。我到底怎么做的？

第一步：给每个 Agent 加索引文件（10 分钟）

在每个 Agent 的 memory 目录下建一个 .abstract 文件，就是 L0 索引。

[

![Image](https://pbs.twimg.com/media/HB2tQqsboAATe-S?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025965909236752384)

Agent 每次启动，先读这个。只有需要具体信息时，才深入读对应的文件。

第二步：给记忆打 P 标签（10 分钟）

[

![Image](https://pbs.twimg.com/media/HB2tZlUaYAAmPsX?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025966062412652544)

然后写个清理脚本，每天扫一次。过期的自动归档。

第三步：共享记忆层——这才是杀手锏（10 分钟）

创建一个所有 Agent 都能读的共享目录：

[

![Image](https://pbs.twimg.com/media/HB2thIraYAAGVG5?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025966192163446784)

怎么让 Agent 自动往里写？

不用写代码。

OpenClaw 每个 Agent 启动都会读

[AGENTS.md](http://agents.md/)

——它的工作手册。加一条规则就行：

[

![Image](https://pbs.twimg.com/media/HB2toyaaQAAhscN?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025966323625508864)

就像给员工立了个规矩："做完事，在共享文档记一笔。"

Agent 会自觉执行。真的会。

## 

改造前 vs 改造后

[

![Image](https://pbs.twimg.com/media/HB2uBGTacAAbHZB?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025966741281730560)

## 

但我想说点不一样的

字节的 OpenViking 确实牛。

但我查了它的 GitHub——

它是一个独立的 Python 服务。 需要单独部署，需要配置 VLM 和 Embedding 模型，需要 API Key。

不是说不好。是说对于大多数 OpenClaw 用户来说，杀鸡用了牛刀。

OpenClaw 本身的

[MEMORY.md](http://memory.md/)

\+ memory/ 目录 +

[AGENTS.md](http://agents.md/)

规则，已经实现了记忆管理的底层架构。

你要做的不是"接入 OpenViking"，而是把 OpenViking 的思想，用 OpenClaw 原生的方式落地。

[

![Image](https://pbs.twimg.com/media/HB2uOZ5bQAA8MlD?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025966969879740416)

不用装任何东西。不用跑任何服务。

30 分钟，纯文件操作，搞定。

## 

一段提示词，让 OpenClaw 帮你搞定

把下面这段扔给你的 OpenClaw Agent：

[

![Image](https://pbs.twimg.com/media/HB2udU9bQAA4i7-?format=png&name=small)





](/jungeAGI/article/2025968331644420288/media/2025967226252378112)

它会帮你全流程搞完。

链接俊哥 进OpenClaw交流群

[

![Image](https://pbs.twimg.com/media/HB2uw0faYAEWjSY?format=jpg&name=900x900)





](/jungeAGI/article/2025968331644420288/media/2025967561133940737)

## 

最后

Agent 的记忆问题，说白了就两件事：

不要每次全读——先看目录，按需取。

让 Agent 之间能互相通气——共享记忆层。

字节的 OpenViking 把这套思路开源了，我们拿来借鉴。但不一定要照搬它的技术方案。

思想是免费的。落地才是本事。

30 分钟改造，token 省 10 倍，7 个 Agent 终于不再是陌生人了。

老铁们，别光让自己多动脑子——

也得让你的 Agent，学会记住你。

Want to publish your own Article?  
想发表自己的文章吗？

[Upgrade to Premium  
升级至高级版](/i/premium_sign_up)
