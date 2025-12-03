import click
import logging

from spacebee_commander.commander import Commander
from spacebee_commander.serial_handler import SerialHandler
from spacebee_commander.app import SpacebeeCommander
from spacebee_commander.logger import Logger, LogLevel


@click.command()
@click.option('--port', default='/dev/ttyACM0', type=str, help='Serial device path.')
@click.option('--baud_rate', default=115200, type=int, help='Baud rate for the serial communication.')
@click.option('--log-level',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              default='INFO',
              help='Set logging level.')
@click.option('--log-file', is_flag=True, help='Enable logging to file.')

def main(port: str, baud_rate: int,log_level: str, log_file: bool):

    level = LogLevel[log_level.upper()]
    Logger().setup(
        log_name='spacebee_commander',
        level=level,
        log_to_file=log_file
    )

    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Spacebee Commander (Serial) starting...")
    logger.info(f"Serial port: {port}")
    logger.info(f"Baud rate: {baud_rate}")
    logger.info("=" * 60)

    try:
        transport = SerialHandler(port, baud_rate)
        commander = Commander(transport)
        cli = SpacebeeCommander(commander)

        logger.info("CLI ready.")
        cli.cmdloop()

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        raise
    finally:
        logger.info("Spacebee Commander terminated")


if __name__ == '__main__':
    main()
