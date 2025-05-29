# app/tray.py

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from app.storage import save_to_wordbook, export_wordbook_to_anki
from pync import Notifier

class TranslatorTray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon.fromTheme("face-smile"))  # Use a system icon or replace with local .ico/.png

        self.last_original = ""
        self.last_translation = ""

        menu = QMenu()
        self.view_action = QAction("Last Translation: None")
        menu.addAction(self.view_action)

        export_action = QAction("Export to Anki")
        export_action.triggered.connect(export_wordbook_to_anki)
        menu.addAction(export_action)

        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def show_translation(self, original, translated):
        self.last_original = original
        self.last_translation = translated
        self.view_action.setText(f"{original} → {translated}")
        save_to_wordbook(original, translated)
        Notifier.notify(translated, title="Translation", subtitle=original)

    def quit_app(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
