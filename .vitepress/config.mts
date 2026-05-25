import { defineConfig } from "vitepress";

// GitHub Pages base path (仓库名作为 base)
const base = process.env.GITHUB_ACTIONS ? "/yuzhupeng/" : "/";

export default defineConfig({
  base,
  title: "fishyue 知识库",
  description: "个人技术文档与笔记",
  lang: "zh-CN",

  head: [
    [
      "meta",
      { name: "viewport", content: "width=device-width, initial-scale=1.0" },
    ],
  ],

  ignoreDeadLinks: true,

  vite: {
    ssr: {
      noExternal: ["vitepress"],
    },
  },

  themeConfig: {
    nav: [
      { text: "首页", link: "/" },
      { text: "全部索引", link: "/索引" },
      { text: "Prompt", link: "/AI与ClaudeCode/prompt/Prompt Engineering Guide" },
      { text: "C#", link: "/技术开发/Csharp/.NET%20Core" },
      { text: "Python", link: "/技术开发/Python环境管理利器Conda" },
    ],

    sidebar: {
      "/": [
        {
          text: "📖 个人成长与人生哲学",
          collapsed: true,
          items: [
            {
              text: "年度总结",
              collapsed: true,
              items: [
                { text: "2025年度人生全景总结", link: "/个人成长/2025年度人生全景总结" },
                { text: "2025年度工作总结", link: "/个人成长/2025年度工作总结" },
              ],
            },
            {
              text: "认知与思维",
              collapsed: true,
              items: [
                { text: "10种顶级思维", link: "/个人成长/10种顶级思维" },
                { text: "5个让你人生逆袭的破局点", link: "/个人成长/5个让你人生逆袭的破局点，帮你构建清晰的成长路径" },
                { text: "十条第一性原理决定人生上限", link: "/个人成长/十条第一性原理决定人生上限" },
                { text: "人生回报率最高的几件小事", link: "/个人成长/人生回报率最高的几件小事" },
                { text: "你需要感到无聊", link: "/个人成长/你需要感到无聊" },
              ],
            },
            {
              text: "读书与处世",
              collapsed: true,
              items: [
                { text: "《原则》", link: "/个人成长/《原则》" },
                { text: "《天涯大佬：25条底层规律+投资哲学》", link: "/个人成长/《天涯大佬：世界运行的25条底层规律+投资哲学》" },
                { text: "金钱心理学", link: "/个人成长/金钱心理学" },
                { text: "成年人必知的10条人情世故", link: "/个人成长/成年人必知的10条人情世故" },
                { text: "芒格推荐的48本书", link: "/个人成长/巴菲特的搭档查理芒格推荐的48本书" },
                { text: "为什么不要轻易讨论价值观", link: "/个人成长/為什麼不要輕易和身邊的人討論價值觀或深刻話題" },
                { text: "《思考，快与慢》", link: "/book/《思考，快与慢》" },
              ],
            },
            {
              text: "职场与内容创作",
              collapsed: true,
              items: [
                { text: "反向面试", link: "/个人成长/反向面试" },
                { text: "技术管理工作", link: "/个人成长/技术管理工作" },
                { text: "文章", link: "/个人成长/文章" },
                { text: "文章生产系统", link: "/个人成长/文章生产系统" },
              ],
            },
          ],
        },
        {
          text: "🤖 AI 与 Claude Code",
          collapsed: true,
          items: [
            {
              text: "Claude Code 指南",
              collapsed: true,
              items: [
                { text: "Claude Code 完全指南", link: "/AI与ClaudeCode/Claude Code 完全指南：使用方式、技巧与最佳实践" },
                { text: "Claude Code 高效使用指南", link: "/AI与ClaudeCode/Claude Code 高效使用指南：从入门到高手（2026 年 4 月更新）" },
                { text: "Claude Code 进阶使用经验分享", link: "/AI与ClaudeCode/Claude Code 进阶使用经验分享" },
                { text: "配置 Chrome DevTools MCP 指南", link: "/AI与ClaudeCode/Claude Code 配置 Chrome DevTools MCP 指南" },
                { text: "Claude Code CLI 命令大全", link: "/AI与ClaudeCode/Claude Code CLI 命令大全" },
                { text: "Claude Code 常用命令速查", link: "/AI与ClaudeCode/Claude Code常用命令速查" },
                { text: "10X Claude", link: "/AI与ClaudeCode/10X cladue" },
                { text: "Claudecode 工程提示词", link: "/AI与ClaudeCode/claudecode工程提示词" },
                { text: "为什么要写 CLAUDE.md", link: "/AI与ClaudeCode/为什么要写 CLAUDE.md它的作用" },
                { text: "效率工具全套配置分享", link: "/AI与ClaudeCode/我的 Claude Code 效率工具全套配置分享" },
              ],
            },
            {
              text: "Agent 与多智能体",
              collapsed: true,
              items: [
                { text: "Agent工程师的三层能力", link: "/AI与ClaudeCode/Agent工程师的三层能力" },
                { text: "未来最值钱的能力", link: "/AI与ClaudeCode/未来最值钱的能力：你能指挥多少Agent替你干活" },
                { text: "Skills的最正确用法", link: "/AI与ClaudeCode/Skills的最正确用法，是将整个Github压缩成你自己的超级技能库" },
                { text: "最新Agent知识点", link: "/AI与ClaudeCode/最新Agent知识点" },
              ],
            },
            {
              text: "AI 趋势与学习",
              collapsed: true,
              items: [
                { text: "AI时代你真的懂AI吗", link: "/AI与ClaudeCode/AI时代，你真的懂AI吗？——从概率匹配到Agent协作的深度洞察" },
                { text: "AI 2025总结", link: "/AI与ClaudeCode/AI2025总结" },
                { text: "AI 高频词汇", link: "/AI与ClaudeCode/AI高频词汇" },
                { text: "软件行业正面临一个奇怪的拐点", link: "/AI与ClaudeCode/软件行业正面临一个奇怪的拐点" },
                { text: "我的AI自学路线", link: "/AI与ClaudeCode/我的AI自学路线" },
                { text: "长期稳定大模型API厂商", link: "/AI与ClaudeCode/长期稳定大模型api的厂商和平台" },
                { text: "程序员最常用的10个AI提示词", link: "/AI与ClaudeCode/程序员最常用的10个AI提示词" },
              ],
            },
            {
              text: "Prompt 工程",
              collapsed: true,
              items: [
                { text: "2026｜自用 Prompt 技巧", link: "/AI与ClaudeCode/2026｜自用 Prompt 技巧" },
                { text: "AI写作", link: "/AI与ClaudeCode/AI写作" },
                { text: "写作Prompt", link: "/AI与ClaudeCode/写作Prompt" },
                { text: "prompt.md", link: "/AI与ClaudeCode/prompt" },
                { text: "语音转文字", link: "/AI与ClaudeCode/语音转文字" },
                { text: "TestPormpts", link: "/AI与ClaudeCode/TestPormpts" },
              ],
            },
            {
              text: "prompt/ 子目录",
              collapsed: true,
              items: [
                { text: "12个Claude提示词", link: "/AI与ClaudeCode/prompt/12个Claude提示词" },
                { text: "BA业务分析", link: "/AI与ClaudeCode/prompt/BA业务分析" },
                { text: "Prompt Engineering Guide", link: "/AI与ClaudeCode/prompt/Prompt Engineering Guide" },
                { text: "SOPPrompt", link: "/AI与ClaudeCode/prompt/SOPPrompt" },
                { text: "SQL优化", link: "/AI与ClaudeCode/prompt/SQL优化" },
                { text: "会议", link: "/AI与ClaudeCode/prompt/会议" },
                { text: "朋友圈", link: "/AI与ClaudeCode/prompt/朋友圈" },
                { text: "资深回答prompt", link: "/AI与ClaudeCode/prompt/资深回答prompt" },
                { text: "重构prompt", link: "/AI与ClaudeCode/prompt/重构prompt" },
              ],
            },
          ],
        },
        {
          text: "💻 技术开发",
          collapsed: true,
          items: [
            {
              text: ".NET / C# 生态",
              collapsed: true,
              items: [
                { text: "C# 数据类型", link: "/技术开发/Csharp 数据类型" },
                { text: ".NET Core", link: "/技术开发/Csharp/.NET Core" },
                { text: "WPF 面试题参考", link: "/技术开发/WPF 面试题参考" },
              ],
            },
            {
              text: "消息队列与中间件",
              collapsed: true,
              items: [
                { text: "MQ如何保证消息不丢失", link: "/技术开发/MQ如何保证消息不丢失" },
                { text: "RocketMQ", link: "/技术开发/RocketMQ" },
              ],
            },
            {
              text: "数据库与缓存",
              collapsed: true,
              items: [
                { text: "缓存与数据库一致性", link: "/技术开发/如何解决缓存和数据库一致性的问题" },
                { text: "雪花算法坑", link: "/技术开发/雪花算法坑" },
                { text: "数据库索引的代价", link: "/技术开发/数据库索引的代价" },
              ],
            },
            {
              text: "并发与系统设计",
              collapsed: true,
              items: [
                { text: "多线程用途", link: "/技术开发/多线程 用途" },
                { text: "多租户ERP仓储管理模块设计", link: "/技术开发/多租户下的ERP系统的仓储管理模块分析设计" },
                { text: "打印高质量日志", link: "/技术开发/打印高质量日志" },
              ],
            },
            {
              text: "工具与实践",
              collapsed: true,
              items: [
                { text: "Git飞行规则", link: "/技术开发/Git飞行规则" },
                { text: "Windows CMD（命令提示符）", link: "/技术开发/Windows CMD（命令提示符）" },
                { text: "Python环境管理利器Conda", link: "/技术开发/Python环境管理利器Conda" },
                { text: "工业设备监测机器学习算法", link: "/技术开发/工业设备监测中的常用机器学习算法" },
                { text: "mysqlmcp", link: "/技术开发/mysqlmcp" },
                { text: "个人能力总结", link: "/技术开发/个人能力总结" },
              ],
            },
            {
              text: "TypeScript",
              collapsed: true,
              items: [
                { text: "TypeScript 系统性学习计划", link: "/技术开发/TypeScript/TypeScript 系统性学习计划" },
              ],
            },
            {
              text: "计算机基础",
              collapsed: true,
              items: [
                { text: "ASCII、Unicode、UTF-8 详细说明", link: "/技术开发/计算机基础/ASCII、Unicode、UTF-8 详细说明" },
                { text: "字符编码知多少", link: "/技术开发/计算机基础/字符编码知多少" },
              ],
            },
            {
              text: "效率工具",
              collapsed: true,
              items: [
                { text: "NotebookLM 制作 PPT 教程", link: "/技术开发/全网最全NotebookLM 制作 PPT教程" },
              ],
            },
          ],
        },
        {
          text: "💪 健康与养生",
          collapsed: true,
          items: [
            {
              text: "断食与代谢",
              collapsed: true,
              items: [
                { text: "每日18点停止进食后腹部脂肪变化", link: "/健康养生/每日18点停止进食后腹部脂肪的生理变化全解析" },
                { text: "空腹力", link: "/健康养生/空腹力" },
                { text: "9種不會打破斷食狀態的食物", link: "/健康养生/9種不會打破斷食狀態的食物" },
              ],
            },
            {
              text: "养生与抗衰老",
              collapsed: true,
              items: [
                { text: "顶级养生", link: "/健康养生/顶级养生" },
                { text: "逆转衰老", link: "/健康养生/逆转衰老" },
                { text: "30岁男性保养", link: "/健康养生/30岁男性保养" },
                { text: "洗发水骗局", link: "/健康养生/洗发水骗局：摧毁发质、引发脱发的日化工业真相全解析" },
                { text: "广东东莞地区食补策略", link: "/健康养生/广东东莞地区食补策略" },
              ],
            },
            {
              text: "营养与生理",
              collapsed: true,
              items: [
                { text: "营养学", link: "/健康养生/营养学" },
                { text: "细胞如何维持酸碱平衡", link: "/健康养生/细胞如何维持酸碱平衡" },
                { text: "智齿的由来与拔除决策", link: "/健康养生/智齿的由来与拔除决策" },
                { text: "个人基因分析", link: "/健康养生/个人基因分析" },
              ],
            },
            {
              text: "健康与医学",
              collapsed: true,
              items: [
                { text: "健康管理", link: "/健康养生/健康与医学/健康管理" },
                { text: "T3三碘甲状腺原氨酸", link: "/健康养生/健康与医学/T3三碘甲状腺原氨酸" },
                { text: "T4 Thyroxine-甲状腺素", link: "/健康养生/健康与医学/T4 Thyroxine-甲状腺素" },
                { text: "前列腺癌风险", link: "/健康养生/健康与医学/前列腺癌风险" },
                { text: "程序员抗疲劳广东版食谱", link: "/健康养生/健康与医学/程序员抗疲劳广东版食谱示例" },
                { text: "程序员高强度工作注意事项", link: "/健康养生/健康与医学/程序员，高强度工作，应该注意什么" },
                { text: "高代谢敏感型体质", link: "/健康养生/健康与医学/高代谢敏感型体质" },
              ],
            },
            {
              text: "生活",
              collapsed: true,
              items: [
                { text: "去除螨虫", link: "/健康养生/去除螨虫" },
              ],
            },
          ],
        },
        {
          text: "📈 投资与财务",
          collapsed: true,
          items: [
            { text: "现金流分析", link: "/投资财务/现金流分析" },
          ],
        },
        {
          text: "🔧 其他",
          collapsed: true,
          items: [
            { text: "resource", link: "/其他/resource" },
            { text: "地址", link: "/其他/地址" },
            { text: "product-strategy-expert", link: "/其他/product-strategy-expert" },
            { text: "openclaw记忆系统", link: "/其他/openclaw记忆系统" },
            { text: "总结书籍prompt", link: "/其他/总结书籍prompt/总结" },
          ],
        },
      ],
    },

    socialLinks: [{ icon: "github", link: "https://github.com/yuzhupeng" }],

    search: {
      provider: "local",
    },

    outline: {
      level: [2, 3],
      label: "目录",
    },

    docFooter: {
      prev: "上一篇",
      next: "下一篇",
    },
  },
});
