## Workflow Orchestration
## 工作流程编排

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity
### 1.计划节点默认
- 进入任何非简单任务的计划模式（3+步骤或架构决策）
- 如果出现问题，立刻停下来重新规划——不要一直逼
- 使用计划模式进行验证步骤，而不仅仅是建造
- 提前详细说明以减少歧义

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One tack per subagent for focused execution
### 2.次代理策略
- 大量使用子代理以保持主上下文窗口干净
- 将研究、探索和并行分析卸给子代理
- 对于复杂问题，通过子代理投入更多计算量
- 每个子代理一个针对执行的专注点

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project
### 3.自我提升循环
- 用户任何纠正后：更新“tasks/lessons.md”，并添加该模式
- 为自己制定规则，防止同样的错误
- 无情迭代这些教训，直到错误率下降
- 在课程开始时回顾相关项目的课程内容

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness
### 4.完成前的验证
- 在未证明任务可行之前，绝不要标记任务已完成
- 在关键时刻，主变更与你的变更之间的差异行为
- 问问自己：“工程师会批准这个吗？”
- 运行测试，检查日志，证明正确性

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it
### 5.要求优雅（平衡）
- 对于非平凡的变化：暂停并问“有没有更优雅的方法？”
- 如果某个修正感觉不靠谱：“现在知道了所有知识，实现优雅的解决方案”
- 跳过这个，因为有简单明显的修复——不要过度设计
- 在展示前先挑战自己的作品

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how
### 6.自主修复错误
- 收到 bug 报告时：直接修复。不要要求牵手
- 指出日志、错误、失败测试——然后加以解决
- 用户无需切换上下文
- 去修复未通过的 CI 测试，但没人告诉我怎么做

## Task Management
## 任务管理

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections
1. **先规划**：将计划写入“tasks/todo.md”，并附有可检查的项目
2. **核实计划**：在开始实施前请先确认
3. **跟踪进度**：在过程中标记完成项目
4. **解释变更**：每一步的高级总结
5. **文档结果**：在“tasks/todo.md”中添加审查部分
6. **捕捉课程**：修正后更新“tasks/lessons.md”

## Core Principles
## 核心原则

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimat Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **简洁优先**：让每一项更改都尽可能简单。影响最小的代码。
- **无懒惰**：找出根本原因。没有临时的解决办法。高级开发者标准。
- **最小影响**：改动应仅涉及必要范围。避免引入虫子。
