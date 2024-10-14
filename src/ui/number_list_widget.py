from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QHBoxLayout, QLineEdit
from PySide6.QtCore import Signal
from utils.file_handler import load_numbers_from_file

class NumberListWidget(QWidget):
    numbers_loaded = Signal(list)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.number_list = QListWidget()
        layout.addWidget(self.number_list)
        
        input_layout = QHBoxLayout()
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter or paste numbers")
        input_layout.addWidget(self.number_input)
        
        self.add_button = QPushButton("Add Number(s)")
        self.add_button.clicked.connect(self.add_numbers)
        input_layout.addWidget(self.add_button)
        
        layout.addLayout(input_layout)
        
        self.load_button = QPushButton("Load Numbers from File")
        self.load_button.clicked.connect(self.load_numbers)
        layout.addWidget(self.load_button)
        
        self.setLayout(layout)

    def load_numbers(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_name:
            numbers = load_numbers_from_file(file_name)
            self.add_numbers_to_list(numbers)

    def add_numbers(self):
        text = self.number_input.text().strip()
        if text:
            numbers = [num.strip() for num in text.split(',')]
            self.add_numbers_to_list(numbers)
            self.number_input.clear()

    def add_numbers_to_list(self, numbers):
        existing_numbers = self.get_numbers()
        new_numbers = [num for num in numbers if num not in existing_numbers]
        self.number_list.addItems(new_numbers)
        self.numbers_loaded.emit(self.get_numbers())

    def get_numbers(self):
        return [self.number_list.item(i).text() for i in range(self.number_list.count())]
