import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Yuzhupeng 知识库',
  description: '个人技术文档与笔记',
  lang: 'zh-CN',
  
  head: [
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }]
  ],

  ignoreDeadLinks: true,

  vite: {
    ssr: {
      noExternal: ['vitepress']
    }
  },

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: 'Prompt', link: '/prompt/' },
      { text: 'C#', link: '/C#/' },
      { text: 'Python', link: '/Python/' }
    ],

    sidebar: {
      '/': [
        {
          text: '技术笔记',
          items: [
            { text: 'Git飞行规则', link: '/Git飞行规则' },
            { text: 'C# 数据类型', link: '/C# 数据类型' },
            { text: 'RocketMQ', link: '/RocketMQ' },
            { text: '缓存与数据库一致性', link: '/如何解决缓存和数据库一致性的问题' },
            { text: '工业设备监测算法', link: '/工业设备监测中的常用机器学习算法' }
          ]
        },
        {
          text: 'Prompt',
          collapsed: true,
          items: [
            { text: 'Prompt Engineering Guide', link: '/prompt/Prompt Engineering Guide' },
            { text: 'BA业务分析', link: '/prompt/BA业务分析' },
            { text: 'SQL优化', link: '/prompt/SQL优化' },
            { text: 'SOP Prompt', link: '/prompt/SOPPrompt' },
            { text: '重构prompt', link: '/prompt/重构prompt' },
            { text: '资深回答prompt', link: '/prompt/资深回答prompt' },
            { text: '会议', link: '/prompt/会议' },
            { text: '朋友圈', link: '/prompt/朋友圈' }
          ]
        },
        {
          text: 'C# / .NET',
          collapsed: true,
          items: [
            { text: '.NET Core', link: '/C#/.NET/.NET Core' }
          ]
        },
        {
          text: 'Python',
          collapsed: true,
          items: [
            { text: 'Conda环境管理', link: '/Python/Python环境管理利器Conda' }
          ]
        },
        {
          text: '健康与医学',
          collapsed: true,
          items: [
            { text: '健康管理', link: '/健康与医学/健康管理' },
            { text: 'T3三碘甲状腺原氨酸', link: '/健康与医学/T3三碘甲状腺原氨酸' },
            { text: '程序员抗疲劳食谱', link: '/健康与医学/程序员抗疲劳广东版食谱示例' },
            { text: '程序员高强度工作注意事项', link: '/健康与医学/程序员，高强度工作，应该注意什么' }
          ]
        },
        {
          text: '计算机基础',
          collapsed: true,
          items: [
            { text: 'ASCII、Unicode、UTF-8', link: '/计算机基础/ASCII、Unicode、UTF-8 详细说明' },
            { text: '字符编码知多少', link: '/计算机基础/字符编码知多少' }
          ]
        },
        {
          text: 'AI学习',
          collapsed: true,
          items: [
            { text: 'AI 2025总结', link: '/AI 2025总结' },
            { text: 'AI写作', link: '/AI写作' },
            { text: '我的AI自学路线', link: '/我的AI自学路线' },
            { text: '长期稳定大模型api', link: '/长期稳定大模型api的厂商和平台' },
            { text: '语音转文字', link: '/语音转文字' }
          ]
        },
        {
          text: '其他',
          collapsed: true,
          items: [
            { text: '2025年度总结', link: '/2025 年度总结' },
            { text: '反向面试', link: '/反向面试' },
            { text: '技术管理工作', link: '/技术管理工作' },
            { text: '资源', link: '/resource' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yuzhupeng' }
    ],

    search: {
      provider: 'local'
    },

    outline: {
      level: [2, 3],
      label: '目录'
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇'
    }
  }
})
