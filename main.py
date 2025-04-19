import os
import uuid
import shutil
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request, Form, BackgroundTasks, WebSocket
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask
from utils.chunking import split_text_into_chunks
from utils.lmstudio_api import generate_audio_for_text
from utils.stitching import stitch_wav_files
from utils.mp3_export import convert_wav_to_mp3

class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

OUTPUT_DIR = "output"
TEMP_CHUNKS_DIR = "static/temp_chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_CHUNKS_DIR, exist_ok=True)

progress_status = {}
session_wav_files = {}
session_text_chunks = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-audiobook/")
async def generate(
    request: Request,
    text: str = Form(...),
    voice: str = Form("tara"),
    title: str = Form("audiobook"),
    session_id: str = Form(...),
    background_tasks: BackgroundTasks = None,
):
    chunks = split_text_into_chunks(text, max_chars=1200, overlap_sentences=1)
    print(f"[INFO] Total chunks: {len(chunks)}")
    progress_status[session_id] = {}
    session_wav_files[session_id] = []
    session_text_chunks[session_id] = chunks

    async def process_chunk(i, chunk):
        progress_status[session_id][i] = "started"
        print(f"[INFO] Starting chunk {i+1}/{len(chunks)}")
        audio_path = await generate_audio_for_text(chunk, voice, session_id, i, output_dir=TEMP_CHUNKS_DIR)
        print(f"[INFO] Finished chunk {i+1}: {audio_path}")
        session_wav_files[session_id].append(audio_path)
        progress_status[session_id][i] = "done"
        return audio_path

    tasks = [process_chunk(i, chunk) for i, chunk in enumerate(chunks)]
    await asyncio.gather(*tasks)

    return JSONResponse({
        "message": "Chunks generated",
        "chunks": len(chunks),
        "texts": chunks
    })

@app.get("/finalize/{session_id}")
async def finalize(session_id: str):
    wav_files = session_wav_files.get(session_id, [])
    if not wav_files:
        return JSONResponse({"error": "No chunks found for session"}, status_code=404)

    output_name = f"{OUTPUT_DIR}/final_{session_id}.wav"
    stitched = await stitch_wav_files(wav_files, output_name)
    final_mp3 = convert_wav_to_mp3(stitched, stitched.replace(".wav", ".mp3"))

    def cleanup():
        for f in wav_files:
            try:
                os.remove(f)
            except Exception as e:
                print(f"[CLEANUP] Failed to remove {f}: {e}")
        try:
            os.remove(stitched)
        except Exception as e:
            print(f"[CLEANUP] Failed to remove stitched file: {e}")
        session_wav_files.pop(session_id, None)
        progress_status.pop(session_id, None)
        session_text_chunks.pop(session_id, None)
        print(f"[CLEANUP] Session {session_id} cleaned up.")

    return FileResponse(final_mp3, filename=Path(final_mp3).name, media_type="audio/mpeg", background=BackgroundTask(cleanup))

@app.websocket("/ws/progress/{session_id}")
async def websocket_progress(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            if session_id in progress_status:
                await websocket.send_json({
                    "progress": progress_status[session_id],
                    "texts": session_text_chunks.get(session_id, [])
                })
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"[WebSocket] Disconnected from {session_id}: {e}")
