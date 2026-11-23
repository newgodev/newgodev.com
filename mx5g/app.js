(() => {
  "use strict";

  const SLIDES = [
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">Form 3 · Unit 2 · Group 5</div>
          <h1>孟子：仁愛謙和與人格尊嚴</h1>
          <p class="lead">根據「學術思想」筆記頁 11–12、14，為同學設計練習與轉盤問答。先看重點，再玩遊戲。</p>
          <div class="grid3" style="margin-top:18px">
            <div class="panel stat"><b>仁</b><span>仁愛謙和</span></div>
            <div class="panel stat"><b>義</b><span>舍生取義</span></div>
            <div class="panel stat"><b>尊</b><span>天賦尊嚴</span></div>
          </div>
          <div class="motif"></div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">範圍</div>
          <h2>今天只攻第 5 組重點</h2>
          <div class="grid2">
            <div class="panel">
              <h3>頁 11–12</h3>
              <ul>
                <li>仁愛謙和：仁愛、恭敬謙讓、和為貴</li>
                <li>三反其身（自我反省）</li>
                <li>生命與義禮：舍生取義</li>
                <li>以德服人 vs 以力服人</li>
              </ul>
            </div>
            <div class="panel">
              <h3>頁 14</h3>
              <ul>
                <li>人格論：天賦尊嚴</li>
                <li>君子美德：成人之美、言行一致</li>
                <li>代表著作：《孟子》</li>
              </ul>
            </div>
          </div>
          <div class="quote">評分關鍵：內容掌握 + 清晰好玩（之後轉盤遊戲衝表達分）</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">仁愛謙和</div>
          <h2>三個精神，一個方向</h2>
          <div class="grid3">
            <div class="panel"><h3>① 仁愛</h3><p>為君、為臣、為民的思想基礎。心存仁愛，行為才高尚。</p></div>
            <div class="panel"><h3>② 恭敬謙讓</h3><p>以恭敬待人，得信任、少恥辱、少失誤；社會互相尊重。</p></div>
            <div class="panel"><h3>③ 和為貴</h3><p>和平安定是多數人心願；前提是仁愛之心。</p></div>
          </div>
          <div class="quote">沒有愛人的心 → 難有符合義禮的行為 → 難達和平安定</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">自我修養</div>
          <h2>三反其身</h2>
          <div class="grid2">
            <div class="panel">
              <h3>遇到三種情況</h3>
              <ul>
                <li>我愛人，別人不親我 → 反省「仁」</li>
                <li>我管理人，管不好 → 反省「智」</li>
                <li>我禮敬人，人不回敬 → 反省「敬」</li>
              </ul>
            </div>
            <div class="panel">
              <h3>結論</h3>
              <p>凡事得不到應有反應，先在自己身心找原因。自己端正了，天下才會歸順。</p>
              <p style="margin-top:10px">校園版：先問「我有沒有做得不夠好？」再怪別人。</p>
            </div>
          </div>
        </div>`
    },
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">價值抉擇</div>
          <h2>舍生取義</h2>
          <p class="lead">魚，我所欲也；熊掌，亦我所欲也。二者不可得兼，舍魚而取熊掌。生與義不可得兼，舍生而取義。</p>
          <div class="grid2">
            <div class="panel"><h3>比喻</h3><p>魚＝生命；熊掌＝義禮。喜歡兩者，但不能同時擁有時，選更重要的。</p></div>
            <div class="panel"><h3>意思</h3><p>義禮比生命更重要。不是叫人隨便送命，而是守住做人底線。</p></div>
          </div>
          <div class="motif"></div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">政治與待人</div>
          <h2>以德服人</h2>
          <div class="grid2">
            <div class="panel">
              <h3>王者 · 德</h3>
              <p>出於仁愛真心，憑德行降服別人 → 對方<strong>心悅誠服</strong>。</p>
            </div>
            <div class="panel">
              <h3>霸者 · 力</h3>
              <p>假借仁義、用武力 → 對方只因力量不足而<strong>暫時屈服</strong>。</p>
            </div>
          </div>
          <div class="quote">君子應該以德服人，而不是只靠外力強迫。</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">頁 14</div>
          <h2>人格論：天賦尊嚴</h2>
          <div class="grid2">
            <div class="panel">
              <h3>心理基礎</h3>
              <ul>
                <li>憐憫之心 → 知善惡</li>
                <li>羞恥之心 → 知該做／不該做</li>
                <li>→ 仁義之心 → 尊嚴人格</li>
              </ul>
            </div>
            <div class="panel">
              <h3>君子美德</h3>
              <ul>
                <li>成人之美、與人為善</li>
                <li>言行一致、真誠正直</li>
                <li>不投機取巧；對毀譽保持清醒</li>
              </ul>
            </div>
          </div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">著作</div>
          <h2>《孟子》一書</h2>
          <div class="grid3">
            <div class="panel stat"><b>7</b><span>篇（各分上下）</span></div>
            <div class="panel stat"><b>261</b><span>章左右</span></div>
            <div class="panel stat"><b>語錄</b><span>記錄孟子言行</span></div>
          </div>
          <p class="lead" style="margin-top:8px">作者說法不一：或孟子自著、或弟子追記、或師生共同完成。唐代以後地位提升，研究日多。</p>
        </div>`
    },
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">Next</div>
          <h1>轉盤時間</h1>
          <p class="lead">隨機抽座號 1–30 → 出題 → 可要提示／近似答案 → 揭曉 → 繼續下一題。多數是易題，夾少量難題。</p>
          <p class="cta-note">按右下「開始轉盤遊戲」，或頂部切換到「轉盤遊戲」。</p>
          <div class="motif"></div>
        </div>`
    }
  ];

  const deckEl = document.getElementById("deck");
  const gameEl = document.getElementById("game");
  const pageLabel = document.getElementById("pageLabel");
  const progress = document.querySelector("#progress i");
  const deckNav = document.getElementById("deckNav");
  let idx = 0;
  let mode = "deck";

  function renderSlides() {
    deckEl.innerHTML = SLIDES.map((s, i) =>
      `<article class="slide ${s.tone}${i === 0 ? " on" : ""}" data-i="${i}">${s.html}</article>`
    ).join("");
    updateDeckUI();
  }

  function updateDeckUI() {
    [...deckEl.querySelectorAll(".slide")].forEach((el, i) => {
      el.classList.toggle("on", i === idx);
    });
    pageLabel.textContent = `${idx + 1} / ${SLIDES.length}`;
    progress.style.width = `${((idx + 1) / SLIDES.length) * 100}%`;
  }

  function showMode(next) {
    mode = next;
    document.querySelectorAll(".mode").forEach((b) => {
      b.classList.toggle("on", b.dataset.mode === mode);
    });
    const isDeck = mode === "deck";
    deckEl.classList.toggle("hidden", !isDeck);
    gameEl.classList.toggle("hidden", isDeck);
    deckNav.classList.toggle("hidden", !isDeck);
    if (!isDeck) drawWheel();
  }

  document.querySelectorAll(".mode").forEach((b) => {
    b.addEventListener("click", () => showMode(b.dataset.mode));
  });
  document.getElementById("prevBtn").onclick = () => {
    idx = Math.max(0, idx - 1);
    updateDeckUI();
  };
  document.getElementById("nextBtn").onclick = () => {
    if (idx < SLIDES.length - 1) {
      idx += 1;
      updateDeckUI();
    } else showMode("game");
  };
  document.getElementById("toGameBtn").onclick = () => showMode("game");

  window.addEventListener("keydown", (e) => {
    if (mode !== "deck") {
      if (e.code === "Space" && !spinning) {
        e.preventDefault();
        spin();
      }
      return;
    }
    if (e.key === "ArrowRight" || e.key === " ") {
      e.preventDefault();
      document.getElementById("nextBtn").click();
    }
    if (e.key === "ArrowLeft") document.getElementById("prevBtn").click();
  });

  // ——— random utils ———
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

  // ——— wheel ———
  const canvas = document.getElementById("wheel");
  const ctx = canvas.getContext("2d");
  const COLORS = [
    "#1f7a55", "#245c48", "#c44b3c", "#8a3a30",
    "#d4a017", "#9a7510", "#2f6f8f", "#1f4f66",
    "#3d8b6e", "#5a6b63"
  ];
  let numbers = Array.from({ length: 30 }, (_, i) => i + 1);
  let rotation = 0;
  let spinning = false;
  let picked = null;

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
      ctx.font = "700 20px 'Noto Sans TC', sans-serif";
      ctx.fillText(String(numbers[i]), r - 18, 7);
      ctx.restore();
    }
    ctx.beginPath();
    ctx.arc(cx, cy, 46, 0, Math.PI * 2);
    ctx.fillStyle = "#0f1a16";
    ctx.fill();
  }

  let audioCtx = null;
  function tick() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const o = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      o.frequency.value = 760 + randInt(180);
      g.gain.value = 0.04;
      o.connect(g);
      g.connect(audioCtx.destination);
      o.start();
      g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
      o.stop(audioCtx.currentTime + 0.06);
    } catch (_) {}
  }

  function winnerIndex() {
    const n = numbers.length;
    const arc = (Math.PI * 2) / n;
    const norm = ((Math.PI * 2) - ((rotation + Math.PI / 2) % (Math.PI * 2))) % (Math.PI * 2);
    return Math.floor(norm / arc) % n;
  }

  function celebrate() {
    const burst = document.getElementById("burstImg");
    const conf = document.getElementById("confettiImg");
    burst.hidden = false;
    conf.hidden = false;
    burst.classList.add("show");
    conf.classList.add("show");
    burst.src = "./assets/burst.gif?" + Date.now();
    setTimeout(() => {
      burst.classList.remove("show");
      conf.classList.remove("show");
    }, 1600);
    spawnCanvasConfetti();
  }

  function spawnCanvasConfetti() {
    const fx = document.getElementById("fx");
    const fctx = fx.getContext("2d");
    fx.width = innerWidth;
    fx.height = innerHeight;
    const parts = Array.from({ length: 90 }, () => ({
      x: fx.width / 2,
      y: fx.height * 0.42,
      vx: (Math.random() - 0.5) * 14,
      vy: -Math.random() * 12 - 2,
      life: 60 + randInt(40),
      color: COLORS[randInt(COLORS.length)],
      s: 3 + randInt(6)
    }));
    let frame = 0;
    (function loop() {
      fctx.clearRect(0, 0, fx.width, fx.height);
      parts.forEach((p) => {
        p.vy += 0.28;
        p.x += p.vx;
        p.y += p.vy;
        p.life -= 1;
        fctx.globalAlpha = Math.max(0, p.life / 80);
        fctx.fillStyle = p.color;
        fctx.fillRect(p.x, p.y, p.s, p.s * 1.6);
      });
      frame++;
      if (frame < 90) requestAnimationFrame(loop);
      else fctx.clearRect(0, 0, fx.width, fx.height);
    })();
  }

  function spin() {
    if (spinning || numbers.length < 2) return;
    spinning = true;
    document.getElementById("spinBtn").disabled = true;
    const hub = document.querySelector(".hub");
    hub.classList.remove("win");
    const n = numbers.length;
    const winIdx = randInt(n);
    const arc = (Math.PI * 2) / n;
    const extra = (5 + Math.random() * 4) * Math.PI * 2;
    const target =
      extra +
      ((Math.PI * 2) - (winIdx * arc + arc * (0.25 + Math.random() * 0.5)) - (rotation % (Math.PI * 2)));
    const start = rotation;
    const dur = 4800;
    const t0 = performance.now();
    let lastSeg = -1;
    function ease(t) {
      return 1 - Math.pow(1 - t, 4);
    }
    function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      rotation = start + target * ease(p);
      drawWheel();
      const seg = winnerIndex();
      if (seg !== lastSeg) {
        tick();
        lastSeg = seg;
      }
      if (p < 1) requestAnimationFrame(frame);
      else {
        spinning = false;
        document.getElementById("spinBtn").disabled = false;
        picked = numbers[winnerIndex()];
        document.getElementById("pickedNum").textContent = picked;
        hub.classList.add("win");
        celebrate();
        document.getElementById("whoLine").textContent =
          `座號 ${picked} 請作答！（可請鄰近同學幫手，但答案要自己講）`;
        enableQuiz(true);
        serveQuestion(true);
      }
    }
    requestAnimationFrame(frame);
  }

  document.getElementById("spinBtn").onclick = spin;
  document.getElementById("reshuffleBtn").onclick = () => {
    numbers = Array.from({ length: 30 }, (_, i) => i + 1);
    picked = null;
    document.getElementById("pickedNum").textContent = "?";
    drawWheel();
  };

  // ——— quiz ———
  let qOrder = [];
  let qPos = -1;
  let score = 0;
  let current = null;
  let selected = null;
  let revealed = false;

  function enableQuiz(on) {
    ["hintBtn", "nearBtn", "revealBtn", "checkBtn", "nextQBtn"].forEach((id) => {
      document.getElementById(id).disabled = !on;
    });
  }

  function norm(s) {
    return String(s || "")
      .toLowerCase()
      .replace(/\s+/g, "")
      .replace(/[，。！？、,.!?;；：:\-—_]/g, "");
  }

  function isNearMatch(input, item) {
    const t = norm(input);
    if (!t) return false;
    if (t === norm(item.answer)) return true;
    return (item.near || []).some((n) => {
      const nn = norm(n);
      return t === nn || t.includes(nn) || nn.includes(t);
    });
  }

  function serveQuestion(freshPack) {
    if (freshPack || !qOrder.length || qPos >= qOrder.length - 1) {
      const bank = window.MX5_QUESTIONS || [];
      // mostly easy: weight easy x3, medium x2, hard x1 then shuffle
      const weighted = [];
      bank.forEach((q) => {
        const w = q.diff === "easy" ? 3 : q.diff === "medium" ? 2 : 1;
        for (let i = 0; i < w; i++) weighted.push(q);
      });
      qOrder = shuffle(weighted);
      qPos = 0;
    } else qPos += 1;

    current = qOrder[qPos];
    revealed = false;
    selected = null;
    document.getElementById("typed").value = "";
    document.getElementById("feedback").hidden = true;
    document.getElementById("hintCard").hidden = true;
    document.getElementById("nearCard").hidden = true;
    document.getElementById("revealCard").hidden = true;

    const pill = document.getElementById("diffPill");
    pill.textContent = current.diff === "easy" ? "易" : current.diff === "medium" ? "中" : "難";
    pill.className = "pill" + (current.diff === "hard" ? " hard" : "");
    document.getElementById("qIndex").textContent = `題 ${qPos + 1} / ${qOrder.length}`;
    document.getElementById("scorePill").textContent = `分 ${score}`;
    document.getElementById("qTitle").textContent = current.q;

    const box = document.getElementById("choices");
    box.innerHTML = "";
    if (current.type === "mc") {
      shuffle(current.choices).forEach((c) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "choice";
        b.textContent = c;
        b.onclick = () => {
          [...box.children].forEach((x) => x.classList.remove("on"));
          b.classList.add("on");
          selected = c;
        };
        box.appendChild(b);
      });
    } else {
      box.innerHTML = `<p style="opacity:.75;margin:0">開放題：打字或口述後按「核對」。近似意思也算對。</p>`;
    }
  }

  document.getElementById("hintBtn").onclick = () => {
    if (!current) return;
    document.getElementById("hintText").textContent = current.hint;
    document.getElementById("hintCard").hidden = false;
  };
  document.getElementById("nearBtn").onclick = () => {
    if (!current) return;
    document.getElementById("nearText").textContent = (current.near || []).join("　／　");
    document.getElementById("nearCard").hidden = false;
  };
  document.getElementById("revealBtn").onclick = () => {
    if (!current) return;
    revealed = true;
    document.getElementById("revealText").textContent =
      current.answer + (current.explain ? " —— " + current.explain : "");
    document.getElementById("revealCard").hidden = false;
    markChoices(true);
  };

  function markChoices(showCorrect) {
    if (current.type !== "mc") return;
    [...document.getElementById("choices").children].forEach((b) => {
      if (showCorrect && b.textContent === current.answer) b.classList.add("good");
    });
  }

  document.getElementById("checkBtn").onclick = () => {
    if (!current || !picked) return;
    const typed = document.getElementById("typed").value;
    let ok = false;
    if (current.type === "mc") {
      ok = selected === current.answer || isNearMatch(typed, current);
    } else {
      ok = isNearMatch(typed, current);
    }
    const fb = document.getElementById("feedback");
    fb.hidden = false;
    if (ok) {
      if (!revealed) score += current.diff === "hard" ? 3 : current.diff === "medium" ? 2 : 1;
      fb.className = "feedback ok";
      fb.textContent = `做得好！座號 ${picked} 答對。${current.explain || ""}`;
      celebrate();
    } else {
      fb.className = "feedback no";
      fb.textContent = "未中。可按提示／近似答案，或揭曉後再試下一題。";
    }
    document.getElementById("scorePill").textContent = `分 ${score}`;
    markChoices(true);
  };

  document.getElementById("nextQBtn").onclick = () => {
    if (!picked) {
      document.getElementById("whoLine").textContent = "請先轉盤抽人！";
      return;
    }
    serveQuestion(false);
  };

  renderSlides();
  drawWheel();
  enableQuiz(false);
})();
