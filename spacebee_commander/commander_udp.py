import click
import spacebee_commander.network_parameters as np
from spacebee_commander.commander import Commander
from spacebee_commander.udp_handler import UdpHandler
from spacebee_commander.app import SpacebeeCommander
from spacebee_commander.logger import Logger, LogLevel


@click.command()
@click.option('--dest-addr', default=np.ROVER_IP, type=str, help='Destination IP address.')
@click.option('--dest-port', default=np.ROVER_PORT_SEND, type=int, help='Destination port.')
@click.option('--host-addr', default=np.RECEIVER_IP, type=str, help='Host IP address.')
@click.option('--host-port', default=np.RECEIVER_PORT, type=int, help='Host port.')
@click.option('--log-level',
              type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
              default='INFO',
              help='Set logging level.')
@click.option('--log-file', is_flag=True, help='Enable logging to file.')
def main(dest_addr: str, dest_port: int, host_addr: str, host_port: int,
    log_level: str, log_file: bool):

    level = LogLevel[log_level.upper()]

    Logger().setup(
        log_name='spacebee_commander',
        level=level,
        log_to_file=log_file
    )

    import logging
    logger = logging.getLogger(__name__)

    logger.info("=" * 60)
    logger.info("Spacebee Commander (UDP) starting...")
    logger.info(f"Destination: {dest_addr}:{dest_port}")
    logger.info(f"Listening on: {host_addr}:{host_port}")
    logger.info("=" * 60)

    try:
        transport = UdpHandler(dest_addr, dest_port, host_addr, host_port)
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
