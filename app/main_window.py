from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
import pyperclip
from app.translator import translate_text
from app.storage import save_to_wordbook, export_wordbook_to_anki
from app.clipboard_monitor import ClipboardMonitor

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Translator")
        self.setGeometry(300, 300, 500, 300)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.original_label = QLabel("Original: ")
        self.translation_label = QLabel("Translation: ")

        self.copy_translate_btn = QPushButton("Translate Copied Text")
        self.copy_translate_btn.clicked.connect(self.handle_manual_translate)

        self.copy_translated_btn = QPushButton("Copy Translated Text")
        self.copy_translated_btn.clicked.connect(self.copy_translated_text)

        self.save_btn = QPushButton("Add to Wordbook")
        self.save_btn.clicked.connect(self.save_to_wordbook)

        self.export_btn = QPushButton("Export Wordbook to Anki")
        self.export_btn.clicked.connect(self.export_to_anki)

        self.auto_check = QCheckBox("Auto-translate on copy")
        self.auto_check.setChecked(False)
        self.auto_check.stateChanged.connect(self.handle_auto_toggle)

        layout = QVBoxLayout()
        layout.addWidget(self.original_label)
        layout.addWidget(self.translation_label)
        layout.addWidget(self.copy_translate_btn)
        layout.addWidget(self.copy_translated_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.auto_check)
        layout.addWidget(self.export_btn)

        self.setLayout(layout)

        self.last_original = ""
        self.last_translation = ""

        self.clipboard_monitor = ClipboardMonitor(self.handle_clipboard_translation)
        self.clipboard_monitor.start()

    def handle_manual_translate(self):
        text = pyperclip.paste().strip()
        if text:
            self.show_translation(text)

    def handle_clipboard_translation(self, text):
        if self.auto_check.isChecked():
            self.show_translation(text)

    def handle_auto_toggle(self, state):
        if state:
            self.clipboard_monitor.enable()
        else:
            self.clipboard_monitor.disable()

    def show_translation(self, text):
        translated = translate_text(text)
        self.last_original = text
        self.last_translation = translated
        self.original_label.setText(f"Original: {text}")
        self.translation_label.setText(f"Translation: {translated}")

    def save_to_wordbook(self):
        if self.last_original and self.last_translation:
            try:
                save_to_wordbook(self.last_original, self.last_translation)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save word: {e}")

    def export_to_anki(self):
        try:
            export_wordbook_to_anki()
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def copy_translated_text(self):
        if self.last_translation:
            pyperclip.copy(self.last_translation)
