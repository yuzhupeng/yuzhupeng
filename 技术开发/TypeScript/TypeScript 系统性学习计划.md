# TypeScript 系统性学习计划

## 定位
全栈架构师视角：不学语法细节，学类型系统的设计哲学 + 工程化落地

---

## Phase 1 — 类型基础 (2-3 天)

| 主题 | 要点 |
|------|------|
| 类型注解 vs 类型推断 | 什么该写、什么能省 |
| `interface` vs `type` | 何时用哪个（本质：declaration merging vs 联合类型） |
| 联合类型 `\|` / 交叉类型 `&` | 用类型组合替代继承 |
| 字面量类型 + `as const` | 精确值约束 |
| `typeof`, `keyof`, `in` | 从值反向提取类型 |
| 泛型基础 | 约束 `extends`、默认值、多参数 |

**产出**：能给已有 JS 函数写完整类型签名

---

## Phase 2 — 类型体操 (3-5 天)

| 主题 | 要点 |
|------|------|
| 条件类型 `T extends U ? X : Y` | 模式匹配，递归 |
| 映射类型 `{ [K in T]: ... }` | `Partial`, `Required`, `Readonly` 怎么造 |
| 模板字面量类型 | `${K}_id` → 严格字符串模式 |
| 递归类型 | JSON 树、深层 Partial |
| `infer` | 从类型中提取片段（`ReturnType`, `Parameters` 实现） |
| 内置工具类型 | `Pick`, `Omit`, `Extract`, `Exclude`, `Awaited` 逐个手写 |

**产出**：能读懂 80% 的开源工具类型代码，能自己写 `DeepPartial<T>`

---

## Phase 3 — 工程化 (2-3 天)

| 主题 | 要点 |
|------|------|
| `tsconfig.json` | `strict` 全开意味着什么？`paths`, `moduleResolution`, `target` |
| 声明文件 `.d.ts` | 为 JS 库写类型、`declare module` |
| `isolatedModules` | 跟 bundler 的关系 |
| import type / export type | 编译时擦除 |
| 三斜线指令 | 何时需要（非现代项目） |
| 与 Babel / SWC / esbuild 配合 | 类型检查 vs 编译分离 |

**产出**：能独立配置一个 monorepo 的 TS 项目

---

## Phase 4 — 框架集成 (3-5 天)

| 场景 | 重点 |
|------|------|
| React + TS | `FC` 过时了，用 `PropsWithChildren`; 泛型组件; `useReducer` 类型安全 |
| Node/Express + TS | `Request`, `Response` 扩展; 装饰器元数据 |
| Next.js / Nest.js | 框架自带类型系统，理解框架类型约定 |
| 状态管理 | Zustand/Valtio/Jotai 的 TS 模式 |
| ORM | Prisma / TypeORM 的生成类型 |

**产出**：能写出框架级的类型安全代码，而非"JS 加类型注解"

---

## Phase 5 — 进阶 (可选，按需)

| 主题 | 适用场景 |
|------|---------|
| 逆变/协变 | 搞懂 `Function` 参数为何双变 |
| Branded Types | 运行时防混淆（`UserId` ≠ `OrderId`） |
| 类型性能优化 | 大项目编译慢的根因（`excessive depth`） |
| `satisfies` | TS 4.9+，兼顾类型检查与精确推断 |
| `ts-reset` / `eslint-plugin-tanstack-query` | 生态工具提升类型体验 |

---

## 推荐学习材料

| 材料 | 理由 |
|------|------|
| **TypeScript Handbook** (官方) | 必须通读，跳过"Basic Types"部分 |
| **type-challenges** (GitHub) | 入门→地狱难度，手写类型体操 |
| **Titian "TypeScript 类型系统" 系列** | 中文，深度够 |
| **Matt Pocock** 的 YouTube/教程 | 实战型，教心智模型非语法 |
| **Vite + Vitest** 当 playground | 零配置起 TS 项目 |

---

## 建议的学习节奏

| 阶段 | 时间 | 方法 |
|------|------|------|
| Phase 1 | 2-3 天 | 通读 Handbook + 写 30 个小例子 |
| Phase 2 | 3-5 天 | type-challenges Easy → Medium 全做 |
| Phase 3 | 2-3 天 | 搭一个 monorepo 实验 |
| Phase 4 | 3-5 天 | 用 TS 重写一个小模块 |
| Phase 5 | 按需 | 遇到问题再深入 |

**核心心法**：TS 不是你写 JS 后加的类型，而是你先想数据形状，用类型系统约束它，再填实现。
