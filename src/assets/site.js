/* 关卡之书 site.js — 阅读进度记录（localStorage，无上报）+ 锚点回流复位 */
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
