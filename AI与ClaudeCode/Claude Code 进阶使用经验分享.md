 
# Claude Code 进阶使用经验分享

## 从“会用”到“用得顺”，靠的是工作流

很多人刚开始用 Claude Code 时，会觉得它很强。  
但再往后走，真正拉开差距的不是“知道它能做什么”，而是“你有没有一套稳定工作流”。

新手最常见的状态是：

-   想到什么就问什么
-   一上来就让 Claude 直接改
-   改完也不验证
-   每一轮都像重新开始

而进阶用户更像是在“带着 Claude 按流程推进任务”。

## 先记住一个总原则

Claude Code 最适合扮演的角色，不是“替你一把梭写完所有东西”，而是：

-   帮你快速理解项目
-   帮你拆方案
-   帮你执行重复性或高密度工作
-   帮你验证和复查

也就是说，最顺的用法通常不是：

> 直接把一个很大的目标扔给 Claude，然后等奇迹出现

而是：

> 让 Claude 先理解，再规划，再执行，再验证

## 一张图看最推荐的进阶工作流

#mermaid-ge6rkyn{font-family:system-ui,sans-serif;font-size:14px;fill:#0F2829;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-ge6rkyn .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-ge6rkyn .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-ge6rkyn .error-icon{fill:#FFFBF2;}#mermaid-ge6rkyn .error-text{fill:#00040d;stroke:#00040d;}#mermaid-ge6rkyn .edge-thickness-normal{stroke-width:1px;}#mermaid-ge6rkyn .edge-thickness-thick{stroke-width:3.5px;}#mermaid-ge6rkyn .edge-pattern-solid{stroke-dasharray:0;}#mermaid-ge6rkyn .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-ge6rkyn .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-ge6rkyn .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-ge6rkyn .marker{fill:#F97316;stroke:#F97316;}#mermaid-ge6rkyn .marker.cross{stroke:#F97316;}#mermaid-ge6rkyn svg{font-family:system-ui,sans-serif;font-size:14px;}#mermaid-ge6rkyn p{margin:0;}#mermaid-ge6rkyn .label{font-family:system-ui,sans-serif;color:#0F2829;}#mermaid-ge6rkyn .cluster-label text{fill:#00040d;}#mermaid-ge6rkyn .cluster-label span{color:#00040d;}#mermaid-ge6rkyn .cluster-label span p{background-color:transparent;}#mermaid-ge6rkyn .label text,#mermaid-ge6rkyn span{fill:#0F2829;color:#0F2829;}#mermaid-ge6rkyn .node rect,#mermaid-ge6rkyn .node circle,#mermaid-ge6rkyn .node ellipse,#mermaid-ge6rkyn .node polygon,#mermaid-ge6rkyn .node path{fill:#FFF7E8;stroke:#F97316;stroke-width:1px;}#mermaid-ge6rkyn .rough-node .label text,#mermaid-ge6rkyn .node .label text,#mermaid-ge6rkyn .image-shape .label,#mermaid-ge6rkyn .icon-shape .label{text-anchor:middle;}#mermaid-ge6rkyn .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-ge6rkyn .rough-node .label,#mermaid-ge6rkyn .node .label,#mermaid-ge6rkyn .image-shape .label,#mermaid-ge6rkyn .icon-shape .label{text-align:center;}#mermaid-ge6rkyn .node.clickable{cursor:pointer;}#mermaid-ge6rkyn .root .anchor path{fill:#F97316!important;stroke-width:0;stroke:#F97316;}#mermaid-ge6rkyn .arrowheadPath{fill:#0b0b0b;}#mermaid-ge6rkyn .edgePath .path{stroke:#F97316;stroke-width:2.0px;}#mermaid-ge6rkyn .flowchart-link{stroke:#F97316;fill:none;}#mermaid-ge6rkyn .edgeLabel{background-color:transparent;text-align:center;}#mermaid-ge6rkyn .edgeLabel p{background-color:transparent;}#mermaid-ge6rkyn .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-ge6rkyn .labelBkg { fill: none; }#mermaid-ge6rkyn .cluster rect{fill:#FFFBF2;stroke:hsl(41.5384615385, 60%, 87.4509803922%);stroke-width:1px;}#mermaid-ge6rkyn .cluster text{fill:#00040d;}#mermaid-ge6rkyn .cluster span{color:#00040d;}#mermaid-ge6rkyn div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:system-ui,sans-serif;font-size:12px;background:#FFFBF2;border:1px solid hsl(41.5384615385, 60%, 87.4509803922%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-ge6rkyn .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#0F2829;}#mermaid-ge6rkyn rect.text{fill:none;stroke-width:0;}#mermaid-ge6rkyn .icon-shape,#mermaid-ge6rkyn .image-shape{background-color:transparent;text-align:center;}#mermaid-ge6rkyn .icon-shape p,#mermaid-ge6rkyn .image-shape p{background-color:transparent;padding:2px;}#mermaid-ge6rkyn .icon-shape .label rect,#mermaid-ge6rkyn .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-ge6rkyn .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-ge6rkyn .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-ge6rkyn :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}

先让 Claude 理解项目

输出方案，不立刻改

确认文件范围和风险

开始修改

运行 build / test 验证

/review 再审一遍

/diff 看改动

/commit 提交

## 这个流程为什么好用

因为它同时解决了几类常见问题：

-   一上来就乱改
-   改了但没验证
-   改动太散、自己都说不清
-   做完没有代码审查视角
-   一个会话里混着分析、实现、审查、提交，最后谁也分不清

也就是说，这不是“更麻烦”，而是“更稳定”。

## 一个很好用的任务模板

你可以直接这样给 Claude Code 下任务：

```text
先分析这个需求会涉及哪些文件，给出实现方案和风险点，先不要改代码。

确认后再开始修改。修改完成后运行 build 和相关测试。

最后从 code review 角度再检查一遍潜在问题。
```

这类提示词的好处是，把任务拆成了：

-   理解
-   规划
-   执行
-   验证
-   复查

这比“帮我把这个功能做了”强很多。

## 工作流一：新功能开发

这是最常见、也最推荐长期使用的一套流程。

### 适用场景

-   新增页面
-   增加一个接口
-   给现有模块加新能力
-   需要改多个文件，但边界还算清晰

### 推荐步骤

1.  先让 Claude 理解相关模块
2.  输出实现方案和涉及文件
3.  确认后开始改代码
4.  跑构建和测试
5.  做一次 review
6.  查看 diff 并提交

### 配套命令

-   `/plan`
-   `/diff`
-   `/review`
-   `/commit`

### 推荐提问方式

```text
先看一下这个功能会影响哪些文件，给出一个最小实现方案，先不要改代码。

我确认后你再开始改，改完运行 build 和相关测试，最后再 review 一遍。
```

### 对应流程图

Claude Code你Claude Code你#mermaid-6k42e8i{font-family:system-ui,sans-serif;font-size:14px;fill:#0F2829;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-6k42e8i .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-6k42e8i .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-6k42e8i .error-icon{fill:#FFFBF2;}#mermaid-6k42e8i .error-text{fill:#00040d;stroke:#00040d;}#mermaid-6k42e8i .edge-thickness-normal{stroke-width:1px;}#mermaid-6k42e8i .edge-thickness-thick{stroke-width:3.5px;}#mermaid-6k42e8i .edge-pattern-solid{stroke-dasharray:0;}#mermaid-6k42e8i .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-6k42e8i .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-6k42e8i .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-6k42e8i .marker{fill:#F97316;stroke:#F97316;}#mermaid-6k42e8i .marker.cross{stroke:#F97316;}#mermaid-6k42e8i svg{font-family:system-ui,sans-serif;font-size:14px;}#mermaid-6k42e8i p{margin:0;}#mermaid-6k42e8i .actor{stroke:#F97316;fill:#FFF7E8;}#mermaid-6k42e8i text.actor>tspan{fill:#0F2829;stroke:none;}#mermaid-6k42e8i .actor-line{stroke:#F97316;}#mermaid-6k42e8i .innerArc{stroke-width:1.5;stroke-dasharray:none;}#mermaid-6k42e8i .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#0F2829;}#mermaid-6k42e8i .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#0F2829;}#mermaid-6k42e8i #arrowhead path{fill:#0F2829;stroke:#0F2829;}#mermaid-6k42e8i .sequenceNumber{fill:#068ce9;}#mermaid-6k42e8i #sequencenumber{fill:#0F2829;}#mermaid-6k42e8i #crosshead path{fill:#0F2829;stroke:#0F2829;}#mermaid-6k42e8i .messageText{fill:#0F2829;stroke:none;}#mermaid-6k42e8i .labelBox{stroke:#F97316;fill:#FFF7E8;}#mermaid-6k42e8i .labelText,#mermaid-6k42e8i .labelText>tspan{fill:#0F2829;stroke:none;}#mermaid-6k42e8i .loopText,#mermaid-6k42e8i .loopText>tspan{fill:#0F2829;stroke:none;}#mermaid-6k42e8i .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:#F97316;fill:#F97316;}#mermaid-6k42e8i .note{stroke:hsl(52.6829268293, 60%, 73.9215686275%);fill:#fff5ad;}#mermaid-6k42e8i .noteText,#mermaid-6k42e8i .noteText>tspan{fill:#333;stroke:none;}#mermaid-6k42e8i .activation0{fill:#FFF1DB;stroke:hsl(36.6666666667, 100%, 82.9411764706%);}#mermaid-6k42e8i .activation1{fill:#FFF1DB;stroke:hsl(36.6666666667, 100%, 82.9411764706%);}#mermaid-6k42e8i .activation2{fill:#FFF1DB;stroke:hsl(36.6666666667, 100%, 82.9411764706%);}#mermaid-6k42e8i .actorPopupMenu{position:absolute;}#mermaid-6k42e8i .actorPopupMenuPanel{position:absolute;fill:#FFF7E8;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#mermaid-6k42e8i .actor-man line{stroke:#F97316;fill:#FFF7E8;}#mermaid-6k42e8i .actor-man circle,#mermaid-6k42e8i line{stroke:#F97316;fill:#FFF7E8;stroke-width:2px;}#mermaid-6k42e8i :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}先分析需求与文件范围输出方案、改动点、风险可以开始改修改代码运行 build / test/review 复查/diff 查看改动并确认

## 工作流二：Bug 修复

很多人修 bug 时容易直接让 Claude 开改。  
但更稳的方式其实是“先定位，再修复，再复现验证”。

### 适用场景

-   页面报错
-   接口异常
-   状态错乱
-   某个场景偶现 bug

### 推荐步骤

1.  让 Claude 先复述问题和排查方向
2.  搜索相关调用链和报错位置
3.  给出 root cause 推断
4.  先说修法，再动代码
5.  用最接近真实问题的方式验证

### 推荐提问方式

```text
先不要改代码，先帮我定位这个 bug 可能在哪几层。

把最可能的根因、相关文件和修复思路列出来。确认后再改。

改完后请尽量复现并验证这个问题是否真的解决。
```

### 这一套为什么比“直接修”更好

因为 bug 修复最怕两件事：

-   修错地方
-   修完没验证到真正问题

## 工作流三：重构与代码整理

这类任务最容易失控，因为目标往往不如“做功能”那么具体。

### 适用场景

-   文件太大想拆分
-   重复逻辑太多
-   命名和结构混乱
-   组件、服务、工具函数边界不清

### 推荐步骤

1.  先让 Claude 评估当前结构问题
2.  明确“这次只做哪一类重构”
3.  先列拆分方案
4.  分批改，不要一轮重构整个系统
5.  每批都验证

### 推荐提问方式

```text
先评估这个模块当前最主要的结构问题，只给我 2 到 3 个最值得做的重构点。

这次只做最小一轮，不要顺手改太多无关内容。

改完后说明具体拆了哪些职责，并运行验证。
```

### 重构任务里最重要的一条

一定要限制范围。  
否则 Claude 很容易“顺手优化”出一大坨额外改动。

## 工作流四：陌生项目接手

这类场景特别适合 Claude Code，因为它非常擅长先帮你建立认知地图。

### 适用场景

-   第一次接手某个仓库
-   别人的项目临时要你修点东西
-   公司老项目你不熟
-   想快速知道某个功能在哪实现

### 推荐步骤

1.  先让 Claude 建项目地图
2.  再锁定和当前目标最相关的目录与文件
3.  再进入方案和修改

### 推荐提问方式

```text
先帮我快速理解这个项目：

1. 技术栈是什么
2. 主要目录分别负责什么
3. 这个需求最可能涉及哪些文件

先不要改代码。
```

### 一个很好用的进阶动作

让 Claude 顺手帮你沉淀 `CLAUDE.md`。  
这样你第二次再回来，这个项目就没那么陌生了。

## 什么时候该切到 Plan Mode

特别适合下面这些场景：

-   改动跨多个模块
-   涉及数据库、权限、接口联动
-   你自己也没想清楚具体实现
-   你想先让 Claude 给出完整步骤
-   你担心它没想清楚就直接改代码

### 一个简单判断标准

如果你脑子里都已经觉得“这个任务有点大”，那就先 `/plan`。  
Plan Mode 最大的价值不是更正式，而是帮你把“想法”变成“执行顺序”。

## 进阶用户常用的命令组合

## 组合一：先规划再实现

```text
/plan
```

适合大任务开局。

## 组合二：做完先看改动

```text
/diff
```

适合：

-   看 Claude 实际改了什么
-   避免只听它口头总结

## 组合三：改完再复查

```text
/review
```

适合：

-   提交前再看一遍 bug、风险和遗漏测试

## 组合四：长会话上下文治理

```text
/context
/compact
```

适合：

-   对话已经很长
-   你感觉 Claude 开始“忘事”
-   想继续当前任务，但不想完全开新会话

## 组合五：最终提交闭环

```text
/diff
/review
/commit
```

这基本就是一次完整的收尾链路。

## 进阶用户的 6 个习惯

### 1\. 大任务先规划

不要让 Claude 直接冲进去改。

### 2\. 明确要求验证

改完一定要让它跑 `build`、`test` 或关键命令。

### 3\. 经常写 `CLAUDE.md`

把长期约束沉淀下来，别每次口述。

### 4\. 会主动限制改动范围

比如明确说：

-   先不要重构
-   只修这个 bug
-   不要顺手改无关文件
-   先最小实现

### 5\. 经常看 `/diff`

不要只看 Claude 的总结，要看真实改动。

### 6\. 把一次长任务拆成多轮

一轮只解决一个清晰目标，比一口气做完整个需求更稳。

## 几个非常常见的进阶坑

## 1\. 会话太长还硬聊

表现：

-   Claude 开始答非所问
-   忘掉之前确认过的约束
-   修改越来越飘

解决：

-   用 `/context` 看占用
-   用 `/compact`
-   必要时新开会话，并重新给目标

## 2\. 没有限定“先别改代码”

表现：

-   你本来想先讨论方案
-   Claude 直接开始改了

解决：

明确写：

```text
先不要改代码，只分析和出方案。
```

## 3\. 验证要求不具体

表现：

-   Claude 说“已经完成”
-   但其实没跑关键验证

解决：

把验证动作说具体：

-   运行 `npm run build`
-   运行相关测试
-   启动本地页面验证
-   提供失败输出

## 4\. 把 Claude 当成唯一判断者

Claude 可以帮你推进任务，但最终是否提交、是否上线、是否接受方案，还是你来决定。  
进阶工作流的重点不是“完全放手”，而是“让 Claude 帮你更快形成可靠闭环”。

## 一套我最推荐的通用工作流

如果你不想记太多，先固定用这一套就够了：

#mermaid-3sy2ln4{font-family:system-ui,sans-serif;font-size:14px;fill:#0F2829;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-3sy2ln4 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-3sy2ln4 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-3sy2ln4 .error-icon{fill:#FFFBF2;}#mermaid-3sy2ln4 .error-text{fill:#00040d;stroke:#00040d;}#mermaid-3sy2ln4 .edge-thickness-normal{stroke-width:1px;}#mermaid-3sy2ln4 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-3sy2ln4 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-3sy2ln4 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-3sy2ln4 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-3sy2ln4 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-3sy2ln4 .marker{fill:#F97316;stroke:#F97316;}#mermaid-3sy2ln4 .marker.cross{stroke:#F97316;}#mermaid-3sy2ln4 svg{font-family:system-ui,sans-serif;font-size:14px;}#mermaid-3sy2ln4 p{margin:0;}#mermaid-3sy2ln4 .label{font-family:system-ui,sans-serif;color:#0F2829;}#mermaid-3sy2ln4 .cluster-label text{fill:#00040d;}#mermaid-3sy2ln4 .cluster-label span{color:#00040d;}#mermaid-3sy2ln4 .cluster-label span p{background-color:transparent;}#mermaid-3sy2ln4 .label text,#mermaid-3sy2ln4 span{fill:#0F2829;color:#0F2829;}#mermaid-3sy2ln4 .node rect,#mermaid-3sy2ln4 .node circle,#mermaid-3sy2ln4 .node ellipse,#mermaid-3sy2ln4 .node polygon,#mermaid-3sy2ln4 .node path{fill:#FFF7E8;stroke:#F97316;stroke-width:1px;}#mermaid-3sy2ln4 .rough-node .label text,#mermaid-3sy2ln4 .node .label text,#mermaid-3sy2ln4 .image-shape .label,#mermaid-3sy2ln4 .icon-shape .label{text-anchor:middle;}#mermaid-3sy2ln4 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-3sy2ln4 .rough-node .label,#mermaid-3sy2ln4 .node .label,#mermaid-3sy2ln4 .image-shape .label,#mermaid-3sy2ln4 .icon-shape .label{text-align:center;}#mermaid-3sy2ln4 .node.clickable{cursor:pointer;}#mermaid-3sy2ln4 .root .anchor path{fill:#F97316!important;stroke-width:0;stroke:#F97316;}#mermaid-3sy2ln4 .arrowheadPath{fill:#0b0b0b;}#mermaid-3sy2ln4 .edgePath .path{stroke:#F97316;stroke-width:2.0px;}#mermaid-3sy2ln4 .flowchart-link{stroke:#F97316;fill:none;}#mermaid-3sy2ln4 .edgeLabel{background-color:transparent;text-align:center;}#mermaid-3sy2ln4 .edgeLabel p{background-color:transparent;}#mermaid-3sy2ln4 .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-3sy2ln4 .labelBkg { fill: none; }#mermaid-3sy2ln4 .cluster rect{fill:#FFFBF2;stroke:hsl(41.5384615385, 60%, 87.4509803922%);stroke-width:1px;}#mermaid-3sy2ln4 .cluster text{fill:#00040d;}#mermaid-3sy2ln4 .cluster span{color:#00040d;}#mermaid-3sy2ln4 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:system-ui,sans-serif;font-size:12px;background:#FFFBF2;border:1px solid hsl(41.5384615385, 60%, 87.4509803922%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-3sy2ln4 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#0F2829;}#mermaid-3sy2ln4 rect.text{fill:none;stroke-width:0;}#mermaid-3sy2ln4 .icon-shape,#mermaid-3sy2ln4 .image-shape{background-color:transparent;text-align:center;}#mermaid-3sy2ln4 .icon-shape p,#mermaid-3sy2ln4 .image-shape p{background-color:transparent;padding:2px;}#mermaid-3sy2ln4 .icon-shape .label rect,#mermaid-3sy2ln4 .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-3sy2ln4 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-3sy2ln4 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-3sy2ln4 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}

理解项目与需求

输出方案

确认范围

开始实现

验证 build / test

/review 复查

/diff 确认

/commit 提交

你每次都按这个节奏来，Claude Code 的稳定性会明显提高。

## 小结

进阶工作流的核心不是更复杂，而是更有节奏：

-   先理解
-   再规划
-   再执行
-   然后验证
-   最后复查和提交

当你形成这套习惯后，Claude Code 的价值会比“想到什么就问什么”高很多。  
它会从“一个很强的 AI 工具”，变成“一个真正融入开发流程的工程搭档”。
