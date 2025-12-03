import serial

from spacebee_commander.communication import Communication
import logging

logger = logging.getLogger(__name__)

class SerialHandler(Communication):
    """
    Implements Communication over a UART/serial interface.
    """

    def __init__(self, port: str = "/dev/ttyACM0", baud_rate: int = 115200, timeout: float = 1.0):
        """
        Initialize the serial connection.

        Args:
            port: Serial device path (e.g. /dev/ttyACM0 or COM3)
            baud_rate: Baud rate for the serial communication
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial = None

        logger.info(f"Initializing serial connection: {port} @ {baud_rate} baud")
        self._open_connection()

    def _open_connection(self):
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            logger.info(f"Serial port {self.port} opened successfully")
            logger.debug(f"Serial config: baud={self.baud_rate}, timeout={self.timeout}s")
        except serial.SerialException as e:
            logger.error(f"Failed to open serial port {self.port}: {e}", exc_info=True)
            raise RuntimeError(f"Failed to open serial port {self.port}: {e}")

    def send(self, message: bytes):
        """
        Send a message over the serial port.

        Args:
            message: Bytes to send
        """
        if not self.serial or not self.serial.is_open:
            logger.error("Attempted to send on closed serial port")
            raise RuntimeError("Serial port not open")

        if isinstance(message, str):
            message = message.encode()

        logger.debug(f"Sending message over serial to {self.port}")

        try:
            self.serial.write(message)
            logger.info(f"Sent message successfully")
            logger.debug(f"Message len: {len(message)} bytes - data: {message.hex()}")
        except serial.SerialException as e:
            logger.error(f"Failed to send message over serial: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.critical(f"Unexpected error sending message: {e}", exc_info=True)
            raise

    def receive(self) -> bytes:
        """
        Receive data from the serial port.

        Returns:
            The received bytes (may be empty if timeout occurs)
        """
        if not self.serial or not self.serial.is_open:
            logger.error("Attempted to receive on closed serial port")
            raise RuntimeError("Serial port not open")

        logger.debug("Waiting for data on serial port...")

        try:
            data = self.serial.readline().strip()

            if data:
                logger.info(f"Received message from serial")
                logger.debug(f"Message len: {len(data)} bytes - data: {data.hex()}")
                return data
            else:
                logger.warning("No data received (timeout or empty line)")
                return b''
        except serial.SerialException as e:
            logger.error(f"Serial error while receiving: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.critical(f"Unexpected error receiving message: {e}", exc_info=True)
            raise

    def close(self):
        """
        Close the serial connection.
        """
        if self.serial and self.serial.is_open:
            logger.info(f"Closing serial port {self.port}")
            self.serial.close()
            logger.debug("Serial port closed")
        else:
            logger.debug("Serial port already closed or not initialized")
