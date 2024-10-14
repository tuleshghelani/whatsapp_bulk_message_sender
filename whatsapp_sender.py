# import sys
# import csv
# import pandas as pd
# from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog
# import pywhatkit

# class WhatsAppSender(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("WhatsApp Bulk Sender")
#         self.setGeometry(100, 100, 400, 500)

#         layout = QVBoxLayout()

#         self.phone_input = QLineEdit()
#         self.phone_input.setPlaceholderText("Enter phone number or upload file")
#         layout.addWidget(self.phone_input)

#         self.upload_button = QPushButton("Upload CSV/Excel")
#         self.upload_button.clicked.connect(self.upload_file)
#         layout.addWidget(self.upload_button)

#         self.message_input = QTextEdit()
#         self.message_input.setPlaceholderText("Enter your message")
#         layout.addWidget(self.message_input)

#         self.attachment_button = QPushButton("Add Attachment")
#         self.attachment_button.clicked.connect(self.add_attachment)
#         layout.addWidget(self.attachment_button)

#         self.send_button = QPushButton("Send Messages")
#         self.send_button.clicked.connect(self.send_messages)
#         layout.addWidget(self.send_button)

#         self.status_label = QLabel()
#         layout.addWidget(self.status_label)

#         container = QWidget()
#         container.setLayout(layout)
#         self.setCentralWidget(container)

#         self.phone_numbers = []
#         self.attachment_path = ""

#     def upload_file(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
#         if file_path:
#             if file_path.endswith('.csv'):
#                 with open(file_path, 'r') as file:
#                     reader = csv.reader(file)
#                     self.phone_numbers = [row[0] for row in reader]
#             elif file_path.endswith('.xlsx'):
#                 df = pd.read_excel(file_path)
#                 self.phone_numbers = df.iloc[:, 0].tolist()
#             self.status_label.setText(f"Loaded {len(self.phone_numbers)} phone numbers")

#     def add_attachment(self):
#         self.attachment_path, _ = QFileDialog.getOpenFileName(self, "Select Attachment", "", "All Files (*)")
#         if self.attachment_path:
#             self.status_label.setText(f"Attachment added: {self.attachment_path}")

#     def send_messages(self):
#         message = self.message_input.toPlainText()
#         if not self.phone_numbers:
#             self.phone_numbers = [self.phone_input.text()]

#         for phone in self.phone_numbers:
#             try:
#                 pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=10)
#                 if self.attachment_path:
#                     pywhatkit.sendwhats_image(phone, self.attachment_path, wait_time=10)
#                 self.status_label.setText(f"Message sent to {phone}")
#             except Exception as e:
#                 self.status_label.setText(f"Error sending to {phone}: {str(e)}")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = WhatsAppSender()
#     window.show()
#     sys.exit(app.exec())