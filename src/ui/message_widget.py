from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton

class MessageWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.message_edit = QTextEdit()
        layout.addWidget(self.message_edit)
        
        self.send_button = QPushButton("Send Message")
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)

    def get_message(self):
        return self.message_edit.toPlainText()
