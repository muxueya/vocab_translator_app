import sys
from PyQt5.QtWidgets import QApplication
from app.clipboard_monitor import setup_hotkey_listener, set_app_context

if __name__ == "__main__":
    from PyQt5.QtCore import QTimer

    app = QApplication(sys.argv)

    # Pass the app context so other files can safely use it
    set_app_context(app)

    setup_hotkey_listener()

    # Keep the app alive (even without windows)
    timer = QTimer()
    timer.start(1000)
    timer.timeout.connect(lambda: None)  # Prevents the app from exiting

    sys.exit(app.exec_())
