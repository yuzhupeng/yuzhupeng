"""以 git 已提交内容模拟 CI 的文件扫描，验证索引收录是否完整。

本地 Windows 有 NTFS 非法文件名被 sparse-checkout 排除（如含双引号的
「底层机制——原生家庭如何"写入"性格.md」），本地 rglob 扫不到，但 CI
在 Linux 上能扫到并自动插入索引。用 git ls-tree 取提交内容可以提前
复现 CI 的结果，避免线上出现低质自动行。
"""
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts"}
EXCLUDE_ROOT = {"README.md", "index.md", "索引.md", "Claude.md"}


def normalize(link: str) -> str:
    s = urllib.parse.unquote(link).replace("\\", "/").lstrip("./").lstrip("/")
    return re.sub(r"\.md$", "", s, flags=re.I).lower()


def main() -> int:
    index_text = (ROOT / "索引.md").read_text(encoding="utf-8")
    links = {normalize(m.group(1)) for m in re.finditer(r"\]\(([^)]+\.md)\)", index_text, re.I)}

    out = subprocess.run(
        # core.quotePath=false：否则 git 会把中文文件名输出成 C 风格八进制转义，
        # 导致所有中文路径匹配不上，检查结果恒为「全部收录」而失去意义。
        ["git", "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", "HEAD"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    ).stdout
    docs = []
    for p in out.splitlines():
        if not p.lower().endswith(".md"):
            continue
        if any(part in EXCLUDE_DIRS for part in p.split("/")[:-1]):
            continue
        if "/" not in p and p in EXCLUDE_ROOT:
            continue
        docs.append(p)

    missing = [p for p in docs if normalize(p) not in links]
    print(f"CI 视角内容文档：{len(docs)} 篇 | 索引收录：{len(docs) - len(missing)}")
    if missing:
        print(f"\n未收录（{len(missing)} 篇，CI 会自动插入低质行，建议手工补）：")
        for p in missing:
            print(f"  - {p}")
        return 1
    print("\n[OK] 索引已覆盖 CI 可见的全部文档")
    return 0


if __name__ == "__main__":
    sys.exit(main())
