# PLAN-05 · SEO 与站点元数据（里程碑 M4）

> **前置条件**：M3 全部自检通过。
> **本卷产出**：① 核对每页 SEO 字符串；② `tools/og-cover.html` + 生成 `src/assets/og-cover.png`；③ `README.md` + `CLAUDE.md` + `.gitignore` + 首次 git 提交。
> SEO 注入逻辑 M1 已随构建器实现（`seo_block()`），本卷是**字符串契约核对 + 补齐资产**。

---

## 1. 每页 SEO 字符串契约（核对构建产物是否符合）

| 页面 | `<title>`（保持素材原有，不改） | meta description | og:type |
|------|--------------------------------|------------------|---------|
| index.html | 关卡之书 · 任天堂关卡设计教程 | rules.json 的 `site.description` | website |
| cheatsheet.html | 速查表 · 16 条规则一句话版 — 关卡之书 | 同上 | website |
| manual.html | （素材原 title）| `任天堂关卡设计实战手册——场景构思的可复用机制。` + site.description | article |
| dossier.html | （素材原 title）| `任天堂开发访谈研究卷宗——「先做出好玩，再做出规模」。` + site.description | article |
| R 页 ×16 | （素材原 title）| 该条 `rule` 宣言，超 155 字符截断加 `…` | article |

统一规则（`seo_block()` 已实现，逐条核对）：
- canonical：`https://level.bluecatbot.com/<file>`，index 为根 `…/`。**域名是候选值**，写死在 rules.json 的 `site.base`，部署时若换子域名只改这一处重构建。
- 所有页：`og:title`（=title）、`og:description`（=description）、`og:url`、`og:image`（`<base>/assets/og-cover.png`）、`og:site_name`（关卡之书）、`twitter:card`（summary_large_image）、favicon link。
- description/og 属性值必须经 HTML 转义（构建器 `esc()`），因为宣言里可能含英文双引号。

## 2. `tools/og-cover.html`（OG 封面截图源，1200×630，照抄）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;position:relative;
  background:radial-gradient(900px 500px at 85% -10%, rgba(200,68,42,.14), transparent 60%),
             radial-gradient(700px 400px at 5% 110%, rgba(74,154,142,.10), transparent 60%),#0d0f12;
  font-family:'Noto Serif SC',serif;color:#d8d2c4}
.mark{position:absolute;right:-30px;top:-40px;font-size:520px;font-weight:900;color:rgba(216,210,196,.045);line-height:1}
.in{position:absolute;left:80px;top:150px}
.kicker{font-family:'JetBrains Mono',monospace;font-size:20px;letter-spacing:.4em;color:#d9a441;margin-bottom:30px}
h1{font-size:120px;font-weight:900;letter-spacing:.04em;line-height:1.15}
h1 em{font-style:normal;color:#c8442a}
.sub{margin-top:26px;font-size:28px;color:#8a8577}
.meta{position:absolute;left:80px;bottom:56px;font-family:'JetBrains Mono',monospace;font-size:17px;color:#8a8577;letter-spacing:.1em}
.meta b{color:#4a9a8e;font-weight:500}
</style>
</head>
<body>
<div class="mark">遊</div>
<div class="in">
  <div class="kicker">LEVEL BOOK — NINTENDO LEVEL DESIGN</div>
  <h1>关卡之书<em>。</em></h1>
  <div class="sub">任天堂关卡设计教程 · 16 条可执行规则 × 2 卷研究卷宗</div>
</div>
<div class="meta">规则 <b>R1–R16</b>　　手册 <b>7 章</b>　　访谈卷宗 <b>7 章</b></div>
</body>
</html>
```

## 3. 生成 `src/assets/og-cover.png`

用系统 Chrome 无头截图（**显式完整命令，不放循环里跑**；跑之前若有残留 headless chrome 进程先杀掉）：

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu --hide-scrollbars `
  --virtual-time-budget=8000 --window-size=1200,630 `
  --screenshot="C:\Users\1\Desktop\note\server-projects\level-book\src\assets\og-cover.png" `
  "file:///C:/Users/1/Desktop/note/server-projects/level-book/tools/og-cover.html"
```

验证三件事：① PNG 存在且 > 20KB；② 用 Read 工具打开图片**目检**——大字「关卡之书」以衬线体渲染（若是黑体/宋体默认字，说明 webfont 没等到，把 virtual-time-budget 提到 15000 重截）；③ 尺寸 1200×630。生成后重跑构建让它进 `out/assets/`。

## 4. `README.md`（项目根，照抄后可微调）

```markdown
# 关卡之书 · 任天堂关卡设计教程

> 把「社長が訊く」与 CEDEC / GDC 讲演里散落的任天堂关卡设计方法论，
> 编成一本可执行的书——**16 条规则 × 1 份实战手册 × 1 卷开发访谈研究**。

每条规则一页，固定结构：**RULE 宣言 → 案例证据 → 执行流程 → 模板 → 检查清单 → 反面信号**。
不是读物，是做关卡时摆在手边的工具书。

## 内容地图

| 分部 | 规则 | 主题 |
|------|------|------|
| 第一部 · 教学 | R1–R4 | 不用文字教会玩家 |
| 第二部 · 结构 | R5–R6 | 一个机制的一生（起承转结） |
| 第三部 · 引导 | R7–R11 | 让玩家自己想去（引力/三角形法则） |
| 第四部 · 流程 | R12–R16 | 先确定好玩，再确定规模 |

另有两册长卷宗：《实战手册》（7 章总纲）与《开发访谈研究卷宗》（岩田聪 / 宫本茂 / BotW 团队）。

## 本地运行

```bash
python build_site.py          # 构建到 out/
python -m http.server 5031 -d out
# 打开 http://localhost:5031/
```

零框架、零 npm、零第三方运行时——构建器是一个纯 Python 标准库脚本。

## 结构

- `src/content/` 18 篇内容页（真相源，构建时注入导航/SEO，不改正文）
- `data/rules.json` 站点数据真相源
- `templates/` 首页与速查表模板
- `out/` 构建产物（勿手改）

内容整理自公开访谈与讲演报道，图示为示意复原，引文为最小限度摘录转述。
```

## 5. `CLAUDE.md`（项目根，照抄）

```markdown
# 关卡之书（level-book）

中文静态教程站：任天堂关卡设计方法论（16 规则 + 2 卷宗）。零框架零 npm。

## 命令

- 构建：`python build_site.py`（清空重建 out/，UTF-8 强制）
- 预览：`python -m http.server 5031 -d out`（端口 5031）
- 数据核对：`python tools/verify_rules.py`（rules.json 宣言 vs 素材原文）
- 死链检查：`python tools/check_links.py`

## 铁律

1. `src/content/` 里 18 篇素材正文**一字不改**——所有站点化改动都通过 build_site.py 注入到 out/。
2. 页面/数据改动永远改源（src / templates / data），跑构建看产物；**绝不手改 out/**。
3. 站壳视觉只用既有令牌（ink #0d0f12 / cinnabar #c8442a / amber #d9a441 / teal #4a9a8e / Noto Serif SC + JetBrains Mono），不引入新美学。
4. 无第三方运行时依赖（Google Fonts 除外）；进度只存 localStorage。
5. 含中文文件禁用 PowerShell Get-Content/-replace 修改（编码会毁），一律 Edit/Write 或 Python UTF-8。

## 部署

尚未部署。上线走 bluecat-deploy（静态站，候选 `level.bluecatbot.com`；换域名改 `data/rules.json` 的 `site.base` 重构建）。

## 计划书

实装计划 7 卷：`docs/plan/PLAN-00` 起。执行进度：`BUILD-LOG.md`。
```

## 6. `.gitignore` + 首次提交

`.gitignore`：

```
out/
__pycache__/
*.pyc
```

然后 `git init` + 全量 `git add` + 提交。提交信息：`feat: 关卡之书站点骨架——构建器/站壳/搜索/进度/SEO（M0-M4）`。
**提交信息里绝不出现任何 Claude/AI 署名**（全局硬规则，有钩子拦截）。不推远端——推送是部署阶段的事。

## 7. M4 自检清单（全过才进 M5）

- [ ] 抽查 3 个页面（index / R05 / manual）的产物源码：SEO 字符串与 §1 契约一致，description 无未转义引号、无截断成半个字的情况。
- [ ] `out/assets/og-cover.png` 存在、>20KB、目检衬线字体正确渲染。
- [ ] `out/sitemap.xml` 恰好 20 个 `<loc>`，全部以 `site.base` 开头；`robots.txt` 指向 sitemap。
- [ ] README.md / CLAUDE.md / .gitignore 就位；`git log --oneline` 有首次提交且不含 AI 署名。
- [ ] BUILD-LOG.md 已追加 M4 记录。
