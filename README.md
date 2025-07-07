# Vocab Translator App

A lightweight, clipboard-driven translator and vocabulary manager built with PyQt5.

## Features

- **Clipboard Translation**:  
  Copy any text and click **Translate** (or enable **Auto-translate on copy**) to get a Google Translate-powered result.
- **Lexikon Lookup**:  
  For a single word, the **Lexikon** button fetches a detailed entry from [Folkets lexikon](https://folkets-lexikon.csc.kth.se/) in a background thread.
- **Save to Wordbook**:  
  Save either the current translation or Lexikon entry to your local wordbook.
  - On **macOS**, a console message (`✅ Word saved: <word>`) appears in Terminal.
  - On **Windows/Linux**, a system tray notification displays for 1 second.
- **Export to Anki**:  
  One-click export of `wordbook.txt` in tab-delimited format with Anki headers, ready to import as Basic cards into the **Vocabulary** deck.
- **Text-to-Speech**:  
  Read aloud original or translated text using Azure Neural TTS in a dedicated Qt thread for UI responsiveness.
- **Customizable Appearance**:  
  Adjust window background, text colors, font size, pane heights, opacity, and max text length via **style_config.json**.
- **Modern Icon & Notifications**:  
  A scalable app icon for window/tray and cross-platform notifications.
- **Help & Troubleshooting**:  
  Access in-app guidance under **Options → Help** for usage tips and common fixes.

---

## Installation

1. **Clone** the repository:
   ```bash
   git clone https://github.com/muxueya/vocab_translator_app.git
   cd vocab_translator_app
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional)** Customize **style_config.json** to tweak appearance.

---

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

- **max_text_length**: Maximum characters to translate/display.
- **text_color**, **text_size**: Font styling for both panes.
- **window_color**: Main window background.
- **opacity**: Window transparency (0.0–1.0).
- **original_bg_color**, **translation_bg_color**: Pane backgrounds.
- **original_frame_height**, **translation_frame_height**: Fixed heights (px) of each pane.

---

## Usage

```bash
python main.py
```

1. Copy text to your clipboard.  
2. Click **Translate**, or check **Auto-translate on copy**.  
3. For a single word, click **Lexikon** to get dictionary details.  
4. Click **Save** to add the entry to your wordbook.  
   - **macOS**: view `✅ Word saved: <word>` in the Terminal.  
   - **Windows/Linux**: see a system tray notification.  
5. To export for Anki, select **Options → Export Wordbook to Anki**.  
6. For help or troubleshooting, select **Options → Help**.

---

## Anki Export Format

Exported `wordbook.txt` contains headers for direct Anki import:
```
#separator:Tab
#columns:Word	Definition
#notetype:Basic
#deck:Vocabulary
word1	definition1<br>more lines
word2	definition2
```
- Multi-line entries use `<br>` tags; enable **Allow HTML in fields** when importing.

---

## Troubleshooting

- **Lexikon button disabled**: Ensure exactly one word on clipboard (no spaces).  
- **No notifications on macOS**: Run the app from Terminal to see the console message.  
- **TTS errors**: Check network connection and Azure TTS credentials.  
- **Appearance not updating**: Edit `style_config.json` then choose **Options → Reload Appearance from File**.

---

## Contributing

Pull requests and issues are welcome! Please adhere to existing code style and add tests when applicable.

---

## License

MIT © 2025 muxueya
