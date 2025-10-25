import click

import spacebee_commander.network_parameters as np

from spacebee_commander.commander import Commander
from spacebee_commander.communication import UdpHandler
from spacebee_commander.app import SpacebeeCommander


@click.command()
@click.option('--dest-addr', default=np.ROVER_IP, type=str, help='Destination IP address.')
@click.option('--dest-port', default=np.ROVER_PORT_SEND, type=int, help='Destination port.')
@click.option('--host-addr', default=np.RECEIVER_IP, type=str, help='Host IP address.')
@click.option('--host-port', default=np.RECEIVER_PORT, type=int, help='Host port.')
def main(dest_addr: str, dest_port: int, host_addr: str, host_port: int):
    transport = UdpHandler(dest_addr, dest_port, host_addr, host_port)
    commander = Commander(transport)
    cli = SpacebeeCommander(commander)
    cli.cmdloop()


if __name__ == '__main__':
    main()
