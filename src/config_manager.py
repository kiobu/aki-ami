import json
import os
import sys


class ConfigManager:
    config_path: str
    server_path: str
    client_path: str

    def __init__(self):

        if getattr(sys, 'frozen', False):
            self.config_path = os.path.dirname(os.path.abspath(sys.executable)) + "/config.json"
        elif __file__:
            self.config_path = os.path.dirname(os.path.abspath(__file__)) + "/config.json"

        self._read_config()

    def _read_config(self) -> tuple[str, str]:
        print("config path: " + self.config_path)
        with open(self.config_path, 'r') as conf:
            data = json.load(conf)

            self.server_path = data['server_path'] if data['server_path'] != "" else None
            self.client_path = data['client_path'] if data['client_path'] != "" else None

            print("got data from config")

            return self.server_path, self.client_path

    def _write_config(self) -> None:
        data = json.dumps({'server_path': self.server_path, 'client_path': self.client_path})

        with open(self.config_path, 'w+') as conf:
            conf.write(data)

    def set_server_path(self, path: str):
        self.server_path = path
        self._write_config()

    def set_client_path(self, path: str):
        self.client_path = path
        self._write_config()

    @staticmethod
    def validate_server_path(path: str) -> bool:
        return all([os.path.exists(path + "/user/mods"), os.path.exists(path + "/user/profiles")])

    @staticmethod
    def validate_client_path(path: str) -> bool:
        return all([os.path.exists(path + "/BepInEx/plugins"), os.path.exists(path + "/BepInEx/config"),
                    os.path.exists(path + "/BepInEx/patchers"), os.path.exists(path + "/BepInEx/core"),
                    os.path.exists(path + "/Aki_Data"), os.path.exists(path + "/user")])
