import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from config_manager import ConfigManager
import sys


class Window(QMainWindow):
    config_manager: ConfigManager

    def __init__(self):
        super().__init__()

        self.config_manager = ConfigManager()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("AKI-AMI")
        self.setWindowOpacity(0.9)
        self.manage_aki_dirs()

        self.show()

    @staticmethod
    def exit():
        sys.exit(1)

    def manage_aki_dirs(self):
        if None in [self.config_manager.server_path, self.config_manager.client_path]:
            self.display_path_config()
        elif (
            not ConfigManager.validate_server_path(self.config_manager.server_path) or
            not ConfigManager.validate_client_path(self.config_manager.client_path)
        ):
            self.display_path_config()
        else:
            title = QLabel("Ready to install mods! ", self)
            title.setFont(QFont('Arial', 20))
            title.setStyleSheet("color: green; font-weight: bold")
            title.setGeometry(10, 10, 100, 100)
            title.adjustSize()


    def display_path_config(self):
        title = QLabel("Directories are missing or incorrect, please set them here: ", self)
        title.setFont(QFont('Arial', 15))
        title.setGeometry(10, 10, 100, 100)
        title.adjustSize()

        sv_path_label = QLabel("Server Path: ", self)
        sv_path_label.setGeometry(10, 100, 10, 10)
        sv_path_label.adjustSize()
        sv_button = QPushButton("Set AKI Server Directory", self)
        sv_button.setGeometry(5, 75,  10, 5)
        sv_button.clicked.connect(lambda: self._set_server_path(sv_path_label))
        sv_button.adjustSize()

        cl_path_label = QLabel("Client Path: ", self)
        cl_path_label.setGeometry(10, 200, 10, 10)
        cl_path_label.adjustSize()
        cl_button = QPushButton("Set AKI Client Directory", self)
        cl_button.setGeometry(5, 175, 100, 100)
        cl_button.clicked.connect(lambda: self._set_client_path(cl_path_label))
        cl_button.adjustSize()

        done_button = QPushButton("Done", self)
        done_button.setGeometry(10, 290, 50, 50)
        done_button.adjustSize()
        done_button.clicked.connect(Window.exit)

    def _set_server_path(self, label: QLabel):
        path = QFileDialog.getExistingDirectory(self, "Select AKI Server Directory")

        if not ConfigManager.validate_server_path(path):
            label.setText("This does not seem to be a valid AKI server directory.")
            label.setStyleSheet("color: red")
        else:
            label.setText(path)
            label.setStyleSheet("color: green")
            self.config_manager.set_server_path(path)

        label.adjustSize()

    def _set_client_path(self, label: QLabel):
        path = QFileDialog.getExistingDirectory(self, "Select AKI Client Directory")

        if not ConfigManager.validate_client_path(path):
            label.setText("This does not seem to be a valid AKI client directory.")
            label.setStyleSheet("color: red")
        else:
            label.setText(path)
            label.setStyleSheet("color: green")
            self.config_manager.set_client_path(path)

        label.adjustSize()
