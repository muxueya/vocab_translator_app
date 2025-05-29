# Vocab Translator App

A desktop app built with PyQt5 that automatically translates text copied to the clipboard. It also features audio playback using Edge TTS with automatic language detection.

---

## 🚀 Features

- ✅ Real-time clipboard monitoring and translation
- ✅ Manual translation and copy buttons
- ✅ Save vocabulary to wordbook and export to Anki format
- ✅ Read original or translated text aloud (Edge TTS)
- ✅ Auto-selects voice based on language (e.g. English or Swedish)
- ✅ Safe thread handling to avoid UI crashes

---

## 🛠 Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourname/clipboard-translator.git
cd clipboard-translator
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. (Linux) Install `mpg123` for audio playback
```bash
sudo apt install mpg123
```

---

## ▶️ Usage

```bash
python main.py
```

- Toggle "Auto-translate on copy" to monitor the clipboard.
- Click "Translate" to manually trigger translation.
- Use "Read Original" / "Read Translated" to listen.

---

## 📦 Data

- Vocabulary saved in `data/wordbook.json`
- Anki export goes to `data/anki_wordbook.txt`

---

## 🔧 Configuration

Customize appearance in:
```
data/style_config.json
```

---

## 🧠 Tech Stack
- Python 3
- PyQt5 GUI
- Google Translate API (via `googletrans`)
- Edge TTS (via `edge-tts`)
- Language detection (`langdetect`)
