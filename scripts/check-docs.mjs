/**
 * 在构建前校验 Markdown 文件能否被 Vue 正常编译。
 *
 * 背景：VitePress 把每个 md 渲染成 Vue SFC 再编译。某些从网页复制粘贴
 * 的内容会渲染出重复的 HTML 属性（如 `margin` 出现两次），Vue 编译器
 * 直接抛 `Duplicate attribute`，导致整个站点构建失败、无法发布。
 *
 * 本脚本用 VitePress 官方 markdown 渲染器 + Vue 官方编译器，逐文件
 * 复现「渲染 → 编译」流程，把构建期才暴露的语法错误提前到提交前。
 *
 * 用法：
 *   node scripts/check-docs.mjs         # 校验全部 md
 *   node scripts/check-docs.mjs a.md    # 只校验指定文件
 * 退出码：0 通过，1 存在问题
 */
import { createMarkdownRenderer } from 'vitepress'
import { parse, compileTemplate } from '@vue/compiler-sfc'
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { join, relative, sep } from 'node:path'

const ROOT = process.cwd()
const PUBLIC_DIR = join(ROOT, '.vitepress', 'public')
const EXCLUDE_DIRS = new Set([
  'node_modules', '.git', '.vitepress', '.claude', '.vs', 'scripts'
])

// 站内绝对路径图片：![](/uploads/x.jpeg) 会按 public 目录解析，缺失则构建失败
const ABS_IMAGE_RE = /!\[[^\]]*\]\((\/[^)\s]+)/g

/** 递归收集 Markdown 文件，跳过排除目录。 */
function collect(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name)
    const stat = statSync(full)
    if (stat.isDirectory()) {
      if (!EXCLUDE_DIRS.has(name)) collect(full, out)
    } else if (name.endsWith('.md')) {
      out.push(full)
    }
  }
  return out
}

/**
 * 把渲染后的 HTML 包成 SFC 并编译，返回 Vue 报错列表。
 * 使用 buildMode 让编译错误以异常形式抛出，便于定位。
 */
function compileSfc(html, filePath) {
  const source = `<template>\n${html}\n</template>\n`
  const { descriptor, errors: parseErrors } = parse(source, { filename: filePath })
  const problems = [...parseErrors]

  if (!parseErrors.length && descriptor.template) {
    try {
      const result = compileTemplate({
        source: descriptor.template.content,
        filename: filePath,
        id: 'check-docs',
      })
      problems.push(...result.errors)
    } catch (err) {
      problems.push(err)
    }
  }
  return problems
}

/** 从 Vue 编译错误对象里提取可读信息（含行号与位置）。 */
function describe(err) {
  if (typeof err === 'string') return err
  const msg = err.message || String(err)
  const loc = err.loc?.start
  const pos = loc ? ` (${loc.line}:${loc.column})` : ''
  return `${msg}${pos}`
}

/**
 * 检查站内绝对路径图片是否真实存在。
 * VitePress 把 `/xxx` 解析为 .vitepress/public/xxx，缺失时 Rollup 直接中断。
 */
function checkImages(src) {
  const problems = []
  for (const match of src.matchAll(ABS_IMAGE_RE)) {
    const url = match[1]
    if (!existsSync(join(PUBLIC_DIR, url.replace(/^\//, '')))) {
      const line = src.slice(0, match.index).split('\n').length
      problems.push(`图片路径不存在：${url} (行 ${line}，应放在 .vitepress/public 下)`)
    }
  }
  return problems
}

async function main() {
  const targets = process.argv.slice(2).map(p => join(ROOT, p))
  const files = targets.length ? targets : collect(ROOT)
  const base = await createMarkdownRenderer(ROOT, {})

  let failures = 0
  for (const file of files) {
    const rel = relative(ROOT, file).split(sep).join('/')
    const src = readFileSync(file, 'utf8').replace(/^﻿/, '')

    for (const msg of checkImages(src)) {
      console.log(`[FAIL] ${rel}: ${msg}`)
      failures++
    }

    let html
    try {
      html = base.render(src, { path: file })
    } catch (err) {
      console.log(`[FAIL] ${rel}: markdown 渲染失败 - ${describe(err)}`)
      failures++
      continue
    }

    for (const err of compileSfc(html, file)) {
      console.log(`[FAIL] ${rel}: ${describe(err)}`)
      failures++
    }
  }

  console.log(
    failures
      ? `\n发现 ${failures} 个编译问题，vitepress build 会失败。`
      : `[OK] ${files.length} 个 Markdown 文件编译校验通过`
  )
  process.exit(failures ? 1 : 0)
}

main()
