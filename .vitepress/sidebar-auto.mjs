/**
 * 构建时动态补全 VitePress 侧边栏。
 *
 * 思路：保留 config.mts 中人工维护的分类树（它决定了文章归属哪个分类），
 * 再扫描磁盘上所有 Markdown，把尚未出现在树里的文档自动追加到对应分组。
 *
 * 这样新增文章无需改 config，构建时即自动进入左侧导航；而人工已经
 * 分好类的文章不会被重排。
 *
 * 映射规则：
 * 1. 人工树中已有该路径 → 不动
 * 2. 否则按顶层目录找对应的一级分组
 * 3. 在该一级分组下按文件名关键词选二级分组，找不到则放入「其他」
 */
import { readdirSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const EXCLUDE_DIRS = new Set([
  "node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts",
]);
const EXCLUDE_ROOT_FILES = new Set(["README.md", "index.md", "索引.md", "Claude.md"]);

const TOP_GROUP = {
  "个人成长": "📖 个人成长与人生哲学",
  "AI与ClaudeCode": "🤖 AI 与 Claude Code",
  "技术开发": "💻 技术开发",
  "健康养生": "💪 健康与养生",
  "投资财务": "📈 投资与财务",
  "其他": "🔧 其他",
  "book": "📖 个人成长与人生哲学",
  "心理学": "📖 个人成长与人生哲学",
  "Vedio": "🔧 其他",
  "": "🔧 其他",
};

// 二级分组关键词路由：命中即归入该分组，顺序敏感
const SUB_GROUP_HINTS = [
  ["健康与医学", ["甲状腺", "健康管理", "前列腺", "低血糖", "高代谢", "食谱"]],
  ["断食与代谢", ["断食", "空腹", "脂肪"]],
  ["营养与生理", ["营养", "基因", "酸碱", "智齿", "维生"]],
  ["养生与抗衰老", ["养生", "衰老", "白发", "洗发", "食补", "线粒体"]],
  ["生活", ["螨虫", "生活"]],
  ["数据库与缓存", ["索引", "缓存", "雪花", "数据库", "SQL"]],
  ["消息队列与中间件", ["MQ", "RocketMQ", "消息"]],
  ["并发与系统设计", ["多线程", "并发", "日志", "多租户", "幂等", "订单", "扫码"]],
  [".NET / C# 生态", ["C#", ".NET", "WPF", "Csharp"]],
  ["TypeScript", ["TypeScript"]],
  ["计算机基础", ["ASCII", "Unicode", "UTF", "编码", "软考", "架构设计师"]],
  ["效率工具", ["NotebookLM", "PPT", "Conda", "CMD"]],
  ["工具与实践", ["Git", "工具", "规范", "mysql", "mcp", "能力"]],
  ["Agent 与多智能体", ["Agent", "Skill", "智能体", "Loop", "Harness"]],
  ["Prompt 工程", ["Prompt", "提示词", "prompt"]],
  ["Claude Code 指南", ["Claude Code", "claude", "Codex", "codex"]],
  ["AI 趋势与学习", ["AI", "LLM", "职业", "学习", "知识库", "rep"]],
  ["年度总结", ["年度", "总结"]],
  ["读书与处世", ["原则", "思考", "心理", "人情", "书", "芒格", "致富", "价值观"]],
  ["职场与内容创作", ["面试", "管理", "文章", "创作", "工作"]],
  ["认知与思维", ["思维", "认知", "原理", "无聊", "野心", "做法", "方法"]],
];

/** 递归收集 Markdown 相对路径。 */
function collect(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    const st = statSync(full);
    if (st.isDirectory()) {
      if (!EXCLUDE_DIRS.has(name)) collect(full, out);
    } else if (name.endsWith(".md")) {
      const rel = relative(ROOT, full).split(sep).join("/");
      const parts = rel.split("/");
      if (parts.length === 1 && EXCLUDE_ROOT_FILES.has(parts[0])) continue;
      out.push(rel);
    }
  }
  return out;
}

function contentDocs() {
  const docs = new Map();
  for (const rel of collect(ROOT)) {
    docs.set(rel.toLowerCase().replace(/\.md$/, ""), rel);
  }
  return docs;
}

function existingLinks(sidebar) {
  const found = new Set();
  const walk = (node) => {
    if (Array.isArray(node)) {
      node.forEach(walk);
    } else if (node && typeof node === "object") {
      if (node.link) {
        // 统一成 contentDocs 的 key 形式：去掉前导斜杠、URL 解码、去 .md、小写
        let key = node.link.toLowerCase().replace(/^\//, "").replace(/\.md$/, "");
        try {
          key = decodeURIComponent(key);
        } catch {
          /* 非法编码保持原样 */
        }
        found.add(key);
      }
      if (node.items) walk(node.items);
      // sidebar 形如 { "/": [...] }，需要递归其属性值才能触达条目
      for (const [k, v] of Object.entries(node)) {
        if (k !== "items" && v && typeof v === "object") walk(v);
      }
    }
  };
  walk(sidebar);
  return found;
}

/** 标题取文件名（去扩展名），避免读文件拖慢构建。 */
function titleOf(rel) {
  return rel.split("/").pop().replace(/\.md$/i, "").trim();
}

function pickSubGroup(rel) {
  const name = rel.replace(/\//g, " ");
  for (const [group, hints] of SUB_GROUP_HINTS) {
    if (hints.some((h) => name.includes(h))) return group;
  }
  return "其他";
}

/** 把未收录文档补进侧边栏（原地修改并返回）。 */
export function enhanceSidebar(sidebar) {
  const docs = contentDocs();
  const linked = existingLinks(sidebar);
  const missing = [...docs.entries()]
    .filter(([key]) => !linked.has(key))
    .sort((a, b) => a[0].localeCompare(b[0]));
  if (!missing.length) return sidebar;

  const root = sidebar["/"];
  if (!Array.isArray(root)) return sidebar;

  const topNodes = new Map();
  for (const g of root) {
    if (g && typeof g === "object" && g.text) topNodes.set(g.text, g);
  }

  for (const [, rel] of missing) {
    const topDir = rel.includes("/") ? rel.split("/")[0] : "";
    const top = topNodes.get(TOP_GROUP[topDir] ?? "🔧 其他");
    if (!top) continue;

    const subName = pickSubGroup(rel);
    let target = (top.items ?? []).find(
      (c) => c && typeof c === "object" && c.text === subName
    );
    if (!target) {
      target = { text: subName, collapsed: true, items: [] };
      top.items = top.items ?? [];
      top.items.push(target);
    }
    target.items = target.items ?? [];
    target.items.push({ text: titleOf(rel), link: "/" + rel.replace(/\.md$/i, "") });
  }

  return sidebar;
}
