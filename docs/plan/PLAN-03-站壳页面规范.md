# PLAN-03 · 站壳页面规范：首页 / 速查表 / 导航条（里程碑 M2）

> **前置条件**：M1 全部自检通过（占位模板已能端到端构建）。
> **本卷产出**：正式版 `templates/index.html`、`templates/cheatsheet.html`、`src/assets/site.css`、`src/assets/favicon.svg`。写完重跑 `python build_site.py` 并在浏览器目检。
> 本卷给出**完整文件内容**，照抄后允许微调间距/字号，但不许改设计令牌、不许引入新颜色新字体。

---

## 1. 设计令牌（全站壳唯一允许的视觉词汇，与素材一致）

| 令牌 | 值 | 用途 |
|------|----|------|
| ink | `#0d0f12` | 页面底色 |
| panel | `#1a1e25` | 卡片/面板 |
| panel2 | `#20252e` | 次级面板 |
| text | `#d8d2c4` | 正文 |
| dim | `#8a8577` | 次要文字 |
| cinnabar | `#c8442a` | 主强调（编号/关键） |
| amber | `#d9a441` | 次强调（小标题/hover） |
| teal | `#4a9a8e` | 第三强调（链接/完成态） |
| hairline | `rgba(216,210,196,.12)` | 分隔线 |
| 亮字 | `#efe9da` | 强调正文 |
| serif | `'Noto Serif SC',serif` | 标题正文 |
| mono | `'JetBrains Mono',monospace` | 编号/标注/小字距文字 |

惯用语法（沿用素材）：mono 大字距 kicker、hero 右侧巨字半透明水印（`rgba(216,210,196,.035)`）、`border-left:3px` 色条引用块、hairline 虚线分隔、`.rv` 滚动渐显（可省）。

## 2. `src/assets/favicon.svg`（照抄）

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0d0f12"/><text x="32" y="46" font-family="'Noto Serif SC',serif" font-size="38" font-weight="900" fill="#c8442a" text-anchor="middle">関</text></svg>
```

## 3. `src/assets/site.css`（照抄；被注入进所有 20 页，**只放跨页组件，全部硬编码色值**）

```css
/* ===== 关卡之书 站壳组件（导航条 + footer 链接）。不依赖页面 CSS 变量 ===== */
.lb-bar{position:sticky;top:0;z-index:99;background:rgba(13,15,18,.92);backdrop-filter:blur(8px);border-bottom:1px solid rgba(216,210,196,.12);font-family:'JetBrains Mono',monospace}
.lb-in{max-width:920px;margin:0 auto;padding:0 26px;display:flex;justify-content:space-between;align-items:center;height:46px;gap:14px}
.lb-brand{color:#d8d2c4;text-decoration:none;font-size:13px;letter-spacing:.14em;display:flex;gap:9px;align-items:center;white-space:nowrap}
.lb-brand:hover{color:#d9a441}
.lb-mark{color:#c8442a;font-weight:700;font-family:'Noto Serif SC',serif;font-size:16px}
.lb-links{display:flex;gap:16px;font-size:12px;overflow-x:auto;white-space:nowrap}
.lb-links a{color:#8a8577;text-decoration:none;letter-spacing:.08em;padding:4px 0}
.lb-links a:hover{color:#d9a441}
.lb-links a.on{color:#d8d2c4;box-shadow:0 1px 0 #c8442a}
.lb-links a.lb-pn{color:#4a9a8e}
@media(max-width:600px){.lb-in{padding:0 14px}.lb-links{gap:10px;font-size:11px}.lb-brand{font-size:12px}}

/* R 页 footer 导航被替换成 <a> 后的样式（原页面只给 span 定过样式） */
footer .nav a{color:#8a8577;text-decoration:none;font-family:'JetBrains Mono',monospace;font-size:12px}
footer .nav a b{color:#4a9a8e;font-weight:500}
footer .nav a:hover{color:#d9a441}
footer .nav a:hover b{color:#d9a441}
```

## 4. `templates/index.html` 正式版（照抄；`{{NAVBAR}}`/`{{RULES_SECTIONS}}` 由构建器替换）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>关卡之书 · 任天堂关卡设计教程</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#0d0f12;--panel:#1a1e25;--panel2:#20252e;
  --text:#d8d2c4;--dim:#8a8577;
  --cinnabar:#c8442a;--amber:#d9a441;--teal:#4a9a8e;
  --hairline:rgba(216,210,196,.12);
  --serif:'Noto Serif SC',serif;--mono:'JetBrains Mono',monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--text);font-family:var(--serif);line-height:1.9}
::selection{background:var(--cinnabar);color:#fff}
.wrap{max-width:920px;margin:0 auto;padding:0 28px}

/* hero */
.hero{min-height:72vh;display:flex;flex-direction:column;justify-content:center;position:relative;overflow:hidden;
  background:radial-gradient(1100px 560px at 82% -10%, rgba(200,68,42,.10), transparent 60%),
             radial-gradient(800px 460px at 8% 110%, rgba(74,154,142,.08), transparent 60%),var(--ink)}
.hero::after{content:"遊";position:absolute;right:-4%;top:6%;font-size:min(44vw,400px);font-weight:900;color:rgba(216,210,196,.035);line-height:1;pointer-events:none}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.35em;color:var(--amber);text-transform:uppercase;margin-bottom:20px}
.hero h1{font-size:clamp(38px,7vw,72px);font-weight:900;line-height:1.2;letter-spacing:.03em}
.hero h1 em{font-style:normal;color:var(--cinnabar)}
.hero .sub{margin-top:24px;max-width:640px;color:var(--dim);font-size:17px}
.hero .meta{margin-top:36px;font-family:var(--mono);font-size:12px;color:var(--dim);display:flex;gap:26px;flex-wrap:wrap}
.hero .meta b{color:var(--teal);font-weight:500}

/* 学习路径 */
section{padding:56px 0}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.24em;color:var(--teal);margin-bottom:10px}
h2{font-size:clamp(22px,3.4vw,30px);font-weight:900;margin-bottom:8px}
.lede{color:var(--dim);max-width:680px;margin-bottom:34px;font-size:15.5px}
.path{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:720px){.path{grid-template-columns:1fr}}
.step{display:block;background:var(--panel);border-top:3px solid var(--amber);padding:22px;text-decoration:none;color:var(--text);transition:.25s}
.step:nth-child(2){border-top-color:var(--cinnabar)}
.step:nth-child(3){border-top-color:var(--teal)}
.step:hover{background:var(--panel2);transform:translateY(-2px)}
.step .pn{font-family:var(--mono);font-size:11px;letter-spacing:.25em;color:var(--dim);margin-bottom:10px}
.step h4{font-size:17px;font-weight:700;color:#efe9da;margin-bottom:8px}
.step p{font-size:13.5px;color:var(--dim);line-height:1.85}

/* 搜索 */
.searchbox{position:relative;margin:6px 0 6px}
#q{width:100%;background:var(--panel);border:1px solid var(--hairline);color:var(--text);
  font-family:var(--serif);font-size:16px;padding:14px 18px;outline:none}
#q:focus{border-color:var(--teal)}
#results{position:absolute;left:0;right:0;top:100%;z-index:50;background:var(--panel2);border:1px solid var(--hairline);border-top:none;max-height:380px;overflow:auto;display:none}
#results a{display:block;padding:11px 18px;color:var(--text);text-decoration:none;border-bottom:1px dashed var(--hairline);font-size:14.5px}
#results a:hover,#results a.sel{background:var(--panel);color:var(--amber)}
#results a .rn{font-family:var(--mono);font-size:11px;color:var(--cinnabar);margin-right:10px}
#results a .hd{color:var(--dim);font-size:12.5px;display:block;margin-top:2px}

/* 规则网格 */
#rules{scroll-margin-top:60px}
.rgroup{margin-top:44px}
.ghead{display:flex;align-items:baseline;gap:16px;margin-bottom:18px;border-bottom:1px solid var(--hairline);padding-bottom:12px}
.gno{font-family:var(--mono);font-size:12px;letter-spacing:.2em;color:var(--cinnabar)}
.ghead h3{font-size:20px;font-weight:900}
.ghead h3 em{font-style:normal;font-family:var(--mono);font-size:12px;color:var(--dim);margin-left:14px;letter-spacing:.08em;font-weight:400}
.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.rcard{position:relative;display:block;background:var(--panel);border:1px solid var(--hairline);padding:18px 20px;text-decoration:none;color:var(--text);transition:.25s}
.rcard:hover{border-color:var(--amber);transform:translateY(-2px)}
.rnum{font-family:var(--mono);font-size:13px;color:var(--cinnabar);font-weight:700;letter-spacing:.1em}
.rtick{display:none;position:absolute;top:14px;right:16px;color:var(--teal);font-family:var(--mono);font-size:14px}
.rcard.read .rtick{display:block}
.rcard h4{font-size:17px;font-weight:700;color:#efe9da;margin:8px 0 6px}
.rcard p{font-size:13px;color:var(--dim);line-height:1.8}
.progress{font-family:var(--mono);font-size:12px;color:var(--dim);margin-left:16px}
.progress b{color:var(--teal);font-weight:500}
.rowhead{display:flex;align-items:baseline}

/* 速查表入口条 */
.cheat-cta{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-top:48px;padding:22px 26px;background:linear-gradient(135deg,rgba(200,68,42,.09),transparent 55%),var(--panel);border:1px solid rgba(200,68,42,.32);text-decoration:none}
.cheat-cta h4{color:#efe9da;font-size:16px;font-weight:700}
.cheat-cta p{color:var(--dim);font-size:13px;margin-top:4px}
.cheat-cta .go{font-family:var(--mono);color:var(--cinnabar);font-size:13px;white-space:nowrap}
.cheat-cta:hover .go{color:var(--amber)}

footer{padding:56px 0 76px;border-top:1px solid var(--hairline);margin-top:30px}
footer p{font-family:var(--mono);font-size:11.5px;color:var(--dim);line-height:2.1}
</style>
</head>
<body>
{{NAVBAR}}

<header class="hero">
  <div class="wrap">
    <div class="kicker">LEVEL BOOK — NINTENDO LEVEL DESIGN</div>
    <h1>关卡之书<em>。</em></h1>
    <p class="sub">把「社長が訊く」与 CEDEC / GDC 讲演里散落的任天堂关卡设计方法论，编成一本可执行的书——16 条规则教程 × 1 份实战手册 × 1 卷开发访谈研究。每条规则都带执行流程、模板、检查清单与反面信号。</p>
    <div class="meta">
      <span>规则 <b>R1–R16</b></span><span>卷宗 <b>2 册</b></span><span>编纂 <b>2026-07</b></span>
    </div>
  </div>
</header>

<div class="wrap">

<section id="path">
  <div class="eyebrow">HOW TO READ</div>
  <h2>学习路径</h2>
  <p class="lede">三步：先建立全景，再逐条精读，最后补思想背景。做项目时回来查速查表。</p>
  <div class="path">
    <a class="step" href="manual.html">
      <div class="pn">STEP 01 · 总纲</div>
      <h4>通读实战手册</h4>
      <p>7 章：马里奥1-1 → 起承转结 → 引力 → 三角形法则 → 三把尺子 → 热力图。约 40 分钟建立全景。</p>
    </a>
    <a class="step" href="#rules">
      <div class="pn">STEP 02 · 精读</div>
      <h4>逐条读 16 规则</h4>
      <p>四部：教学 / 结构 / 引导 / 流程。每条一页，带模板、检查清单与反面信号，边做边查。</p>
    </a>
    <a class="step" href="dossier.html">
      <div class="pn">STEP 03 · 背景</div>
      <h4>读开发访谈卷宗</h4>
      <p>岩田聪的瓶颈论、宫本茂的点子观、旷野之息的乘法设计——规则背后的思想从哪来。</p>
    </a>
  </div>
</section>

<section id="search-sec" style="padding-top:0">
  <div class="eyebrow">SEARCH</div>
  <div class="searchbox">
    <input id="q" type="search" placeholder="搜索规则、章节、关键词…（如：起承转结）" autocomplete="off">
    <div id="results"></div>
  </div>
</section>

<section id="rules" style="padding-top:12px">
  <div class="rowhead">
    <div>
      <div class="eyebrow">THE 16 RULES</div>
      <h2>规则 R1–R16</h2>
    </div>
    <span class="progress">已读 <b id="readcount">0</b>/16</span>
  </div>
  {{RULES_SECTIONS}}
  <a class="cheat-cta" href="cheatsheet.html">
    <div>
      <h4>速查表 · 16 条一句话版</h4>
      <p>全站最高频回访页——做关卡时贴在手边的那一页，可直接打印。</p>
    </div>
    <span class="go">打开速查表 ▶</span>
  </a>
</section>

</div>

<footer>
  <div class="wrap">
    <p>关卡之书 · 任天堂关卡设计教程 ／ 内容整理自公开访谈（社長が訊く、開発者に訊きました）与公开讲演（GDC、CEDEC）报道，图示为示意复原，引文为最小限度摘录转述 ／ 编纂 2026-07</p>
  </div>
</footer>

<!-- M3: 在此插入 搜索+进度 脚本（见 PLAN-04 §3），置于 </body> 之前 -->
</body>
</html>
```

## 5. `templates/cheatsheet.html` 正式版（照抄；`{{CHEAT_LIST}}` 由构建器替换）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>速查表 · 16 条规则一句话版 — 关卡之书</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0d0f12;--panel:#1a1e25;--text:#d8d2c4;--dim:#8a8577;
  --cinnabar:#c8442a;--amber:#d9a441;--teal:#4a9a8e;--hairline:rgba(216,210,196,.12);
  --serif:'Noto Serif SC',serif;--mono:'JetBrains Mono',monospace}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--ink);color:var(--text);font-family:var(--serif);line-height:1.9}
::selection{background:var(--cinnabar);color:#fff}
.wrap{max-width:880px;margin:0 auto;padding:0 26px}
.hero{padding:64px 0 36px;position:relative;overflow:hidden}
.hero::after{content:"査";position:absolute;right:-2%;top:-18%;font-size:min(34vw,280px);font-weight:900;color:rgba(216,210,196,.035);line-height:1;pointer-events:none}
.rid{font-family:var(--mono);font-size:12px;letter-spacing:.3em;color:var(--cinnabar);margin-bottom:12px}
h1{font-size:clamp(26px,4.4vw,40px);font-weight:900;line-height:1.3}
.sub{margin-top:14px;color:var(--dim);font-size:15px;max-width:620px}
.sub b{color:var(--teal);font-weight:500}
ol{list-style:none;margin:34px 0 70px;counter-reset:cs}
ol li{border-bottom:1px dashed var(--hairline)}
ol li a{display:block;padding:16px 4px;text-decoration:none;color:var(--text);transition:.2s}
ol li a:hover{background:var(--panel)}
ol li b{display:block;font-family:var(--mono);font-size:13px;color:var(--cinnabar);letter-spacing:.08em;margin-bottom:6px}
ol li span{font-size:14.5px;color:var(--text);line-height:1.9}
footer{padding:0 0 70px}
footer p{font-family:var(--mono);font-size:11px;color:var(--dim);line-height:2}
@media print{
  body{background:#fff;color:#111}
  .lb-bar,.hero::after,footer{display:none}
  ol li b{color:#b03418}ol li span{color:#111}
  ol li a{padding:8px 0}
}
</style>
</head>
<body>
{{NAVBAR}}
<div class="wrap">
<header class="hero">
  <div class="rid">CHEATSHEET <b style="color:var(--dim);font-weight:400">/ R1–R16 一句话版</b></div>
  <h1>速查表<br>做关卡时贴在手边的那一页</h1>
  <p class="sub">16 条规则的宣言原文，按 R1→R16 排列。点任意一条进入精读页；<b>Ctrl+P</b> 可直接打印（自动转浅色）。</p>
</header>
<ol>{{CHEAT_LIST}}</ol>
<footer><p>关卡之书 · 速查表 ／ 宣言为各规则页 THE RULE 原文 ／ 编纂 2026-07</p></footer>
</div>
</body>
</html>
```

## 6. M2 自检清单（全过才进 M3）

- [ ] 重跑 `python build_site.py` 成功；`out/index.html`、`out/cheatsheet.html` 已是正式版。
- [ ] 浏览器打开 `http://localhost:5031/`：hero 巨字水印可见、学习路径 3 卡可点、四个分部（第一部教学 4 卡 / 第二部结构 2 卡 / 第三部引导 5 卡 / 第四部流程 5 卡）共 16 张规则卡全部渲染、速查表入口条可点。
- [ ] 首页视觉与素材页并排对比：同一套底色/字体/强调色，无突兀新美学。
- [ ] `http://localhost:5031/cheatsheet.html`：16 条宣言完整显示、每条可点进对应 R 页；Ctrl+P 打印预览为浅色。
- [ ] 任一 R 页顶部导航条正常显示且不遮挡内容（sticky 生效、hero 未被盖住文字）；导航条 5 个链接 + prev/next 全部可点且指向正确。
- [ ] 390px 宽（手机模拟）下：首页网格变单列不破版；导航条不换行溢出（可横向滚动）。
- [ ] BUILD-LOG.md 已追加 M2 记录。
