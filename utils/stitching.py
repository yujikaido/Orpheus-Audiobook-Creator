from pydub import AudioSegment
import asyncio

async def stitch_wav_files(wav_files, output_path):
    combined = AudioSegment.empty()
    for wf in wav_files:
        combined += AudioSegment.from_wav(wf)
    combined.export(output_path, format="wav")
    return output_path
