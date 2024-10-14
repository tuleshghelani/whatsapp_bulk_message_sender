from PySide6.QtCore import Qt, Signal, QUrl, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings

import logging

logger = logging.getLogger(__name__)

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        if not message.startswith(("WAWebLoggerWorker", "[storage]", "JS:")):
            logger.info(f"JS: {message}")

class WhatsAppWebView(QWidget):
    login_status_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("WhatsApp Web")
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout(self)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        profile = QWebEngineProfile("WhatsAppProfile", self)
        profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        settings = profile.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)

        self.page = CustomWebEnginePage(profile, self.web_view)
        self.web_view.setPage(self.page)

        self.web_view.loadFinished.connect(self.handle_load_finished)

        self.login_check_timer = QTimer(self)
        self.login_check_timer.timeout.connect(self.check_login_status)
        self.login_check_timer.start(5000)  # Check every 5 seconds

        self.is_logged_in = False
        self.load_whatsapp()

    def load_whatsapp(self):
        self.web_view.load(QUrl("https://web.whatsapp.com"))

    def handle_load_finished(self, ok):
        if not ok:
            logger.error("Failed to load WhatsApp Web. Please check your internet connection.")
            self.web_view.setHtml("<html><body><h1>Failed to load WhatsApp Web</h1><p>Please check your internet connection and try again.</p></body></html>")
        else:
            logger.info("WhatsApp Web loaded successfully.")

    def check_login_status(self):
        self.page.runJavaScript(
            "document.getElementsByClassName('_1XkO3').length > 0",
            self.update_login_status
        )

    def update_login_status(self, result):
        is_logged_in = bool(result)
        if is_logged_in != self.is_logged_in:
            self.is_logged_in = is_logged_in
            self.login_status_changed.emit(self.is_logged_in)
            logger.info(f"Login status changed: {'Logged in' if self.is_logged_in else 'Logged out'}")

    def is_logged_in(self):
        return self.is_logged_in
