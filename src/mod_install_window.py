import os.path
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.config_manager import ConfigManager
from src.mod_metadata_parser import *
from typing import Literal, Union
import sys


class ModInstallWindow(QMainWindow):
    config_manager: ConfigManager
    args: list[str]

    def __init__(self, sys_args: list[str]):
        super().__init__()

        self.config_manager = ConfigManager()
        self.args = sys_args

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("AKI-AMI")
        self.setWindowOpacity(0.9)

        if not self.check_for_errors():
            self.load_metadata_and_install_mod(self.args[0])

        self.show()

    def check_for_errors(self):
        not_configured = False

        if None in [self.config_manager.server_path, self.config_manager.client_path]:
            not_configured = True
        elif (
            not ConfigManager.validate_server_path(self.config_manager.server_path) or
            not ConfigManager.validate_client_path(self.config_manager.client_path)
        ):
            not_configured = True

        if not_configured:
            self.create_boot_error_label(
                "AMI is not configured or is incorrectly\n configured, restart"
                " AMI.exe standalone to\n set up AKI paths."
            )
            return True

        if len(self.args) > 1:
            self.create_boot_error_label(
                "Currently, AMI does not work with multiple mods\nat once, please install one mod at a time."
            )
            return True

        if 'metadata.ami' not in self.args[0]:
            self.create_boot_error_label(
                f"The given file does not seem to be a metadata.ami file.\n{self.args}"
            )
            print("arg: " + self.args[0])
            return True

        return False

    def load_metadata_and_install_mod(self, ami_path: str):
        ami = None
        # Load mod's metadata.ami.
        try:
            ami = MetadataParser(ami_path)
        except (
                MetadataInvalidException, MetadataServerModStructureInvalid, MetadataModTypeInvalidException,
                MetadataPathNotFoundException, MetadataPathNotFoundException
        ) as ex:
            self.create_boot_error_label(
                f"The AMI file is invalid. \n {str(type(ex).__name__)} \n {str(ex)}"
            )

        if ami:

            # Set up message log.
            label = QLabel("Installing: ", self)
            label.setGeometry(10, 10, 100, 100)
            label.setFont(QFont('Arial', 15))
            label.setStyleSheet("color: black")
            label.adjustSize()

            for idx, mod in enumerate(ami.metadata['mods']):

                # Use mod path as a default when there's no package.json 'name' property to grab,
                # or it is a client mod.
                mod_name = mod['path_to_root']

                # Move server mod.
                if mod['type'] == 'server':

                    # Attempt to get server mod's package.json for the mod name.
                    try:
                        with open(ami.mod_dir + mod['path_to_root'] + "/package.json") as f:
                            _json = json.load(f)
                            mod_name = _json['name']
                    except Exception:
                        print("couldn't get name in package.json")

                    try:
                        src = ami.mod_dir + mod['path_to_root']

                        # /aki-dir/Server/user/mods/
                        dst = self.config_manager.server_path + "/user/mods" + mod['path_to_root']

                        print("src: " + src)
                        print("dst: " + dst)

                        shutil.copytree(src, dst, dirs_exist_ok=True)

                        self.create_mod_label(f"SUCCESS: {mod_name}", idx, 'green')
                    except Exception as ex:
                        self.create_mod_label(f"FAILED: {mod_name} - {str(ex)}", idx, 'red')

                # Move client mod.
                else:
                    # TODO: Grab .dll names recursively to display in AMI window.
                    try:
                        src = ami.mod_dir + mod['path_to_root']

                        # /aki-dir/Client/
                        dst = self.config_manager.client_path + "/"

                        print("src: " + src)
                        print("dst: " + dst)

                        shutil.copytree(src, dst, dirs_exist_ok=True)

                        self.create_mod_label(f"SUCCESS: {mod_name}", idx, 'green')
                    except Exception as ex:
                        self.create_mod_label(f"FAILED: {mod_name} - {str(ex)}", idx, 'red')


        done_label = QLabel("DONE!", self)
        done_label.setGeometry(10, self.get_line_y(len(ami.metadata['mods'])) + 30, 100, 100)
        done_label.setFont(QFont('Arial', 12))
        done_label.setStyleSheet(f"color: green; font-weight: bold")
        done_label.adjustSize()


    def create_mod_label(self, text: str, idx: int, color: Union[Literal['red'], Literal['green']]):
        idx += 1
        y = self.get_line_y(idx)

        label = QLabel(text, self)
        label.setGeometry(10, y, 100, 100)
        label.setFont(QFont('Arial', 10))
        label.setStyleSheet(f"color: {color}; font-weight: bold")
        label.adjustSize()


    def create_boot_error_label(self, text: str):
        label = QLabel(text, self)
        label.setGeometry(10, 10, 100, 100)
        label.setFont(QFont('Arial', 20))
        label.setStyleSheet("color: red; font-weight: bold")
        label.adjustSize()

    def get_line_y(self, idx: int) -> int:
        return 20 + (idx * 20)

    @staticmethod
    def exit():
        sys.exit(1)