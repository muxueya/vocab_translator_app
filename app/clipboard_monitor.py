import pyperclip
import threading
import time
from app.translator import translate_text
from app.config import AUTO_TRANSLATE_ON_COPY

class ClipboardMonitor(threading.Thread):
    def __init__(self, on_new_text):
        super().__init__(daemon=True)
        self.last_text = ""
        self.on_new_text = on_new_text
        self.running = AUTO_TRANSLATE_ON_COPY

    def run(self):
        while True:
            try:
                if self.running:
                    current_text = pyperclip.paste().strip()
                    if current_text and current_text != self.last_text:
                        self.last_text = current_text
                        self.on_new_text(current_text)
                time.sleep(0.5)
            except Exception as e:
                print("Clipboard error:", e)

    def enable(self):
        self.running = True

    def disable(self):
        self.running = False

