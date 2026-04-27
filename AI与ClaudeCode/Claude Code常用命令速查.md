 Claude Code常用命令速查指南前言Claude Code是Anthropic推出的AI编程助手，运行在终端中，能通过自然语言帮你编写、调试和管理代码。高频命令
    
    
    
  # 打开当前目录下的聊天记录claude --resume# 继续当前目录的上一次聊天claude -c# 清除终端屏幕，但保留对话历史control + L# 为项目生成或更新文档CLAUDE.md/init# 给予全部权限（风险大）开启聊天时赋予权限claude -c --dangerously-skip-permissions聊天时赋予权限shift + TAB# 开启plan模式（仅赋予Read权限，可用于快速了解代码库而不轻易更改）两次 shift + TAB# 开启思考模式在提示词中加入 ultrathink 等关键字# 选择模型/model# 查看上下文占用情况/context# 引用文件@ + 文件名# 请求代码审查/review# 取消当前输入或生成control + C# 管道输入cat file.py | claude -p "优化这段代码"# 粘贴图片control + v# 换行Option+Enter# 编辑CLAUDE.md/memory# 开启任务结束响铃通知claude config set --global preferredNotifChannel terminal_bell# 退出 Claude Code 会话control + D# 在控制台查看每日API费用npx ccusage@latest      ccusage其他常用指令：      # 基础用法        ccusage          # 显示每日报告（默认）        ccusage daily    # 每日 token 使用量及费用        ccusage monthly  # 月度汇总报告        ccusage session  # 按会话统计用量        ccusage blocks   # 5小时计费窗口数据        # 实时监控        ccusage blocks --live  # 实时用量仪表盘        # 筛选与选项        ccusage daily --since 20250525 --until 20250530  # 指定日期范围        ccusage daily --json      # 输出 JSON 格式        ccusage daily --breakdown # 按模型细分费用# 在CC中跑Bash命令！+ Bash命令# 内存快捷键 - 添加到 CLAUDE.md    # + 需要写入到CLAUDE.md中的规则一、基础启动命令1.1 启动方式
    
    
    
  # 直接启动交互模式claude# 带初始问题启动claude "帮我分析这个项目结构"# 一次性执行并退出claude -p "解释这个函数"# 管道输入cat file.py | claude -p "优化这段代码"1.2 常用启动参数• --resume: 恢复上次会话• --plan: 启用计划模式（适合复杂任务）• --architect: 大型项目架构模式二、核心Slash命令2.1 基础管理
    
    
    
  /help          # 查看帮助/clear         # 清除历史记录/exit          # 退出程序/cost          # 查看Token使用情况/doctor        # 检查系统状态2.2 项目管理
    
    
    
  /memory        # 编辑项目记忆/memory view   # 查看项目记忆/config        # 查看配置/init          # 初始化项目文档2.3 会话优化
    
    
    
  /compact       # 压缩会话内容/bug           # 报告问题/terminal-setup # 终端设置三、实用技巧3.1 CLAUDE.md文件在项目根目录创建CLAUDE.md文件，Claude会自动读取：
    
    
    
  # 项目说明这是一个React项目## 常用命令- 启动：npm start- 测试：npm test- 构建：npm run build## 注意事项- 使用TypeScript- 遵循ESLint规则3.2 Memory功能
    
    
    
  # 设置项目记忆/memory项目使用Vue3 + TypeScriptAPI地址：https://api.example.com测试账号：test@example.com3.3 自定义命令在.claude/commands/目录创建.md文件：
    
    
    
  # debug.md请帮我调试以下问题：$ARGUMENTS步骤：1. 检查错误日志2. 分析原因3. 提供解决方案使用：/debug "登录失败"四、常见使用场景4.1 代码调试
    
    
    
  "这个函数报错了，帮我看看问题在哪""为什么我的API请求失败了？""这个React组件渲染有问题"4.2 代码优化
    
    
    
  "优化这段代码的性能""重构这个函数，让它更简洁""添加错误处理"4.3 项目管理
    
    
    
  "帮我写单元测试""创建一个新的API接口""更新项目文档""提交代码到git"五、最佳实践5.1 高效工作流1. 项目启动：创建CLAUDE.md文件2. 设置记忆：使用/memory记录项目信息3. 定期清理：使用/clear清除无关历史4. 善用自定义命令：创建常用工作流模板5.2 提问技巧• 明确具体：不要说"有问题"，要说"登录接口返回500错误"• 提供上下文：告诉Claude你的技术栈和项目类型• 分步骤：复杂任务可以分解为多个简单步骤5.3 性能优化
    
    
    
  /compact       # 会话过长时压缩/clear         # 切换任务时清理/cost          # 定期检查Token使用六、常见问题解决6.1 安装问题
    
    
    
  # 检查安装claude --version# 重新安装npm install -g @anthropic/claude-code# 检查系统状态claude /doctor6.2 权限问题• 确保已设置API Key• 检查网络连接• 验证账户状态6.3 性能问题• 定期使用/clear清理历史• 使用/compact压缩会话• 避免上传大文件七、进阶技巧7.1 团队协作• 将.claude/目录提交到git• 共享CLAUDE.md文件• 统一自定义命令7.2 多项目管理• 不同项目使用不同的Memory设置• 为每个项目创建专用的CLAUDE.md• 使用项目特定的自定义命令7.3 自动化工作流
    
    
    
  # 创建开发启动命令# .claude/commands/dev.md启动开发环境：1. npm install2. npm start3. 打开浏览器访问 http://localhost:3000八、实用命令速查表
        
          
            命令功能使用频率
            /help查看帮助⭐⭐⭐⭐⭐/clear清除历史⭐⭐⭐⭐⭐/memory项目记忆⭐⭐⭐⭐/costToken使用⭐⭐⭐⭐/compact压缩会话⭐⭐⭐/doctor系统检查⭐⭐⭐/config查看配置⭐⭐/init初始化项目⭐⭐
          
        
      总结Claude Code是一个强大的AI编程助手，掌握这些常用命令就能处理大部分日常开发任务：1. 启动时：使用claude进入交互模式2. 设置项目：创建CLAUDE.md文件，设置Memory3. 日常使用：善用自然语言描述需求4. 优化性能：定期/clear和/compact5. 解决问题：使用/doctor检查，/help查看帮助记住：Claude Code最大的优势是理解自然语言，所以直接说出你的需求即可！相关资源：• Claude Code官方文档• 安装指南使用开发建议：要求Claude在编码前制定计划。明确告诉它在您确认其计划看起来不错之前不要编码。按Escape中断Claude在任何阶段（思考、工具调用、文件编辑），保留上下文以便您可以纠偏或扩展指令。双击Escape跳回历史，编辑之前的提示词，并探索不同的方向。您可以编辑提示词并重复直到获得您要寻找的结果。要求Claude撤销更改，通常与选项#2结合使用以采取不同的方法。0
    
  
    
  
    
   
