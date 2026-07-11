# PLAN-04 · 搜索与阅读进度（里程碑 M3）

> **前置条件**：M2 全部自检通过（正式版首页/速查表已上线本地）。
> **本卷产出**：`src/assets/site.js` 正式版 + `templates/index.html` 末尾的搜索/进度脚本。全部原生 JS，无任何库。
> 隐私边界：进度只存浏览器 localStorage，无网络上报、无账号。

---

## 1. `search-index.json` 结构（M1 构建器已生成，此处为契约确认）

数组，18 条（16 R 页 + 2 卷宗页），每条：

```json
{
  "file": "R05-kishotenketsu.html",
  "num": "R5",
  "title": "起承转结",
  "subtitle": "一关只教一个机制,按四段展开它的一生",
  "rule": "每一关只围绕一个核心机制,按「起→承→転→結」四段展开:…",
  "headings": [{ "id": "h2-1", "text": "《3D世界》塞了几十个新机制,却没有一个教程弹窗" }, …]
}
```

卷宗页条目 `num` 为 `"卷宗"`、`rule` 为空串、headings 的 id 是 `s1`–`s7`。**M3 开始前先打开 `out/assets/search-index.json` 目检**：18 条、字段齐全、headings 非空。不符则回 M1 修构建器。

## 2. `src/assets/site.js` 正式版（照抄；注入所有 20 页）

职责只有一个：R 页被打开时记录"已读"。

```js
/* 关卡之书 site.js — 阅读进度记录（localStorage，无上报） */
(function () {
  var file = location.pathname.split("/").pop() || "index.html";
  if (!/^R\d{2}-/.test(file)) return;           // 只在 R 页记录
  var id = file.slice(0, 3);                    // "R05"
  try {
    var KEY = "lb-read";
    var read = JSON.parse(localStorage.getItem(KEY) || "[]");
    if (read.indexOf(id) === -1) {
      read.push(id);
      localStorage.setItem(KEY, JSON.stringify(read));
    }
  } catch (e) { /* 隐私模式等存储不可用时静默 */ }
})();
```

约定：**进度键 = `lb-read`，值 = `["R01","R05",…]`（R 页文件名前 3 字符）**。首页脚本按同一约定读取。

## 3. 首页搜索 + 进度显示脚本（照抄，替换 `templates/index.html` 末尾的 `<!-- M3: … -->` 注释，位置在 `</body>` 之前）

```html
<script>
(function () {
  /* ---------- 阅读进度：卡片打勾 + n/16 ---------- */
  try {
    var read = JSON.parse(localStorage.getItem("lb-read") || "[]");
    var n = 0;
    document.querySelectorAll(".rcard").forEach(function (card) {
      if (read.indexOf(card.getAttribute("data-id")) !== -1) { card.classList.add("read"); n++; }
    });
    var rc = document.getElementById("readcount");
    if (rc) rc.textContent = n;
  } catch (e) {}

  /* ---------- 搜索 ---------- */
  var q = document.getElementById("q");
  var box = document.getElementById("results");
  if (!q || !box) return;
  var INDEX = null, sel = -1;

  function load(cb) {
    if (INDEX) return cb();
    fetch("assets/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { INDEX = d; cb(); })
      .catch(function () { INDEX = []; cb(); });
  }

  function match(entry, kw) {
    /* 返回 {score, hitHeading|null}。标题/编号命中优先于宣言，宣言优先于章节。 */
    var t = (entry.num + " " + entry.title + " " + entry.subtitle).toLowerCase();
    if (t.indexOf(kw) !== -1) return { score: 3, h: null };
    if ((entry.rule || "").toLowerCase().indexOf(kw) !== -1) return { score: 2, h: null };
    for (var i = 0; i < entry.headings.length; i++) {
      if (entry.headings[i].text.toLowerCase().indexOf(kw) !== -1)
        return { score: 1, h: entry.headings[i] };
    }
    return null;
  }

  function render(kw) {
    if (!kw) { box.style.display = "none"; box.innerHTML = ""; sel = -1; return; }
    var hits = [];
    INDEX.forEach(function (e) {
      var m = match(e, kw);
      if (m) hits.push({ e: e, m: m });
    });
    hits.sort(function (a, b) { return b.m.score - a.m.score; });
    hits = hits.slice(0, 12);
    if (!hits.length) {
      box.innerHTML = '<a><span class="rn">·</span>无结果</a>';
      box.style.display = "block"; return;
    }
    box.innerHTML = hits.map(function (h) {
      var href = h.e.file + (h.m.h ? "#" + h.m.h.id : "");
      var sub = h.m.h ? '<span class="hd">§ ' + h.m.h.text + "</span>" : "";
      return '<a href="' + href + '"><span class="rn">' + h.e.num + "</span>" +
             h.e.title + " · " + h.e.subtitle + sub + "</a>";
    }).join("");
    box.style.display = "block"; sel = -1;
  }

  q.addEventListener("input", function () {
    var kw = q.value.trim().toLowerCase();
    load(function () { render(kw); });
  });
  q.addEventListener("keydown", function (ev) {
    var links = box.querySelectorAll("a[href]");
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault();
      if (!links.length) return;
      sel = ev.key === "ArrowDown" ? Math.min(sel + 1, links.length - 1) : Math.max(sel - 1, 0);
      links.forEach(function (a, i) { a.classList.toggle("sel", i === sel); });
    } else if (ev.key === "Enter") {
      if (links.length) location.href = links[sel === -1 ? 0 : sel].getAttribute("href");
    } else if (ev.key === "Escape") {
      render("");
    }
  });
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest(".searchbox")) render("");
  });
})();
</script>
```

实现要点（照做，别自由发挥）：
- 搜索是**纯客户端 substring 匹配**（转小写 includes），不做分词/拼音/模糊——中文 substring 已够用。
- 排序：标题/副题命中(3) > 宣言命中(2) > 章节命中(1)；章节命中跳锚点（R 页 `#h2-N`，卷宗页 `#sN`）。
- 最多显示 12 条；键盘 ↑↓ 选择、Enter 跳转、Esc 关闭、点击空白关闭。
- 索引懒加载：第一次输入才 fetch。

## 4. h2 锚点跳转的遮挡修正

sticky 导航条高 46px，锚点跳转会被盖住标题。在 `src/assets/site.css` 末尾追加一行：

```css
h2[id],section[id]{scroll-margin-top:60px}
```

（放 site.css 是因为素材页自身没有这条；首页模板里 `#rules` 已单独写过。）

## 5. M3 自检清单（全过才进 M4）

- [ ] 重跑构建；`out/assets/site.js` 为正式版、首页末尾有搜索脚本。
- [ ] 浏览器打开首页 → 搜索框输入 `起承转结`：下拉出现 ≥2 条结果（R5 排最前；manual 的章节"起承转结：四段式关卡构造"也命中）；点击 R5 结果正确跳转。
- [ ] 输入 `热力图`：命中 R14 与 manual 章节；输入乱串 `zzzz`：显示"无结果"。
- [ ] 键盘操作：↓↓ 高亮第二条，Enter 跳转成功；Esc 关闭下拉。
- [ ] 章节级命中跳转后，标题未被导航条遮挡（scroll-margin 生效）。
- [ ] 访问 R01、R05 两页后回首页：两张卡片出现 ✓、计数显示 `已读 2/16`；无痕窗口打开则为 0/16（进度隔离正常）。
- [ ] DevTools Console 在首页/R 页/速查表均无报错（fetch 404、JS 异常都算不过）。
- [ ] BUILD-LOG.md 已追加 M3 记录。
