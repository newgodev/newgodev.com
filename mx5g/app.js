(() => {
  "use strict";

  const SLIDES = [
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">3G · 第5組 · 唔好訓呀</div>
          <div class="hero-row">
            <div>
              <h1>孟子其實好「校園」</h1>
              <p class="lead">仁愛謙和、舍生取義、天賦尊嚴——用生活例子講明，再轉盤抽人問答。</p>
              <div class="chip-row" style="margin-top:14px">
                <span class="chip">有情境</span>
                <span class="chip">有對決</span>
                <span class="chip">有轉盤</span>
              </div>
            </div>
            <img class="hero-art" src="./assets/ex-friends.png" alt="">
          </div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">開場挑戰</div>
          <h2>如果你係班長，點算？</h2>
          <div class="grid2">
            <div class="scene tap" data-tap>
              <img src="./assets/ex-devforce.png" alt="">
              <div>
                <span class="tag">情境 A</span>
                <strong>用大聲嚇到全班聽話</strong>
                <p>「再嘈就扣分！」大家即刻靜——但係心裏面翻白眼。</p>
                <div class="secret">= 以力服人（暫時屈服）</div>
              </div>
            </div>
            <div class="scene tap" data-tap>
              <img src="./assets/ex-friends.png" alt="">
              <div>
                <span class="tag">情境 B</span>
                <strong>講清楚、聽意見、帶頭做</strong>
                <p>同學覺得你公道，自願配合，氣氛都好啲。</p>
                <div class="secret">= 以德服人（心悅誠服）· 撳我睇答案</div>
              </div>
            </div>
          </div>
          <div class="quote">撳上面兩格睇答案 → 孟子話：君子應該以德服人</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">仁愛謙和 · 校園版</div>
          <h2>三個場面，三個重點</h2>
          <div class="grid3">
            <div class="scene">
              <img src="./assets/ex-friends.png" alt="">
              <div>
                <span class="tag">① 仁愛</span>
                <strong>借筆記唔係施捨</strong>
                <p>同學欠筆記，你主動分享——因為心存仁愛，唔係想換名氣。</p>
              </div>
            </div>
            <div class="scene">
              <img src="./assets/ex-mirror.png" alt="">
              <div>
                <span class="tag">② 恭敬謙讓</span>
                <strong>排隊唔插隊</strong>
                <p>對師長、同學有禮；謙讓一步，衝突少咗，信任多咗。</p>
              </div>
            </div>
            <div class="scene">
              <img src="./assets/ex-dignity.png" alt="">
              <div>
                <span class="tag">③ 和為貴</span>
                <strong>吵完照一隊</strong>
                <p>班際比賽輸咗都唔互相怪責——和平安定先嚟玩得長。</p>
              </div>
            </div>
          </div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">三反其身 · 超實用</div>
          <h2>別人唔買帳？先照鏡</h2>
          <div class="hero-row">
            <div>
              <div class="bubble">「我對佢好好，點解佢疏遠我？」</div>
              <p class="lead" style="margin-top:16px">孟子教：愛人不親 → 反省「仁」夠唔夠真；管人唔掂 → 反省「智」；禮敬冇回禮 → 反省「敬」。</p>
              <div class="chip-row">
                <span class="chip">唔好即刻怪別人</span>
                <span class="chip">自己端正 → 關係先好</span>
              </div>
            </div>
            <img class="hero-art" src="./assets/ex-mirror.png" alt="">
          </div>
        </div>`
    },
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">舍生取義 · 比喻大對決</div>
          <h2>魚 VS 熊掌</h2>
          <div class="vs">
            <div class="side bad">
              <img src="./assets/ex-fishbear.png" alt="">
              <h3>魚 ≈ 生命</h3>
              <p>我想活、我想舒服、我想避麻煩</p>
            </div>
            <div class="mid">VS</div>
            <div class="side good">
              <img src="./assets/ex-dignity.png" alt="">
              <h3>熊掌 ≈ 義</h3>
              <p>誠信、公義、做人底線</p>
            </div>
          </div>
          <div class="quote">兩者唔可以一齊要？→ 舍生取義（守住義，唔係叫你亂送命）</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">今日校園版「取義」</div>
          <h2>你會揀邊邊？</h2>
          <div class="grid2">
            <div class="scene tap" data-tap>
              <img src="./assets/ex-fishbear.png" alt="">
              <div>
                <span class="tag">考試</span>
                <strong>好友要你傳答案</strong>
                <p>幫＝人情；拒絕＝得罪人。你點揀？</p>
                <div class="secret">取義：拒絕作弊，用其他方法幫温習 = 守誠信</div>
              </div>
            </div>
            <div class="scene tap" data-tap>
              <img src="./assets/ex-friends.png" alt="">
              <div>
                <span class="tag">操場</span>
                <strong>見到有人被欺負</strong>
                <p>裝冇睇見好安全；出聲可能麻煩。</p>
                <div class="secret">取義：通報老師／陪伴求助 = 義 > 怕事</div>
              </div>
            </div>
          </div>
          <div class="quote">撳格仔揭「取義」做法 · 匯報時可問全班舉手</div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">以德服人</div>
          <h2>班長對決：德 vs 力</h2>
          <div class="vs">
            <div class="side good">
              <img src="./assets/ex-devforce.png" alt="">
              <h3>德 · 王者路</h3>
              <p>真心、帶頭、公道 → 同學<strong>心悅誠服</strong></p>
            </div>
            <div class="mid">PK</div>
            <div class="side bad">
              <img src="./assets/ex-devforce.png" alt="">
              <h3>力 · 霸者路</h3>
              <p>恐嚇、罰、壓場 → 只係<strong>暫時屈服</strong></p>
            </div>
          </div>
        </div>`
    },
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">人格論</div>
          <div class="hero-row">
            <div>
              <h2>天賦尊嚴：你本來就有</h2>
              <p class="lead">憐憫之心 → 知善惡<br>羞恥之心 → 知該做／唔該做<br>→ 仁義 → 堂堂正正做人</p>
              <div class="chip-row">
                <span class="chip">成人之美</span>
                <span class="chip">言行一致</span>
                <span class="chip">唔走歪路</span>
              </div>
            </div>
            <img class="hero-art" src="./assets/ex-dignity.png" alt="">
          </div>
        </div>`
    },
    {
      tone: "light",
      html: `
        <div class="slide-inner">
          <div class="kicker">《孟子》速記</div>
          <h2>記住三個數就夠上台</h2>
          <div class="grid3">
            <div class="panel stat"><b>7</b><span>篇（上下）</span></div>
            <div class="panel stat"><b>261</b><span>章左右</span></div>
            <div class="panel stat"><b>語錄</b><span>言行記錄</span></div>
          </div>
          <div class="quote">下一頁：轉盤抽座號 → 問題彈出 → 提示已顯示 → 撳掣睇答案 → 5 秒自動返嚟</div>
        </div>`
    },
    {
      tone: "dark",
      html: `
        <div class="slide-inner">
          <div class="kicker">Game time</div>
          <h1>轉盤 · 彈出問答</h1>
          <p class="lead">1–30 真隨機抽人 → 問題＋提示即彈 → 同學答完 → 撳金色掣睇正確＋近似答案 → 倒數 5 秒自動返回轉盤再玩。</p>
          <p class="cta-note">撳右下「開始轉盤遊戲」即開波！</p>
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

  function wireTaps(root) {
    root.querySelectorAll("[data-tap]").forEach((el) => {
      el.addEventListener("click", () => el.classList.toggle("open"));
    });
  }

  function renderSlides() {
    deckEl.innerHTML = SLIDES.map(
      (s, i) =>
        `<article class="slide ${s.tone}${i === 0 ? " on" : ""}" data-i="${i}">${s.html}</article>`
    ).join("");
    wireTaps(deckEl);
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
      if (e.code === "Space" && !spinning && qModal.hidden && aModal.hidden) {
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
  let score = 0;
  let played = 0;

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
    }, 1400);
    const fx = document.getElementById("fx");
    const fctx = fx.getContext("2d");
    fx.width = innerWidth;
    fx.height = innerHeight;
    const parts = Array.from({ length: 80 }, () => ({
      x: fx.width / 2,
      y: fx.height * 0.4,
      vx: (Math.random() - 0.5) * 14,
      vy: -Math.random() * 12 - 2,
      life: 55 + randInt(35),
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
        fctx.globalAlpha = Math.max(0, p.life / 70);
        fctx.fillStyle = p.color;
        fctx.fillRect(p.x, p.y, p.s, p.s * 1.5);
      });
      frame++;
      if (frame < 85) requestAnimationFrame(loop);
      else fctx.clearRect(0, 0, fx.width, fx.height);
    })();
  }

  // ——— popups ———
  const qModal = document.getElementById("qModal");
  const aModal = document.getElementById("aModal");
  let qOrder = [];
  let qPos = -1;
  let current = null;
  let backTimer = null;
  let backRaf = null;

  function pickQuestion() {
    if (!qOrder.length || qPos >= qOrder.length - 1) {
      const bank = window.MX5_QUESTIONS || [];
      const weighted = [];
      bank.forEach((q) => {
        const w = q.diff === "easy" ? 3 : q.diff === "medium" ? 2 : 1;
        for (let i = 0; i < w; i++) weighted.push(q);
      });
      qOrder = shuffle(weighted);
      qPos = 0;
    } else qPos += 1;
    current = qOrder[qPos];
  }

  function openQuestionPopup() {
    pickQuestion();
    played += 1;
    document.getElementById("qIndex").textContent = String(played);
    document.getElementById("whoBadge").textContent = `座號 ${picked}`;
    const pill = document.getElementById("diffPill");
    pill.textContent = current.diff === "easy" ? "易" : current.diff === "medium" ? "中" : "難";
    pill.className = "pill" + (current.diff === "hard" ? " hard" : "");
    document.getElementById("qTitle").textContent = current.q;
    document.getElementById("hintText").textContent = current.hint;

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
          if (c === current.answer) {
            b.classList.add("good");
            score += 1;
            document.getElementById("scorePill").textContent = String(score);
          } else b.classList.add("bad");
        };
        box.appendChild(b);
      });
    } else {
      box.innerHTML =
        `<p style="opacity:.8;margin:0;line-height:1.5">開放題：請座號 ${picked} 用自己的話答（近似意思都算）。答完撳下面金色掣。</p>`;
    }

    aModal.hidden = true;
    qModal.hidden = false;
    celebrate();
  }

  function clearBackTimer() {
    if (backTimer) {
      clearTimeout(backTimer);
      backTimer = null;
    }
    if (backRaf) {
      cancelAnimationFrame(backRaf);
      backRaf = null;
    }
  }

  function returnToWheel() {
    clearBackTimer();
    qModal.hidden = true;
    aModal.hidden = true;
    document.getElementById("spinBtn").disabled = false;
  }

  function openAnswerPopup() {
    if (!current) return;
    qModal.hidden = true;
    document.getElementById("revealText").textContent = current.answer;
    document.getElementById("nearText").textContent = (current.near || []).join("　／　");
    document.getElementById("explainText").textContent = current.explain || "";
    aModal.hidden = false;
    celebrate();

    clearBackTimer();
    const bar = document.getElementById("cdBar");
    const label = document.getElementById("countdown");
    const total = 5000;
    const t0 = performance.now();
    function tickCd(now) {
      const left = Math.max(0, total - (now - t0));
      const sec = Math.ceil(left / 1000);
      label.textContent = `${sec} 秒後返回轉盤`;
      bar.style.transform = `scaleX(${left / total})`;
      if (left > 0) backRaf = requestAnimationFrame(tickCd);
    }
    bar.style.transform = "scaleX(1)";
    backRaf = requestAnimationFrame(tickCd);
    backTimer = setTimeout(returnToWheel, total);
  }

  document.getElementById("showAnswerBtn").onclick = openAnswerPopup;
  document.getElementById("backNowBtn").onclick = returnToWheel;

  function spin() {
    if (spinning || numbers.length < 2) return;
    if (!qModal.hidden || !aModal.hidden) return;
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
      ((Math.PI * 2) -
        (winIdx * arc + arc * (0.25 + Math.random() * 0.5)) -
        (rotation % (Math.PI * 2)));
    const start = rotation;
    const dur = 4500;
    const t0 = performance.now();
    let lastSeg = -1;
    const ease = (t) => 1 - Math.pow(1 - t, 4);
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
        picked = numbers[winnerIndex()];
        document.getElementById("pickedNum").textContent = picked;
        hub.classList.add("win");
        openQuestionPopup();
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

  renderSlides();
  drawWheel();
})();
