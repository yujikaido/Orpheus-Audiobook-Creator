
# 🎧 Orpheus Audiobook Creator by Luke

A sleek, self-hosted audiobook generator powered by the [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) model and LM Studio — designed for creators who want a fast and simple way to convert text into beautifully narrated MP3s.

---

## ✨ Features

- 🎤 High-quality voice generation using [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS)
- 💻 100% local — no internet or API keys required
- 🔊 Multiple voice options: `tara`, `jess`, `leo`, `leah`, `dan`, `mia`, `zac`, `zoe`
- 🎵 MP3 output with a single click
- 🧠 Built-in voice preview feature
- 🧰 Clean, modern UI with progress tracking

---

## 🚀 Quick Setup

### 1. Install LM Studio

- Download and install [LM Studio](https://lmstudio.ai/)
- In LM Studio, download the model: `orpheus-3b-0.1-ft-q4_k_m.gguf`
- Load and run the model with the local server enabled (default: `http://127.0.0.1:1234`)

### 2. Clone this repository

```bash
git clone https://github.com/yujikaido/Orpheus-Audiobook-Creator.git
cd Orpheus-Audiobook-Creator
```

### 3. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
python main.py
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
- Final `.mp3` files are saved in the `output/` folder

---

## 🙌 Credits

- Created by [Luke](https://github.com/yujikaido)
- Powered by [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) from Canopy AI

---

Enjoy creating your audiobooks! 🎧📚
