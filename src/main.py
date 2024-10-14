import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication, Qt
from ui.main_window import MainWindow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def exception_hook(exc_type, exc_value, exc_traceback):
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main():
    sys.excepthook = exception_hook
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.exception("Application crashed")

if __name__ == "__main__":
    main()
