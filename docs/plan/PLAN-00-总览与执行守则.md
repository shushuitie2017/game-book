# PLAN-00 · 总览与执行守则

> **本卷是整套计划书的入口。执行任何操作前，先把本卷从头读到尾。**
> 计划书共 7 卷，放在 `docs/plan/`。你（执行模型）按里程碑顺序 M0→M5 执行，每个里程碑对应一卷，做完跑该卷末尾的自检清单，全部通过才进入下一个里程碑。

---

## 1. 项目是什么

把一套已完成的中文知识库——**任天堂关卡设计方法论**（16 条规则教程 + 1 份实战手册 + 1 份开发访谈卷宗，共 18 个自包含 HTML）——组织成一个独立静态教程网站。

- **站名**：关卡之书（副题：任天堂关卡设计教程）。已定稿，不要另起名。
- **项目根目录**：`C:\Users\1\Desktop\note\server-projects\level-book\`（本计划书所在项目）。
- **素材源目录（只读！）**：`C:\Users\1\Desktop\note\分析报告\game\`。
- **形态**：纯静态站，零框架、零 npm、零第三方 JS（Google Fonts 除外）。构建器是一个纯 Python 标准库脚本 `build_site.py`。
- **本地预览**：`python -m http.server 5031 -d out`（端口固定 5031）。
- **本项目只做到本地验收，不部署**。部署是后续另一个会话的事。

## 2. 卷目与里程碑对照

| 里程碑 | 卷 | 内容 | 产出 |
|--------|----|------|------|
| （通读） | PLAN-00 本卷 | 守则、红线、执行协议 | — |
| M0 | PLAN-01 | 素材清单与数据真相源 | `src/content/` 18 个 HTML + `data/rules.json` |
| M1 | PLAN-02 | 工程骨架与构建流水线 | `build_site.py` + 可运行的 `out/` |
| M2 | PLAN-03 | 站壳页面（首页/速查表/导航条） | `templates/` + `assets/site.css` |
| M3 | PLAN-04 | 搜索与阅读进度 | `search-index.json` + 搜索框 + localStorage 进度 |
| M4 | PLAN-05 | SEO 与站点元数据 | 每页 SEO 头 + og-cover + sitemap + README/CLAUDE.md |
| M5 | PLAN-06 | 验收闸门 | 链接检查脚本 + 浏览器实测 + Lighthouse |

## 3. 红线（违反任何一条 = 本次执行失败）

1. **素材正文一字不改**。不改写、不删减、不"顺手润色"、不重排 18 个文档的内部章节。构建时只允许做四类注入：`<head>` 里加 SEO 标签与 site.css 链接、`<body>` 开头加导航条、`</body>` 前加 site.js、把 R 页底部纯文本导航替换成真实链接（外加给 h2 补 id 属性）。注入发生在**构建产物**上，`src/content/` 里的文件在 M0 复制入库后永不再改。
2. **素材源目录 `分析报告\game\` 绝对只读**。只从那里复制，不往那里写任何东西。
3. **不引入任何第三方运行时依赖**：无 npm、无 CDN JS 库、无分析统计、无评论、无账号、无后端。Python 构建脚本只用标准库。
4. **设计零新美学**：站壳所有页面复用素材既有设计令牌（见 PLAN-03 第 1 节），不引入新颜色、新字体、新组件语言。
5. **不做翻译**。全站中文；三语化是后续独立任务。
6. **绝不用 PowerShell 的 `Get-Content`/`-replace`/`Set-Content` 去改任何含中文的文件**（会因编码毁掉文件且不可逆）。改文件一律用 Edit/Write 工具；Python 里读写一律显式 `encoding="utf-8"`。

## 4. 执行协议（给执行模型的工作方式约定）

1. **顺序执行，不跳卷**。M(n) 自检没全过，不开 M(n+1)。
2. **先读整卷再动手**。每卷开头有"前置条件"，确认满足再开始。
3. **计划与现实冲突时**：以素材文件的实际内容为准（比如某个正则锚点在真实文件里长得不一样），修正你的实现去适配现实，**但不得改变设计意图**；把冲突和你的处理记进 `BUILD-LOG.md`。
4. **BUILD-LOG.md**（项目根目录）：每完成一个里程碑追加一节——日期、做了什么、自检结果（逐条✅/❌）、遇到的坑。这是跨会话交接的唯一进度真相源。中途断了，新会话先读它。
5. **每条结论对照真实输出核验**：说"构建成功"之前必须真的跑过 `python build_site.py` 且退出码为 0；说"页面正常"之前必须真的在浏览器里打开看过。
6. **计划书里的代码是参考实现**：允许你修 bug、补边角，但函数职责、文件名、数据结构、注入锚点不许改——那些是接口，后面的卷依赖它们。
7. 卡住超过 3 次尝试仍不能解决的问题：记录进 BUILD-LOG.md，标注 `[BLOCKED]`，继续做不依赖它的部分，最后统一汇报，不要死磕也不要静默跳过。

## 5. 最终目录结构（全部完成后应长这样）

```
level-book/
├── build_site.py           # 构建器（M1）
├── BUILD-LOG.md            # 执行日志（贯穿）
├── README.md               # （M4）
├── CLAUDE.md               # （M4）
├── data/
│   └── rules.json          # 数据真相源（M0，内容见 PLAN-01）
├── src/
│   ├── content/            # 18 个素材 HTML（M0 复制入库，此后只读）
│   └── assets/             # 站壳静态资产：site.css / site.js / favicon.svg / og-cover.png（M2-M4）
├── templates/
│   ├── index.html          # 首页模板（M2）
│   └── cheatsheet.html     # 速查表模板（M2）
├── tools/
│   ├── verify_rules.py     # rules.json 与素材宣言一致性核对（M1）
│   ├── check_links.py      # 死链检查（M5）
│   └── og-cover.html       # OG 封面截图源（M4）
├── docs/
│   └── plan/               # 本计划书 7 卷
└── out/                    # 构建产物（git 不入库；每次构建可全删重建）
    ├── index.html
    ├── cheatsheet.html
    ├── manual.html
    ├── dossier.html
    ├── R01-teaching-elements.html … R16-anti-busywork.html
    └── assets/
        ├── site.css
        ├── site.js
        ├── search-index.json
        ├── favicon.svg
        └── og-cover.png
```

## 6. 术语表

| 术语 | 含义 |
|------|------|
| R 页 | R01–R16 共 16 篇规则教程页 |
| 卷宗页 | `manual.html`（实战手册）与 `dossier.html`（访谈卷宗）两个长文档 |
| 站壳 | 非素材内容的部分：首页、速查表、导航条、搜索、进度 |
| RULE 宣言 | 每个 R 页 hero 区 `<div class="rule">` 里的一句话规则原文 |
| 注入 | 构建时对素材 HTML 做的机械修改（加头、加导航、加脚本、修链接） |
| 数据真相源 | `data/rules.json`——所有页面清单、标题、宣言、分组、前后件关系的唯一出处 |

## 7. 通读完本卷后的第一步

打开 `PLAN-01-素材与数据真相源.md`，开始 M0。
