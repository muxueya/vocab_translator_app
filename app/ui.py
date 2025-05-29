from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from app.storage import save_to_wordbook

class TranslationPopup(QWidget):
    def __init__(self, original, translated):
        super().__init__()
        self.setWindowTitle("Translation")
        self.setGeometry(300, 300, 400, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Original: {original}"))
        layout.addWidget(QLabel(f"Translation: {translated}"))

        save_btn = QPushButton("Add to Wordbook")
        save_btn.clicked.connect(lambda: self.try_save(original, translated))
        layout.addWidget(save_btn)

        self.setLayout(layout)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.show()

    def try_save(self, original, translated):
        try:
            save_to_wordbook(original, translated)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save word: {e}")
