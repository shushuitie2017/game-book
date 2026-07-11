# PLAN-06 · 验收闸门（里程碑 M5，最终关）

> **前置条件**：M0–M4 全部通过。
> **本卷产出**：`tools/check_links.py` + 全部闸门的真实执行结果。**每个闸门都要真跑，把输出贴进 BUILD-LOG.md**；任何一个闸门失败就修复后重跑，全绿才算项目完成。

---

## 闸门 A：构建幂等

连续跑两遍 `python build_site.py`，两遍都退出码 0，且两遍后 `out/` 文件清单一致（用 Python 列出排序后的相对路径列表比对）。

## 闸门 B：零死链 + 链条完整（`tools/check_links.py`，照抄）

```python
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

# 1) 死链
for page in htmls:
    html = page.read_text(encoding="utf-8")
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
        errors.append(f"链条: 找不到唯一的 {cur} 页"); break
    seen.append(cur)
    html = matches[0].read_text(encoding="utf-8")
    m = re.search(r'(?s)<footer>.*?NEXT ▶.*?</footer>', html)
    href = re.search(r'<a href="([^"]+)">NEXT ▶', html)
    if not href:
        errors.append(f"链条: {cur} 页 footer 无 NEXT 链接"); break
    nxt = href.group(1)
    if nxt == "cheatsheet.html":
        break
    m2 = re.match(r"(R\d{2})-", nxt)
    if not m2:
        errors.append(f"链条: {cur} 的 NEXT 指向异常 {nxt}"); break
    cur = m2.group(1)
if len(seen) != 16:
    errors.append(f"链条: 只走过 {len(seen)} 个 R 页 {seen}")

if errors:
    print(f"FAIL: {len(errors)} 处问题"); [print(" -", e) for e in errors]; sys.exit(1)
print(f"PASS: {len(htmls)} 页零死链, R1→R16 链条完整")
```

要求输出 `PASS: 20 页零死链, R1→R16 链条完整`。

## 闸门 C：浏览器实测（chrome-devtools MCP；不可用时退路：playwright-core + 系统 Chrome `channel:'chrome'`）

前置：`python -m http.server 5031 -d out` 已在后台运行。逐项执行并记录：

| # | 操作 | 通过标准 |
|---|------|----------|
| C1 | 打开 `http://localhost:5031/` | hero、学习路径 3 卡、4 分部 16 卡、速查表入口条全部渲染；Console 无报错 |
| C2 | 点击 R1 卡片 | 跳到 `R01-teaching-elements.html`，页面样式完好，顶部导航条 sticky |
| C3 | 在 R1 页连点 3 次 footer 的 NEXT | 依次到 R2→R3→R4，标题正确 |
| C4 | 点导航条「速查表」 | 到 cheatsheet.html，16 条宣言完整，点第 7 条进 R7 |
| C5 | 回首页刷新 | R1–R4、R7 五张卡带 ✓，计数「已读 5/16」 |
| C6 | 搜索框输入 `起承转结` | 下拉含 R5（最前）与 manual 章节项；Enter 跳 R5 |
| C7 | 搜索 `热力图` 点章节级结果 | 跳转后章节标题未被导航条遮挡 |
| C8 | resize 到 390×844 | 首页单列不破版；导航条不溢出；R 页正文可读 |
| C9 | 打开 manual.html、dossier.html | 页内 TOC 锚点可跳；正文与素材原样一致 |
| C10 | 三页（index/R05/manual）各截一张图 | 目检视觉统一、无破版，截图留档 |

## 闸门 D：Lighthouse

用 chrome-devtools 的 lighthouse_audit 分别审 `http://localhost:5031/` 与 `http://localhost:5031/R05-kishotenketsu.html`：
- **SEO ≥ 95**（硬指标）。常见扣分：缺 description（回查 M1 注入）、链接不可爬、缺 h1——首页 h1 在 hero 里已有，R 页素材自带 h1。
- Performance / Accessibility 记录分数即可，不设硬线（素材页样式不许为分数而改）；但**对比度、tap target 类的站壳问题**（导航条、卡片）要修。

## 闸门 E：文件与文档

- [ ] 最终目录结构与 PLAN-00 §5 一致（外加 `src/assets/`）。
- [ ] README.md、CLAUDE.md、.gitignore、BUILD-LOG.md 齐全。
- [ ] git 工作区干净（全部提交完），提交信息无 AI 署名。

## 完成汇报（给用户的最终交付说明，写进 BUILD-LOG.md 末尾并在会话里输出）

按以下格式汇报，每条附真实证据（命令输出/截图）：

```
✅ 关卡之书 本地验收完成
- 构建：build ok, 20 pages（幂等两遍通过）
- 死链：PASS 20 页零死链，R1→R16 链条完整
- 浏览器：C1–C10 全过（附 3 张截图）
- Lighthouse SEO：index __ / R05 __
- 未做（按计划）：部署、三语化
- 遗留问题：（如有，逐条列出）
下一步建议：跑 bluecat-deploy 上线（候选 level.bluecatbot.com，换域名只需改 rules.json 的 site.base 重构建）。
```

**不许在任何闸门未真实通过的情况下写"完成"。** 测试失败就贴失败输出，标记 `[BLOCKED]` 或修复后重跑。
