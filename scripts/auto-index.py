"""把未收录的 Markdown 自动插入 索引.md。

按顶层目录映射到索引分区，标题取文件首个 H1（回退文件名），摘要取首个
有效正文段落（限长），关键词留空由人工补。

设计取舍：
- 摘要与关键词无法可靠自动生成（实测机摘质量差），因此默认填写
  「（待补充摘要）」占位符，人工补一句话即可，避免低质内容混进索引。
- 已收录的文档不会被改动，可反复运行（幂等）。
- 文件名尾部空格的链接必须保留空格，否则 404。

用法：
    python scripts/auto-index.py            # 预览将要插入的内容
    python scripts/auto-index.py --write    # 实际写入 索引.md
"""
import io
import re
import sys
import urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "索引.md"

EXCLUDE_DIRS = {"node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts"}
EXCLUDE_ROOT_FILES = {"README.md", "index.md", "索引.md", "Claude.md"}

# 顶层目录 → 索引分区标题前缀
SECTION_BY_DIR = {
    "个人成长": "## A.",
    "心理学": "## A.",
    "book": "## A.",
    "AI与ClaudeCode": "## B.",
    "技术开发": "## C.",
    "健康养生": "## D.",
    "投资财务": "## E.",
    "其他": "## F.",
    "Vedio": "## F.",
    "": "## F.",  # 根目录文档归入杂项
}

PLACEHOLDER_SUMMARY = "（待补充：一句话说明这篇讲了什么）"
PLACEHOLDER_KEYWORDS = "`待补充`"


def content_docs() -> dict[str, Path]:
    docs = {}
    for f in ROOT.rglob("*.md"):
        parts = f.relative_to(ROOT).parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if len(parts) == 1 and parts[0] in EXCLUDE_ROOT_FILES:
            continue
        docs[f.relative_to(ROOT).as_posix().lower()] = f
    return docs


def normalize(link: str) -> str:
    s = urllib.parse.unquote(link).replace("\\", "/").lstrip("./").lstrip("/")
    return re.sub(r"\.md$", "", s, flags=re.I).lower()


def linked_paths() -> set[str]:
    text = INDEX_FILE.read_text(encoding="utf-8")
    return {normalize(m.group(1)) for m in re.finditer(r"\]\(([^)]+\.md)\)", text, re.I)}


def doc_title(path: Path) -> str:
    """取首个一级标题（# ）。"""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip() or path.stem.strip()
    return path.stem.strip()


def first_paragraph(path: Path) -> str:
    """提取摘要：优先用文章自带「摘要」小节里最能概括全篇的一句。

    策略：在「摘要」小节内，优先选含「本文/整理/总结/共/分为/介绍」等
    概括性词汇的段落（通常在小节末尾），否则取该小节首段。
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""

    summary_start = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*#{1,3}\s*摘要\s*$", line):
            summary_start = i + 1
            break

    if summary_start is not None:
        paragraphs = []
        buf = []
        for line in lines[summary_start:]:
            s = line.strip()
            # 遇到任何标题都必须无条件中断：摘要小节与下一小节之间通常正好
            # 隔一个空行，此时 buf 已被清空，若要求 buf 非空才 break，
            # 标题本身就会被当成正文收集进去，进而扫到正文各节取错段落。
            if re.match(r"^#{1,6}\s", s):
                break
            if not s:
                if buf:
                    paragraphs.append(" ".join(buf))
                    buf = []
                continue
            if s.startswith(">"):
                continue  # 跳过引用块
            buf.append(s)
        if buf:
            paragraphs.append(" ".join(buf))

        if paragraphs:
            keywords = ("本文", "整理", "总结", "共", "分为", "介绍", "阐述")
            for para in reversed(paragraphs):
                cleaned = cleanup(para)
                if any(k in cleaned for k in keywords) and 15 <= len(cleaned):
                    return first_sentence(cleaned)
            return first_sentence(cleanup(paragraphs[0]))

    # 回退：首个像自然语言的正文段落（跳过标题/引用/表格/列表/图片/代码注释）
    for line in lines:
        s = line.strip()
        if not s or s.startswith(("#", ">", "|", "-", "*", "+", "!", "`", "---", "//", "<!--")):
            continue
        # 纯英文短词、URL、代码片段都不适合做摘要
        if len(s) < 15 or " " not in s and len(s) < 25:
            continue
        if re.match(r"^(https?://|www\.)", s):
            continue
        return first_sentence(cleanup(s))
    return ""


def cleanup(text: str) -> str:
    """去掉 markdown 强调/链接标记，压成一行。"""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def first_sentence(text: str, limit: int = 60) -> str:
    """取首句，让自动摘要与人工撰写的索引行长度接近。

    首句长度合适（10~limit 字）就用首句，否则硬截断到 limit 字。
    """
    m = re.match(r"^(.{10,%d}?[。！？!?])" % limit, text)
    if m:
        return m.group(1)
    return text[:limit]


def url_encode(rel: str) -> str:
    """按现有索引风格编码链接：只把空格和 markdown 敏感字符转义，中文保持原样。"""
    return (
        rel.replace("%", "%25")
        .replace(" ", "%20")
        .replace("(", "%28")
        .replace(")", "%29")
        .replace("|", "%7C")
    )


def section_of(rel: str) -> str:
    top = rel.split("/")[0] if "/" in rel else ""
    return SECTION_BY_DIR.get(top, "## F.")


def insert_into_section(text: str, section_prefix: str, row: str) -> tuple[str, bool]:
    """把 row 插到指定分区「最后一张表的最后一行」之后。

    注意：连续表格行之间不能有空行，否则 Markdown 会把该行当成普通段落。
    因此正则的尾部空白只允许空格/制表符，绝不能用 \\s（会吞掉换行，
    导致插入点落到空行之后、表格被截断）。
    """
    start = text.find(section_prefix)
    if start < 0:
        return text, False
    nxt = text.find("\n## ", start + 1)
    end = nxt if nxt > 0 else len(text)
    block = text[start:end]

    rows = list(re.finditer(r"^\|.*\|[ \t]*$", block, re.M))
    if not rows:
        return text, False

    # 从末尾向前找「连续的表格块」：最后一行往上，直到遇到空行或非表格行
    last_idx = len(rows) - 1
    first_in_block = last_idx
    while first_in_block > 0:
        prev_end = rows[first_in_block - 1].end()
        gap = block[prev_end:rows[first_in_block].start()]
        if gap.strip():
            break
        first_in_block -= 1

    insert_at = start + rows[last_idx].end()
    return text[:insert_at] + "\n" + row + text[insert_at:], True


def main() -> int:
    write = "--write" in sys.argv
    auto_summary = "--auto-summary" in sys.argv
    docs = content_docs()
    done = linked_paths()
    missing = sorted(
        (p.relative_to(ROOT).as_posix(), p)
        for k, p in docs.items()
        if normalize(k) not in done
    )

    if not missing:
        print("[OK] 索引已包含全部文档，无需插入")
        return 0

    print(f"发现 {len(missing)} 篇未收录，将插入：\n")
    text = INDEX_FILE.read_text(encoding="utf-8")
    inserted = 0
    for rel, path in missing:
        title = doc_title(path)
        enc = url_encode(rel)
        if auto_summary:
            summary = first_paragraph(path) or PLACEHOLDER_SUMMARY
        else:
            summary = PLACEHOLDER_SUMMARY
        row = f"| [{title}]({enc}) | {summary} | {PLACEHOLDER_KEYWORDS} |"
        sec = section_of(rel)
        text, ok = insert_into_section(text, sec, row)
        status = "OK " if ok else "MISS"
        print(f"[{status}] {sec} <- {rel}")
        inserted += 1 if ok else 0

    if write:
        INDEX_FILE.write_text(text, encoding="utf-8")
        print(f"\n[WRITE] 已写入 {inserted} 行到 索引.md，请补全摘要与关键词")
    else:
        print(f"\n[DRY-RUN] 共 {inserted} 行待写入。确认后运行 --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
