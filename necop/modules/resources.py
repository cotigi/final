"""Responsable for data storage to avoid unnecessary read operations."""

from . import files

class Resources:
    def __init__(
            self, 
            user = {
                "username": "AAAadmin",
                "password": "AAAadminpa55",
            },
            enable_password = "enpa55"
        ):

        self.update_devices()
        self.user = user
        self.enable_password = enable_password

    def update_devices(self):
        """Calls the file reader from the files module."""
        self.devices = files.read_devices()

    def gen_conn_infos(self):
        """Generates the necessary connection information and returns it."""
        conn_infos = []

        for device in self.devices:
            conn_infos.append({
                "general_info": device,
                "thread_info": {
                    "device_type": "cisco_ios",
                    "host": device["ip"],
                    "username": self.user["username"],
                    "password": self.user["password"]
                }
            })

        return conn_infos

    def update_user(self, username, password):
        """Updates the user."""
        self.user["username"] = username
        self.user["password"] = password

    def update_enable_password(self, enable_password):
        """Updates the enable password."""
        self.enable_password = enable_password

resources = Resources()
