from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                               QFileDialog, QListWidget)

class MessageComposerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.message_edit = QTextEdit()
        layout.addWidget(self.message_edit)

        self.attachment_list = QListWidget()
        layout.addWidget(self.attachment_list)

        self.attach_button = QPushButton("Attach File")
        self.attach_button.clicked.connect(self.attach_file)
        layout.addWidget(self.attach_button)

    def attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Attach File", "", "All Files (*)")
        if file_path:
            self.attachment_list.addItem(file_path)

    def get_message(self):
        return self.message_edit.toPlainText()

    def get_attachments(self):
        return [self.attachment_list.item(i).text() for i in range(self.attachment_list.count())]

