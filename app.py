from PyQt5.QtWidgets import QApplication
from base_window import Window
from mod_install_window import ModInstallWindow
import sys

app = QApplication(sys.argv)

if __file__ in sys.argv:
    sys.argv.remove(__file__)

if len(sys.argv) > 0:
    window = ModInstallWindow(sys.argv)
else:
    window = Window()

sys.exit(app.exec_())
