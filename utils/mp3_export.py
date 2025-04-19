import subprocess
import os

def convert_wav_to_mp3(wav_path, mp3_path):
    print(f"[MP3] Using ffmpeg with libmp3lame: {wav_path} ? {mp3_path}")
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-c:a", "libmp3lame", "-b:a", "128k", mp3_path],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
        print(f"[MP3] Export success: {mp3_path}")
        return mp3_path
    else:
        print(f"[MP3] Export failed:\n{result.stderr}")
        return None
