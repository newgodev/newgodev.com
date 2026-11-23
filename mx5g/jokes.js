(function (global) {
  "use strict";

  const LINES = [
    "同學，唔好扮睇電話，我喺畫像入面都睇到你。",
    "以力服人？即係靠大聲？我亞聖都搖頭。",
    "魚好食，但抄襲唔好食——記住舍生取義。",
    "三反其身：第一步，先反省點解你而家笑。",
    "仁愛謙和：請把筆記分享，唔好只 share meme。",
    "老師打分緊，你哋玩得開心＝表達分＋＋",
    "霸者靠罰分，王者靠公道。班長你揀邊條路？",
    "呢個簡報係 HTML，唔係 Canva——所以我可以飛出嚟寸你。",
    "心悅誠服先長久；暫時屈服得一陣。",
    "被抽中唔好喊——呢個叫鍛鍊膽識。"
  ];

  let i = 0;

  function nextLine(el) {
    if (!el) return;
    i = (i + 1) % LINES.length;
    el.textContent = LINES[i];
  }

  function wire() {
    const host = document.getElementById("mengHost");
    const line = document.getElementById("mengLine");
    const boot = document.getElementById("laughBoot");
    const roastBtn = document.getElementById("roastBtn");
    const roastLine = document.getElementById("roastLine");

    if (host) {
      host.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        nextLine(line);
      });
    }
    if (boot) {
      boot.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        boot.textContent = "✓ 笑場 ON（老師當你投入）";
        if (line) line.textContent = "笑場模式 ON。請全班出聲，我繼續寸你。";
      });
    }
    if (roastBtn) {
      roastBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        nextLine(roastLine);
      });
    }
  }

  global.MX5Jokes = { wire, LINES };
})(window);
