import pyperclip
from pynput import keyboard
from PyQt5.QtWidgets import QApplication
from app.translator import translate_text
from app.ui import TranslationPopup
import sys

def on_activate():
    text = pyperclip.paste().strip()
    print("[✓] Hotkey pressed.")
    if text:
        translated = translate_text(text)
        print(f"[✓] Translated: {translated}")
        app = QApplication(sys.argv)
        popup = TranslationPopup(text, translated)
        popup.show()
        app.exec_()
    else:
        print("[!] No text in clipboard.")

def start_monitor():
    print("[✓] Hotkey monitor started. Press ⌘ + ⌥ + T after copying text.")
    with keyboard.GlobalHotKeys({
        '<cmd>+<alt>+t': on_activate
    }) as h:
        h.join()
