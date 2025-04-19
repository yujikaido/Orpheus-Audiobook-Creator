
# 🎧 Orpheus Audiobook Creator by Luke

A simple sleek, self-hosted audiobook generator powered by the [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) model and LM Studio — designed for creators who want a fast and simple way to convert text into beautifully narrated MP3s. 
Well, it makes audiobooks... when it feels like it. Work in progress! 😅🎧

---

## ✨ Features

- 🎤 High-quality voice generation using [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS)
- 💻 100% local — no internet 
- 🔊 Multiple voice options: `tara`, `jess`, `leo`, `leah`, `dan`, `mia`, `zac`, `zoe`
- 🎵 MP3 output with a single click
- 🧠 Built-in voice preview feature
- 🧰 Clean, modern UI with progress tracking(WIP see console window for progress updates)
  

---

## 🚀 Quick Setup

### 1. Install LM Studio

- Download and install [LM Studio](https://lmstudio.ai/)
- In LM Studio, download the model: `orpheus-3b-0.1-ft-q4_k_m.gguf`
- Load and run the model with the local server enabled

📌 **Note**: LM Studio runs on a local IP address.  
You will need to update the API URL in `lmstudio_api.py` to match what LM Studio shows (e.g., `http://127.0.0.1:1234` or another `169.254.x.x:1234` address):

```python
# Inside lmstudio_api.py
API_URL = "http://127.0.0.1:1234/v1/completions"
```

---

### 2. Clone this repository

```
Open a command window where you want the folder to be created then>
git clone https://github.com/yujikaido/Orpheus-Audiobook-Creator.git
cd Orpheus-Audiobook-Creator
```

### 3. Create and activate the Conda environment

conda create -n orpheus python=3.11
conda activate orpheus
pip install -r requirements.txt
```
pip install nltk
python -m nltk.downloader punkt
You can then close the window and run the bat file below.
---

## ▶️ Run the App

Run the included batch script:

```
audiobookmaker.bat
```

Then open your browser to:

```
http://localhost:8000
```

---

## 🗣️ Voice Preview

Click the "🔊 Preview Voice" button to hear the selected voice say:

> “This is what my voice sounds like, is it good enough for your audiobook?”

---

## 📁 Output Files

- Temporary `.wav` files are stored in `static/temp_chunks`
- Final `.mp3` files are saved in the `output/` folder or where you want after clicking download
  in the UI you can select a location and name the file.

---

## 🙌 Credits

- Created by [Luke](https://github.com/yujikaido)
- Powered by [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) from Canopy AI
- I run it on a 4070 Super 12gb vram

---

Enjoy creating your audiobooks! 🎧📚
