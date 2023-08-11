from PyQt5.QtWidgets import QApplication
from base_window import Window
import sys

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
