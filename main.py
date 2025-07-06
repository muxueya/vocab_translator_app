#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from app.main_window import TranslatorApp
from PyQt5.QtGui import QIcon
import os

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
    app.setWindowIcon(QIcon(icon_path))
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())