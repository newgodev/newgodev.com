# mx5g 技術與圖像說明

## 簡報引擎（抄自成熟開源專案，唔再自造 buggy deck）

- **[reveal.js](https://revealjs.com/)**（MIT）— HTML 簡報框架  
  - 官方：https://revealjs.com/  
  - GitHub：https://github.com/hakimel/reveal.js  
  - 內建：觸控滑動、全螢幕 `F`、fragments 逐步動畫、Esc 總覽  
  - 本機：`vendor/reveal/`（v5.1.0，可離線／iPad 用）
- 轉盤問答：`wheel.html`（分開頁，避免同簡報搶手勢）

參考過嘅同類做法：
- 台灣教師 Reveal.js 教學簡報（GSAP／觸控）：https://cagoooo.github.io/ccu-ai-workshop/
- Reveal 模板：https://isaac-cf-wong.github.io/presentation-template/

## 圖像原則

- **唔用 emoji**
- **唔用人臉照片**（真人相）
- 人物：古典畫像／古典教子畫（公開領域）
- 魚／熊掌／鏡／書：畫風圖（非 emoji）

| 檔案 | 用途 |
|------|------|
| `photo-mencius.png` / `photo-mencius2.png` | 孟子古典半身畫像 |
| `photo-students.png` 等 | 古典教子畫（Educating a Son） |
| `photo-loom.png` | 孟母教子典故畫 |
| `photo-fish.png` / `photo-bear.png` | 魚圖／古典木刻熊（非 Python 幾何圖） |
| `photo-hand.png` | 熊掌＋三道刮痕＝暴力（無血）· 以力服人 |
| `photo-mirror.png` / `photo-book.png` | 銅鏡／書冊畫風 |
| `photo-heart.png` | 古典畫意象 |

## iPad（第 8 代）用法

1. Safari 開 `index.html`（或網站 `/mx5g/`）
2. 撳右上角 **全螢幕 F**（或鍵盤 F）
3. 左右掃／空白鍵翻頁；逐步內容用「下一頁」逐段出
4. 最後一頁撳 **打開轉盤遊戲**
