from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QPushButton, QFileDialog, QInputDialog)
from PySide6.QtCore import Qt
import csv
import openpyxl

class ContactListWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.contact_list = QListWidget()
        layout.addWidget(self.contact_list)

        button_layout = QHBoxLayout()
        self.import_button = QPushButton("Import Contacts")
        self.import_button.clicked.connect(self.import_contacts)
        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.add_contact)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout)

    def import_contacts(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Contacts", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            if file_path.endswith('.csv'):
                with open(file_path, 'r') as file:
                    reader = csv.reader(file)
                    contacts = [row[0] for row in reader]
            elif file_path.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active
                contacts = [cell.value for cell in sheet['A'] if cell.value]
            
            self.contact_list.addItems(contacts)

    def add_contact(self):
        contact, ok = QInputDialog.getText(self, "Add Contact", "Enter contact number:")
        if ok and contact:
            self.contact_list.addItem(contact)

    def get_contacts(self):
        return [self.contact_list.item(i).text() for i in range(self.contact_list.count())]

