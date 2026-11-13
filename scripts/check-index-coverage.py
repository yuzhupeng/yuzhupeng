"""检查哪些文档还没被 索引.md 或侧边栏收录。

新增 Markdown 后运行，输出未收录清单，便于补齐摘要与导航。

用法：
    python scripts/check-index-coverage.py
退出码：0 全部收录，1 存在遗漏（方便接入 CI 作提示）
"""
import io
import re
import sys
import urllib.parse
from pathlib import Path

# Windows 控制台默认 GBK，中文/emoji 会报错，统一切 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "索引.md"
CONFIG_FILE = ROOT / ".vitepress" / "config.mts"

EXCLUDE_DIRS = {"node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts"}
# 根级系统文件不算内容文档（Claude.md 是 Claude Code 项目配置）
EXCLUDE_ROOT_FILES = {"README.md", "index.md", "索引.md", "Claude.md"}


def content_docs() -> dict[str, str]:
    """返回 {小写相对路径: 真实相对路径}。"""
    docs = {}
    for f in ROOT.rglob("*.md"):
        if any(part in EXCLUDE_DIRS for part in f.relative_to(ROOT).parts):
            continue
        rel = f.relative_to(ROOT).as_posix()
        if f.parent == ROOT and f.name in EXCLUDE_ROOT_FILES:
            continue
        docs[rel.lower()] = rel
    return docs


def normalize(link: str) -> str:
    """去掉 URL 编码、反斜杠、前后斜杠与 .md 后缀，便于比对。

    注意：不 strip 尾部空格——文件名本身可能以空格结尾
    （如 "Loop Engineering .md"），链接必须完全一致才不会 404。
    """
    s = urllib.parse.unquote(link).replace("\\", "/").lstrip("./").lstrip("/")
    return re.sub(r"\.md$", "", s, flags=re.I).lower()


def index_links() -> set[str]:
    text = INDEX_FILE.read_text(encoding="utf-8")
    return {normalize(m.group(1)) for m in re.finditer(r"\]\(([^)]+\.md)\)", text, re.I)}


def sidebar_links() -> set[str]:
    text = CONFIG_FILE.read_text(encoding="utf-8")
    return {normalize(m.group(1)) for m in re.finditer(r'link:\s*"([^"]+)"', text)}


def main() -> int:
    docs = content_docs()
    idx = index_links()
    nav = sidebar_links()

    missing_index = sorted(v for k, v in docs.items() if normalize(k) not in idx)
    missing_nav = sorted(v for k, v in docs.items() if normalize(k) not in nav)

    def report(title: str, items: list[str]):
        if items:
            print(f"\n{title}（{len(items)} 篇）：")
            for p in items:
                print(f"  - {p}")
        else:
            print(f"\n{title}：无")

    print(f"内容文档 {len(docs)} 篇 | 索引收录 {len(docs) - len(missing_index)} | 侧边栏收录 {len(docs) - len(missing_nav)}")
    report("索引.md 未收录", missing_index)
    report("侧边栏未收录", missing_nav)

    if missing_index or missing_nav:
        print("\n补齐方式：在 索引.md 对应小节加一行表格，在 config.mts 对应分组加一条 link。")
        return 1
    print("\n[OK] 全部文档已收录")
    return 0


if __name__ == "__main__":
    sys.exit(main())
