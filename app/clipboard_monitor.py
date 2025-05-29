import pyperclip
from pynput import keyboard
from PyQt5.QtCore import QTimer
from app.translator import translate_text
from app.ui import TranslationPopup

_app = None  # App context to create popups safely

def set_app_context(app):
    global _app
    _app = app

def on_activate():
    text = pyperclip.paste().strip()
    print("[✓] Hotkey pressed.")
    if text:
        translated = translate_text(text)
        print(f"[✓] Translated: {translated}")

        def show_popup():
            popup = TranslationPopup(text, translated)
            popup.show()

        QTimer.singleShot(0, show_popup)  # Schedule GUI update in main thread

def setup_hotkey_listener():
    print("[✓] Hotkey listener started. Press ⌘ + ⌥ + T after copying text.")
    hotkeys = keyboard.GlobalHotKeys({
        '<cmd>+<alt>+t': on_activate
    })
    hotkeys.start()
