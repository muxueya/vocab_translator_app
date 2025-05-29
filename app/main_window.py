from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox, QMenuBar, QAction, QTextEdit, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, QTimer, pyqtSignal  # ✅ Added pyqtSignal
import pyperclip
import json
import os
import subprocess
from app.translator import translate_text
from app.storage import save_to_wordbook, export_wordbook_to_anki
from app.clipboard_monitor import ClipboardMonitor
from app.config import APPEARANCE_FILE

class TranslatorApp(QWidget):
    clipboard_text_received = pyqtSignal(str)  # ✅ Define signal to handle clipboard text in GUI thread

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Translator")
        self.setGeometry(300, 300, 500, 300)
        self.setFixedSize(800, 400)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("Options")

        appearance_action = QAction("Change Appearance", self)
        appearance_action.triggered.connect(self.open_appearance_file)
        file_menu.addAction(appearance_action)

        reload_appearance_action = QAction("Reload Appearance from File", self)
        reload_appearance_action.triggered.connect(self.apply_appearance)
        file_menu.addAction(reload_appearance_action)

        export_action = QAction("Export Wordbook to Anki", self)
        export_action.triggered.connect(self.export_to_anki)
        file_menu.addAction(export_action)

        self.original_label = QTextEdit()
        self.original_label.setReadOnly(True)
        self.original_label.setWordWrapMode(True)
        self.original_label.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.translation_label = QTextEdit()
        self.translation_label.setReadOnly(True)
        self.translation_label.setWordWrapMode(True)
        self.translation_label.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.translation_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_layout = QHBoxLayout()
        self.copy_translate_btn = QPushButton("Translate")
        self.copy_translate_btn.setFixedWidth(100)
        self.copy_translate_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0;")
        self.copy_translate_btn.clicked.connect(self.handle_manual_translate)

        self.copy_translated_btn = QPushButton("Copy")
        self.copy_translated_btn.setFixedWidth(100)
        self.copy_translated_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0;")
        self.copy_translated_btn.clicked.connect(self.copy_translated_text)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(100)
        self.save_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0;")
        self.save_btn.clicked.connect(self.save_to_wordbook)

        button_layout.addWidget(self.copy_translate_btn)
        button_layout.addWidget(self.copy_translated_btn)
        button_layout.addWidget(self.save_btn)

        self.auto_check = QCheckBox("Auto-translate on copy")
        self.auto_check.setChecked(False)
        self.auto_check.stateChanged.connect(self.handle_auto_toggle)

        layout = QVBoxLayout()
        layout.setMenuBar(self.menu_bar)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Original:"))
        layout.addWidget(self.original_label)
        layout.addWidget(QLabel("Translation:"))
        layout.addWidget(self.translation_label)
        layout.addWidget(self.auto_check)

        self.setLayout(layout)

        self.last_original = ""
        self.last_translation = ""

        self.clipboard_text_received.connect(self.process_clipboard_text)  # ✅ Connect signal to handler
        self.clipboard_monitor = ClipboardMonitor(self.handle_clipboard_translation)
        self.clipboard_monitor.start()

        self.apply_appearance()
        self.max_text_length = 2000

    def handle_manual_translate(self):
        try:
            text = pyperclip.paste()
            if not isinstance(text, str):
                raise ValueError("Clipboard does not contain text.")
            text = text.strip()
            if text:
                self.show_translation(text)
        except Exception as e:
            QMessageBox.warning(self, "Clipboard Error", f"Could not read text from clipboard: {e}")

    def handle_clipboard_translation(self, text):
        print("[DEBUG] Clipboard callback triggered")
        print(f"[DEBUG] Raw clipboard content: {repr(text)}")

        # ✅ Emit the signal to safely process translation in main thread
        self.clipboard_text_received.emit(text)

    def process_clipboard_text(self, text):  # ✅ Slot for signal
        print("[DEBUG] Processing clipboard content")

        if not self.clipboard_monitor.running:
            print("[DEBUG] Clipboard monitor is disabled. Skipping translation.")
            return

        if not isinstance(text, str):
            print("[DEBUG] Clipboard content is not text. Ignored.")
            return
        try:
            text_cleaned = text.strip()
        except AttributeError:
            print("[DEBUG] Clipboard content is not valid text (strip failed). Ignored.")
            return
        if not text_cleaned:
            print("[DEBUG] Clipboard text is empty after stripping. Ignored.")
            return

        max_length = getattr(self, "max_text_length", 2000)
        truncated = False
        if len(text_cleaned) > max_length:
            text_cleaned = text_cleaned[:max_length] + "..."
            truncated = True

        print(f"[DEBUG] Text to translate: {repr(text_cleaned)}")
        translated = translate_text(text_cleaned)
        if not isinstance(translated, str):
            print("[DEBUG] Translation result is not text. Ignored.")
            return

        if truncated:
            translated += "..."

        print(f"[DEBUG] Translation result: {repr(translated)}")
        self.last_original = text_cleaned
        self.last_translation = translated
        self.original_label.setText(text_cleaned)
        self.translation_label.setText(translated)

    def handle_auto_toggle(self, state):
        if state == Qt.Checked:
            print("[DEBUG] Auto-translate checkbox changed: True")
            self.clipboard_monitor.enable()  # ✅ Control monitor state
        else:
            print("[DEBUG] Auto-translate checkbox changed: False")
            self.clipboard_monitor.disable()

    def show_translation(self, text):
        try:
            translated = translate_text(text)
            self.last_original = text
            self.last_translation = translated
            self.original_label.setText(text)
            self.translation_label.setText(translated)
        except Exception as e:
            QMessageBox.warning(self, "Translation Error", f"Failed to translate text: {e}")

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

    def apply_appearance(self):
        if os.path.exists(APPEARANCE_FILE):
            try:
                with open(APPEARANCE_FILE, 'r', encoding='utf-8') as f:
                    style = json.load(f)
                self.setStyleSheet(f"background-color: {style.get('window_color', '#ffffff')};")
                self.original_label.setStyleSheet(f"color: {style.get('text_color', '#000000')}; font-size: {style.get('text_size', '12pt')};")
                self.translation_label.setStyleSheet(f"color: {style.get('text_color', '#000000')}; font-size: {style.get('text_size', '12pt')};")
                self.setWindowOpacity(style.get('opacity', 1.0))
                self.max_text_length = style.get('max_text_length', 2000)
            except Exception as e:
                QMessageBox.warning(self, "Appearance Error", f"Failed to apply appearance: {e}")

    def open_appearance_file(self):
        try:
            subprocess.run(["open", "-a", "Visual Studio Code", APPEARANCE_FILE])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open appearance file: {e}")
