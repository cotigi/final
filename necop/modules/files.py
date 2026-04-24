"""This module is responsable for handling file reading and writing."""

def read_devices():
    """Read all the device informations out into a dictionary.
    Returns: Dict containing the names and ip addresses
    """

    devices = []
    file = open('resources/devices.txt', 'r') 

    lines = file.read().splitlines()

    for line in lines:
        location, name, ip = line.split(',')

        device = {
            "location": location,
            "name": name,
            "ip": ip,
        }

        devices.append(device)

    file.close()

    return devices
