   

 

  

# Claude Code 配置 Chrome DevTools MCP 指南

[diligence](/user/2752832846177294/posts)

2025-12-30 186 阅读5分钟

关注

.markdown-body{word-break:break-word;line-height:1.75;font-weight:400;font-size:16px;overflow-x:hidden;color:#252933}.markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4,.markdown-body h5,.markdown-body h6{line-height:1.5;margin-top:35px;margin-bottom:10px;padding-bottom:5px}.markdown-body h1{font-size:24px;line-height:38px;margin-bottom:5px}.markdown-body h2{font-size:22px;line-height:34px;padding-bottom:12px;border-bottom:1px solid #ececec}.markdown-body h3{font-size:20px;line-height:28px}.markdown-body h4{font-size:18px;line-height:26px}.markdown-body h5{font-size:17px;line-height:24px}.markdown-body h6{font-size:16px;line-height:24px}.markdown-body p{line-height:inherit;margin-top:22px;margin-bottom:22px}.markdown-body img{max-width:100%}.markdown-body hr{border:none;border-top:1px solid #ddd;margin-top:32px;margin-bottom:32px}.markdown-body code{word-break:break-word;border-radius:2px;overflow-x:auto;background-color:#fff5f5;color:#ff502c;font-size:.87em;padding:.065em .4em}.markdown-body code,.markdown-body pre{font-family:Menlo,Monaco,Consolas,Courier New,monospace}.markdown-body pre{overflow:auto;position:relative;line-height:1.75}.markdown-body pre>code{font-size:12px;padding:15px 12px;margin:0;word-break:normal;display:block;overflow-x:auto;color:#333;background:#f8f8f8}.markdown-body a{text-decoration:none;color:#0269c8;border-bottom:1px solid #d1e9ff}.markdown-body a:active,.markdown-body a:hover{color:#275b8c}.markdown-body table{display:inline-block!important;font-size:12px;width:auto;max-width:100%;overflow:auto;border:1px solid #f6f6f6}.markdown-body thead{background:#f6f6f6;color:#000;text-align:left}.markdown-body tr:nth-child(2n){background-color:#fcfcfc}.markdown-body td,.markdown-body th{padding:12px 7px;line-height:24px}.markdown-body td{min-width:120px}.markdown-body blockquote{color:#666;padding:1px 23px;margin:22px 0;border-left:4px solid #cbcbcb;background-color:#f8f8f8}.markdown-body blockquote:after{display:block;content:""}.markdown-body blockquote>p{margin:10px 0}.markdown-body ol,.markdown-body ul{padding-left:28px}.markdown-body ol li,.markdown-body ul li{margin-bottom:0;list-style:inherit}.markdown-body ol li .task-list-item,.markdown-body ul li .task-list-item{list-style:none}.markdown-body ol li .task-list-item ol,.markdown-body ol li .task-list-item ul,.markdown-body ul li .task-list-item ol,.markdown-body ul li .task-list-item ul{margin-top:0}.markdown-body ol ol,.markdown-body ol ul,.markdown-body ul ol,.markdown-body ul ul{margin-top:3px}.markdown-body ol li{padding-left:6px}.markdown-body .contains-task-list{padding-left:0}.markdown-body .task-list-item{list-style:none}@media (max-width:720px){.markdown-body h1{font-size:24px}.markdown-body h2{font-size:20px}.markdown-body h3{font-size:18px}}.markdown-body pre,.markdown-body pre>code.hljs{color:#333;background:#f8f8f8}.hljs-comment,.hljs-quote{color:#998;font-style:italic}.hljs-keyword,.hljs-selector-tag,.hljs-subst{color:#333;font-weight:700}.hljs-literal,.hljs-number,.hljs-tag .hljs-attr,.hljs-template-variable,.hljs-variable{color:teal}.hljs-doctag,.hljs-string{color:#d14}.hljs-section,.hljs-selector-id,.hljs-title{color:#900;font-weight:700}.hljs-subst{font-weight:400}.hljs-class .hljs-title,.hljs-type{color:#458;font-weight:700}.hljs-attribute,.hljs-name,.hljs-tag{color:navy;font-weight:400}.hljs-link,.hljs-regexp{color:#009926}.hljs-bullet,.hljs-symbol{color:#990073}.hljs-built\_in,.hljs-builtin-name{color:#0086b3}.hljs-meta{color:#999;font-weight:700}.hljs-deletion{background:#fdd}.hljs-addition{background:#dfd}.hljs-emphasis{font-style:italic}.hljs-strong{font-weight:700}

## Claude Code 配置 Chrome DevTools MCP 指南

> 本文详细介绍如何在 Windows 系统上为 Claude Code 配置 Chrome DevTools MCP，包括踩坑经验和解决方案。

### 一、MCP 是什么？

**MCP（Model Context Protocol）** 是一种模型上下文协议，它允许 AI 工具（如 Claude Code）通过标准化的方式与外部服务进行交互。简单来说，MCP 就像是 AI 与各种工具之间的"桥梁"。

#### Chrome DevTools MCP 介绍

[Chrome DevTools MCP](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FChromeDevTools%2Fchrome-devtools-mcp "https://github.com/ChromeDevTools/chrome-devtools-mcp") 是一个基于 MCP 协议的服务器，它允许 Claude Code 通过 Chrome DevTools Protocol (CDP) 直接控制浏览器，实现：

-   🌐 **访问并分析真实页面内容**：例如直接打开后台或内部系统页面，在已登录状态下查看真实用户视角下的页面表现
-   🔍 **检查控制台错误与网络请求（Network / Console）**：例如页面白屏时，快速判断是脚本报错、接口异常还是资源加载失败
-   🖱️ **自动化用户操作（点击、滚动、填写表单）**：例如自动复现用户操作路径，用于问题复现或功能验证
-   📡 **分析接口请求与响应数据**：例如定位某个页面行为实际触发了哪些接口，以及返回数据是否正确
-   ⚡ **页面加载与性能分析**：例如分析首屏慢的原因，是接口延迟、资源体积过大，还是脚本阻塞
-   🧪 **前端自动化测试与回归验证**：例如在真实浏览器环境中快速跑一遍核心业务流程，验证改动是否影响功能

**GitHub 仓库**：[github.com/ChromeDevTo…](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FChromeDevTools%2Fchrome-devtools-mcp "https://github.com/ChromeDevTools/chrome-devtools-mcp")

### 二、Chrome 开启远程调试

1.  找到 Chrome 快捷方式，右键 → 属性
2.  在「目标」栏末尾添加参数：

ini

 体验AI代码助手

 代码解读

复制代码

`"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\software\chromeDebugProfile"`

Chrome快捷方式配置

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7577ea1d15f4462d92fb585b4fd70be6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=z0IEbzcqCyt1NSVLDPyq9B0yIKo%3D)

**参数说明**：

-   `--remote-debugging-port=9222`：开启远程调试端口（9222 是约定俗成的默认端口）
-   `--user-data-dir="D:\software\chromeDebugProfile"`：指定独立的用户数据目录

#### 为什么需要 `--user-data-dir` 参数？

**⚠️ 这是本文最重要的一个坑！**

从 **Chrome 136 版本**开始，Chrome 出于安全考虑，对远程调试做了限制：

> 如果使用默认的用户数据目录，`--remote-debugging-port` 参数会被忽略，不会真正监听端口。

这意味着：

-   ❌ 只加 `--remote-debugging-port=9222` **不够**
-   ✅ 必须同时指定 `--user-data-dir` 为一个**独立的目录**

#### 推荐做法：创建调试专用 Chrome

你可以同时拥有两个 Chrome：

1.  **日常使用的 Chrome**：正常启动，保留所有登录状态
2.  **调试专用的 Chrome**：带调试参数启动，用于 MCP 连接

> 💡 **提示**：第一次启动调试 Chrome 时需要重新登录账号，但之后会一直保留登录状态（因为是固定目录，不会丢失）。

#### 验证调试端口是否开启

启动调试 Chrome 后，验证端口是否正常监听：

powershell

 体验AI代码助手

 代码解读

复制代码

`# 检查端口监听状态 netstat -ano | findstr :9222`

如果看到 `LISTENING`，说明端口已开启。

或者直接访问：

arduino

 体验AI代码助手

 代码解读

复制代码

`http://127.0.0.1:9222/json/version`

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3ae9e9f7ce0347b0b0a38ef173bb5c22~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=V1Tv%2BqpP3L44mRuREKPb2ovHCoM%3D)

如果返回 JSON 数据，说明 Chrome DevTools Protocol 已就绪。

### 三、安装 Chrome DevTools MCP

#### 方式一：全局安装（用户级别，推荐）

bash

 体验AI代码助手

 代码解读

复制代码

`claude mcp add chrome-devtools -s user -- npx chrome-devtools-mcp@latest`

**参数说明**：

-   `-s user`：指定安装到用户级别配置，所有项目都可使用
-   `--`：分隔符，后面的参数传递给 MCP 服务器

配置会写入：`C:\Users\<用户名>\.claude.json`

#### 方式二：项目级别安装

bash

 体验AI代码助手

 代码解读

复制代码

`claude mcp add chrome-devtools npx chrome-devtools-mcp@latest`

这会将配置写入用户配置文件 `C:\Users\<用户名>\.claude.json` 中对应项目路径下的 `mcpServers` 部分。

#### 验证安装

bash

 体验AI代码助手

 代码解读

复制代码

`claude mcp list`

安装成功后，在 Claude Code 中输入 `/mcp` 可以看到 MCP 服务器状态：

### 四、修改配置文件

安装后，需要修改配置文件，添加 `--browserUrl` 参数让 MCP 连接到我们手动启动的 Chrome。

#### 配置文件位置

`C:\Users\<用户名>\.claude.json`

#### 完整配置示例

json

 体验AI代码助手

 代码解读

复制代码

`{   "mcpServers": {     "chrome-devtools": {       "type": "stdio",       "command": "npx",       "args": [         "chrome-devtools-mcp@latest",         "--browserUrl=http://127.0.0.1:9222"       ],       "env": {}     }   } }`

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/739a24e1562941c3bd4d04382f0e920c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=8AkFZ%2FpedbVeAzH1wm1E2ObSWuo%3D)

**关键参数说明**：

-   `--browserUrl=http://127.0.0.1:9222`：告诉 MCP 连接到我们手动启动的 Chrome 调试端口

此时运行 /mcp

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/449bd56547b948b894bb5b36767cf646~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=1uo4ONXzY4gUFRHY%2BOwP6zAcdOY%3D)

### 五、实战测试

配置完成后，我们来测试一下 MCP 是否正常工作。

#### 测试示例：网站性能分析

在 Claude Code 中输入：

arduino

 体验AI代码助手

 代码解读

复制代码

`帮我测试一下这个网站的性能 https://tongyi.aliyun.com/`

Claude 会通过 Chrome DevTools MCP 自动：

1.  打开目标网页
2.  收集性能指标（加载时间、资源大小等）
3.  分析控制台错误
4.  给出优化建议

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a85d1e7120e24fb194e939e3d1c678fc~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=TltVEzEG1xwC4Kqk%2FLGF37SgzAk%3D)

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/83ac1b040c434dc0b232c17ad3d57407~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=n3eMIBPHMEPPyEsNdh0fihonkHw%3D)

![image.png](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a4d991ad226549dab07a55916365521b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgZGlsaWdlbmNl:q75.awebp?rk3s=f64ab15b&x-expires=1768864503&x-signature=vr4IyIqydu0Hx4tZuR7dFaYN3Es%3D)

#### 更多使用场景

你还可以尝试这些指令：

bash

 体验AI代码助手

 代码解读

复制代码

`# 抓取页面内容 帮我获取 https://example.com 的页面标题和主要内容 # 检查控制台错误 打开 https://example.com 并告诉我有没有 JavaScript 错误 # 截图 帮我截取 https://example.com 的页面截图 # 自动化操作 打开百度，搜索"Claude Code"`

### 六、常见问题排查

#### 问题 1：`localhost:9222` 连接被拒绝

**原因**：Chrome 没有真正监听 9222 端口

**解决**：

1.  确保使用了 `--user-data-dir` 参数（Chrome 136+ 必须）
2.  确保没有其他 Chrome 进程在后台运行（任务管理器结束所有 chrome.exe）
3.  使用 `netstat -ano | findstr :9222` 检查端口是否在监听

### 七、总结

| 步骤 | 操作 |
| --- | --- |
| 1 | 创建调试专用目录（如 `D:\software\chromeDebugProfile`） |
| 2 | 使用带参数的命令启动 Chrome |
| 3 | 验证 `http://127.0.0.1:9222/json/version` 可访问 |
| 4 | 安装 MCP：`claude mcp add chrome-devtools -s user -- npx chrome-devtools-mcp@latest` |
| 5 | 修改配置文件，添加 `--browserUrl` 参数 |
| 6 | 重启 Claude Code，开始使用 |

**核心要点**：

-   Chrome 136+ 必须配合 `--user-data-dir` 才能开启远程调试
-   建议创建独立的调试 Chrome，不影响日常使用
-   安装时使用 `-s user` 可以全局生效

希望这篇文章能帮助你顺利配置 Chrome DevTools MCP！如有问题欢迎评论交流。

* * *

**参考链接**：

-   [Chrome DevTools MCP GitHub](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2FChromeDevTools%2Fchrome-devtools-mcp "https://github.com/ChromeDevTools/chrome-devtools-mcp")
-   [Chrome Remote Debugging](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.chrome.com%2Fdocs%2Fdevtools%2Fremote-debugging%2F "https://developer.chrome.com/docs/devtools/remote-debugging/")
-   [Model Context Protocol](https://link.juejin.cn?target=https%3A%2F%2Fmodelcontextprotocol.io%2F "https://modelcontextprotocol.io/")
