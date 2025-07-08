from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox, QMenuBar, QAction, QTextEdit, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import pyperclip
import json
import os
import subprocess
import asyncio
import edge_tts
import tempfile
import platform
from langdetect import detect
from app.translator import translate_text, get_formatted_entry
from app.storage import save_to_wordbook, export_wordbook_to_anki
from app.clipboard_monitor import ClipboardMonitor
from app.config import APPEARANCE_FILE
from app.config import AUTO_TRANSLATE_ON_COPY


class LexikonWorker(QThread):
    entry_ready = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, word):
        super().__init__()
        self.word = word

    def run(self):
        try:
            entry = get_formatted_entry(self.word)
            if entry:
                self.entry_ready.emit(entry)
            else:
                self.error.emit("No entry found.")
        except Exception as e:
            self.error.emit(str(e))

class TTSWorker(QThread):
    audio_ready = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, text, voice):
        super().__init__()
        self.text = text
        self.voice = voice

    def run(self):
        try:
            # reuse a single asyncio loop by creating one at module level or use get_event_loop()
            communicate = edge_tts.Communicate(self.text, self.voice)
            # save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                filepath = tmp.name
            asyncio.run(communicate.save(filepath))
            self.audio_ready.emit(filepath)
        except Exception as e:
            self.error.emit(str(e))

class TranslatorApp(QWidget):
    clipboard_text_received = pyqtSignal(str)
    audio_ready = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Translator")
        self.setGeometry(300, 300, 500, 300)
        self.setFixedSize(800, 400)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.tray = QSystemTrayIcon(self)
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        app_icon = QIcon(icon_path)
        # set window icon too (optional, but ensures tray has it)
        self.setWindowIcon(app_icon)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(app_icon)       # <- must have a valid icon
        self.tray.setVisible(True)          
        self.tray.setIcon(self.windowIcon() or QIcon())
        self.tray.show()

        self.audio_process = None
        self.audio_file = None
        self.lexikon_worker = None

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

        # New Lexikon button
        self.lexikon_btn = QPushButton("Lexikon")
        self.lexikon_btn.setFixedWidth(100)
        self.lexikon_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0; color: #a0a0a0;")
        self.lexikon_btn.setEnabled(False)
        self.lexikon_btn.clicked.connect(self.lookup_lexikon)

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedWidth(100)
        self.save_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0;")
        self.save_btn.clicked.connect(self.save_to_wordbook)

        self.read_original_btn = QPushButton("Read Original")
        self.read_original_btn.setFixedWidth(120)
        self.read_original_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #d0f0d0;")
        self.read_original_btn.clicked.connect(self.read_original)

        self.read_translated_btn = QPushButton("Read Translated")
        self.read_translated_btn.setFixedWidth(120)
        self.read_translated_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #d0f0d0;")
        self.read_translated_btn.clicked.connect(self.read_translated)

        button_layout.addWidget(self.copy_translate_btn)
        button_layout.addWidget(self.copy_translated_btn)
        button_layout.addWidget(self.lexikon_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.read_original_btn)
        button_layout.addWidget(self.read_translated_btn)

        self.auto_check = QCheckBox("Auto-translate on copy")
        self.auto_check.setChecked(AUTO_TRANSLATE_ON_COPY)
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
        self.current_mode = 'translate'

        self.clipboard_text_received.connect(self.process_clipboard_text)
        self.audio_ready.connect(self.play_audio)
        self.clipboard_monitor = ClipboardMonitor(self.handle_clipboard_translation)
        self.clipboard_monitor.start()

        self.apply_appearance()
        self.max_text_length = 2000
        # Initialize lexikon button state
        self.update_lexikon_button()

    def handle_manual_translate(self):
        try:
            text = pyperclip.paste().strip()
            if text:
                self.show_translation(text)
        except Exception as e:
            QMessageBox.warning(self, "Clipboard Error", f"Could not read text from clipboard: {e}")

    def handle_clipboard_translation(self, text):
        self.clipboard_text_received.emit(text)

    def process_clipboard_text(self, text):
        if not self.clipboard_monitor.running:
            return
        try:
            text_cleaned = text.strip()
        except AttributeError:
            return
        if not text_cleaned:
            return
        if len(text_cleaned) > self.max_text_length:
            text_cleaned = text_cleaned[:self.max_text_length] + "..."
        translated = translate_text(text_cleaned)
        if not isinstance(translated, str):
            return
        self.last_original = text_cleaned
        self.last_translation = translated
        self.original_label.setText(text_cleaned)
        self.translation_label.setText(translated)
        self.current_mode = 'translate'
        self.update_lexikon_button()

    def handle_auto_toggle(self, state):
        if state == Qt.Checked:
            self.clipboard_monitor.enable()
        else:
            self.clipboard_monitor.disable()

    def show_translation(self, text):
        translated = translate_text(text)
        self.last_original = text
        self.last_translation = translated
        self.original_label.setText(text)
        self.translation_label.setText(translated)
        self.current_mode = 'translate'
        self.update_lexikon_button()

    def save_to_wordbook(self):
        if self.last_original:
            displayed = self.translation_label.toPlainText().strip()
            if displayed:
                # Persist to disk
                success = save_to_wordbook(self.last_original, displayed)

                # Show a one-second native notification
                if success:
                    # Word was newly saved
                    if platform.system() == "Darwin":
                        print(f"✅ Word saved: {self.last_original}")
                    else:
                        self.tray.showMessage(
                            "Wordbook",
                            f"Saved: {self.last_original}",
                            QSystemTrayIcon.Information,
                            1000
                        )
                else:
                    # Word was already present
                    if platform.system() == "Darwin":
                        print(f"⚠️ Already saved: {self.last_original}")
                    else:
                        self.tray.showMessage(
                            "Wordbook",
                            f"Already saved: {self.last_original}",
                            QSystemTrayIcon.Warning,
                            1000
                        )

    def export_to_anki(self):
        export_wordbook_to_anki()

    def copy_translated_text(self):
        if self.last_translation:
            pyperclip.copy(self.last_translation)

    def lookup_lexikon(self):
        # Only lookup when single word
        if self.last_original and len(self.last_original.split()) == 1:
            self.lexikon_btn.setEnabled(False)
            # Start background worker
            self.lexikon_worker = LexikonWorker(self.last_original.strip())
            self.lexikon_worker.entry_ready.connect(self.on_lexikon_ready)
            self.lexikon_worker.error.connect(self.on_lexikon_error)
            self.lexikon_worker.finished.connect(lambda: self.lexikon_btn.setEnabled(True))
            self.lexikon_worker.start()
        # Otherwise, do nothing

    def on_lexikon_ready(self, entry):
        self.translation_label.setText(entry)
        self.current_mode = 'lexikon'

    def on_lexikon_error(self, message):
        QMessageBox.warning(self, "Lexikon Error", f"Failed to fetch entry: {message}")

    def update_lexikon_button(self):
        # Enable only for single-word original text
        if self.last_original and len(self.last_original.split()) == 1:
            self.lexikon_btn.setEnabled(True)
            self.lexikon_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: skyblue; color: white;")
        else:
            self.lexikon_btn.setEnabled(False)
            self.lexikon_btn.setStyleSheet("padding: 6px; border-radius: 5px; background-color: #e0e0e0; color: #a0a0a0;")

    def apply_appearance(self):
        if os.path.exists(APPEARANCE_FILE):
            try:
                with open(APPEARANCE_FILE, 'r', encoding='utf-8') as f:
                    style = json.load(f)

                # Window
                self.setStyleSheet(f"background-color: {style.get('window_color', '#ffffff')};")
                self.setWindowOpacity(style.get('opacity', 1.0))
                self.max_text_length = style.get('max_text_length', 2000)

                # === ORIGINAL TEXT AREA ===
                orig_bg    = style.get('original_bg_color', '#ffffff')
                orig_color = style.get('original_text_color', '#000000')
                orig_size  = style.get('original_text_size', '12pt')
                orig_h     = style.get('original_frame_height', None)
                orig_style = (
                    f"background-color: {orig_bg}; "
                    f"color: {orig_color}; "
                    f"font-size: {orig_size};"
                )
                self.original_label.setStyleSheet(orig_style)
                if orig_h is not None:
                    self.original_label.setFixedHeight(orig_h)

                # === TRANSLATION TEXT AREA ===
                trans_bg    = style.get('translation_bg_color', '#ffffff')
                trans_color = style.get('translation_text_color', '#000000')
                trans_size  = style.get('translation_text_size', '12pt')
                trans_h     = style.get('translation_frame_height', None)
                trans_style = (
                    f"background-color: {trans_bg}; "
                    f"color: {trans_color}; "
                    f"font-size: {trans_size};"
                )
                self.translation_label.setStyleSheet(trans_style)
                if trans_h is not None:
                    self.translation_label.setFixedHeight(trans_h)
            except Exception as e:
                QMessageBox.warning(self, "Appearance Error", f"Failed to apply appearance: {e}")

    def open_appearance_file(self):
        try:
            subprocess.run(["open", "-a", "Visual Studio Code", APPEARANCE_FILE])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open appearance file: {e}")

    def read_text_aloud(self, text):
        try:
            lang = detect(text)
            voice = "sv-SE-MattiasNeural" if lang == "sv" else "en-US-GuyNeural"
        except:
            voice = "en-US-GuyNeural"

        if self.audio_process:
            self.stop_audio()
            return
        
        # start TTS in a dedicated QThread worker
        self.tts_worker = TTSWorker(text, voice)
        self.tts_worker.audio_ready.connect(self.play_audio)
        self.tts_worker.error.connect(lambda msg: print(f"[TTS ERROR] {msg}"))
        self.tts_worker.start()


    def play_audio(self, filepath):
        if platform.system() == "Darwin":
            self.audio_process = subprocess.Popen(["afplay", filepath])
        elif platform.system() == "Windows":
            self.audio_process = subprocess.Popen([
                "powershell", "-c",
                f"(New-Object Media.SoundPlayer '{filepath}').PlaySync();"
            ])
        else:
            self.audio_process = subprocess.Popen(["mpg123", filepath])

    def stop_audio(self):
        if self.audio_process:
            try:
                self.audio_process.terminate()
            except Exception as e:
                print(f"[DEBUG] Could not stop audio: {e}")
            self.audio_process = None

    def read_original(self):
        if self.last_original:
            self.read_text_aloud(self.last_original)

    def read_translated(self):
        if self.last_translation:
            self.read_text_aloud(self.last_translation)
