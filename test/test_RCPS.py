"""
The test evaluates packet loss during the transmission of telecommands by
continuously sending requests, monitoring responses.
"""
import time

import spacebee_commander.network_parameters as np

from spacebee_commander.commander import Commander
from spacebee_commander.udp_handler import UdpHandler


count = 0
batch = 50
received = 0


while True:

    transport = UdpHandler(np.ROVER_IP, np.ROVER_PORT_SEND, np.RECEIVER_IP, np.RECEIVER_PORT)
    commander = Commander(transport)

    id = 1
    tc_test = commander.getTelecommand(id)
    if tc_test is None:
        print(f"Telecommand with ID {id} not found.")
        continue

    delay = 0.01

    for _ in range(0, batch):
        tc_test.load_input_arguments(None)
        response = commander.request(tc_test)
        if response:
            received += 1
        time.sleep(delay)
    count += batch

    print("\n\n------------------------------------------------")
    print(f"Send {count} packages")
    print(f"{received/count*100}% packages received\n\n")

    time.sleep(10)
