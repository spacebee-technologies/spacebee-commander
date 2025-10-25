import serial

from spacebee_commander.communication import Communication


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

        self._open_connection()

    def _open_connection(self):
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        except serial.SerialException as e:
            raise RuntimeError(f"Failed to open serial port {self.port}: {e}")

    def send(self, message: bytes):
        """
        Send a message over the serial port.

        Args:
            message: Bytes to send
        """
        if not self.serial or not self.serial.is_open:
            raise RuntimeError("Serial port not open")

        if isinstance(message, str):
            message = message.encode()

        self.serial.write(message)

    def receive(self) -> bytes:
        """
        Receive data from the serial port.

        Returns:
            The received bytes (may be empty if timeout occurs)
        """
        if not self.serial or not self.serial.is_open:
            raise RuntimeError("Serial port not open")

        return self.serial.readline().strip()

    def close(self):
        """
        Close the serial connection.
        """
        if self.serial and self.serial.is_open:
            self.serial.close()
