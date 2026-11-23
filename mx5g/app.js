(() => {
  "use strict";

  // Fallback if questions.js fails to load
  const FALLBACK_QS = [
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

  function bank() {
    const q = window.MX5_QUESTIONS;
    return Array.isArray(q) && q.length ? q : FALLBACK_QS;
  }

  const SLIDES = [
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">3G · 第5組</div>
        <div class="hero-row">
          <div>
            <h1>孟子其實好「校園」</h1>
            <p class="lead">仁愛謙和、舍生取義、天賦尊嚴——用生活例子講明，再轉盤抽人問答。</p>
            <div class="chip-row"><span class="chip">有情境</span><span class="chip">有對決</span><span class="chip">有轉盤</span></div>
          </div>
          <img class="hero-art" src="./assets/char-student.png" alt="">
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">開場挑戰</div>
        <h2>如果你係班長，點算？</h2>
        <div class="grid2">
          <div class="scene tap" data-tap>
            <img src="./assets/char-fist.png" alt="">
            <div><span class="tag">情境 A</span><strong>用大聲嚇到全班聽話</strong>
            <p>「再嘈就扣分！」即刻靜——但心裏面翻白眼。</p>
            <div class="secret">= 以力服人（暫時屈服）</div></div>
          </div>
          <div class="scene tap" data-tap>
            <img src="./assets/char-student.png" alt="">
            <div><span class="tag">情境 B</span><strong>講清楚、聽意見、帶頭做</strong>
            <p>同學覺得你公道，自願配合。</p>
            <div class="secret">= 以德服人（心悅誠服）</div></div>
          </div>
        </div>
        <div class="quote">撳上面兩格睇答案 → 君子應該以德服人</div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">仁愛謙和 · 校園版</div>
        <h2>三個場面，三個重點</h2>
        <div class="grid3">
          <div class="scene"><img src="./assets/char-book.png" alt=""><div>
            <span class="tag">① 仁愛</span><strong>借筆記唔係施捨</strong>
            <p>主動分享，因為仁愛，唔係換名氣。</p></div></div>
          <div class="scene"><img src="./assets/char-mirror.png" alt=""><div>
            <span class="tag">② 恭敬謙讓</span><strong>排隊唔插隊</strong>
            <p>有禮謙讓 → 衝突少、信任多。</p></div></div>
          <div class="scene"><img src="./assets/char-heart.png" alt=""><div>
            <span class="tag">③ 和為貴</span><strong>吵完照一隊</strong>
            <p>輸比賽都唔互相怪責。</p></div></div>
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">三反其身</div>
        <h2>別人唔買帳？先照鏡</h2>
        <div class="hero-row">
          <div>
            <div class="bubble">「我對佢好好，點解疏遠我？」</div>
            <p class="lead" style="margin-top:14px">愛人不親→反省仁；管人唔掂→反省智；禮敬冇回禮→反省敬。</p>
            <div class="chip-row"><span class="chip">唔好即刻怪別人</span><span class="chip">自己端正先</span></div>
          </div>
          <img class="hero-art" src="./assets/char-mirror.png" alt="">
        </div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">舍生取義</div>
        <h2>魚 VS 熊掌</h2>
        <div class="vs">
          <div class="side bad"><img src="./assets/char-fish.png" alt=""><h3>魚 ≈ 生命</h3><p>想活、想舒服、想避麻煩</p></div>
          <div class="mid">VS</div>
          <div class="side good"><img src="./assets/char-bear.png" alt=""><h3>熊掌 ≈ 義</h3><p>誠信、公義、做人底線</p></div>
        </div>
        <div class="quote">唔可以一齊要？→ 舍生取義（守義，唔係亂送命）</div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">校園版取義</div>
        <h2>你會揀邊邊？（撳格揭曉）</h2>
        <div class="grid2">
          <div class="scene tap" data-tap>
            <img src="./assets/char-fish.png" alt="">
            <div><span class="tag">考試</span><strong>好友要你傳答案</strong>
            <p>幫＝人情；拒絕＝得罪人？</p>
            <div class="secret">取義：拒絕作弊，改為幫温習</div></div>
          </div>
          <div class="scene tap" data-tap>
            <img src="./assets/char-student.png" alt="">
            <div><span class="tag">操場</span><strong>見到有人被欺負</strong>
            <p>裝冇睇見好安全？</p>
            <div class="secret">取義：通報老師／陪伴求助</div></div>
          </div>
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">以德服人</div>
        <h2>班長對決：德 vs 力</h2>
        <div class="vs">
          <div class="side good"><img src="./assets/char-crown.png" alt=""><h3>德 · 王者</h3><p>真心帶頭 → <strong>心悅誠服</strong></p></div>
          <div class="mid">PK</div>
          <div class="side bad"><img src="./assets/char-fist.png" alt=""><h3>力 · 霸者</h3><p>恐嚇壓場 → <strong>暫時屈服</strong></p></div>
        </div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">人格論</div>
        <div class="hero-row">
          <div>
            <h2>天賦尊嚴</h2>
            <p class="lead">憐憫→知善惡<br>羞恥→知該／唔該做<br>→仁義→堂堂正正</p>
            <div class="chip-row"><span class="chip">成人之美</span><span class="chip">言行一致</span></div>
          </div>
          <img class="hero-art" src="./assets/char-heart.png" alt="">
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">《孟子》速記</div>
        <h2>三個數就夠上台</h2>
        <div class="grid3">
          <div class="panel stat"><b>7</b><span>篇（上下）</span></div>
          <div class="panel stat"><b>261</b><span>章左右</span></div>
          <div class="panel stat"><b>語錄</b><span>言行記錄</span></div>
        </div>
        <div class="quote">下一頁：筆記理據（衝內容分）</div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">內容分 · 理據</div>
        <h2>上台一定要講到嘅句</h2>
        <div class="grid2">
          <div class="panel"><h3>舍生取義</h3>
            <p>「生，亦我所欲也；義，亦我所欲也。二者不可得兼，舍生而取義。」（《孟子·告子上》）</p></div>
          <div class="panel"><h3>三反其身</h3>
            <p>愛人不親→反省仁；治人不得→反省智；禮人不答→反省敬。先求諸己。</p></div>
          <div class="panel"><h3>以德服人</h3>
            <p>德→心悅誠服；力→暫時屈服。君子以德服人。</p></div>
          <div class="panel"><h3>天賦尊嚴</h3>
            <p>憐憫＋羞恥→仁義→尊嚴人格；君子成人之美、言行一致。</p></div>
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">動畫複習（可邊播邊講）</div>
        <h2>五段 GIF · 對住 SCRIPT.md</h2>
        <div class="grid3" style="align-items:start">
          <div class="panel" style="text-align:center"><img src="./anim/01_de_vs_li.gif" alt="" style="width:100%;border-radius:10px"><p>德 vs 力</p></div>
          <div class="panel" style="text-align:center"><img src="./anim/02_ren_ai.gif" alt="" style="width:100%;border-radius:10px"><p>仁愛謙和</p></div>
          <div class="panel" style="text-align:center"><img src="./anim/04_yu_xiong.gif" alt="" style="width:100%;border-radius:10px"><p>舍生取義</p></div>
        </div>
        <div class="quote">完整講稿：SCRIPT.md　高分攻略：HIGH_MARKS.md</div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">Game</div>
        <h1>轉盤 · 彈出問答</h1>
        <p class="lead">1–30 真隨機 → 問題＋提示彈出 → 金色掣睇正確＋近似答案 → 5 秒自動返回。</p>
        <p class="cta-note">撳右下「開始轉盤遊戲」！</p>
        <div class="motif"></div>
      </div>`
    }
  ];

  const $ = (id) => document.getElementById(id);
  const deckEl = $("deck");
  const gameEl = $("game");
  const deckNav = $("deckNav");
  const qModal = $("qModal");
  const aModal = $("aModal");
  const canvas = $("wheel");
  const ctx = canvas.getContext("2d");

  let idx = 0;
  let mode = "deck";
  let spinning = false;
  let rotation = 0;
  let numbers = Array.from({ length: 30 }, (_, i) => i + 1);
  let picked = null;
  let score = 0;
  let played = 0;
  let qOrder = [];
  let qPos = -1;
  let current = null;
  let backTimer = null;
  let backRaf = null;
  let intendedWin = 0;

  const COLORS = ["#1f7a55","#245c48","#c44b3c","#8a3a30","#d4a017","#9a7510","#2f6f8f","#1f4f66","#3d8b6e","#5a6b63"];

  function show(el) { el.classList.remove("is-hide"); }
  function hide(el) { el.classList.add("is-hide"); }
  function isHidden(el) { return el.classList.contains("is-hide"); }

  function wireTaps(root) {
    root.querySelectorAll("[data-tap]").forEach((el) => {
      el.onclick = () => el.classList.toggle("open");
    });
  }

  function renderSlides() {
    deckEl.innerHTML = SLIDES.map(
      (s, i) => `<article class="slide ${s.tone}${i === 0 ? " on" : ""}">${s.html}</article>`
    ).join("");
    wireTaps(deckEl);
    updateDeckUI();
  }

  function updateDeckUI() {
    const slides = deckEl.querySelectorAll(".slide");
    slides.forEach((el, i) => el.classList.toggle("on", i === idx));
    $("pageLabel").textContent = `${idx + 1} / ${SLIDES.length}`;
    $("progressBar").style.width = `${((idx + 1) / SLIDES.length) * 100}%`;
  }

  function setMode(next) {
    mode = next;
    $("modeDeck").classList.toggle("on", mode === "deck");
    $("modeGame").classList.toggle("on", mode === "game");
    if (mode === "deck") {
      show(deckEl);
      hide(gameEl);
      deckNav.classList.remove("is-hide");
      hide(qModal);
      hide(aModal);
    } else {
      hide(deckEl);
      show(gameEl);
      deckNav.classList.add("is-hide");
      drawWheel();
    }
  }

  $("modeDeck").onclick = () => setMode("deck");
  $("modeGame").onclick = () => setMode("game");
  $("prevBtn").onclick = () => {
    idx = Math.max(0, idx - 1);
    updateDeckUI();
  };
  $("nextBtn").onclick = () => {
    if (idx < SLIDES.length - 1) {
      idx += 1;
      updateDeckUI();
    } else setMode("game");
  };
  $("toGameBtn").onclick = () => setMode("game");

  function randInt(max) {
    if (max <= 0) return 0;
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

  let audioCtx = null;
  function tickSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const o = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      o.frequency.value = 700 + randInt(200);
      g.gain.value = 0.035;
      o.connect(g);
      g.connect(audioCtx.destination);
      o.start();
      g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
      o.stop(audioCtx.currentTime + 0.06);
    } catch (_) {}
  }

  function celebrate() {
    const burst = $("burstImg");
    const conf = $("confettiImg");
    burst.classList.add("show");
    conf.classList.add("show");
    burst.src = "./assets/burst.gif?" + Date.now();
    setTimeout(() => {
      burst.classList.remove("show");
      conf.classList.remove("show");
    }, 1200);
  }

  function pickQuestion() {
    const b = bank();
    if (!qOrder.length || qPos >= qOrder.length - 1) {
      const weighted = [];
      b.forEach((q) => {
        const w = q.diff === "easy" ? 3 : q.diff === "medium" ? 2 : 1;
        for (let i = 0; i < w; i++) weighted.push(q);
      });
      qOrder = shuffle(weighted.length ? weighted : FALLBACK_QS);
      qPos = 0;
    } else qPos += 1;
    current = qOrder[qPos] || FALLBACK_QS[0];
  }

  function openQuestionPopup() {
    try {
      pickQuestion();
      if (!current) current = FALLBACK_QS[0];
      played += 1;
      $("playedPill").textContent = String(played);
      $("whoBadge").textContent = `座號 ${picked}`;
      const pill = $("diffPill");
      const d = current.diff || "easy";
      pill.textContent = d === "easy" ? "易" : d === "medium" ? "中" : "難";
      pill.className = "pill" + (d === "hard" ? " hard" : "");
      $("qTitle").textContent = current.q || "問題";
      $("hintText").textContent = current.hint || "想想筆記重點。";

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
      } else {
        box.innerHTML = `<p style="opacity:.85;margin:0;line-height:1.5">開放題：請座號 ${picked} 用自己的話答。答完撳金色掣。</p>`;
      }

      hide(aModal);
      show(qModal);
      celebrate();
    } catch (err) {
      console.error(err);
      $("spinBtn").disabled = false;
      alert("出題出錯，已重設。再轉一次。");
    }
  }

  function clearBackTimer() {
    if (backTimer) clearTimeout(backTimer);
    if (backRaf) cancelAnimationFrame(backRaf);
    backTimer = null;
    backRaf = null;
  }

  function returnToWheel() {
    clearBackTimer();
    hide(qModal);
    hide(aModal);
    $("spinBtn").disabled = false;
  }

  function openAnswerPopup() {
    if (!current) current = FALLBACK_QS[0];
    hide(qModal);
    $("revealText").textContent = current.answer || "";
    $("nearText").textContent = (current.near || []).join("　／　");
    $("explainText").textContent = current.explain || "";
    show(aModal);
    celebrate();

    clearBackTimer();
    const bar = $("cdBar");
    const label = $("countdown");
    const total = 5000;
    const t0 = performance.now();
    bar.style.transform = "scaleX(1)";
    function tickCd(now) {
      const left = Math.max(0, total - (now - t0));
      label.textContent = `${Math.ceil(left / 1000)} 秒後返回轉盤`;
      bar.style.transform = `scaleX(${left / total})`;
      if (left > 0) backRaf = requestAnimationFrame(tickCd);
    }
    backRaf = requestAnimationFrame(tickCd);
    backTimer = setTimeout(returnToWheel, total);
  }

  $("showAnswerBtn").onclick = openAnswerPopup;
  $("backNowBtn").onclick = returnToWheel;

  function spin() {
    if (spinning || numbers.length < 2) return;
    if (!isHidden(qModal) || !isHidden(aModal)) return;
    spinning = true;
    $("spinBtn").disabled = true;
    $("hub").classList.remove("win");

    const n = numbers.length;
    intendedWin = randInt(n);
    const arc = (Math.PI * 2) / n;
    // Pointer at top (-PI/2). Land near center of intended segment.
    const land =
      (Math.PI * 2) -
      (intendedWin * arc + arc * 0.5) -
      (rotation % (Math.PI * 2));
    const extra = (5 + Math.random() * 3) * Math.PI * 2;
    const target = extra + ((land % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
    const start = rotation;
    const dur = 4200;
    const t0 = performance.now();
    let lastSeg = -1;
    const ease = (t) => 1 - Math.pow(1 - t, 4);

    function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      rotation = start + target * ease(p);
      drawWheel();
      const seg = Math.floor((((Math.PI * 2) - ((rotation + Math.PI / 2) % (Math.PI * 2))) % (Math.PI * 2)) / arc) % n;
      if (seg !== lastSeg) {
        tickSound();
        lastSeg = seg;
      }
      if (p < 1) requestAnimationFrame(frame);
      else {
        spinning = false;
        // Force exact intended winner (true random already chosen)
        picked = numbers[intendedWin];
        // Snap rotation so intended segment is under pointer
        rotation = (Math.PI * 2) - (intendedWin * arc + arc * 0.5) - Math.PI / 2;
        // normalize visually via redraw with consistent formula used in drawWheel
        rotation = rotation - Math.floor(rotation / (Math.PI * 2)) * (Math.PI * 2);
        drawWheel();
        $("pickedNum").textContent = String(picked);
        $("hub").classList.add("win");
        openQuestionPopup();
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

  window.addEventListener("keydown", (e) => {
    if (mode === "deck") {
      if (e.key === "ArrowRight" || e.key === " ") {
        e.preventDefault();
        $("nextBtn").click();
      }
      if (e.key === "ArrowLeft") $("prevBtn").click();
      return;
    }
    if (e.code === "Space" && !spinning && isHidden(qModal) && isHidden(aModal)) {
      e.preventDefault();
      spin();
    }
  });

  // boot
  try {
    renderSlides();
    drawWheel();
    hide(qModal);
    hide(aModal);
    console.log("[mx5g] ready · questions:", bank().length);
  } catch (err) {
    console.error(err);
    document.body.insertAdjacentHTML(
      "afterbegin",
      `<p style="color:#fff;padding:20px;background:#c44b3c">載入失敗：${String(err)}</p>`
    );
  }
})();
