from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SchedulerWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Scheduler functionality coming soon..."))