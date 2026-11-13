"""更新 索引.md 头部的统计信息（文档数与最后更新日期）。

口径说明：
- 只统计「内容文档」，排除系统文件（README/index/索引）、隐藏目录与脚本目录。
- 日期取最新的文档修改时间，而非构建时间——CI 上拿到的 git checkout
  时间戳不可靠，所以优先用 git 记录的最后提交日期，回退到文件 mtime。

用法：
    python scripts/update-index-stats.py
"""
import re
import subprocess
from datetime import date
from pathlib import Path

root = Path(__file__).resolve().parent.parent
index_file = root / "索引.md"

# 排除目录：依赖、构建产物、工具配置
EXCLUDE_DIRS = {
    "node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts",
}
# 排除的根级系统文件：它们不是知识库内容
EXCLUDE_ROOT_FILES = {"README.md", "index.md", "索引.md"}


def is_content_doc(path: Path) -> bool:
    """判断是否为知识库正文文档。"""
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    if path.parent == root and path.name in EXCLUDE_ROOT_FILES:
        return False
    return True


def last_update_date(docs: list[Path]) -> str:
    """取「最近一次内容变更」的日期。

    优先用 git 记录的仓库最后提交日期；但本地新增文件尚未提交时，
    git 日期会落后于实际内容，所以再与文档的最大修改时间取较大者。
    只取 mtime 不可靠（CI checkout 会刷新所有文件时间），故两者取 max。
    """
    candidates = []
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            candidates.append(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    newest_mtime = max((f.stat().st_mtime for f in docs), default=None)
    if newest_mtime is not None:
        candidates.append(date.fromtimestamp(newest_mtime).isoformat())

    return max(candidates) if candidates else date.today().isoformat()


docs = [f for f in root.rglob("*.md") if is_content_doc(f)]
count = len(docs)

# 日期取 git 提交日期与文档最新 mtime 的较大者（CI 环境 mtime 会被 checkout 刷新）
updated = last_update_date(docs)

content = index_file.read_text(encoding="utf-8")
new_header = f"> 最后更新：{updated} | 共收录 {count} 篇 Markdown 文档"
content, replaced = re.subn(
    r"> 最后更新：\d{4}-\d{2}-\d{2} \| 共收录 \d+ 篇 Markdown 文档",
    new_header,
    content,
    count=1,
)

if not replaced:
    raise SystemExit("[FAIL] 索引.md 头部统计行格式不匹配，未做任何修改")

index_file.write_text(content, encoding="utf-8")
print(f"[OK] 索引已更新：{updated}，{count} 篇")
