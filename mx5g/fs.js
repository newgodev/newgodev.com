/* iPad-first fullscreen helper */
(function (global) {
  "use strict";

  function isStandalone() {
    return (
      window.navigator.standalone === true ||
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: fullscreen)").matches
    );
  }

  function isIOS() {
    const ua = navigator.userAgent || "";
    return /iPad|iPhone|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  }

  function isFs() {
    return !!(
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.msFullscreenElement
    );
  }

  function requestFs(el) {
    el = el || document.documentElement;
    const req =
      el.requestFullscreen ||
      el.webkitRequestFullscreen ||
      el.webkitRequestFullScreen ||
      el.msRequestFullscreen;
    if (!req) return Promise.reject(new Error("no-api"));
    try {
      const out = req.call(el);
      return out && typeof out.then === "function" ? out : Promise.resolve();
    } catch (e) {
      return Promise.reject(e);
    }
  }

  function exitFs() {
    const exit =
      document.exitFullscreen ||
      document.webkitExitFullscreen ||
      document.webkitCancelFullScreen ||
      document.msExitFullscreen;
    if (!exit) return Promise.resolve();
    try {
      const out = exit.call(document);
      return out && typeof out.then === "function" ? out : Promise.resolve();
    } catch (e) {
      return Promise.reject(e);
    }
  }

  function openHelp() {
    const box = document.getElementById("ipadHelp");
    if (box) box.classList.add("open");
  }

  function closeHelp() {
    const box = document.getElementById("ipadHelp");
    if (box) box.classList.remove("open");
  }

  function markStandalone() {
    if (isStandalone()) document.documentElement.classList.add("standalone");
  }

  function syncButtons() {
    document.querySelectorAll("[data-fs-btn]").forEach((btn) => {
      if (isStandalone()) {
        btn.style.display = "none";
        return;
      }
      btn.textContent = isFs() ? "退出全螢幕" : "全螢幕";
    });
  }

  async function toggleFs() {
    if (isStandalone()) {
      openHelp();
      return;
    }
    if (isFs()) {
      await exitFs().catch(() => {});
      syncButtons();
      return;
    }
    try {
      await requestFs(document.documentElement);
      syncButtons();
      // If still not fullscreen (common on older iPad Safari), show help
      setTimeout(() => {
        if (!isFs()) openHelp();
        syncButtons();
      }, 350);
    } catch (_) {
      openHelp();
      syncButtons();
    }
  }

  function wire() {
    markStandalone();
    syncButtons();
    document.querySelectorAll("[data-fs-btn]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleFs();
      });
    });
    const close = document.getElementById("ipadHelpClose");
    if (close) close.addEventListener("click", closeHelp);
    const tryBtn = document.getElementById("ipadHelpTry");
    if (tryBtn) {
      tryBtn.addEventListener("click", async () => {
        closeHelp();
        try {
          await requestFs(document.documentElement);
        } catch (_) {
          openHelp();
        }
        syncButtons();
      });
    }
    document.addEventListener("fullscreenchange", syncButtons);
    document.addEventListener("webkitfullscreenchange", syncButtons);
  }

  global.MX5FS = { toggleFs, openHelp, closeHelp, isStandalone, wire, syncButtons };
})(window);
