# 歡唱K歌房 後端 — 線上搜尋歌曲 / 伴奏，並把音訊抓回本機給播放器用
# 啟動：python server.py   （第一次請先 pip install -r requirements.txt，並安裝 ffmpeg）
import os, re, hashlib, threading
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp

CACHE = Path(__file__).parent / "cache"
CACHE.mkdir(exist_ok=True)

app = FastAPI(title="Karaoke Server")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_lock = threading.Lock()
_jobs: dict[str, str] = {}   # video_id -> "downloading" | "done" | "error:..."

YDL_SEARCH = {"quiet": True, "skip_download": True, "extract_flat": "in_playlist", "noplaylist": True}


def fmt_dur(sec):
    if not sec: return ""
    sec = int(sec); return f"{sec // 60}:{sec % 60:02d}"


@app.get("/api/search")
def search(q: str = Query(..., min_length=1), mode: str = "song", n: int = 12):
    """mode=song 找原曲；mode=karaoke 自動加上伴奏關鍵字"""
    query = q if mode == "song" else f"{q} 伴奏 KTV karaoke instrumental"
    with yt_dlp.YoutubeDL(YDL_SEARCH) as ydl:
        info = ydl.extract_info(f"ytsearch{n}:{query}", download=False)
    out = []
    for e in info.get("entries") or []:
        if not e: continue
        out.append({
            "id": e.get("id"),
            "title": e.get("title"),
            "channel": e.get("channel") or e.get("uploader") or "",
            "duration": fmt_dur(e.get("duration")),
            "seconds": e.get("duration") or 0,
            "thumb": (e.get("thumbnails") or [{}])[-1].get("url") if e.get("thumbnails") else f"https://i.ytimg.com/vi/{e.get('id')}/mqdefault.jpg",
        })
    return out


def _download(vid: str):
    try:
        opts = {
            "quiet": True, "noplaylist": True,
            "format": "bestaudio/best",
            "outtmpl": str(CACHE / f"{vid}.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "m4a", "preferredquality": "0"}],
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={vid}"])
        _jobs[vid] = "done"
    except Exception as ex:  # noqa
        _jobs[vid] = f"error:{ex}"


@app.get("/api/fetch/{vid}")
def fetch(vid: str):
    """開始抓取（背景執行），回傳目前狀態"""
    if not re.fullmatch(r"[\w-]{6,20}", vid):
        raise HTTPException(400, "bad id")
    path = CACHE / f"{vid}.m4a"
    if path.exists():
        _jobs[vid] = "done"
        return {"status": "done"}
    with _lock:
        if _jobs.get(vid) != "downloading":
            _jobs[vid] = "downloading"
            threading.Thread(target=_download, args=(vid,), daemon=True).start()
    return {"status": _jobs[vid]}


@app.get("/api/status/{vid}")
def status(vid: str):
    return {"status": _jobs.get(vid, "done" if (CACHE / f"{vid}.m4a").exists() else "idle")}


@app.get("/api/audio/{vid}")
def audio(vid: str):
    path = CACHE / f"{vid}.m4a"
    if not path.exists():
        raise HTTPException(404, "not ready")
    return FileResponse(path, media_type="audio/mp4", filename=f"{vid}.m4a")


@app.get("/")
def root():
    return JSONResponse({"ok": True, "msg": "歡唱K歌房後端運作中，請開啟 karaoke-player.html"})


if __name__ == "__main__":
    import uvicorn
    print("歡唱K歌房後端啟動：http://127.0.0.1:8765")
    uvicorn.run(app, host="127.0.0.1", port=8765)
