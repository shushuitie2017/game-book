# PLAN-02 · 工程骨架与构建流水线（里程碑 M1）

> **前置条件**：M0 全部自检通过（`src/content/` 18 文件 + `data/rules.json` 就位）。
> **本卷产出**：`build_site.py`、`tools/verify_rules.py`，以及一次成功构建出的 `out/`。
> 本卷代码是**参考实现**：允许修 bug，但文件名、函数职责、注入锚点、数据结构不许改（后续卷依赖）。模板文件 `templates/index.html`、`templates/cheatsheet.html` 与 `src/assets/*` 在 M2（PLAN-03/04）才写全——**M1 阶段先放最小占位版**（本卷 §5 给出），保证流水线端到端跑通，M2 再替换成正式版。

---

## 1. 构建总流程（build_site.py 做的事，按序）

1. 读 `data/rules.json`。
2. 清空并重建 `out/` 与 `out/assets/`。
3. **处理 18 个内容页**（`src/content/*.html` → `out/`），每页做且只做这些机械注入：
   - `</head>` 前插入：SEO 块（description/canonical/favicon/OG，字符串规则见 PLAN-05 §1）+ `<link rel="stylesheet" href="assets/site.css">`；
   - `<body>` 后插入：统一导航条（§3）；
   - `</body>` 前插入：`<script src="assets/site.js"></script>`；
   - **仅 R 页**：给无属性的 `<h2>` 依序补 `id="h2-1"、"h2-2"…`；把 footer 里的 `<div class="nav">…</div>`（纯文本）替换为真实链接（§4）。
4. 渲染 `templates/index.html`、`templates/cheatsheet.html`（替换 `{{...}}` 占位符）→ `out/`。
5. 生成 `out/assets/search-index.json`（结构见 PLAN-04 §1）。
6. 生成 `out/sitemap.xml`、`out/robots.txt`（20 个 URL：index、cheatsheet、manual、dossier、R01–R16）。
7. 复制 `src/assets/` 下所有文件到 `out/assets/`。
8. 打印统计（页数、索引条目数）并以退出码 0 结束；任何一步异常直接抛出（fail loud，不静默兜底）。

## 2. 目录补充约定

- 站壳静态资产放 `src/assets/`（`site.css`、`site.js`、`favicon.svg`，M4 再加 `og-cover.png`），构建时原样拷到 `out/assets/`。
- `out/` 每次构建整体重建，**任何手工修改都会丢**——所以永远改源（src/templates/data），跑构建，看产物。
- Windows 坑：如果 `python -m http.server` 正开着服务 `out/`，`shutil.rmtree` 可能因文件句柄失败。构建前先停预览服务；若仍失败，重试一次再报错。

## 3. 导航条注入（所有 20 页统一）

紧跟 `<body>` 之后插入（`{...}` 为构建器填充）：

```html
<nav class="lb-bar"><div class="lb-in">
  <a class="lb-brand" href="index.html"><span class="lb-mark">関</span>关卡之书</a>
  <div class="lb-links">
    <a href="manual.html">手册</a>
    <a href="index.html#rules">规则</a>
    <a href="dossier.html">卷宗</a>
    <a href="cheatsheet.html">速查表</a>
    {PREV_NEXT}
  </div>
</div></nav>
```

- 当前页对应的链接加 class `on`（manual 页高亮"手册"，R 页高亮"规则"，以此类推；index 不高亮任何项）。
- `{PREV_NEXT}` 仅 R 页有：`<a class="lb-pn" href="{prev_file}">◀ {prev_num}</a><a class="lb-pn" href="{next_file}">{next_num} ▶</a>`，其中 R01 的 prev 指 `index.html#rules` 文字 `◀ 索引`，R16 的 next 指 `cheatsheet.html` 文字 `速查 ▶`；其余按 `rules` 数组相邻推导（prev_num/next_num 用 `num` 字段如 `R4`）。
- 导航条样式在 `site.css` 里全部自带硬编码色值（素材页 CSS 变量名不统一，**不得依赖页面变量**），见 PLAN-03 §3。

## 4. R 页 footer 导航替换

R 页 footer 里现存块形如（纯文本，无链接——这是素材的真实现状）：

```html
<div class="nav">
  <span>◀ R4 · 参数教学</span>
  <span>NEXT ▶ <b>R6 · 结尾段复杂度回落:炫技谢幕</b></span>
</div>
```

用正则 `(?s)<div class="nav">.*?</div>`（count=1）整块替换为：

```html
<div class="nav">
  <a href="{prev_file}">◀ {prev_num} · {prev_title}</a>
  <a href="{next_file}">NEXT ▶ <b>{next_num} · {next_title}</b></a>
</div>
```

端点：R01 prev → `index.html#rules` / `◀ 教程索引`；R16 next → `cheatsheet.html` / `NEXT ▶ <b>速查表 · R1–R16 一句话版</b>`。标题用 rules.json 的 `title` 字段（不必复刻原 span 里的长句）。`.nav a` 的样式由 site.css 提供。

## 5. M1 最小占位模板（M2 会整体替换）

`templates/index.html`（占位版，能通链接即可）：

```html
<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>关卡之书 · 任天堂关卡设计教程</title></head><body>
{{NAVBAR}}
<main style="max-width:880px;margin:0 auto;padding:40px 26px;color:#d8d2c4;background:#0d0f12">
<h1>关卡之书（占位首页）</h1>
<p><a href="manual.html">手册</a> · <a href="dossier.html">卷宗</a> · <a href="cheatsheet.html">速查表</a></p>
<div id="rules">{{RULES_SECTIONS}}</div>
</main>
<script src="assets/site.js"></script></body></html>
```

`templates/cheatsheet.html`（占位版）：

```html
<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>速查表 · 关卡之书</title></head><body>
{{NAVBAR}}
<main style="max-width:880px;margin:0 auto;padding:40px 26px;color:#d8d2c4;background:#0d0f12">
<h1>速查表（占位）</h1><ol>{{CHEAT_LIST}}</ol>
</main>
<script src="assets/site.js"></script></body></html>
```

`src/assets/site.css` 与 `site.js` 的 M1 占位：建空文件即可（M2/M3 填正式内容）。

## 6. `build_site.py` 参考实现

```python
#!/usr/bin/env python3
"""关卡之书 构建器。纯标准库。用法: python build_site.py"""
import html as htmllib
import json, re, shutil, sys, time
from pathlib import Path

ROOT = Path(__file__).parent
SRC, ASSETS, TPL, OUT = ROOT/"src"/"content", ROOT/"src"/"assets", ROOT/"templates", ROOT/"out"
DATA = json.loads((ROOT/"data"/"rules.json").read_text(encoding="utf-8"))
SITE, RULES, GROUPS, DOCS = DATA["site"], DATA["rules"], DATA["groups"], DATA["docs"]

def esc(s):  # HTML 属性安全转义
    return htmllib.escape(s, quote=True)

def truncate(s, n=155):
    return s if len(s) <= n else s[:n-1] + "…"

# ---------- 注入件 ----------
def seo_block(title, desc, fname):
    url = f'{SITE["base"]}/{fname}' if fname != "index.html" else SITE["base"] + "/"
    og_type = "website" if fname in ("index.html", "cheatsheet.html") else "article"
    return (
        f'<meta name="description" content="{esc(truncate(desc))}">\n'
        f'<link rel="canonical" href="{url}">\n'
        f'<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(truncate(desc))}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{SITE["base"]}/assets/og-cover.png">\n'
        f'<meta property="og:site_name" content="{esc(SITE["name"])}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<link rel="stylesheet" href="assets/site.css">\n'
    )

def navbar(current, prev_next=""):
    def a(href, label, key):
        cls = ' class="on"' if key == current else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    return (
        '<nav class="lb-bar"><div class="lb-in">'
        '<a class="lb-brand" href="index.html"><span class="lb-mark">関</span>关卡之书</a>'
        '<div class="lb-links">'
        + a("manual.html", "手册", "manual") + a("index.html#rules", "规则", "rules")
        + a("dossier.html", "卷宗", "dossier") + a("cheatsheet.html", "速查表", "cheatsheet")
        + prev_next + "</div></div></nav>"
    )

def rule_prev_next(i):
    """返回 (footer替换块, 导航条prev/next块)。i 为 rules 数组下标。"""
    if i == 0:
        pf, pn, pt = "index.html#rules", "索引", "教程索引"
    else:
        p = RULES[i-1]; pf, pn, pt = p["file"], p["num"], p["title"]
    if i == len(RULES) - 1:
        nf, nn, nt = "cheatsheet.html", "速查", "速查表 · R1–R16 一句话版"
    else:
        n = RULES[i+1]; nf, nn, nt = n["file"], n["num"], n["title"]
    footer = (f'<div class="nav"><a href="{pf}">◀ {pn if i==0 else pn + " · " + pt}</a>'
              f'<a href="{nf}">NEXT ▶ <b>{(nn + " · " + nt) if i < len(RULES)-1 else nt}</b></a></div>')
    bar = f'<a class="lb-pn" href="{pf}">◀ {pn}</a><a class="lb-pn" href="{nf}">{nn} ▶</a>'
    return footer, bar

def inject(page_html, seo, nav):
    out = page_html.replace("</head>", seo + "</head>", 1)
    out = re.sub(r"(<body[^>]*>)", r"\1\n" + nav.replace("\\", r"\\"), out, count=1)
    out = out.replace("</body>", '<script src="assets/site.js"></script>\n</body>', 1)
    return out

def add_h2_ids(page_html):
    counter = {"n": 0}
    def repl(m):
        counter["n"] += 1
        return f'<h2 id="h2-{counter["n"]}">'
    return re.sub(r"<h2>", repl, page_html)

def extract_headings(page_html):
    return [{"id": m.group(1), "text": re.sub(r"<[^>]+>", "", m.group(2)).strip()}
            for m in re.finditer(r'<h2 id="(h2-\d+)">(.*?)</h2>', page_html, re.S)]

# ---------- 主流程 ----------
def main():
    for attempt in (1, 2):  # Windows: 预览服务占句柄时重试一次
        try:
            if OUT.exists(): shutil.rmtree(OUT)
            break
        except OSError:
            if attempt == 2: raise
            time.sleep(1)
    (OUT/"assets").mkdir(parents=True)

    search_index = []

    # 1) R 页
    for i, r in enumerate(RULES):
        raw = (SRC/r["file"]).read_text(encoding="utf-8")
        page = add_h2_ids(raw)
        footer_nav, bar_pn = rule_prev_next(i)
        page, n_sub = re.subn(r'(?s)<div class="nav">.*?</div>', footer_nav, page, count=1)
        assert n_sub == 1, f'{r["file"]}: footer .nav 未找到,检查素材'
        title = f'{r["num"]} · {r["title"]} — 任天堂关卡设计教程'
        page = inject(page, seo_block(title, r["rule"], r["file"]), navbar("rules", bar_pn))
        (OUT/r["file"]).write_text(page, encoding="utf-8")
        search_index.append({"file": r["file"], "num": r["num"], "title": r["title"],
                             "subtitle": r["subtitle"], "rule": r["rule"],
                             "headings": extract_headings(page)})

    # 2) 卷宗页(manual/dossier): 不动 h2、不动 footer,只注入
    for d in DOCS:
        src_name = "nintendo-level-design-manual.html" if d["id"] == "manual" else "nintendo-dev-dossier.html"
        # M0 已把它们改名入库,直接按目标名读:
        raw = (SRC/d["file"]).read_text(encoding="utf-8")
        title = f'{d["title"]} · {d["subtitle"]}'
        page = inject(raw, seo_block(title, f'{d["title"]}——{d["subtitle"]}。{SITE["description"]}', d["file"]),
                      navbar(d["id"]))
        (OUT/d["file"]).write_text(page, encoding="utf-8")
        search_index.append({"file": d["file"], "num": "卷宗", "title": d["title"],
                             "subtitle": d["subtitle"], "rule": "",
                             "headings": [{"id": f"s{j+1}", "text": t} for j, t in enumerate(d["sections"])]})

    # 3) 首页与速查表(模板渲染,占位符见 PLAN-03)
    read_map = {g["id"]: [r for r in RULES if r["group"] == g["id"]] for g in GROUPS}
    sections_html = ""
    for g in GROUPS:
        cards = "".join(
            f'<a class="rcard" href="{r["file"]}" data-id="{r["id"]}">'
            f'<span class="rnum">{r["num"]}</span><span class="rtick">✓</span>'
            f'<h4>{r["title"]}</h4><p>{r["subtitle"]}</p></a>'
            for r in read_map[g["id"]])
        sections_html += (f'<section class="rgroup" id="g-{g["id"]}">'
                          f'<div class="ghead"><span class="gno">{g["no"]}</span>'
                          f'<h3>{g["label"]}<em>{g["motto"]}</em></h3></div>'
                          f'<div class="rgrid">{cards}</div></section>')
    cheat_list = "".join(
        f'<li><a href="{r["file"]}"><b>{r["num"]} · {r["title"]}</b><span>{r["rule"]}</span></a></li>'
        for r in RULES)

    for tpl_name, subs in (
        ("index.html", {"{{NAVBAR}}": navbar("index"), "{{RULES_SECTIONS}}": sections_html}),
        ("cheatsheet.html", {"{{NAVBAR}}": navbar("cheatsheet"), "{{CHEAT_LIST}}": cheat_list}),
    ):
        page = (TPL/tpl_name).read_text(encoding="utf-8")
        for k, v in subs.items():
            page = page.replace(k, v)
        title = ("关卡之书 · 任天堂关卡设计教程" if tpl_name == "index.html"
                 else "速查表 · 16 条规则一句话版 — 关卡之书")
        page = page.replace("</head>", seo_block(title, SITE["description"], tpl_name) + "</head>", 1)
        (OUT/tpl_name).write_text(page, encoding="utf-8")

    # 4) 搜索索引 / sitemap / robots / assets
    (OUT/"assets"/"search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, indent=1), encoding="utf-8")
    pages = ["index.html", "cheatsheet.html"] + [d["file"] for d in DOCS] + [r["file"] for r in RULES]
    urls = "".join(f'<url><loc>{SITE["base"]}/{p if p != "index.html" else ""}</loc></url>' for p in pages)
    (OUT/"sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        encoding="utf-8")
    (OUT/"robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE["base"]}/sitemap.xml\n', encoding="utf-8")
    for f in ASSETS.iterdir():
        shutil.copy2(f, OUT/"assets"/f.name)

    print(f'build ok: {len(pages)} pages, {len(search_index)} search entries')

if __name__ == "__main__":
    main()
```

**实现注意**：
- `inject()` 里 navbar 经 `re.sub` 作为替换串时，反斜杠/`\g` 序列会被解释——参考实现里已用 `.replace("\\", r"\\")` 防御；更稳的写法是用 `lambda m: m.group(1) + "\n" + nav`，允许你改成后者。
- 所有 `read_text/write_text` 必须带 `encoding="utf-8"`（Windows 默认 GBK，不带必坏）。
- `assert n_sub == 1`：footer 替换失败要炸出来，不许静默。

## 7. `tools/verify_rules.py`（防数据漂移：JSON 里的宣言必须与素材原文一致）

```python
#!/usr/bin/env python3
"""核对 data/rules.json 的 rule 字段与素材 .rule 块原文一致(去空白比较)。"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
DATA = json.loads((ROOT/"data"/"rules.json").read_text(encoding="utf-8"))
bad = 0
for r in DATA["rules"]:
    raw = (ROOT/"src"/"content"/r["file"]).read_text(encoding="utf-8")
    m = re.search(r'(?s)<div class="rule">.*?</span>(.*?)</div>', raw)
    src = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", m.group(1)))
    js = re.sub(r"\s+", "", r["rule"])
    if src != js:
        bad += 1
        print(f'[MISMATCH] {r["id"]}\n  素材: {src[:80]}...\n  JSON: {js[:80]}...')
print("all rules match" if bad == 0 else f"{bad} mismatches")
sys.exit(1 if bad else 0)
```

**若报 MISMATCH：以素材为准修改 rules.json**（引号形态、标点等以素材原文为唯一真相），改完重跑直到 `all rules match`。

## 8. M1 自检清单（全过才进 M2）

- [ ] `python tools/verify_rules.py` 输出 `all rules match`，退出码 0。
- [ ] `python build_site.py` 退出码 0，打印 `build ok: 20 pages, 18 search entries`。
- [ ] **连跑两遍**构建都成功且 `out/` 文件清单一致（幂等）。
- [ ] `out/` 下恰好：20 个 html + sitemap.xml + robots.txt + `assets/`（site.css、site.js、favicon.svg 可为空占位、search-index.json）。
- [ ] 抽查 `out/R05-kishotenketsu.html`：`<body>` 后有 `lb-bar` 导航条；footer `.nav` 里是 `<a href="R04-parameter-teaching.html">` 与 `<a href="R06-finale-flourish.html">`；h2 带 `id="h2-1"` 起的连续 id；`</head>` 前有 description/canonical/og 标签。
- [ ] 抽查 `out/R01…` 的 prev 指 `index.html#rules`、`out/R16…` 的 next 指 `cheatsheet.html`。
- [ ] 抽查 `out/manual.html`：有导航条与 SEO 头，**footer 未被改动**、正文无 h2-id 注入痕迹以外的变化。
- [ ] `python -m http.server 5031 -d out` 起服后，浏览器打开 `http://localhost:5031/R05-kishotenketsu.html` 页面渲染正常（素材样式未破坏）。
- [ ] BUILD-LOG.md 已追加 M1 记录。
