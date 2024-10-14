from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog

class AttachmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.attachment_list = QListWidget()
        layout.addWidget(self.attachment_list)
        
        self.add_button = QPushButton("Add Attachment")
        self.add_button.clicked.connect(self.add_attachment)
        layout.addWidget(self.add_button)
        
        self.setLayout(layout)

    def add_attachment(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_name:
            self.attachment_list.addItem(file_name)

    def get_attachments(self):
        return [self.attachment_list.item(i).text() for i in range(self.attachment_list.count())]
