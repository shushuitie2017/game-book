#!/usr/bin/env python3
"""关卡之书 构建器。纯标准库。用法: python build_site.py"""
import html as htmllib
import json, re, shutil, time
from pathlib import Path

ROOT = Path(__file__).parent
SRC, ASSETS, TPL, OUT = ROOT / "src" / "content", ROOT / "src" / "assets", ROOT / "templates", ROOT / "out"
DATA = json.loads((ROOT / "data" / "rules.json").read_text(encoding="utf-8"))
SITE, RULES, GROUPS, DOCS = DATA["site"], DATA["rules"], DATA["groups"], DATA["docs"]


def esc(s):  # HTML 属性安全转义
    return htmllib.escape(s, quote=True)


def truncate(s, n=155):
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------- 注入件 ----------
def seo_block(title, desc, fname):
    url = f'{SITE["base"]}/{fname}' if fname != "index.html" else SITE["base"] + "/"
    og_type = "website" if fname in ("index.html", "cheatsheet.html") else "article"
    schema_type = "WebSite" if og_type == "website" else "Article"
    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": schema_type,
        "name" if schema_type == "WebSite" else "headline": title,
        "description": truncate(desc),
        "url": url,
        **({"publisher": {"@type": "Organization", "name": SITE["name"]}} if schema_type == "Article" else {}),
    }, ensure_ascii=False)
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
        f'<meta property="og:locale" content="zh_CN">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<script type="application/ld+json">{ld}</script>\n'
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
        + a("manual.html", "手册", "manual")
        + a("index.html#rules", "规则", "rules")
        + a("dossier.html", "卷宗", "dossier")
        + a("cheatsheet.html", "速查表", "cheatsheet")
        + prev_next
        + "</div></div></nav>"
    )


def rule_prev_next(i):
    """返回 (footer替换块, 导航条prev/next块)。i 为 rules 数组下标。"""
    if i == 0:
        pf, pn, ptext = "index.html#rules", "索引", "◀ 教程索引"
    else:
        p = RULES[i - 1]
        pf, pn, ptext = p["file"], p["num"], f'◀ {p["num"]} · {p["title"]}'
    if i == len(RULES) - 1:
        nf, nn, ntext = "cheatsheet.html", "速查", "NEXT ▶ <b>速查表 · R1–R16 一句话版</b>"
    else:
        n = RULES[i + 1]
        nf, nn, ntext = n["file"], n["num"], f'NEXT ▶ <b>{n["num"]} · {n["title"]}</b>'
    footer = f'<div class="nav"><a href="{pf}">{ptext}</a><a href="{nf}">{ntext}</a></div>'
    bar = f'<a class="lb-pn" href="{pf}">◀ {pn}</a><a class="lb-pn" href="{nf}">{nn} ▶</a>'
    return footer, bar


def inject(page_html, seo, nav):
    out = page_html.replace("</head>", seo + "</head>", 1)
    out = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + nav, out, count=1)
    out = out.replace("</body>", '<script src="assets/site.js"></script>\n</body>', 1)
    return out


def add_h2_ids(page_html):
    counter = {"n": 0}

    def repl(m):
        counter["n"] += 1
        return f'<h2 id="h2-{counter["n"]}">'

    return re.sub(r"<h2>", repl, page_html)


def extract_headings(page_html):
    return [
        {"id": m.group(1), "text": re.sub(r"<[^>]+>", "", m.group(2)).strip()}
        for m in re.finditer(r'<h2 id="(h2-\d+)">(.*?)</h2>', page_html, re.S)
    ]


# ---------- 主流程 ----------
def main():
    for attempt in (1, 2):  # Windows: 预览服务占句柄时重试一次
        try:
            if OUT.exists():
                shutil.rmtree(OUT)
            break
        except OSError:
            if attempt == 2:
                raise
            time.sleep(1)
    (OUT / "assets").mkdir(parents=True)

    search_index = []

    # 1) R 页
    for i, r in enumerate(RULES):
        raw = (SRC / r["file"]).read_text(encoding="utf-8")
        page = add_h2_ids(raw)
        footer_nav, bar_pn = rule_prev_next(i)
        page, n_sub = re.subn(r'(?s)<div class="nav">.*?</div>', footer_nav, page, count=1)
        assert n_sub == 1, f'{r["file"]}: footer .nav 未找到,检查素材'
        title = f'{r["num"]} · {r["title"]} — 任天堂关卡设计教程'
        page = inject(page, seo_block(title, r["rule"], r["file"]), navbar("rules", bar_pn))
        (OUT / r["file"]).write_text(page, encoding="utf-8")
        search_index.append(
            {"file": r["file"], "num": r["num"], "title": r["title"],
             "subtitle": r["subtitle"], "rule": r["rule"],
             "headings": extract_headings(page)}
        )

    # 2) 卷宗页(manual/dossier): 不动 h2、不动 footer,只注入
    for d in DOCS:
        raw = (SRC / d["file"]).read_text(encoding="utf-8")
        title = f'{d["title"]} · {d["subtitle"]}'
        desc = f'{d["title"]}——{d["subtitle"]}。{SITE["description"]}'
        page = inject(raw, seo_block(title, desc, d["file"]), navbar(d["id"]))
        (OUT / d["file"]).write_text(page, encoding="utf-8")
        search_index.append(
            {"file": d["file"], "num": "卷宗", "title": d["title"],
             "subtitle": d["subtitle"], "rule": "",
             "headings": [{"id": f"s{j + 1}", "text": t} for j, t in enumerate(d["sections"])]}
        )

    # 3) 首页与速查表(模板渲染)
    by_group = {g["id"]: [r for r in RULES if r["group"] == g["id"]] for g in GROUPS}
    sections_html = ""
    for g in GROUPS:
        cards = "".join(
            f'<a class="rcard" href="{r["file"]}" data-id="{r["id"]}">'
            f'<span class="rnum">{r["num"]}</span><span class="rtick">✓</span>'
            f'<h4>{r["title"]}</h4><p>{r["subtitle"]}</p></a>'
            for r in by_group[g["id"]]
        )
        sections_html += (
            f'<section class="rgroup" id="g-{g["id"]}">'
            f'<div class="ghead"><span class="gno">{g["no"]}</span>'
            f'<h3>{g["label"]}<em>{g["motto"]}</em></h3></div>'
            f'<div class="rgrid">{cards}</div></section>'
        )
    cheat_list = "".join(
        f'<li><a href="{r["file"]}"><b>{r["num"]} · {r["title"]}</b><span>{r["rule"]}</span></a></li>'
        for r in RULES
    )

    for tpl_name, subs in (
        ("index.html", {"{{NAVBAR}}": navbar("index"), "{{RULES_SECTIONS}}": sections_html}),
        ("cheatsheet.html", {"{{NAVBAR}}": navbar("cheatsheet"), "{{CHEAT_LIST}}": cheat_list}),
    ):
        page = (TPL / tpl_name).read_text(encoding="utf-8")
        for k, v in subs.items():
            page = page.replace(k, v)
        title = ("关卡之书 · 任天堂关卡设计教程" if tpl_name == "index.html"
                 else "速查表 · 16 条规则一句话版 — 关卡之书")
        page = page.replace("</head>", seo_block(title, SITE["description"], tpl_name) + "</head>", 1)
        (OUT / tpl_name).write_text(page, encoding="utf-8")

    # 4) 搜索索引 / sitemap / robots / assets
    (OUT / "assets" / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, indent=1), encoding="utf-8")
    pages = ["index.html", "cheatsheet.html"] + [d["file"] for d in DOCS] + [r["file"] for r in RULES]
    urls = "".join(
        f'<url><loc>{SITE["base"]}/{p if p != "index.html" else ""}</loc></url>' for p in pages)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f'User-agent: *\nAllow: /\nSitemap: {SITE["base"]}/sitemap.xml\n', encoding="utf-8")
    for f in ASSETS.iterdir():
        shutil.copy2(f, OUT / "assets" / f.name)

    print(f"build ok: {len(pages)} pages, {len(search_index)} search entries")


if __name__ == "__main__":
    main()
