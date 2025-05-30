# Vocab Translator App

A lightweight clipboard-based translator and vocabulary manager built with PyQt5.

## Features

* **Clipboard Translation**: Copy any text and click **Translate** (or enable auto-translate) to get a Google Translate-powered translation.
* **Lexikon Lookup**: For single words, click **Lexikon** to fetch detailed entries from [Folkets lexikon](https://folkets-lexikon.csc.kth.se/).
* **Save to Wordbook**: Save either the translation or the Lexikon entry to your local wordbook.
* **Export to Anki**: One-click export of your wordbook to an Anki deck for flashcard study.
* **Text-to-Speech**: Read aloud original or translated text using Azure Neural TTS.
* **Customizable Appearance**: Change colors, font sizes, opacity, and frame dimensions via **style\_config.json**.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/muxueya/vocab_translator_app.git
   cd vocab_translator_app
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create or modify **style\_config.json** for your preferred appearance.

## Configuration (`style_config.json`)

```json
{
  "max_text_length": 2000,
  "text_color": "#000000",
  "text_size": "12pt",
  "window_color": "#ffffff",
  "opacity": 1.0,
  "original_bg_color": "#f7f7f7",
  "translation_bg_color": "#ffffff",
  "original_frame_height": 150,
  "translation_frame_height": 250
}
```

* **window\_color**: Main window background
* **text\_color**, **text\_size**: Font settings for text frames
* **opacity**: Window transparency (0.0–1.0)
* **original\_bg\_color**, **translation\_bg\_color**: Background colors for the two text panes
* **original\_frame\_height**, **translation\_frame\_height**: Fixed heights of the text panes
* **max\_text\_length**: Maximum characters to translate or display

## Usage

```bash
python main.py
```

1. Copy text to your clipboard.
2. Click **Translate** or enable **Auto-translate on copy**.
3. For single words, click **Lexikon** to get detailed dictionary entries.
4. Click **Save** to add the current entry to your wordbook.
5. Export your wordbook to Anki via **Options → Export Wordbook to Anki**.

## Troubleshooting

* If the **Lexikon** button stays disabled, ensure you've copied exactly one word (no spaces).
* For missing voices or TTS errors, check your network and Azure TTS subscription.
* If the appearance isn’t updating, use **Options → Reload Appearance from File**.

