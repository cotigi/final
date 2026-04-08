"""File responsable for frontend"""

from argenta import App, Command, Orchestrator, Router, Response
from getpass import getpass
import pandas as pd

from .resources import resources
from . import misc

app = App(
    prompt=">> ",
    initial_message="Necop",
    farewell_message="Goodbye!",
    repeat_command_groups_printing=False,
)
orchestrator = Orchestrator()

main_router = Router(title="Main commands")

@main_router.command(Command(
    "get_devices",
    description="Prints registered devices"
))
def get_devices_handler(_response: Response):
    """Prints information regarding registered devices"""
    device_arr = []

    for device in resources.devices:
        device_arr.append(misc.dict_to_arr(device))

    print(pd.DataFrame(device_arr, columns=["Hostname", "IP"]))

@main_router.command(Command(
    "update_devices",
    description="Updates devices from resources/devices.txt"
))
def update_devices_handler(_response: Response):
    """Updates registered device informations"""
    resources.update_devices()
    print("Success!")

@main_router.command(Command(
    "get_user",
    description="Prints current user"
))
def get_user_handler(_response: Response):
    """Prints the current user"""
    print(f'Username: {resources.user["username"]}\
        \nPassword: {resources.user["password"]}')

@main_router.command(Command(
    "set_user",
    description="Sets current user"
))
def set_user_handler(_response: Response):
    """Set the current user"""
    username = input("Username: ")  
    password = getpass("Password: ")  

    resources.update_user(username, password)

@main_router.command(Command(
    "get_enab_pass",
    description="Prints current enable password"
))
def get_enab_pass_handler(_response: Response):
    """Prints the current enable password"""
    print(f'Enable password: {resources.enable_password}')

@main_router.command(Command(
    "set_enable_password",
    description="Sets current enable password"
))
def set_enable_password_handler(_response: Response):
    """Set the current enable password"""
    password = getpass("Password: ")  

    resources.update_enable_password(password)

app.include_router(main_router)
