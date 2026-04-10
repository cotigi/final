"""TFTP procedure"""

from netmiko import ConnectHandler

def tftp(conn_info):
    conn = ConnectHandler(**conn_info["thread_info"])

    conn.disconnect()
