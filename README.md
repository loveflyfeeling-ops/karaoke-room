# 歡唱K歌房 — 使用說明

## 第一次安裝（Windows / Mac 皆可）
1. 安裝 Python 3.10 以上：https://www.python.org/downloads/
2. 安裝 ffmpeg：
   - Windows：`winget install Gyan.FFmpeg`（或到 ffmpeg.org 下載並加入 PATH）
   - Mac：`brew install ffmpeg`
3. 在本資料夾開啟終端機，執行：
   pip install -r requirements.txt

## 每次使用
1. 執行 `python server.py`（視窗保持開著）
2. 用 Chrome 開啟 `karaoke-player.html`
3. 頂端「線上搜尋歌曲」輸入歌名，選「伴奏」或「原曲」→ 點選結果即自動抓取、載入並找歌詞

抓過的歌會存在 `cache/` 資料夾，第二次播放不用再下載。
