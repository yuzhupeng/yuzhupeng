- [一、引子-课程介绍](#_label1)
- * [1.1 目的](#_lab2_1_0)
  * [1.2 思考如何进阶](#_lab2_1_1)
  * * [1.3 关于RocketMQ，我们都知道啥？](#_label3_1_1_0)
    [1.4 成体系化研究RocketMQ](#_lab2_1_2)
    * [1.4.1 基础架构](#_label3_1_2_0)
    * [1.4.2 功能架构](#_label3_1_2_1)
    * [1.4.3 性能/稳定性测试](#_label3_1_2_2)
    * [1.4.4 运维管理](#_label3_1_2_3)
  [二、架构进阶](#_label2)
- * [2.1 基础架构](#_lab2_2_0)
  * [2.2 特性](#_lab2_2_1)
  * * [1.基本能力](#_label3_2_1_0)
    * [2.可靠性](#_label3_2_1_1)
    [2.3 核心原理](#_lab2_2_2)
    * [2.3.1 启动运行原理](#_label3_2_2_0)
    * [2.3.2 其它](#_label3_2_2_1)
  [三、总结]  [](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606143608126-1908302205.png)[]()## 1.2 思考如何进阶**方向**入门后，架构进阶的方向有很多：通用能力、专业技能（业务能力、技术能力、职业软实力）。**改变**每个架构师都有自己的优缺点，对于团队来说，架构师并无优劣，只有合适与否。 架构师应该结合自身短板和团队需求，去加强相关能力，不满足就可能会被淘汰。**加强认知**未雨绸缪，布局未来，引领团队。下面，围绕技术能力，以RocketMQ为例，从多角度剖析架构原理，期望能给大家带来一些灵感。本节课会偏向技术。[]()### 1.3 关于RocketMQ，我们都知道啥？- 1.一个消息队列，整体模型依然是发布-订阅模型。
- 2.阿里开源的，经受住了阿里双11内部业务验证。
- 3.支持事务消息。
- 4.消费失败，会重试。
- 5.4个模块组成：nameserver、producer、consumer、broker。**没了？这就是典型的技术能力不成体系！！！**[]()## 1.4 成体系化研究RocketMQ一般作为架构师，我们需要了解一个东西，最少4个模块：**模型、功能、性能、运维。（大家有其它想法多多讨论，不一定对，一般博主会从这4点入手。）**[]()### 1.4.1 基础架构【存储原理】消息如何存储？文件、目录结构？如何实现根据key快速查询消息？【通信原理】底层通信模型是什么，如何运转？[]()### 1.4.2 功能架构【功能设计】RocketMQ中的负载均衡（往哪发，从哪里消费）怎么做的？【功能设计】broker如何支持事务消息？底层源码级实现原理？[]()### 1.4.3 性能/稳定性测试吞吐量：10+W/S时延：消息堆积越大，时延越长。可靠性：对消息不丢失的保障程度。例如是否支持同步/异步刷盘。可用性：无故障运行的时间百分比，通常用几个9来衡量。[]()### 1.4.4 运维管理监控告警：对消息中间件的使用进行全方位的监控。部署：是否易部署，扩容、降低方案。故障容灾：机器掉电、网络异常、磁盘损坏等单机故障处理；机房故障异地灾备。[回到顶部(go to top)](#_labelTop)[]()# 二、架构进阶下面我们以rocketMQ为例，讲解 **架构级别的认知，应该是怎么样的**。[]()## 2.1 基础架构![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606144809269-1488828841.png) 1.生产者（Producer）：负责发布消息。Producer通过负载均衡选择Broker集群队列进行消息投递。2.消费者（Consumer）：负责消费消息。支持以push推，pull拉两种模式对消息进行消费。3.代理服务器（Broker Server）：消息中转角色，负责存储消息、转发消息。主要包含2个功能：接收从生产者发送来的消息并存储、同时为消费者的拉取请求作准备。存储消息相关的元数据：消费者组consumer Group、消费进度偏移offset、主题Topic、队列消息Message Queue等。4.名字服务（Name Server）：是Topic路由的注册中心，支持Broker的动态注册与发现。生产者或消费者能够通过名字服务查找各主题相应的Broker IP列表。多个实例组成集群，无状态。[]()## 2.2 特性遇事不决，看官网！！！成熟的技术组件，不要直接搜问题，最好的、最原始的、最正确的描述一定在官网。官网介绍了12种特性，其中有4个是基本能力，8个是泛可靠性。[]()### 1.基本能力订阅与发布：消息发布是指生产者向topic发送消息；消息订阅是指消费者关注了topic-tag的消息，消费对应消息。**消息顺序**：消息有序指的是一类消息消费时，能按照发送的顺序来消费。顺序消息分为全局顺序消息与分区顺序消息。消息过滤：消费者根据Tag进行消息过滤，也支持自定义属性过滤。定时消息：定时消息（延迟队列）是指消息发送到broker后，不会立即被消费，等待特定时间投递给真正的topic。[]()### 2.可靠性消息可靠性：RocketMQ支持消息的高可靠（异步复制、同步双写技术）。至少一次：支持At least Once，指每个消息必须投递一次。回溯消费：RocketMQ支持按照时间回溯消费，时间维度精确到毫秒。流量控制：生产者流控，因为broker处理能力达到瓶颈；消费者流控，因为消费能力达到瓶颈。**事务消息**：RocketMQ的事务消息提供类似 X/Open XA 的分布事务功能，通过事务消息能达到分布式事务的最终一致。**消息重投**（生产者）：生产者在发送消息时失败，支持同步/异步重发。**消息重试**（消费者）：Consumer消费消息失败后，要提供一种重试机制，令消息再消费一次。死信队列：当消息消费失败，达到最大重试次数后，若消费依然失败，则将其发送到Dead-Letter队列中。[]()## 2.3 核心原理为了实现12个特性，RocketMQ做了很多核心设计，我们从以下五个方向来剖析核心原理1) 启动原理：了解整体架构的启动运行基本运作原理。
2) 消息存储：首先明白消息如何快速罗盘、查询过滤。
3) 通信机制：底层netty实现，RocketMQ的高效很大一部分依赖于Netty通信协议机制。
4) 负载均衡：RocketMQ中的负载均衡都在Client端完成，主要可以分为Producer端发送消息时候的负载均衡和Consumer端订阅消息的负载均衡。
5) 事务消息：RocketMQ采用了2PC的思想来实现了提交事务消息，同时增加一个补偿逻辑来处理二阶段超时或者失败的消息。[]()### 2.3.1 启动运行原理  ![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606154319057-974978095.png)rocketMQ启动顺序： nameserver->broker->producer->consumer。#### 1.nameserver启动原理![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606154458892-1374589448.png)NameServer作为rocketMQ的基于Topic路由的注册中心，支持Broker的动态注册与发现，启动流程如下：1) 加载kv配置。
2) 构建NettyRemotingServer初始化netty通信实例。
3) 初始化远程通信执行器。
4) 注册请求执行器。
5) 定时轮训清除宕机的broker。
6) 注册SSL证书变化监听器。
7) 启动远程通信服务端（netty）。
8) 启动SSL证书监听服务。其中，1-6步是初始化过程，7-8是启动流程。#### 2.broker启动原理![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606154707988-1129103496.png)1).初始化1) 载入各种配置文件（topic配置、消费偏移量、订阅群组..）
2) 初始化DefaultMessageStore消息存储器
3) 构造远程通信服务器
4) registerProcessor()：注册处理器
5) 初始化定时任务、事务相关服务、监听器。
6) 初始化RPC请求钩子RPCHook2).启动1) messageStore启动消息存储服务
2) 启动远程通信服务端（netty）
3) 开启请求长轮训服务
4) 启动netty客户端探活服务（生产者、消费者、过滤器）
5) 定时任务：每30s向nameserver注册所有broker。#### 3.producer启动原理![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606154926682-1314866503.png)producer启动流程：1) checkConfig()校验配置
2) MQClientInstance创建客户端实例。
3) registerProducer向broker注册生产者。
4) MQClientInstance.start()启动客户端实例。
5) 服务状态更新为RUNNING。MQClientInstance客户端实例启动流程如下：1) 获取nameserver地址。
2) 启动netty远程客户端。
3) 开启定时任务。
4) 开启守护线程，执行拉取消息
5) 启动负载均衡器
6) 启动消息生产者
7) 客户端实例状态更新为RUNNING#### 4.consumer启动原理![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606155119279-2121922466.png)消费者启动流程如下：1) 校验配置、复制订阅信息、创建客户端实例
2) 创建消费端负载均衡
3) 创建pull请求包装器
4) 初始化偏移量：广播模式：client存储；集群模式：broker存储
5) 初始化消费消息服务，并启动。(1.并发消费：延迟15m后，每过15分钟清理一次超时未处理完消息2.顺序消息：延迟1s后，每20s锁一次broker中mq队列+消费者端ProcessQueue)
6) 向broker注册消费者。
7) 启动客户端实例 服务状态更新为：RUNNING[]()### 2.3.2 其它消息存储、消息查询、通信机制-通信架构图、负载均衡-Producer的负载均衡、事务消息（半消息事务）、事务消息-broker2PC设计、事务消息-Op消息等。--限于篇幅，就不都举例了，详情见[RocketMQ详解（四）核心设计原理（源码级剖析必读）](https://www.cnblogs.com/dennyzhangdd/p/15035116.html "发布于 2021-07-20 16:05")。[回到顶部(go to top)](#_labelTop)[]()# 三、总结本文主要想表达的是，作为一名架构师，要能成体系的去研究技术。兼顾广度和深度。核心原理是架构师的技术域的核心，只有掌握了核心原理，各种问题迎刃而解。剩下的无非是一些基于原理上的应用、调优、二次开发。由于篇幅有限，讲解的不够细致，详情可见链接。展望未来 最近发现RocketMQ官网已全面升级5.0,基础架构云原生化升级。技术无止境，云原生来了！![](https://img2024.cnblogs.com/blog/584866/202506/584866-20250606160157119-752996848.png) ------------------个人能力有限，大家多交流，一起壮哉我大JAVA！------------------如果你觉得本文对你有点帮助的话，记得在右下角点个“推荐”哦，博主在此感谢！[好文要顶](javascript:void\(0\);) [关注我](javascript:void\(0\);) [收藏该文](javascript:void\(0\);) [微信分享](javascript:void\(0\);)[![](https://pic.cnblogs.com/face/584866/20190830130004.png)](https://home.cnblogs.com/u/dennyzhangdd/)[只会一点java](https://home.cnblogs.com/u/dennyzhangdd/) [![](https://assets.cnblogs.com/vip.png "博客园VIP会员")](https://home.cnblogs.com/u/dennyzhangdd/) [粉丝 - 728](https://home.cnblogs.com/u/dennyzhangdd/followers/) [关注 - 11](https://home.cnblogs.com/u/dennyzhangdd/followees/) [会员号：2048（终身会员VIP）](https://cnblogs.vip/)[+加关注](javascript:void\(0\);)[点关注不迷路](javascript:void\(0\);)10[« ](https://www.cnblogs.com/dennyzhangdd/p/18913823)上一篇： [架构师之我见（一）入门篇](https://www.cnblogs.com/dennyzhangdd/p/18913823 "发布于 2025-06-06 11:55") [» ](https://www.cnblogs.com/dennyzhangdd/p/19198597)下一篇： [广州，广州-程序员视角在当下局势的总结](https://www.cnblogs.com/dennyzhangdd/p/19198597 "发布于 2025-12-08 09:16")[]()[]()[刷新评论](javascript:void\(0\);)[刷新页面](#)[返回顶部](#top)发表评论 [升级成为园子VIP会员](https://cnblogs.vip/)编辑 预览cb43a26c-3ba2-e611-845c-ac853d9f53ac![]()    自动补全提交评论 [不改了](javascript:void\(0\);) [退出](javascript:void\(0\);) [订阅评论](javascript:void\(0\); "订阅后有新评论时会邮件通知您") [我的博客](//www.cnblogs.com/YzpJason/)\[Ctrl+Enter快捷键提交][【推荐】注册成为HarmonyOS开发者，支持博客园HarmonyOS社区建设](https://www.cnblogs.com/cmt/p/19241983) [【推荐】英博云GPU容器服务平台，智能算力即开即用，立即免费试用](https://www.ebcloud.com/chn_xhpwpopm) [【推荐】科研领域的连接者艾思科蓝，一站式科研学术服务数字化平台](https://ais.cn/u/VZZZJj) [【推荐】诚邀您体验阿里巴巴推出的新一代 Agentic 编程平台 Qoder](https://www.cnblogs.com/cmt/p/19165152) [【推荐】鸿蒙应用开发者认证：学鸿蒙、考认证，跻身“抢手开发者”](https://developer.huawei.com/consumer/cn/training/classDetail/d6bfe940eba3442f8ddf79e91eea0a71?type=1?ha_source=hmosclass-bokeyuan\&ha_sourceId=89000444)[![](https://img2024.cnblogs.com/blog/35695/202512/35695-20251205171919392-144975027.jpg)](https://dis.chatdesks.cn/chatdesk/jmcnblogs.html)编辑推荐：- [SAM3模型来了，手把手带你运行SAM3模型代码](https://www.cnblogs.com/codingtea/p/19316272)
 
