# BUILD-LOG · 关卡之书

执行进度真相源。每完成一个里程碑追加一节。计划书见 `docs/plan/PLAN-00` 起。

---

## M0 素材入库与数据真相源 — 2026-07-11

- 建目录 `src/content`、`src/assets`、`data`、`templates`、`tools`。
- 18 个 HTML 从 `分析报告\game\` 复制入库，三处改名（`R01…(1)`→`R01…`、manual、dossier）。
- 自检：✅ 18 文件字节数与源全部一致（ALL 18 SIZES MATCH）；✅ `rules.json` 解析出 16 规则/4 分组/2 卷宗；✅ 16 个 file 字段全部存在；✅ `verify_rules.py` 输出 `all rules match`（宣言与素材原文逐字一致，含 ASCII 引号形态）。
- 备注：verify_rules.py 提前到 M0 就位并跑过（计划里属 M1，提前无副作用）。

## M1+M2+M3 构建流水线 / 站壳 / 搜索进度 — 2026-07-11

计划偏差（记录）：M1 占位模板步骤跳过，模板直接写正式版（PLAN-03 全文），一次过 M1-M3 三道闸；site.js 也一并写正式版。设计意图未变。

- build_site.py 落地（含 lambda 防反斜杠注入、footer nav 替换 assert fail-loud）。
- 自检结果：
  - ✅ verify_rules.py `all rules match`；✅ 构建两遍幂等（`build ok: 20 pages, 18 search entries`，文件清单一致）
  - ✅ R05 抽查：导航条/footer 真链接（R04↔R06）/h2-id ×8/SEO 头全部就位；R01 prev→index#rules、R16 next→cheatsheet
  - ✅ manual footer 未被改动、无 h2-id 注入；首页 16 卡 4 分部、速查表 16 条
  - ✅ 浏览器实测（chrome-devtools）：C1 首页渲染+Console 零报错；C2 点卡进 R01；C3 NEXT 链 R1→R4；C4 速查表第 7 条→R7；C5 进度 5/16 打勾正确；C6 搜「起承转结」R5 居首+manual#s2 章节命中、搜「热力图」R14+manual#s6、乱串显示无结果、Esc 关闭；C8 手机 390×844 模拟零横向溢出（index 与 R05）；C9 dossier TOC 7 锚点全通
- 坑与修复：
  1. **锚点跳转量到"被导航条遮挡"是假阳性**——`scroll-behavior:smooth` 动画中途取值 36px，落定实测 59.95px（scroll-margin-top:60px 一直生效）。仍给 site.js 加了 fonts.ready 后 hash 复位（防 webfont 回流位移，带"用户已滚动则不动"守卫），属加固非必需。
  2. **首页 Lighthouse A11y 84→100**：站壳三处问题按闸门 D 修复——小字号朱砂对比度不足（新增派生令牌 `--cinnabar-hi:#e2694f`，仅限深底小字），.step h4 跳级改 h3，内容区加 `<main>` landmark。速查表模板同步修。R 页 A11y 93 的 2 项失败（h5 跳级/无 main）属素材结构，按红线不动。
- Lighthouse（desktop）：首页 A11y 100 / BP 100 / SEO 100；R05 A11y 93 / BP 100 / SEO 100。
