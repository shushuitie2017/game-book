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
3. 站壳视觉只用既有令牌（ink #0d0f12 / cinnabar #c8442a / amber #d9a441 / teal #4a9a8e / Noto Serif SC + JetBrains Mono）+ 派生提亮档 `--cinnabar-hi:#e2694f`（仅限深底小字号，保对比度），不引入新美学。
4. 无第三方运行时依赖（Google Fonts 除外）；进度只存 localStorage。
5. 含中文文件禁用 PowerShell Get-Content/-replace 修改（编码会毁），一律 Edit/Write 或 Python UTF-8。

## 部署

- **线上**：GitHub Pages https://shushuitie2017.github.io/game-book/（仓库 shushuitie2017/game-book，main 推送触发 `.github/workflows/pages.yml`：Actions 跑 build_site.py → deploy-pages，本机无需构建产物入库）。
- 换域名（如日后上 bluecatbot）：只改 `data/rules.json` 的 `site.base` 重构建/重推。

## 计划书

实装计划 7 卷：`docs/plan/PLAN-00` 起。执行进度：`BUILD-LOG.md`。
