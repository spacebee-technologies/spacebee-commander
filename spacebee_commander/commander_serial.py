import click

from spacebee_commander.commander import Commander
from spacebee_commander.serial_handler import SerialHandler
from spacebee_commander.app import SpacebeeCommander


@click.command()
@click.option('--port', default='/dev/ttyACM0', type=str, help='Serial device path.')
@click.option('--baud_rate', default=115200, type=int, help='Baud rate for the serial communication.')
def main(port: str, baud_rate: int):
    transport = SerialHandler(port, baud_rate)
    commander = Commander(transport)
    cli = SpacebeeCommander(commander)
    cli.cmdloop()


if __name__ == '__main__':
    main()
