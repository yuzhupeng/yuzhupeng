现在AI的使用场景越来越多，公益站有时也不稳定，给大家整理一些能提供相对长期稳定大模型api的厂商和平台，作为备用或测试。

主要收集文本大模型相关，图片视频生成相关的大模型没有专门做整理。

**tldr**

-   国内大模型平台太卷了，免费额度真的很多，如果没有特殊需求，用国内的就够用了。
-   主力模型推荐: iflow, 字节火山引擎, modelscope魔搭社区。
-   免费vibe coding推荐: 腾讯codebuddy, 快手codeflicker, 阿里通义灵码/qwen-code

# [](#p-11535851-h-1)国内厂商或平台

## [](#p-11535851-iflow-2)阿里心流 iflow

-   [心流开放平台](https://platform.iflow.cn/)
-   目前我所知的免费额度最大的平台，不限量
-   主要提供的模型: 千问系列模型较多， Kimi-K2-Instruct-0905, GLM-4.6, DeepSeek-V3.2-Exp, Qwen3-Coder-Plus
-   [限流](https://platform.iflow.cn/docs/limitSpeed)
    -   每个用户最多只能 **同时发起一个** 请求，超出限制的请求会返回429错误码。

## [](#p-11535851-h-3)字节火山方舟大模型

-   目前**每个模型**每天免费 250w token， 速度很快，体验很好，但单模型token不够用，经常切换模型我觉得麻烦
-   主要提供的模型: 豆包系列模型较多，最新的deepseek-v3.2, Kimi-K2-Instruct-0905
-   ![:framed_picture:](https://linux.do/images/emoji/twemoji/framed_picture.png?v=15 ":framed_picture:") 还提供文生图相关模型
-   [免费推理额度](https://www.volcengine.com/docs/82379/1399514?lang=zh)
    -   rpm/tpm各模型不同，一般rpm为1000～10000， tpm为500w

## [](#p-11535851-modelscope-4)阿里 modelscope 魔搭社区

-   每天允许进行总数为2000次的API-Inference调用，其中每单个模型不超过500次，具体每个模型的限制可能随时动态调整。
-   我不太喜欢modelscope， 受欢迎的模型总是开放一段时间就下架，但提供的免费额度很稳定
-   ![:framed_picture:](https://linux.do/images/emoji/twemoji/framed_picture.png?v=15 ":framed_picture:") 还提供文生图相关模型
-   [API推理介绍](https://modelscope.cn/docs/model-service/API-Inference/intro)
    -   在每个模型每天不超过 500 次调用的基础上，平台可能对于部分模型再进行单独的限制，例如，deepseek-ai/DeepSeek-R1-0528，deepseek-ai/DeepSeek-V3.1等规格较大模型，当前限制单模型每天200次调用额度。  
        \-在上述调用次数限制的基础上，不同模型允许的调用并发，会根据平台的压力进行动态的速率限制调整，原则上以保障开发者单并发正常使用为目标

## [](#p-11535851-kat-coder-5)快手 KAT-Coder 系列模型

-   KAT-Coder-Pro V1 和 KAT-Coder-Air 目前都提供免费使用，其中 KAT-Coder-Air 长期提供免费使用
-   我经常拿来做测试，速度很快，对结果要求不高可以试试
-   [KAT-Coder-Air V1 模型免费使用规则](https://www.streamlake.com/document/WANQING/mh1g9y6knewv5sft54k)
    -   高峰时段: 08:00-02:00（次日） 每6小时内您将可以发起120次对话请求。
    -   非高峰时段: 02:00-08:00 每6小时内您将可以发起200次对话请求

## [](#p-11535851-glm-flash-6)智谱 glm flash 系列模型

-   [智谱AI开放平台 福利专区](https://bigmodel.cn/dev/activities/free/glm-4-flash)
-   少数的模型厂商自己提供免费模型api，长期稳定，免费模型种类比较全
-   速度很快，但效果不好，适合用来测试
-   模型包括: GLM-4-Flash-250414, GLM-4.1V-Thinking-Flash, Cogview-3-Flash(文生图), CogVideoX-Flash(视频生成)
-   [速率限制](https://www.bigmodel.cn/dev/howuse/rate-limits)
    -   限制的维度是请求 **并发** 数量（在途请求任务数量）， GLM-4-Flash为200, GLM-4V-Flash为10

## [](#p-11535851-siliconflow-7)硅基流动 SiliconFlow

-   长期稳定提供免费的小模型，大多7b/8b/9b的小模型，速度快
-   不提供32b以上的模型，小模型质量较差，我平时用的少
-   [Rate Limits](https://docs.siliconflow.cn/cn/userguide/rate-limits/rate-limit-and-upgradation)
    -   大多都是 tpm-50k

## [](#p-11535851-others-8)国内 Others

-   上面都是我用的比较多的，下面是一些其他免费模型，大家也可以补充
    
-   美团 LongCat 系列模型
    
    -   [LongCat API开放平台](https://longcat.chat/platform/docs/zh/)
    -   每个账号每天自动获得 **500,000 Tokens** 免费额度
    -   单次请求限制 输出文本：最大8K Tokens， 当触发限流时，API将返回HTTP状态码429
-   特别提及: 七牛 AI 大模型推理服务
    
    -   这是我所知的国内仅有的大模型平台，官方提供 OpenAI/Claude/Gemini 模型，不知道是不是 2API 的渠道 ![:zany_face:](https://linux.do/images/emoji/twemoji/zany_face.png?v=15 ":zany_face:")
    -   官方提供300w免费token, 有效期一年，
    -   速度很快，强烈推荐，能用各种模型
    -   [AI 大模型推理服务 - 七牛云](https://www.qiniu.com/ai/chat)

# [](#p-11535851-h-9)国外厂商或平台

## [](#p-11535851-nvidia-nim-api-10)Nvidia NIM api

-   我觉得比openrouter更好用，似乎免费不限量
-   提供各种模型， 包括国外模型: deepseek-v3.2, qwen3-coder-480b, kimi-k2-thinking, minimax-m2, mistral-large, devstral
    -   不提供glm-4.5/4.6
-   [Try NVIDIA NIM APIs](https://build.nvidia.com/models)
    -   限制rpm: 40

## [](#p-11535851-cerebras-inference-11)Cerebras Inference

-   我体验过的速度最快的大模型平台，速度可达 220+ token/s, 强烈推荐
-   提供的免费模型较少，经常更换，现在包括: glm-4.6, qwen-3-235b-a22b-instruct-2507, gpt-oss-120b, …
-   [Rate Limits](https://inference-docs.cerebras.ai/support/rate-limits)
    -   RPM: 10~30
    -   TPD: 1m

## [](#p-11535851-openrouter-12)OpenRouter

-   长期稳定，模型丰富
-   [API Rate Limits](https://openrouter.ai/docs/api/reference/limits)
    -   不充钱的用户每天 50 rpm, 充了10刀的用户每天 1000 rpm
-   很多公益站都用了openrouter的渠道

## [](#p-11535851-mistral-13)Mistral

-   欧洲主流模型厂商，提供长期稳定的模型api
-   我在官方聊天网站[Le Chat](https://chat.mistral.ai/chat)体验的效果很差，远不如国内的模型，
-   我在本地用ollama/lm-studio跑mistral/devstral系列的模型也远不如国内的qwen3-32b内的模型，但reddit论坛很多人都在吹mistral系列的模型，我觉得就是老欧人的自嗨
-   [Rate Limits & Usage tiers](https://docs.mistral.ai/deployment/ai-studio/tier)
    -   免费额度非常大， Tokens per Minute 500,000; Tokens per Month 1,000,000,000
-   [**Codestral**](https://docs.mistral.ai/capabilities/code_generation)
    -   这个针对coding的模型似乎有额外的免费额度，但我没用过，因为coding模型竞争太激烈了，有其他选择

## [](#p-11535851-others-14)国外 Others

-   groq
    
    -   免费模型种类多，但大模型不多，大多是小模型， 免费额度很小
    -   大模型包括: kimi-k2-instruct-0905, gpt-oss-120b, llama-4-maverick-17b-128e
    -   [Rate Limits](https://console.groq.com/docs/rate-limits)
        -   大多模型是= token per day 是 500K
-   国外平台我用的少，大家可以补充一些反馈和其他平台
    

# [](#p-11535851-vibe-coding-15)![:input_latin_lowercase:](https://linux.do/images/emoji/twemoji/input_latin_lowercase.png?v=15 ":input_latin_lowercase:") vibe coding 相关

-   国内的ai coding太卷了，各家都提供了很大的免费额度

## [](#p-11535851-codebuddyhttpscopilottencentcomide-16)[腾讯云代码助手 CodeBuddy](https://copilot.tencent.com/ide/)

-   目前免费不限量使用 glm-4.6, deepseek-v3.1-terminus, huyuan-2.0

## [](#p-11535851-codeflicker-httpswwwcodeflickerai-17)快手 [CodeFlicker](https://www.codeflicker.ai/)

-   目前免费不限量使用 kimi-k2-0905, kat-coder-pro

## [](#p-11535851-httpslingmaaliyuncom-18)阿里 [通义灵码](https://lingma.aliyun.com/)

-   目前免费不限量使用 千问系列模型，但不可更换其他模型

# [](#p-11535851-h-19)其他

-   不知道这么多免费api额度，可不可以整理在自己部署的new api上面统一管理 ![:thinking:](https://linux.do/images/emoji/twemoji/thinking.png?v=15 ":thinking:")
