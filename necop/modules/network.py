"""Network device connection and configuration handling."""

import threading

from necop.modules.resources import resources
from necop.modules.network_procs import tftp

def tftp_handler():
    """Run and manage tftp connections"""

    conn_infos = resources.gen_conn_infos()
    threads = []

    # Generate a thread for each connection
    for conn_info in conn_infos:
        threads.append(
            threading.Thread(target=tftp.tftp, args=(conn_info))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
