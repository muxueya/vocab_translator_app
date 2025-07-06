#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from app.main_window import TranslatorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())