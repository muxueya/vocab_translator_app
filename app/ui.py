from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from app.storage import save_to_wordbook

class TranslationPopup(QWidget):
    def __init__(self, original, translated):
        super().__init__()
        self.setWindowTitle("Translation")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Original: {original}"))
        layout.addWidget(QLabel(f"Translation: {translated}"))

        save_btn = QPushButton("Add to Wordbook")
        save_btn.clicked.connect(lambda: save_to_wordbook(original, translated))
        layout.addWidget(save_btn)

        self.setLayout(layout)