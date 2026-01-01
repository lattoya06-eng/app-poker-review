from ui.app import PokerReviewApp
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = PokerReviewApp()
window.show()
sys.exit(app.exec())
