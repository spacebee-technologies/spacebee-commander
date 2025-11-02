import abc

from typing import Any, Type, Optional


class TelecommandInterface(abc.ABC):

    operation: int = 0        # 16 bits: Unique identifier for a given telemetry or telecommand
    body_length = None        # 16 bits: Longitude in bytes of the message body
    body = b''
    name = ""                 # string: Name of the telecommand
    help = ""                 # string: Description and usage for the telecommand
    help_input = ""           # string: Description for the input arguments

    def get_operation_number(self):
        return self.operation

    @classmethod
    @abc.abstractmethod
    def get_input_type(cls) -> Optional[Type[Any]]:
        """Return the dataclass type expected as input arguments, or None if none."""

    @abc.abstractmethod
    def load_input_arguments(self, args: Optional[Any]) -> None:
        """Load input arguments into the body. Args may be None if no input exists."""

    @abc.abstractmethod
    def parse_output_arguments(self, response: bytes) -> Optional[Any]:
        """Parse output arguments from raw bytes, or return None if no output."""
