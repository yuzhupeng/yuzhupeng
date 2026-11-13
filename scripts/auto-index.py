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
    "AI与ClaudeCode": "## B.",
    "技术开发": "## C.",
    "健康养生": "## D.",
    "投资财务": "## E.",
    "其他": "## F.",
    "book": "## A.",
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
    """取首个有效正文段落作为摘要（去 markdown 标记、截断）。

    仅在 --auto-summary 时使用；默认留占位符，因为机摘质量不足以直接发布。
    """
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">", "|", "-", "*", "!", "`", "---")):
            continue
        s = re.sub(r"[*_`\[\]]", "", s)
        s = re.sub(r"\([^)]*\)", "", s)
        return s[:45]
    return ""


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
    """把 row 插到指定分区的最后一行表格之后。"""
    start = text.find(section_prefix)
    if start < 0:
        return text, False
    nxt = text.find("\n## ", start + 1)
    end = nxt if nxt > 0 else len(text)
    block = text[start:end]

    # 找该分区最后一条表格行
    rows = list(re.finditer(r"^\| \[.*\|\s*$", block, re.M))
    if not rows:
        return text, False
    last = rows[-1]
    insert_at = start + last.end()
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
