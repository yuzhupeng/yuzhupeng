Claude Code 是 Anthropic 推出的一个 agentic 编码工具 (agentic coding tool)，可以在命令行（terminal）中运行，或者集成在一些支持终端的 IDE 中，借助 Claude 的语言模型能力来辅助写代码、重构、调试、维护、理解代码库等。

![Claude Code国内使用_保姆级新手安装使用教程_神马中转API Claude Code代理API](https://pic.imgdd.cc/item/68ef0f7367147de033449517.png)

## **一、Claude Code 简介与工作原理**

在深入 CLAUDE.md 之前，先快速了解 Claude Code 是什么，以及它如何与项目交互。

### **什么是 Claude Code？**

-   Claude Code 是 Anthropic 提供的一个命令行（CLI）工具 / 编程代理（agentic coding）工具，允许你用自然语言直接与代码库交互：让 Claude 理解你的项目结构、生成/修改代码、执行 shell 命令、提交 Git 更改等。
    
-   它并不是简单的代码补全或聊天机器人，而是能主动采取操作（编辑文件、运行命令、Git 操作等）的智能体。
    
-   Claude Code 会尝试把项目的上下文（文件内容、历史、提示）纳入考虑，以便做出合理决策。
    

### **Claude 如何获取上下文 / 记忆**

-   启动时，Claude Code 会 **递归向上** 从当前目录开始查找 CLAUDE.md 或 CLAUDE.local.md（目前主流是 CLAUDE.md）文件，并把这些内容作为“记忆”或“上下文”读入。
    
-   如果某些子目录（子树）也有 CLAUDE.md，在进入这些子目录、读取这些子树时，这些子树中的 CLAUDE.md 也会被包含进上下文。它不会在启动时就预先载入它们。
    
-   CLAUDE.md 的内容会成为 Claude 的默认 “系统提示 / 背景” 的一部分，也就是说，Claude 在思考/决策时会参考它里面的说明。
    
-   在对话过程中你可以用快捷方式（如以 # 开头的行）把内容写入 CLAUDE.md。例如：
    

```highlighter-hljs hljs bash
# 始终使用描述性变量名称
```

-   Claude 会提示你把这行放入哪个记忆文件（即哪个 CLAUDE.md）里。
    
-   在对话中你也可以用 /memory 命令直接编辑记忆文件（即打开 CLAUDE.md 或其他记忆文件进行修改）。
    
-   CLAUDE.md 支持导入其他文件（@path/to/file.md 语法），这样你可以把说明或配置拆成多个文件。
    
-   为了避免冲突或安全隐患，导入语法在 Markdown 的代码块或反引号（ \`\`\` 或 \`）中不会被解释为导入。
    

### **Claude Code安装与国内配置**

Mac & Liunx 配置方式

确保系统已安装 Node.js 18+ 版本

**1.安装 Homebrew (mac推荐)**

如果尚未安装 Homebrew：

```highlighter-hljs hljs bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2\. 安装 Node.js**

使用 Homebrew：

```highlighter-hljs hljs mipsasm
brew install node
```

**2\. 安装 Claude Code**

```highlighter-hljs hljs bash
npm install -g @anthropic-ai/claude-code
```

**3\. 配置Claude API 密钥**

国内使用 Claude Code 的主要挑战是网络限制和高昂的费用，通常需要借助第三方镜像或代理服务

**小编直接用的神马中转API（api.whatai.cc） 获取Auth Token** 

![神马中转API Claude Code代理API_低价稳定好用的claude API代理服务](https://pic.imgdd.cc/item/68e86c368dc72b176e7e6846.jpg)

`sk-xxx替换成令牌页面密钥`

**方法一：使用 Bash（推荐）**

```highlighter-hljs hljs bash
echo 'export ANTHROPIC_AUTH_TOKEN="sk-xxx"' >> ~/.bash_profile echo 'export ANTHROPIC_BASE_URL="https://api.whatai.cc"' >> ~/.bash_profile source ~/.bash_profile
```

**方法二：使用 Zsh（如果使用 Oh My Zsh）**

```highlighter-hljs hljs bash
echo 'export ANTHROPIC_AUTH_TOKEN="sk-xxx"' >> ~/.zshrc echo 'export ANTHROPIC_BASE_URL="https://api.whatai.cc"' >> ~/.zshrc source ~/.zshrc
```

**注意：** 永久设置后需要重启终端才能生效。

**4\. 启动使用 Claude Code**

```highlighter-hljs hljs bash
# 进入项目目录
cd your-project-folder

# 启动 Claude Code
claude
```

**首次启动后需要先进行主题的选择等操作：**

-   • 选择喜欢的主题（回车）
-   • 确认安全须知（回车）
-   • 使用默认 Terminal 配置（回车）
-   • 信任工作目录（回车）
-   • 开始编程！🚀

![Claude Code国内使用_保姆级新手安装使用教程](https://pic.imgdd.cc/item/68ef0ef067147de0334494d9.png)

* * *

## **二、为什么要写** **CLAUDE.md****它的作用**

CLAUDE.md 是 Claude 在启动时就会读取并纳入思考的背景说明文件。其作用包括：

1.  **为项目／团队设定 “行为指南”**
    
    例如：变量命名规则、代码风格、重要模块说明、工具脚本使用方式、开发者约定等。这样 Claude 在做决定或修改代码时更符合团队规范。
    
2.  **减少每次提示重复写背景**
    
    因为是在启动时就载入，后续你对 Claude 发出的自然语言提示，就可以省掉再次讲述这些约定或规则。
    
3.  **引导 Claude 行为 / 限制其权限 / 指定工具**
    
    你可以在 CLAUDE.md 中说明哪些工具是安全可用的、哪些要谨慎，或者告诉 Claude “在遇到这种情况用这个脚本 / 命令”。
    
4.  **项目结构说明 / 关键模块和约定**
    
    在多人协作或大型项目中，CLAUDE.md 能帮助 Claude 快速理解模块职责、入口文件、依赖关系等，从而做出更合理的建议。
    
5.  **分层记忆 / 子目录定制**
    
    项目中不同子模块、子目录可以有自己的 CLAUDE.md 来定制局部行为。这样即使在子模块中调用 Claude，也能参考子模块的特定规则。
    
6.  **导入 / 组合多个说明**
    
    通过 @ 语法，你可以将不同功能模块的说明拆入多个 .md 文件，然后在主 CLAUDE.md 中导入。这样结构更清晰，便于维护。
    
7.  **提升 Claude 决策质量 / 减少猜测**
    
    许多用户反馈：写得越规范、说明越明确的 CLAUDE.md，Claude 的输出越稳定、符合预期。
    

综上，CLAUDE.md 是 Claude Code 的“驾驶舱说明书”，好好写能显著提升体验。

* * *

## **三、如何创建与配置** **CLAUDE.md**

下面是一个比较系统的步骤（从零开始）：

### **1\. 初始化** **CLAUDE.md**

-   在项目根目录运行：
    

```highlighter-hljs hljs bash
/init
```

-   Claude Code 会尝试读取项目结构、关键文件、依赖等，然后自动生成一个初步的 CLAUDE.md。
    
-   生成之后建议你人工审核、修改。
    

### **2\. 放置位置和层级**

-   通常放在项目根目录：./CLAUDE.md。
    
-   对于 monorepo 或多模块项目，也可以在父目录或子目录放额外的 CLAUDE.md。当 Claude 在子目录中工作时，会优先载入子目录的 CLAUDE.md。
    
-   你还可以在用户目录（如 ~/.claude/CLAUDE.md）放个人偏好 / 跨项目的说明。
    
-   目前 CLAUDE.local.md（旧名）已逐渐弃用，推荐用导入机制替代。
    

### **3\.** **CLAUDE.md****的内容结构与建议写法**

下面是一个推荐的内容结构与写作规范，可根据团队 / 项目情况增删：

```highlighter-hljs hljs yaml
# 项目名称 / 简介

简要的一两行：这个项目是做什么的、关键模块、技术栈等。

---

## 约定与规则

- 代码风格 / 格式化（如 ESLint 规则、缩进、命名风格等）  
- 命名规则（变量名、函数名、类名、接口名等）  
- 分支策略 / Git 工作流  
- 提交规范 / commit message 格式  
- 测试 / 覆盖率要求  
- 构建 / 部署 / 环境变量说明  

---

## 目录结构与模块说明

- `src/`：前端代码  
- `backend/`：后端服务  
- `scripts/`：工具脚本  
- `database/`：数据库迁移、架构说明  

（也可以导入 README、架构文档等）

---

## 常用命令 / 工具脚本

- `npm run dev`：启动开发模式  
- `npm run build`：打包  
- `npm test`：运行测试  
- `scripts/generate-report.sh`：生成报告脚本  

---

## 特殊行为 / 边界条件 / 警告

- 在某些环境某个模块必须以某种方式启动  
- 某些文件不可修改或受限  
- 性能敏感模块需注意  

---

## 导入 (可选)

你可以使用 `@path/to/file.md` 语法导入其他说明文件：
```

@README.md

@docs/api-guidelines.md

```highlighter-hljs hljs yaml
---

（可以添加更多章节，如代码示意、约定模板、例子等）
```

**写作建议：**

-   保持简洁与清晰，避免把过多细节塞进去。过长的背景可能反而让 Claude 更难抓住重点。
    
-   用自然语言写规则，而不是只给代码片段。Claude 能理解这种指令。
    
-   在规则中适度给出例子 / 模板，帮助 Claude 理解意思。
    
-   当项目演变、规范变更时，及时更新 CLAUDE.md。
    
-   对于团队项目，可以把主 CLAUDE.md 提交到版本控制，让团队成员共享。
    

### **4\. 导入其他文件（****@****语法）**

如前文所述，为了避免让 CLAUDE.md 变得臃肿，你可以把不同模块或子系统的规则分别写入独立 .md 文件，然后在主文件用导入语法引用。例如：

```highlighter-hljs hljs bash
# 主 CLAUDE.md

项目简介与一般约定在这里。

# 子系统说明
@backend/backend-guidelines.md
@frontend/style-guidelines.md
```

这样结构清晰、易于维护。

注意：导入语法在代码块 / 反引号内不会生效。

* * *

## **四、Claude Code 的基本使用流程 / 常见命令**

在有了 CLAUDE.md 之后，我们聊聊 Claude Code 的一些基本用法和交互流程。

### **安装与配置**

-   使用 npm 全局安装（前提是已安装 Node.js）：
    

```highlighter-hljs hljs bash
npm install -g @anthropic-ai/claude-code
```

-   初次启动会走配置流程，包括 OAuth、API key、权限授权等。
    
-   安装后可以执行 claude doctor 检查环境与版本状态。
    
-   在 Windows 上可能需要在 WSL 或 Git Bash 环境下运行。
    

### **常见交互 / 指令**

以下是 Claude Code 常用的交互指令与技巧：

| 指令 / 方式         | 作用 / 说明                            |
| --------------- | ---------------------------------- |
| claude          | 启动交互式会话                            |
| claude -p "..." | 在非交互模式下直接发提示（类似 “prompt” 模式）       |
| claude -c       | 继续上一次会话（保持上下文）                     |
| /help           | 显示帮助文档                             |
| /clear          | 清除当前对话历史                           |
| /config         | 查看 / 修改配置                          |
| /cost           | 查看当前会话或累计 token 使用 / 费用情况          |
| /model          | 切换所用的 Claude 模型（如 Sonnet / Opus 等） |
| /memory         | 在对话中打开记忆编辑器（编辑 CLAUDE.md 等记忆文件）    |
| /review         | 请求对当前代码更改做审查 / 建议                  |
| /vim            | 进入 vim 模式进行编辑（如果支持）                |

此外，有些命令可以结合 shell 管道使用，例如：

```highlighter-hljs hljs bash
cat logs.txt | claude -p "analyze these errors and suggest fixes"
```

这会把 logs.txt 的内容输入 Claude 作为上下文。

还有无头 / 自动化模式（用于脚本、CI 等）：

-   使用 \-p 提示 + \--output-format stream-json 获取 JSON 输出
    
-   无头模式不会保留对话上下文（每次是独立的请求）
    

### **流程范例：一次典型任务**

从一个自然语言需求走到代码变更，大致流程可能像：

1.  启动 Claude：claude
    
2.  提出需求：\> 给这个项目添加一个用户登录注册功能
    
3.  Claude 会扫描 CLAUDE.md、项目文件，列出一个 plan（子任务清单），可能先让你确认 plan
    
4.  你确认 plan 后，Claude 会依次对文件做更改（生成、修改、删除等），在每步修改前询问你是否接受
    
5.  最后 Claude 会生成提交、PR、commit message 等
    
6.  你可以接着让 Claude 审查改动、写文档、重构、修 bug 等
    

在这个过程中，CLAUDE.md 的规则和约定会被 Claude 用来指导其行为。

* * *

## **五、几个实战示例（含** **CLAUDE.md****\+ 输入输出）**

下面给你几个完整的示例，演示 CLAUDE.md + 提示 + Claude 的输出 / 行动。

* * *

### **示例 1：小型 Node.js 项目**

**项目结构：**

```highlighter-hljs hljs x86asm
my-app/
  CLAUDE.md
  package.json
  src/
    index.js
    user.js
  tests/
    user.test.js
```

**CLAUDE.md（初稿）：**

```highlighter-hljs hljs yaml
# MyApp

这是一个简单的用户管理服务，包含用户注册、登录、查询接口。

---

## 约定与规则

- 使用 JavaScript (Node.js, ES6+)  
- 命名风格：变量采用 `camelCase`，类名 `PascalCase`  
- 使用 async/await 异步风格，不用 callback  
- 所有请求输入要做基本校验  
- commit message 用 “<模块>: <说明>” 形式  

---

## 常用命令

- `npm run dev`：启动  
- `npm test`：运行测试  
- `npm run lint`：静态检查  
```

**提示给 Claude：**

```highlighter-hljs hljs markdown
> 为这个项目添加用户注册与登录功能（有 email + password），并写测试。
```

**Claude 的可能行为 / 输出（模拟）：**

1.  Claude 读取 CLAUDE.md，理解项目背景、约定
    
2.  扫描项目文件结构，发现 src/user.js 和 tests/user.test.js
    
3.  返回一个 plan，比如：
    

```highlighter-hljs hljs markdown
我建议按以下步骤实施：
1. 在 src/user.js 中添加 register 和 login 方法  
2. 在 tests/user.test.js 中为 register/login 写单元测试  
3. 在 index.js 中添加相应路由和调用  
4. 在 package.json 添加必要依赖（如 bcrypt, jsonwebtoken）  
5. 执行 lint & 测试，确保一切通过  
```

3.  你确认后，Claude 逐步生成代码更动，询问你是否接受每一步
    
4.  最终生成提交（如 “user: add register & login with tests”）
    

你如果接着说：

```highlighter-hljs hljs markdown
> 审查一下刚才的更改，有什么优化建议吗？
```

Claude 会给你代码审查意见，比如密码加盐策略、错误处理、异常捕获等。

* * *

### **示例 2：使用导入多个说明文件**

假设项目比较大，有前端、后端两个模块，各自有不同规则。你可以这样写主 CLAUDE.md：

```highlighter-hljs hljs perl
# 大型项目

通用背景与说明在这里。

## 前端说明
@frontend/CLAUDE.md

## 后端说明
@backend/CLAUDE.md
```

然后在 frontend/CLAUDE.md：

```highlighter-hljs hljs markdown
# 前端模块规则

- 使用 React + TypeScript  
- CSS 模块化或 Tailwind  
- 命名：组件首字母大写，prop 用 camelCase  
- 使用 React Hook 风格  
```

在 backend/CLAUDE.md：

```highlighter-hljs hljs markdown
# 后端模块规则

- 使用 Node.js + Express  
- 路由控制器分离  
- 错误统一处理  
- 日志使用 Winston  
```

当你在 backend/ 目录中运行 Claude，Claude 会读取 backend/CLAUDE.md 并结合主 CLAUDE.md 的通用规则一起理解你的指令。

然后你可以在 backend 目录中给 Claude 说：

```highlighter-hljs hljs shell
> 为后端添加一个 GET /users 接口，返回用户列表
```

Claude 会根据 backend/CLAUDE.md 的规则，用 Express 写出合规风格的代码。

* * *

### **示例 3：调试日志 + 管道输入**

假设你有一个日志文件 error.log，内容是一个堆栈跟踪 / 异常信息。你希望 Claude 帮你分析错误。

命令行：

```highlighter-hljs hljs lua
cat error.log | claude -p "分析这段错误日志，并建议可能的根因与修复方法"
```

（或者用 /prompt 模式）

Claude 会接受日志内容作为输入，上下文中又有 CLAUDE.md 的项目背景，从而给你更贴近项目的错误分析建议。

* * *

## **六、进阶技巧与最佳实践总结**

下面是一些社区 / 官方推荐的技巧，帮你写好 CLAUDE.md、提升 Claude Code 的效率和稳定性。

| 技巧 / 建议                     | 说明 / 原理                                                     |
| --------------------------- | ----------------------------------------------------------- |
| 精炼优先                        | 不要在 CLAUDE.md 塞太多冗余内容。让规则清晰、简洁，聚焦最关键的决策点。                   |
| 使用 # 快速写入记忆                 | 在对话中以 # 开头写一句规则，Claude 会提示你把它写入哪个 CLAUDE.md。                |
| 动态 / 临时记忆                   | 对于一次性调整、短期规则，也可以在对话中写入，不一定完全写入 CLAUDE.md。                   |
| 定期维护 / 清理                   | 项目演进时，CLAUDE.md 可能过时或混乱。建议定期审查、调整结构与规则。                     |
| 授权工具要谨慎                     | Claude 默认在修改文件 / Git 等操作前会请求授权。你可以在对话中 / 配置中调整哪些工具允许、哪些不允许。 |
| 让 Claude 先生成 plan / TODO 清单 | 在执行代码修改之前先让它列 plan，你可以确认是否合理，避免它偏离预期。                       |
| 在提示中给足背景 / 约束               | 即使有 CLAUDE.md，在复杂任务里也可以在提示里提炼关键约束，避免 Claude 偏离。             |
| 利用子目录 CLAUDE.md细化           | 在子模块内写局部 CLAUDE.md，让规则更接近业务逻辑。                              |
| 开启 / 关闭自动更新                 | 如果你希望控制版本稳定性，可以禁用 Claude Code 的自动更新行为。                      |

* * *
 
