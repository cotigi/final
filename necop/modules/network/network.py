"""Network device connection and configuration handling."""

from netmiko.exceptions import NetmikoTimeoutException
from ..resources import resources

import os
from netmiko import ConnectHandler

async def save_to_tftp(hostname, ip):
    device = {
            "device_type": "cisco_ios",
            "host": ip,
            "username": resources.user["username"],
            "password": resources.user["password"],
            "secret": resources.enable_password
    }

    try:
        conn = ConnectHandler(**device)
    except NetmikoTimeoutException:
        return (False, "Null")

    conn.enable()

    response = conn.send_command_timing(
        command_string="copy running-config tftp:",
        strip_command=False,
        strip_prompt=False
    )

    if "Address or name of remote host" in response:
        response = conn.send_command_timing(
            command_string=resources.tftp_server,
            strip_command=False,
            strip_prompt=False
        )

    if "Destination filename" in response:
        response = conn.send_command_timing(
            command_string=f"{hostname.lower()}-confg",
            strip_command=False,
            strip_prompt=False
        )

    conn.disconnect()

    if "OK" in response:
        bytes_uploaded = str(response)\
                            .splitlines()[1]\
                            .lstrip("[")\
                            .rstrip("]")\
                            .split("-")[1]\
                            .rstrip("bytes")\
                            .strip()

        return (True, bytes_uploaded)

    return (False, "Null")

async def is_up(count, host):
    response = os.system(f"ping -c {count} {host} >/dev/null")

    return not bool(response)
