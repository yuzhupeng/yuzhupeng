"""更新 索引.md 头部统计信息（文档数和最后更新日期）"""
import re
from pathlib import Path
from datetime import date

root = Path(__file__).resolve().parent.parent
index_file = root / "索引.md"

# 统计 Markdown 文件（排除系统目录）
exclude_dirs = {"node_modules", ".git", ".vitepress", ".claude", ".vs", "scripts"}
count = 0
for f in root.rglob("*.md"):
    if not any(p in f.parts for p in exclude_dirs):
        count += 1

today = date.today().isoformat()
content = index_file.read_text(encoding="utf-8")

# 替换头部行
new_header = f"> 最后更新：{today} | 共收录 {count} 篇 Markdown 文档\n"
content = re.sub(
    r"> 最后更新：\d{4}-\d{2}-\d{2} \| 共收录 \d+ 篇 Markdown 文档",
    new_header.strip(),
    content,
    count=1,
)

index_file.write_text(content, encoding="utf-8")
print(f"[OK] 索引已更新：{today}，{count} 篇")
