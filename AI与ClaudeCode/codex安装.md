# [Codex 接入国产大模型详解] 

最近看大家都在聊codex，一直没有用过，于是趁周末兴冲冲的装完，准备接入买的火山方舟coding plan，结果给我返回了报错……

问题不在火山方舟，在 API 协议。

Codex 用的是 OpenAI 的 Responses API，火山方舟兼容的是 Chat Completions 格式。两边说的不是一种语言，中间缺个翻译。

下面把这整条链路讲清楚，从协议到工具到实操，一条龙走完。

（还没装 Codex CLI 的话，`npm install -g @openai/codex` 一条命令搞定，`codex --version` 验证。）

## 三种 API 格式，各有各的方言

Codex 连不上国产模型，根子在 API 协议。目前主流的有三套。

![三种接口对比图](https://img2024.cnblogs.com/blog/44814/202605/44814-20260527004302481-55229758.png)

### OpenAI Chat Completions：国产模型的门槛

国产模型（DeepSeek、Kimi、GLM、豆包等）几乎都兼容这个格式：

```json
POST /v1/chat/completions{  "model": "deepseek-chat",  "messages": [    {"role": "system", "content": "你是一个 AI 助手"},    {"role": "user", "content": "你好"}  ]}
```

核心结构：`messages` 数组 + `role` 分 system/user/assistant。

### Anthropic Messages：Claude 的母语

```json
POST /v1/messages{  "model": "claude-sonnet-4",  "system": "你是一个 AI 助手",  "messages": [    {"role": "user", "content": "你好"}  ]}
```

区别：`system` 是独立参数，`content` 可以是文本块或图片块的数组。

> 注：这个格式现在国产模型支持面已经很广了，各家 Coding Plan 基本都接上了。

### OpenAI Responses API：Codex 在用的那套

这是 OpenAI 2025 年推的统一接口，Codex 就在用这套：

```json
POST /v1/responses{  "model": "gpt-5.3-codex",  "input": "你好",  "tools": [{"type": "web_search_preview"}]}
```

和 Chat Completions 比，几个关键变化：

-   没有 `messages` 了，换成 `input` 字段，不再分 system/user/assistant
-   工具调用（web search、code interpreter 等）内建在 API 里
-   支持 `previous_response_id`，服务端可以帮你维持上下文
-   流式响应的事件结构完全不同

## AxonHub：API 翻译官

AxonHub 是个开源的 AI 网关，Go 写的。核心功能：国产模型说 Chat Completions，Codex 要听 Responses，它在中间做双向翻译。Codex 以为自己连的是 OpenAI，背后接的其实是国产模型。

![AxonHub Proxy](https://img2024.cnblogs.com/blog/44814/202605/44814-20260527004409760-1188994142.png)

### 部署

Docker 一行启动，单容器跑，资源占用极低：

```yaml
services:  axonhub:    image: looplj/axonhub:latest    container_name: axonhub    environment:      AXONHUB_DB_DIALECT: sqlite3      AXONHUB_DB_DSN: "file:/data/axonhub.db?cache=shared&_fk=1"    ports:      - "8090:8090"    volumes:      - ./data:/data    restart: unless-stopped
```

```bash
docker compose up -d
```

启动后访问 `http://localhost:8090`，进初始化向导，设管理员账号密码就行。

> 我自己跑的就是 SQLite 方案，内存 50-100MB，WSL 里毫无压力。PostgreSQL 功能更全但资源开销大，个人用 SQLite 够了。

### 配置 Codex 指向 AxonHub

编辑 `~/.codex/config.toml`：

```toml
model = "gpt-5"model_provider = "axonhub" [model_providers.axonhub]name = "AxonHub"base_url = "http://127.0.0.1:8090/v1"env_key = "AXONHUB_API_KEY"wire_api = "responses"
```

导出 API Key：

```bash
export AXONHUB_API_KEY="你的AxonHub API Key"
```

然后启动 Codex，所有请求走 AxonHub 中转。模型返回的 Chat Completions 响应，AxonHub 翻译成 Codex 认的 Responses 格式。

## 实战：接入火山方舟

说一万遍不如跑一遍。以火山方舟为例，完整走流程。

### 1\. 拿 API Key和Base URL

打开火山方舟控制台，创建 API Key，复制保存。  
找到接入点的BaseUrl：[https://ark.cn-beijing.volces.com/api/coding](https://ark.cn-beijing.volces.com/api/coding)

### 2\. 在 AxonHub 加渠道

在 AxonHub 管理界面加一个新的 Channel：

-   类型：Anthropic Messages
-   Base URL：`https://ark.cn-beijing.volces.com/api/coding`
-   API Key：刚才从火山方舟拿的
-   模型映射：把 AxonHub 里看到的模型名（比如 `gpt-5`）映射到火山方舟的接入点 ID

AxonHub的详细配置可以看我前面的文章：[https://mp.weixin.qq.com/s/wodNHJabYNfxdJzHLWjyjA](https://mp.weixin.qq.com/s/wodNHJabYNfxdJzHLWjyjA)

### 3\. 配置codex模型

打开~/.codex/config.toml文件，添加自定义模型：

```ini
# ===== 默认配置：日常轻量 =====model = "deepseek-v4-flash"model_provider = "axonhub-responses" approval_policy = "on-request"sandbox_mode = "workspace-write"model_reasoning_effort = "high"model_verbosity = "medium"check_for_update_on_startup = false # ===== 共享 Provider =====[model_providers.axonhub-responses]name = "AxonHub"base_url = "http://localhost:8090/v1"env_key = "AXONHUB_API_KEY"wire_api = "responses"
```

### 4\. 验证

确认前面几步没问题，环境变量已导出，启动 Codex：

```bash
codex "写一个 Hello World 的 Python 程序"
```

正常响应、生成代码，链路就走通了。

### 踩坑区

-   AxonHub 默认超时偏短。DeepSeek 的推理模型响应慢，容易断。在 `config.yml` 里把 `llm_request_timeout` 调到 600s
-   使用火山方舟的Anthropic 地址接入 [https://ark.cn-beijing.volces.com/api/coding](https://ark.cn-beijing.volces.com/api/coding)
-   报 401？先 `echo $AXONHUB_API_KEY` 确认环境变量导没导出

## 阿里百炼：更省事的方案

不想搭 AxonHub 的话，阿里百炼的 Qwen 系列有更省事的办法。

Qwen-3.6plus 和 Qwen-3.7max 原生支持 OpenAI Responses API，可以直接对接 Codex，不用中间代理。

配置简单得多，直接指向阿里百炼的端点：

```toml
model = "qwen-3.7max"model_provider = "bailian" [model_providers.bailian]name = "阿里百炼"base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"env_key = "DASHSCOPE_API_KEY"wire_api = "responses"
```

导出 API Key，直接就能用。

不是 Qwen 最新版，或者想跑 DeepSeek、GLM 等其他模型的，还得走 AxonHub。

## 总结

| 方案 | 适用场景 | 优点 | 缺点 |
| --- | --- | --- | --- |
| AxonHub + 火山方舟 | 想用豆包/DeepSeek 等 | 模型选择多，灵活 | 多搭一个代理 |
| 阿里百炼直连 | 只用 Qwen | 零配置，即开即用 | 模型选择有限 |

Qwen 新模型可以直接上，其他国产模型需要一个 AxonHub 帮你翻译。就这么简单。

* * *

 
