#!/usr/bin/env python3
"""死链检查 + R1→R16 链条完整性。对 out/ 全量扫描。"""
import re, sys
from pathlib import Path
OUT = Path(__file__).parent.parent / "out"
errors = []

htmls = sorted(OUT.glob("*.html"))
ids_cache = {}


def ids_of(f):
    if f not in ids_cache:
        ids_cache[f] = set(re.findall(r'(?:id|name)="([^"]+)"', f.read_text(encoding="utf-8")))
    return ids_cache[f]


# 1) 死链（<script> 块内的 JS 字符串拼接易误判——先单独校验 script src，再剥块扫其余）
for page in htmls:
    html = page.read_text(encoding="utf-8")
    for src in re.findall(r'<script src="([^"]+)"', html):
        if not src.startswith(("http://", "https://")) and not (OUT / src).exists():
            errors.append(f"{page.name}: script src -> {src} (文件不存在)")
    html = re.sub(r"(?s)<script[^>]*>.*?</script>", "", html)
    for attr, val in re.findall(r'(href|src)="([^"]+)"', html):
        if val.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        target, _, frag = val.partition("#")
        tf = page if not target else OUT / target
        if target and not tf.exists():
            errors.append(f"{page.name}: {attr} -> {val} (文件不存在)")
        elif frag and tf.suffix == ".html" and tf.exists() and frag not in ids_of(tf):
            errors.append(f"{page.name}: {attr} -> {val} (锚点不存在)")

# 2) R 链条: 从 R01 沿 footer NEXT 走,必须恰好经过 16 个 R 页后到 cheatsheet
cur, seen = "R01", []
while True:
    matches = [f for f in htmls if f.name.startswith(cur + "-")]
    if len(matches) != 1:
        errors.append(f"链条: 找不到唯一的 {cur} 页")
        break
    seen.append(cur)
    html = matches[0].read_text(encoding="utf-8")
    href = re.search(r'<a href="([^"]+)">NEXT ▶', html)
    if not href:
        errors.append(f"链条: {cur} 页 footer 无 NEXT 链接")
        break
    nxt = href.group(1)
    if nxt == "cheatsheet.html":
        break
    m2 = re.match(r"(R\d{2})-", nxt)
    if not m2:
        errors.append(f"链条: {cur} 的 NEXT 指向异常 {nxt}")
        break
    cur = m2.group(1)
if len(seen) != 16:
    errors.append(f"链条: 只走过 {len(seen)} 个 R 页 {seen}")

if errors:
    print(f"FAIL: {len(errors)} 处问题")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"PASS: {len(htmls)} 页零死链, R1→R16 链条完整")
