from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, 
                               QPushButton, QTabWidget, QMessageBox)
from PySide6.QtCore import Qt
from .contact_list_widget import ContactListWidget
from .message_composer_widget import MessageComposerWidget
from .scheduler_widget import SchedulerWidget
from .whatsapp_web_view import WhatsAppWebView
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WhatsApp Bulk Messenger")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        
        # Tabs for different functionalities
        self.tab_widget = QTabWidget()
        self.contact_list = ContactListWidget()
        self.message_composer = MessageComposerWidget()
        self.scheduler = SchedulerWidget()

        self.tab_widget.addTab(self.contact_list, "Contacts")
        self.tab_widget.addTab(self.message_composer, "Compose")
        self.tab_widget.addTab(self.scheduler, "Schedule")

        main_layout.addWidget(self.tab_widget)

        self.send_button = QPushButton("Send Messages")
        self.send_button.clicked.connect(self.send_messages)
        main_layout.addWidget(self.send_button)

        self.login_button = QPushButton("WhatsApp Login")
        self.login_button.clicked.connect(self.toggle_whatsapp_view)
        main_layout.addWidget(self.login_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.whatsapp_view = None
        self.is_logged_in = False

    def send_messages(self):
        if not self.is_logged_in:
            QMessageBox.warning(self, "Not Logged In", "Please log in to WhatsApp Web first.")
            return

        contacts = self.contact_list.get_contacts()
        message = self.message_composer.get_message()
        attachments = self.message_composer.get_attachments()
        # Implement sending logic here

    def toggle_whatsapp_view(self):
        if not self.whatsapp_view:
            try:
                self.whatsapp_view = WhatsAppWebView()
                self.whatsapp_view.login_status_changed.connect(self.handle_login_status_change)
            except Exception as e:
                logger.error(f"Failed to create WhatsApp Web view: {str(e)}")
                QMessageBox.critical(self, "Error", "Failed to open WhatsApp Web. Please try again.")
                return

        if self.whatsapp_view.isVisible():
            self.whatsapp_view.hide()
            self.login_button.setText("WhatsApp Login")
        else:
            self.whatsapp_view.show()
            self.login_button.setText("Hide WhatsApp")
            self.is_logged_in = self.whatsapp_view.is_logged_in()

    def handle_login_status_change(self, is_logged_in):
        self.is_logged_in = is_logged_in
        if is_logged_in:
            QMessageBox.information(self, "Login Status", "Successfully logged in to WhatsApp Web.")
        else:
            QMessageBox.warning(self, "Login Status", "Logged out from WhatsApp Web.")
