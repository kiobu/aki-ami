from PyQt5.QtWidgets import QApplication
from src.base_window import Window
from src.mod_install_window import ModInstallWindow
import sys

app = QApplication(sys.argv)

# debug
if __file__ in sys.argv:
    sys.argv.remove(__file__)

# release
if sys.executable in sys.argv:
    sys.argv.remove(sys.executable)

if len(sys.argv) > 0:
    window = ModInstallWindow(sys.argv)
else:
    window = Window()

sys.exit(app.exec_())
