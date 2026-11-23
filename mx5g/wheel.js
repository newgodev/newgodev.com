(() => {
  "use strict";

  const FALLBACK = [
    {
      diff: "easy",
      q: "仁愛謙和的第一個重點是？",
      type: "mc",
      choices: ["強調仁愛", "強調法治", "強調武力", "強調財利"],
      answer: "強調仁愛",
      near: ["仁愛", "愛人", "仁"],
      hint: "為君為臣為民的思想基礎。",
      explain: "心存仁愛，行為才高尚。"
    },
    {
      diff: "easy",
      q: "魚與熊掌不能兼得時，孟子教人？",
      type: "mc",
      choices: ["舍生取義", "舍義取生", "兩者都不要", "先求財利"],
      answer: "舍生取義",
      near: ["取義", "捨生取義"],
      hint: "生命＝魚；義＝熊掌。",
      explain: "義禮比生命更重要（守底線）。"
    },
    {
      diff: "easy",
      q: "以德服人，對方通常會？",
      type: "mc",
      choices: ["心悅誠服", "暫時屈服", "立刻造反", "完全不理"],
      answer: "心悅誠服",
      near: ["誠心信服", "真心服"],
      hint: "對比以力服人。",
      explain: "德服＝心服；力服＝被迫。"
    }
  ];

  const $ = (id) => document.getElementById(id);
  const canvas = $("wheel");
  const ctx = canvas.getContext("2d");
  const qModal = $("qModal");
  const aModal = $("aModal");

  let numbers = Array.from({ length: 30 }, (_, i) => i + 1);
  let rotation = 0;
  let spinning = false;
  let picked = null;
  let score = 0;
  let played = 0;
  let qOrder = [];
  let qPos = -1;
  let current = null;
  let backTimer = null;
  let backRaf = null;

  const COLORS = ["#1f7a55","#245c48","#c44b3c","#8a3a30","#d4a017","#9a7510","#2f6f8f","#1f4f66","#3d8b6e","#5a6b63"];

  function bank() {
    const q = window.MX5_QUESTIONS;
    return Array.isArray(q) && q.length ? q : FALLBACK;
  }
  function show(el) { el.classList.remove("hide"); }
  function hide(el) { el.classList.add("hide"); }
  function isHidden(el) { return el.classList.contains("hide"); }

  function randInt(max) {
    const buf = new Uint32Array(1);
    crypto.getRandomValues(buf);
    return buf[0] % max;
  }
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = randInt(i + 1);
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function normAngle(a) {
    const t = Math.PI * 2;
    a %= t;
    return a < 0 ? a + t : a;
  }
  function rotationForIndex(i, n) {
    const arc = (Math.PI * 2) / n;
    return normAngle(-(i * arc + arc * 0.5));
  }
  function indexAtPointer(rot, n) {
    const arc = (Math.PI * 2) / n;
    return Math.floor(normAngle(-rot) / arc) % n;
  }

  function drawWheel() {
    const n = numbers.length;
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const r = cx - 8;
    const arc = (Math.PI * 2) / n;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < n; i++) {
      const start = rotation + i * arc - Math.PI / 2;
      const end = start + arc;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, start, end);
      ctx.closePath();
      ctx.fillStyle = COLORS[i % COLORS.length];
      ctx.fill();
      ctx.strokeStyle = "rgba(0,0,0,.25)";
      ctx.stroke();
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(start + arc / 2);
      ctx.textAlign = "right";
      ctx.fillStyle = "#fff";
      ctx.font = "700 20px sans-serif";
      ctx.fillText(String(numbers[i]), r - 16, 6);
      ctx.restore();
    }
  }

  function pickQuestion() {
    const b = bank();
    if (!qOrder.length || qPos >= qOrder.length - 1) {
      const weighted = [];
      b.forEach((q) => {
        const w = q.diff === "easy" ? 3 : q.diff === "medium" ? 2 : 1;
        for (let i = 0; i < w; i++) weighted.push(q);
      });
      qOrder = shuffle(weighted.length ? weighted : FALLBACK);
      qPos = 0;
    } else qPos += 1;
    current = qOrder[qPos] || FALLBACK[0];
  }

  function openQuestion() {
    pickQuestion();
    played += 1;
    $("playedPill").textContent = String(played);
    $("whoBadge").textContent = `座號 ${picked}`;
    const d = current.diff || "easy";
    const pill = $("diffPill");
    pill.textContent = d === "easy" ? "易" : d === "medium" ? "中" : "難";
    pill.className = "pill" + (d === "hard" ? " hard" : "");
    $("qTitle").textContent = current.q || "問題";
    $("hintText").textContent = current.hint || "";
    const box = $("choices");
    box.innerHTML = "";
    if (current.type === "mc" && Array.isArray(current.choices)) {
      shuffle(current.choices).forEach((c) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "choice";
        btn.textContent = c;
        btn.onclick = () => {
          [...box.children].forEach((x) => x.classList.remove("on", "good", "bad"));
          btn.classList.add("on");
          if (c === current.answer) {
            btn.classList.add("good");
            score += 1;
            $("scorePill").textContent = String(score);
          } else btn.classList.add("bad");
        };
        box.appendChild(btn);
      });
    }
    hide(aModal);
    show(qModal);
  }

  function clearBack() {
    if (backTimer) clearTimeout(backTimer);
    if (backRaf) cancelAnimationFrame(backRaf);
    backTimer = null;
    backRaf = null;
  }

  function returnWheel() {
    clearBack();
    hide(qModal);
    hide(aModal);
    $("spinBtn").disabled = false;
  }

  function openAnswer() {
    hide(qModal);
    $("revealText").textContent = current.answer || "";
    $("nearText").textContent = (current.near || []).join("　／　");
    $("explainText").textContent = current.explain || "";
    show(aModal);
    clearBack();
    const bar = $("cdBar");
    const label = $("countdown");
    const total = 5000;
    const t0 = performance.now();
    bar.style.transform = "scaleX(1)";
    function tick(now) {
      const left = Math.max(0, total - (now - t0));
      label.textContent = `${Math.ceil(left / 1000)} 秒後返回`;
      bar.style.transform = `scaleX(${left / total})`;
      if (left > 0) backRaf = requestAnimationFrame(tick);
    }
    backRaf = requestAnimationFrame(tick);
    backTimer = setTimeout(returnWheel, total);
  }

  function spin() {
    if (spinning || numbers.length < 2) return;
    if (!isHidden(qModal) || !isHidden(aModal)) return;
    spinning = true;
    $("spinBtn").disabled = true;
    $("hub").classList.remove("win");

    const n = numbers.length;
    const intended = randInt(n);
    const finalRot = rotationForIndex(intended, n);
    const start = rotation;
    let delta = normAngle(finalRot - normAngle(start));
    if (delta < 0.0001) delta = Math.PI * 2;
    const target = (5 + Math.random() * 3) * Math.PI * 2 + delta;
    const dur = 4200;
    const t0 = performance.now();
    const ease = (t) => 1 - Math.pow(1 - t, 4);

    function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      rotation = start + target * ease(p);
      drawWheel();
      if (p < 1) requestAnimationFrame(frame);
      else {
        spinning = false;
        rotation = finalRot;
        drawWheel();
        const landed = indexAtPointer(rotation, n);
        picked = numbers[landed];
        $("pickedNum").textContent = String(picked);
        $("hub").classList.add("win");
        openQuestion();
      }
    }
    requestAnimationFrame(frame);
  }

  $("spinBtn").onclick = spin;
  $("reshuffleBtn").onclick = () => {
    numbers = Array.from({ length: 30 }, (_, i) => i + 1);
    picked = null;
    $("pickedNum").textContent = "?";
    drawWheel();
  };
  $("showAnswerBtn").onclick = openAnswer;
  $("backNowBtn").onclick = returnWheel;
  $("fsBtn").onclick = () => {
    const el = document.documentElement;
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {
      (el.requestFullscreen || el.webkitRequestFullscreen).call(el);
    } else {
      (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    }
  };

  drawWheel();
  hide(qModal);
  hide(aModal);
})();
