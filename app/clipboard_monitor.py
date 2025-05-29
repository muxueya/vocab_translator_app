import pyperclip
import keyboard
from PyQt5.QtWidgets import QApplication
from app.translator import translate_text
from app.ui import TranslationPopup
from app.config import HOTKEY
import sys

def on_hotkey():
    text = pyperclip.paste().strip()
    if text:
        translated = translate_text(text)
        app = QApplication(sys.argv)
        popup = TranslationPopup(text, translated)
        popup.show()
        app.exec_()

def start_monitor():
    keyboard.add_hotkey(HOTKEY, on_hotkey)
    print(f"[✓] Clipboard monitor running. Press {HOTKEY} after copying text to translate.")
    keyboard.wait()