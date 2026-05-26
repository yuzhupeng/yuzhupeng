---
layout: home

hero:
  name: "fishyue"
  text: "个人知识库"
  tagline: 技术笔记 · AI & Prompt · 健康养生 · 个人成长 · 投资财务
  actions:
    - theme: brand
      text: 完整索引
      link: /索引
    - theme: alt
      text: GitHub
      link: https://github.com/yuzhupeng

features:
  - title: 💻 技术开发
    details: C#/.NET、消息队列、数据库、多线程、Git、字符编码等 22 篇
    link: /索引#c-技术开发-22-篇
  - title: 🤖 AI 与 Claude Code
    details: Claude Code 指南、Agent 协作、Prompt 工程、大模型 API 等 27 篇
    link: /索引#b-ai-与-claude-code-27-篇-prompt-子目录-9-篇
  - title: 💪 健康与养生
    details: 断食代谢、抗衰老、营养学、甲状腺、程序员健康等 20 篇
    link: /索引#d-健康与养生-20-篇
  - title: 🧠 个人成长与人生哲学
    details: 年度总结、认知破局、金钱心理学、读书处世等 18 篇
    link: /索引#a-个人成长与人生哲学-18-篇
  - title: 📈 投资与财务
    details: 现金流分析、投资哲学
    link: /索引#e-投资与财务-1-篇
  - title: 🔧 其他
    details: 项目配置、Agent 定义、学习资源、工具链接等 5 篇
    link: /索引#f-项目配置与杂项-5-篇
---

<style>
/* 将关注横幅移到 hero 与 features 之间 */
.VPHome {
  display: flex;
  flex-direction: column;
}
.VPHomeHero { order: 1; }
.VPHome .vp-doc { order: 2; }
.VPHomeFeatures { order: 3; }

.follow-banner {
  margin: 0 auto 2.5rem;
  max-width: 680px;
  width: 100%;
  padding: 0 24px;
}
.follow-banner .banner-img {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  transition: box-shadow 0.3s ease;
  line-height: 0;
}
.follow-banner .banner-img:hover {
  box-shadow: 0 8px 40px rgba(0,0,0,0.12);
}
.follow-banner .banner-img img {
  width: 100%;
  height: auto;
  display: block;
}
</style>

<div class="follow-banner">
  <div class="banner-img">
    <img src="./qrcode-banner.png" alt="关注公众号" />
  </div>
</div>
