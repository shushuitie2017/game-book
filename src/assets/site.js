/* 关卡之书 site.js — 阅读进度记录（localStorage，无上报）+ 锚点回流复位 + 复制给 AI */
(function () {
  /* webfont 载入后文本回流会使锚点目标偏移——fonts.ready 后复位一次（仅当用户尚未手动滚动） */
  if (location.hash && document.fonts && document.fonts.ready) {
    var moved = false;
    var onScroll = function () { moved = true; };
    setTimeout(function () { addEventListener("wheel", onScroll, { once: true, passive: true }); addEventListener("touchmove", onScroll, { once: true, passive: true }); }, 0);
    document.fonts.ready.then(function () {
      if (moved) return;
      var el = document.getElementById(location.hash.slice(1));
      if (el) el.scrollIntoView();
    });
  }
})();
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
(function () {
  var file = location.pathname.split("/").pop() || "index.html";
  if (!/^R\d{2}-/.test(file)) return;   // 只在 R 页显示

  function extractText() {
    var lines = [];
    // 规则头：编号 + 标题 + 规则宣言 + 来源
    var rid   = document.querySelector('.rid');
    var h1    = document.querySelector('.hero h1');
    var rule  = document.querySelector('.rule');
    var src   = document.querySelector('.src');
    if (rid)  lines.push(rid.innerText.trim());
    if (h1)   lines.push(h1.innerText.trim());
    if (rule) lines.push('\n【规则宣言】\n' + rule.innerText.replace(/^THE RULE[\s\S]*?\n/, '').trim());
    if (src)  lines.push('\n【来源】\n' + src.innerText.trim());
    // 正文 section（排除 footer 内的）
    document.querySelectorAll('section').forEach(function (sec) {
      if (sec.closest('footer')) return;
      var text = sec.innerText.trim();
      if (text) lines.push('\n---\n' + text);
    });
    var prefix = '以下是《关卡之书》中的一条任天堂关卡设计规则。请根据这条规则为我设计一个游戏关卡（或机制/关卡片段）：\n\n';
    return prefix + lines.join('\n');
  }

  var btn = document.createElement('button');
  btn.id = 'lb-copy';
  btn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="5" width="9" height="9" rx="1"/><path d="M3 11V3a1 1 0 011-1h8"/></svg>复制给 AI';
  btn.addEventListener('click', function () {
    var text = extractText();
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function done() {
      btn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="2,9 6,13 14,4"/></svg>已复制！';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="5" width="9" height="9" rx="1"/><path d="M3 11V3a1 1 0 011-1h8"/></svg>复制给 AI';
        btn.classList.remove('copied');
      }, 2200);
    }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { alert('请手动复制：\n\n' + text.slice(0, 200) + '…'); }
      document.body.removeChild(ta);
    }
  });
  document.body.appendChild(btn);
})();
