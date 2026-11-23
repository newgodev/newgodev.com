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

  const MENG_LINES = [
    "仁愛謙和：仁愛、恭敬謙讓、和為貴。",
    "三反其身：行有不得，皆反求諸己。",
    "舍生取義：義禮比生命更重要（守底線）。",
    "以德服人：心悅誠服；以力服人：暫時屈服。",
    "憐憫之心＋羞恥之心 → 尊嚴人格。"
  ];

  const SLIDES = [
    {
      tone: "dark",
      html: `<div class="hero-split">
        <div class="hero-copy">
          <div class="kicker">3G 第5組 · 中文單元二</div>
          <h1>孟子：仁愛謙和</h1>
          <p class="lead">仁愛謙和 · 三反其身 · 舍生取義 · 以德服人 · 天賦尊嚴<br>
          用校園例子講清楚四字詞同理據。撳「全螢幕」後用下一頁繼續。</p>
          <div class="chip-row" style="margin-top:8px">
            <span class="chip">古典畫像 · 無人臉照片</span>
            <span class="chip">內容＋理據</span>
            <span class="chip">全螢幕（iPad 適用）</span>
          </div>
          <p class="click-hint">提示：撳「全螢幕」→ 下一頁</p>
        </div>
        <div class="hero-media">
          <img src="./assets/photo-mencius.png" alt="孟子古典畫像">
          <div class="cap">孟子（孟軻）· 古典半身畫像</div>
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner map-slide">
        <div class="kicker">範圍地圖 · 每點有解釋＋校園例子</div>
        <h2>第5組重點一覽</h2>
        <div class="map-grid">
          <article class="map-card">
            <h3>仁愛謙和</h3>
            <p class="map-ex"><b>解釋：</b>對人有仁愛、恭敬謙讓，以和為貴。</p>
            <p class="map-eg"><b>例子：</b>同學欠筆記你主動 share；排隊唔插隊；比賽輸咗都唔互怪。</p>
          </article>
          <article class="map-card">
            <h3>三反其身</h3>
            <p class="map-ex"><b>解釋：</b>事情唔順利，先反省自己有冇仁、智、敬。</p>
            <p class="map-eg"><b>例子：</b>朋友疏遠你 → 唔好先鬧佢，先問自己有冇做得唔夠好。</p>
          </article>
          <article class="map-card">
            <h3>舍生取義</h3>
            <p class="map-ex"><b>解釋：</b>魚＝生命／舒服；熊掌＝義。兩者唔能兼得就取義。</p>
            <p class="map-eg"><b>例子：</b>寧願自己溫書，都唔抄功課；見人被欺負要出聲。</p>
          </article>
          <article class="map-card">
            <h3>以德服人 vs 以力服人</h3>
            <p class="map-ex"><b>解釋：</b>德服→心悅誠服（長久）；力服→暫時屈服（唔真心）。</p>
            <p class="map-eg"><b>例子：</b>班長靠公道帶頭 vs 靠罰分恐嚇同學聽話。</p>
          </article>
          <article class="map-card">
            <h3>人格論 · 天賦尊嚴</h3>
            <p class="map-ex"><b>解釋：</b>人人天生有尊嚴；憐憫之心＋羞恥之心→仁義。</p>
            <p class="map-eg"><b>例子：</b>見人跌倒想扶＝惻隱；覺得抄襲唔對＝羞惡之心。</p>
          </article>
          <article class="map-card">
            <h3>君子美德 ·《孟子》</h3>
            <p class="map-ex"><b>解釋：</b>成人之美、言行一致；著作《孟子》七篇語錄。</p>
            <p class="map-eg"><b>例子：</b>幫同學進步而唔踩低佢；講到做到，唔講一套做一套。</p>
          </article>
        </div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">開場互動 · 全班投票</div>
        <h2>如果你是班長，你揀邊種？</h2>
        <p class="lead">撳左邊或右邊作答。</p>
        <div class="vs-pick">
          <button type="button" class="force-card" data-force>
            <img src="./assets/photo-hand.png?v=20251123j" alt="純劍一揮 · 綠墨血 · 以力服人">
            <h3>以力服人</h3>
            <p>靠武力／恐嚇強迫 → 暴力<br>→ <strong>暫時屈服</strong></p>
          </button>
          <div class="vs-mid">VS</div>
          <button type="button" class="virtue-card" data-virtue>
            <img src="./assets/photo-mencius.png" alt="孟子古典畫像 · 德">
            <h3>以德服人</h3>
            <p>公道／帶頭／聽意見<br>→ <strong>心悅誠服</strong></p>
          </button>
        </div>
        <div class="quote proof" data-vote-msg>孟子：君子應該以德服人，不是只靠外力強迫。（撳卡先）</div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">仁愛謙和 · 校園三場面</div>
        <h2>一個精神，三種做法</h2>
        <div class="grid3 ren-grid">
          <div class="scene scene-tall tap" data-tap>
            <img src="./assets/photo-book.png?v=20251123m" alt="古典書冊圖">
            <div>
              <span class="tag">① 仁愛</span>
              <strong>分享筆記</strong>
              <p>同學欠筆記你主動分享——心存仁愛，不是換名氣。</p>
              <div class="secret">重點：分享筆記＝仁愛；只分享答案唔夠。</div>
            </div>
          </div>
          <div class="scene scene-tall tap" data-tap>
            <img src="./assets/photo-pupils.png?v=20251123m" alt="古典教子畫">
            <div>
              <span class="tag">② 恭敬謙讓</span>
              <strong>排隊有禮</strong>
              <p>對師長同學恭敬謙讓 → 得信任、少衝突。</p>
              <div class="secret">重點：對人有禮＝恭敬謙讓。</div>
            </div>
          </div>
          <div class="scene scene-tall tap" data-tap>
            <img src="./assets/photo-loom.png?v=20251123m" alt="孟母斷機古典畫">
            <div>
              <span class="tag">③ 和為貴</span>
              <strong>輸完仍一隊</strong>
              <p>班際比賽輸了也不互怪。和平安定靠仁愛之心。</p>
              <div class="secret">重點：互撐＝和為貴。</div>
            </div>
          </div>
        </div>
        <div class="quote">沒有愛人的心 → 難有符合義禮的行為 → 難達和平安定</div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner sanfan-stage">
        <div class="kicker">三反其身 · 撳鏡看動畫</div>
        <h2>別人唔買帳？先照銅鏡</h2>
        <p class="lead click-hint" data-mirror-hint>👉 撳右邊漢代銅鏡 —— 裂開後彈出三個校園例子</p>
        <div class="sanfan-layout">
          <div class="mirror-zone" data-mirror tabindex="0" role="button" aria-label="撳鏡反省">
            <img src="./assets/photo-mirror.png?v=20251123k" alt="漢代青銅鏡 · 自我反省">
            <div class="mirror-tap">撳我反省</div>
            <div class="crack-msg">鏡光一閃：先反求諸己，唔好先鬧人。</div>
            <div class="mirror-shine" aria-hidden="true"></div>
          </div>
          <div class="reflect-stack" data-reflect-stack>
            <article class="reflect-card" data-reflect>
              <h3>① 仁</h3>
              <p><b>愛人不親</b> → 反省仁愛夠唔夠真</p>
              <p class="eg">例子：成日幫人抄功課但唔聽心事 → 疏遠你＝仁愛得表面</p>
            </article>
            <article class="reflect-card" data-reflect>
              <h3>② 智</h3>
              <p><b>管人管不好</b> → 反省夠唔夠智</p>
              <p class="eg">例子：組長派工亂、死線唔清 → 組員喊＝先改計劃</p>
            </article>
            <article class="reflect-card" data-reflect>
              <h3>③ 敬</h3>
              <p><b>禮敬沒回禮</b> → 反省恭敬夠唔夠</p>
              <p class="eg">例子：借筆記唔道謝仲嘲笑人 → 下次冇人理＝欠敬</p>
            </article>
          </div>
        </div>
        <div class="quote">行有不得，皆反求諸己。——自己端正了，別人才較易靠近你。</div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner gag-stage">
        <div class="kicker">舍生取義 · 擂台對決</div>
        <h2>魚 VS 熊掌 —— 撳邊邊贏？</h2>
        <p class="lead">玩法：狂撳你撐嘅一邊。孟子會宣判真正贏家（劇透：義）。</p>
        <div class="fight-arena">
          <div class="fighter fish" data-fight="fish">
            <img src="./assets/photo-fish.png" alt="魚：水墨畫風">
            <h3>魚 ≈ 生命／舒服</h3>
            <p>想避麻煩、少得罪人</p>
            <span class="chip" data-fish-hp>氣勢 0</span>
          </div>
          <div class="fighter bear" data-fight="bear">
            <img src="./assets/photo-bear.png" alt="熊 · 古典木刻">
            <h3>熊掌 ≈ 義</h3>
            <p>誠信、公義、做人底線</p>
            <span class="chip" data-bear-hp>氣勢 0</span>
          </div>
        </div>
        <div class="quote proof" data-fight-msg>「二者不可得兼，舍生而取義。」（《孟子·告子上》）—— 先打一場再講</div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner">
        <div class="kicker">校園版取義 · 撳格揭曉</div>
        <h2>兩個場面，你會點揀？（班房爆笑位）</h2>
        <div class="grid2 eq">
          <div class="scene tap" data-tap>
            <img src="./assets/photo-book.png" alt="">
            <div>
              <span class="tag">考試</span>
              <strong>好友要你傳答案</strong>
              <p>幫＝人情；拒絕＝得罪人。孟子會點睇？</p>
              <div class="secret">取義：拒絕作弊，改為幫温習＝守誠信（義 &gt; 避麻煩）<br><span class="stamp">孟子蓋章：合格</span></div>
            </div>
          </div>
          <div class="scene tap" data-tap>
            <img src="./assets/photo-loom.png" alt="古典畫">
            <div>
              <span class="tag">操場</span>
              <strong>見到有人被欺負</strong>
              <p>裝看不見較安全；出聲可能麻煩。</p>
              <div class="secret">取義：通報老師／陪伴求助＝義 &gt; 怕事<br><span class="stamp">君子認證</span></div>
            </div>
          </div>
        </div>
        <div class="quote">不是叫人亂送命，而是價值排序：義禮重要過只顧舒服。</div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner gag-stage">
        <div class="kicker">以德服人 · 逐句 unlock</div>
        <h2>王者路 vs 霸者路（撳掣出重點）</h2>
        <div class="chip-row">
          <button type="button" class="gag-btn" data-reveal-next>下一句重點 →</button>
          <span class="click-hint" data-reveal-count>0 / 4</span>
        </div>
        <div class="reveal-stack" data-reveal-stack>
          <div class="reveal-line">德 · 王者：出於仁愛真心 → 對方<strong>心悅誠服</strong></div>
          <div class="reveal-line">力 · 霸者：假借仁義、用武力 → 只是<strong>暫時屈服</strong></div>
          <div class="reveal-line">校園翻譯：罰分可以噤聲，但唔可以令人真心跟你。</div>
          <div class="reveal-line">匯報金句：<strong>心服才長久，力屈只一時。</strong></div>
        </div>
        <div class="grid2" style="flex:0;margin-top:8px">
          <div class="img-frame" style="min-height:160px"><img src="./assets/photo-mencius2.png" alt="孟子古典畫"></div>
          <div class="img-frame" style="min-height:160px"><img src="./assets/photo-students.png" alt="古典教子畫"></div>
        </div>
      </div>`
    },
    {
      tone: "light",
      html: `<div class="slide-inner gag-stage">
        <div class="kicker">人格論 · 頁14</div>
        <h2>天賦尊嚴（撳卡開重點）</h2>
        <div class="grid2">
          <div class="joke-board">
            <div class="joke-card" data-joke>
              <div class="setup">憐憫之心 → 知善惡</div>
              <div class="punch">見同學跌倒你想扶＝惻隱；見人抄襲你覺得怪＝羞惡開始發光。</div>
            </div>
            <div class="joke-card" data-joke>
              <div class="setup">羞恥之心 → 知該做／不該做</div>
              <div class="punch">孟子：有羞恥先有底線；冇底線就只剩「我以為冇人知」。</div>
            </div>
            <div class="joke-card" data-joke>
              <div class="setup">仁義之心 → 尊嚴人格</div>
              <div class="punch">君子要堂堂正正：成人之美、言行一致、不走歪路。</div>
            </div>
            <div class="joke-card" data-joke>
              <div class="setup">記住這句</div>
              <div class="punch">憐憫＋羞恥 → 尊嚴人格。請舉手複述一次。</div>
            </div>
          </div>
          <div class="hero-media" style="border-radius:16px;min-height:280px">
            <img src="./assets/photo-heart.png" alt="古典畫：心性／九歌意象">
            <div class="cap">古典畫意象 · 唔用真人臉 · 唔用 emoji</div>
          </div>
        </div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="slide-inner">
        <div class="kicker">代表著作 · 速記＋理據</div>
        <h2>《孟子》速記（老師愛聽呢啲）</h2>
        <div class="grid3">
          <div class="panel stat"><b>7</b><span>篇（各分上下）</span></div>
          <div class="panel stat"><b>261</b><span>章左右</span></div>
          <div class="panel stat"><b>語錄</b><span>記錄言行</span></div>
        </div>
        <div class="grid2" style="flex:1;min-height:0;margin-top:8px">
          <div class="panel"><h3>上台必講</h3>
            <ul>
              <li>舍生取義原文出自《孟子·告子上》</li>
              <li>德服／力服對比 → 心悅誠服 vs 暫時屈服</li>
              <li>三反其身：仁／智／敬</li>
              <li>憐憫＋羞恥 → 尊嚴人格</li>
            </ul>
            <p style="margin-top:10px">記數字可以，但要識解釋「點解緊要」。</p>
          </div>
          <div class="img-frame cover"><img src="./assets/photo-loom.png" alt="孟母教子典故圖像"></div>
        </div>
      </div>`
    },
    {
      tone: "dark",
      html: `<div class="hero-split">
        <div class="hero-copy">
          <div class="kicker">Game time</div>
          <h1>轉盤抽人問答</h1>
          <p class="lead">1–30 真隨機抽座號 → 問題＋提示彈出 → 撳金色掣睇正確答案同近似答案 → 5 秒自動返回轉盤。</p>
          <p class="cta-note">撳右下「開始轉盤遊戲」！被抽中唔好喊——孟子話呢個叫「鍛鍊膽識」。</p>
        </div>
        <div class="hero-media">
          <img src="./assets/photo-students.png" alt="古典教子畫">
          <div class="cap">全班一起玩 · 近似答案也算對 · 古典畫</div>
        </div>
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
  let mengI = 0;
  let roastI = 0;
  let fishHp = 0;
  let bearHp = 0;
  let laugh = 12;

  const COLORS = ["#1f7a55","#245c48","#c44b3c","#8a3a30","#d4a017","#9a7510","#2f6f8f","#1f4f66","#3d8b6e","#5a6b63"];

  function show(el) { el.classList.remove("is-hide"); }
  function hide(el) { el.classList.add("is-hide"); }
  function isHidden(el) { return el.classList.contains("is-hide"); }

  function wireTaps(root) {
    root.querySelectorAll("[data-tap]").forEach((el) => {
      el.onclick = () => el.classList.toggle("open");
    });
  }

  function wireComedy(root) {
    // Mencius floating host
    root.querySelectorAll("[data-meng-host]").forEach((host) => {
      host.style.pointerEvents = "auto";
      host.style.cursor = "pointer";
      const line = host.querySelector("[data-meng-line]");
      host.onclick = (e) => {
        e.stopPropagation();
        mengI = (mengI + 1) % MENG_LINES.length;
        if (line) line.textContent = MENG_LINES[mengI];
        celebrate();
      };
    });

    // Fake bug boot on title
    root.querySelectorAll("[data-bug-boot]").forEach((btn) => {
      btn.onclick = () => {
        const host = root.querySelector("[data-meng-line]");
        if (host) host.textContent = "簡報開始。請專心聽重點。";
        btn.textContent = "✓ 已開始";
        celebrate();
      };
    });

    // Force vs virtue
    root.querySelectorAll("[data-force]").forEach((el) => {
      el.onclick = () => {
        el.classList.add("fall");
        const v = root.querySelector("[data-virtue]");
        if (v) v.classList.add("glow");
        const msg = root.querySelector("[data-vote-msg]");
        if (msg) msg.textContent = "力服跌倒了：暫時屈服冇用。孟子宣判——以德服人勝！";
        celebrate();
      };
    });
    root.querySelectorAll("[data-virtue]").forEach((el) => {
      el.onclick = () => {
        el.classList.add("glow");
        const f = root.querySelector("[data-force]");
        if (f) f.classList.add("fall");
        const msg = root.querySelector("[data-vote-msg]");
        if (msg) msg.textContent = "正確：以德服人 → 心悅誠服。";
        celebrate();
      };
    });

    // Mirror crack + staggered reflect cards
    root.querySelectorAll("[data-mirror]").forEach((el) => {
      const run = () => {
        el.classList.add("crack");
        const cards = root.querySelectorAll("[data-reflect]");
        cards.forEach((c) => c.classList.remove("show"));
        // force reflow then stagger in
        void el.offsetWidth;
        cards.forEach((c, i) => {
          setTimeout(() => c.classList.add("show"), 120 + i * 160);
        });
        const hint = root.querySelector("[data-mirror-hint]");
        if (hint) hint.textContent = "✓ 三面鏡已開：仁／智／敬 —— 再撳可重播動畫";
        celebrate();
      };
      el.onclick = () => {
        if (el.classList.contains("crack")) {
          el.classList.remove("crack");
          root.querySelectorAll("[data-reflect]").forEach((c) => c.classList.remove("show"));
          setTimeout(run, 80);
        } else run();
      };
    });

    // Fish vs bear fight
    let fightOver = false;
    root.querySelectorAll("[data-fight]").forEach((el) => {
      el.onclick = () => {
        if (fightOver) return;
        const side = el.getAttribute("data-fight");
        el.classList.remove("hit");
        void el.offsetWidth;
        el.classList.add("hit");
        if (side === "fish") {
          fishHp += 1;
          const hp = root.querySelector("[data-fish-hp]");
          if (hp) hp.textContent = `氣勢 ${fishHp}`;
        } else {
          bearHp += 1;
          const hp = root.querySelector("[data-bear-hp]");
          if (hp) hp.textContent = `氣勢 ${bearHp}`;
        }
        const total = fishHp + bearHp;
        if (total >= 5) {
          fightOver = true;
          const fish = root.querySelector('[data-fight="fish"]');
          const bear = root.querySelector('[data-fight="bear"]');
          if (fish) { fish.classList.add("lose"); fish.classList.remove("win"); }
          if (bear) { bear.classList.add("win"); bear.classList.remove("lose"); }
          const msg = root.querySelector("[data-fight-msg]");
          if (msg) msg.textContent = "裁判孟子：就算魚氣勢高，最後都要舍生取義——熊掌（義）勝！";
          celebrate();
        }
      };
    });

    // Reveal stack
    root.querySelectorAll("[data-reveal-next]").forEach((btn) => {
      let step = 0;
      const lines = root.querySelectorAll("[data-reveal-stack] .reveal-line");
      const count = root.querySelector("[data-reveal-count]");
      btn.onclick = () => {
        if (step < lines.length) {
          lines[step].classList.add("show");
          step += 1;
          if (count) count.textContent = `${step} / ${lines.length}`;
          if (step === lines.length) celebrate();
        } else {
          lines.forEach((l) => l.classList.remove("show"));
          step = 0;
          if (count) count.textContent = `0 / ${lines.length}`;
        }
      };
    });

    // Joke cards + laugh meter
    root.querySelectorAll("[data-joke]").forEach((card) => {
      card.onclick = () => {
        card.classList.toggle("open");
        if (card.classList.contains("open")) {
          laugh = Math.min(100, laugh + 22);
          const bar = root.querySelector("[data-laugh]");
          if (bar) bar.style.width = laugh + "%";
        }
      };
    });

    // Roast lines
    root.querySelectorAll("[data-roast]").forEach((btn) => {
      const line = root.querySelector("[data-roast-line]");
      btn.onclick = () => {
        roastI = (roastI + 1) % MENG_LINES.length;
        if (line) line.textContent = MENG_LINES[roastI];
        celebrate();
      };
    });
  }

  function renderSlides() {
    deckEl.innerHTML = SLIDES.map((s, i) => {
      const bleed = s.html.includes("hero-split") ? " bleed" : "";
      return `<article class="slide ${s.tone}${bleed}${i === 0 ? " on" : ""}">${s.html}</article>`;
    }).join("");
    wireTaps(deckEl);
    wireComedy(deckEl);
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
      // Keep bottom 上一頁/下一頁/轉盤 bar visible in game mode too
      deckNav.classList.remove("is-hide");
      $("progressBar").style.width = "100%";
      drawWheel();
    }
  }

  $("modeDeck").onclick = () => setMode("deck");
  $("modeGame").onclick = () => setMode("game");
  $("prevBtn").onclick = () => {
    if (mode === "game") {
      setMode("deck");
      return;
    }
    idx = Math.max(0, idx - 1);
    updateDeckUI();
  };
  $("nextBtn").onclick = () => {
    if (mode === "game") return;
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

  // Wheel: rotation=0 puts segment 0 starting at the top.
  // Pointer is fixed at the top; segment i is under the pointer when
  // rotation === -(i*arc + arc/2) (normalized to [0, 2π)).
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
    // no spark / burst / confetti
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
    const finalRot = rotationForIndex(intendedWin, n);
    const start = rotation;
    // Shortest forward distance (≥ full turns) from start → finalRot
    let delta = normAngle(finalRot - normAngle(start));
    if (delta < 0.0001) delta = Math.PI * 2;
    const extra = (5 + Math.random() * 3) * Math.PI * 2;
    const target = extra + delta;
    const dur = 4200;
    const t0 = performance.now();
    let lastSeg = -1;
    const ease = (t) => 1 - Math.pow(1 - t, 4);

    function frame(now) {
      const p = Math.min(1, (now - t0) / dur);
      rotation = start + target * ease(p);
      drawWheel();
      const seg = indexAtPointer(rotation, n);
      if (seg !== lastSeg) {
        tickSound();
        lastSeg = seg;
      }
      if (p < 1) requestAnimationFrame(frame);
      else {
        spinning = false;
        rotation = finalRot;
        drawWheel();
        // Trust geometry: hub must match whatever is under the pointer
        const landed = indexAtPointer(rotation, n);
        intendedWin = landed;
        picked = numbers[landed];
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
