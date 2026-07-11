#!/usr/bin/env python3
"""核对 data/rules.json 的 rule 字段与素材 .rule 块原文一致(去空白比较)。"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT / "data" / "rules.json").read_text(encoding="utf-8"))
bad = 0
for r in DATA["rules"]:
    raw = (ROOT / "src" / "content" / r["file"]).read_text(encoding="utf-8")
    m = re.search(r'(?s)<div class="rule">.*?</span>(.*?)</div>', raw)
    if not m:
        bad += 1
        print(f'[NO RULE BLOCK] {r["id"]}')
        continue
    src = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", m.group(1)))
    js = re.sub(r"\s+", "", r["rule"])
    if src != js:
        bad += 1
        print(f'[MISMATCH] {r["id"]}')
        print(f'  素材: {src}')
        print(f'  JSON: {js}')
print("all rules match" if bad == 0 else f"{bad} mismatches")
sys.exit(1 if bad else 0)
