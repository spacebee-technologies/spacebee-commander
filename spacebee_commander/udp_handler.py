import socket

from spacebee_commander.communication import Communication
import logging

logger = logging.getLogger(__name__)

class UdpHandler(Communication):

    def __init__(self, ip, port_send, receiver_ip, port_response):
        self.rover_ip = ip
        self.rover_port_send = port_send
        self.receiver_ip = receiver_ip
        self.rover_port_receive = port_response

        logger.info(
            f"UDP Handler initialized - "
            f"Target: {ip}:{port_send}, "
            f"Listen: {receiver_ip}:{port_response}"
        )

    def send(self, message):
        logger.debug(f"Sending {len(message)} bytes to {self.rover_ip}:{self.rover_port_send}")
        try:
            socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port_send))
            socket_file_descriptor.close()

            logger.info(f"Sent message successfully")
            logger.debug(f"Message {len(message)} bytes - data: {message.hex()}")

        except socket.error as e:
            logger.error(f"Failed to send message: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.critical(f"Unexpected error sending message: {e}", exc_info=True)
            raise

    def receive(self):
        logger.info(f"Listening on {self.receiver_ip}:{self.rover_port_receive}...")
        sock = None
        timeout_seconds = 1

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.receiver_ip, self.rover_port_receive))

            sock.settimeout(timeout_seconds)
            logger.debug(f"Socket timeout set to {timeout_seconds}s")

            data, addr = sock.recvfrom(1024)

            if addr[0] == self.rover_ip:
                logger.info(f"Received message from {addr[0]}:{addr[1]}")
                logger.debug(f"Message len: {len(data)} bytes - data: {data.hex()}")
                return data
            else:
                logger.warning(f"Received message from unexpected address: {addr[0]} (expected {self.rover_ip})")
                return None

        except socket.timeout:
            logger.warning(f"No response received within {timeout_seconds}s timeout")
            return None
        except socket.error as e:
            logger.error(f"Socket error while receiving: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.critical(f"Unexpected error receiving message: {e}", exc_info=True)
            return None
        finally:
            if sock:
                sock.close()
                logger.debug("Socket closed")
