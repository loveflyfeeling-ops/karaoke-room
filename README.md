# 歡唱K歌房

線上搜尋伴奏／原曲、升降 Key、男女聲切換、同步歌詞提示的網頁 K 歌房。

## 🌐 直接使用（GitHub Pages）
網頁：https://loveflyfeeling-ops.github.io/karaoke-room/

網頁本身放在 GitHub Pages，但「線上搜尋歌曲」需要一個後端幫忙抓音訊，有兩種方式：

### 方式 A：後端跑在自己電腦（最穩定，推薦）
1. 安裝 Python 3.10+ 與 ffmpeg（Windows：`winget install Gyan.FFmpeg`；Mac：`brew install ffmpeg`）
2. 下載本專案，在資料夾內執行：
   ```
   pip install -r requirements.txt
   python server.py
   ```
3. 開啟上面的網頁，後端狀態顯示「已連線 ✔」即可使用（預設網址 `http://127.0.0.1:8765`）

### 方式 B：後端放到雲端（Render / Railway / Hugging Face Spaces）
本專案附 `Dockerfile`，可直接部署到支援 Docker 的免費平台。
部署完成後，把平台給的網址填入網頁右上「後端網址」欄位並按「套用」。
> 注意：部分雲端 IP 會被 YouTube 要求驗證而抓取失敗，若遇到請改用方式 A。

## 功能
- 線上搜尋原曲或伴奏（YouTube，透過 yt-dlp），自動載入並搜尋同步歌詞（lrclib.net）
- 升降 Key ±12 半音（速度不變），男生唱女歌 −5 / 女生唱男歌 +5 快捷鍵
- 歌詞逐句高亮、下一句預覽、間奏倒數、偏移微調
- 也可直接載入本機 mp3 / m4a / wav 與 .lrc 檔

## 開發路線
1. ✅ 播放器＋調 Key＋歌詞
2. ✅ 線上搜尋歌曲後端
3. ⏳ Demucs 去人聲（原曲 → 伴奏）
4. ⏳ 麥克風混音、男女聲音色轉換
