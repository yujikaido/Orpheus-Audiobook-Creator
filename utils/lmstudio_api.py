import os
import wave
import requests
import json
import asyncio
from utils.decoder import convert_to_audio as orpheus_convert_to_audio
from utils.decoder import turn_token_into_id

API_URL = "http://169.254.83.107:1234/v1/completions"
MODEL_NAME = "orpheus-3b-0.1-ft-q4_k_m"
SAMPLE_RATE = 24000
OUTPUT_DIR = "static/temp_chunks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_prompt(prompt, voice):
    return f"<|audio|>{voice}: {prompt}<|eot_id|>"

def get_tokens(prompt, voice):
    payload = {
        "model": MODEL_NAME,
        "prompt": format_prompt(prompt, voice),
        "max_tokens": 2000,
        "temperature": 0.6,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "stream": True
    }
    print(f"[LMStudio] Prompting model for voice '{voice}'...")
    response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=payload, stream=True)

    if response.status_code != 200:
        print(f"[ERROR] LM Studio returned {response.status_code}: {response.text}")
        return

    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data_str = line[6:]
                if data_str.strip() == '[DONE]':
                    break
                try:
                    data = json.loads(data_str)
                    token = data['choices'][0]['text']
                    if token.startswith("<custom_token_"):
                        #print("[TOKEN]", token)
                        yield token
                except Exception as e:
                    print(f"[TOKEN ERROR] {e}")

async def generate_audio_for_text(text, voice, session_id, chunk_index, output_dir=None):
    buffer = []
    audio_segments = []
    count = 0
    print(f"[INFO] Generating audio for chunk {chunk_index}")

    window_size = 28
    step_size = 7

    # Convert text to token IDs
    for token_text in get_tokens(text, voice):
        token = turn_token_into_id(token_text, count)
        if token is not None and token > 0:
            buffer.append(token)
            count += 1

    total_tokens = len(buffer)
    #print(f"[INFO] Total tokens: {total_tokens}")

    # Process all tokens with windows
    # Use overlapping windows to ensure we process all tokens
    for i in range(0, max(1, total_tokens - window_size + 1), step_size):
        window = buffer[i:i + window_size]
        if len(window) < window_size and i > 0:
            # Pad the last window with tokens from the previous window if needed
            padding_needed = window_size - len(window)
            start_idx = max(0, i - padding_needed)
            window = buffer[start_idx:i + len(window)]
        
        # Ensure the window is exactly window_size tokens
        if len(window) < window_size:
            # If we still don't have enough tokens, just process what we have
            # This typically only happens for very short texts
            if len(window) < 7:  # Minimum size needed for processing
                print(f"[WARNING] Window too small ({len(window)} tokens) to process")
                continue
        
        audio = orpheus_convert_to_audio(window, i)
        if audio:
            audio_segments.append(audio)
        else:
            print(f"[WARNING] Audio generation failed at window {i}")

    # Handle the very end - ensure the last tokens are always processed
    if total_tokens > window_size and total_tokens % step_size != 0:
        last_window = buffer[-window_size:]
        # Only process if we haven't already processed this window
        last_processed_idx = ((total_tokens - window_size) // step_size) * step_size
        if last_processed_idx + window_size < total_tokens:
            audio = orpheus_convert_to_audio(last_window, total_tokens - window_size)
            if audio:
                audio_segments.append(audio)
            else:
                print("[WARNING] Final window audio was empty")

    # Combine and write to WAV
    audio_data = b''.join(audio_segments)
    output_path = os.path.join(OUTPUT_DIR, f"{session_id}_{chunk_index}.wav")
    output_path = output_path.replace("\\", "/")  # ? force web-compatible path
    print(f"[INFO] Writing audio to: {output_path} ({len(audio_data)} bytes)")

    # Combine and write to WAV
    from pydub import AudioSegment
    import io

    audio_data = b''.join(audio_segments)

    audio_segment = AudioSegment(
        data=audio_data,
        sample_width=2,
        frame_rate=SAMPLE_RATE,
        channels=1
    )
    output_path = os.path.join(OUTPUT_DIR, f"{session_id}_{chunk_index}.wav")
    output_path = output_path.replace("\\", "/")  # Ensure web-compatible path
    audio_segment.export(output_path, format="wav")

    return output_path
