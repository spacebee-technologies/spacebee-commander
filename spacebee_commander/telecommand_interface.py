import abc

from typing import Any, Type, Optional


class TelecommandInterface(abc.ABC):

    operation: int = 0        # 16 bits: Unique identifier for a given telemetry or telecommand
    body_length = None        # 16 bits: Longitude in bytes of the message body
    body = b''
    name = ""                 # string: Name of the telecommand
    help = ""                 # string: Description and usage for the telecommand
    help_input = ""           # string: Description for the input arguments

    def getOperationNumber(self):
        return self.operation

    @classmethod
    @abc.abstractmethod
    def getInputType(cls) -> Optional[Type[Any]]:
        """Return the dataclass type expected as input arguments, or None if none."""

    @abc.abstractmethod
    def loadInputArguments(self, args: Optional[Any]) -> None:
        """Load input arguments into the body. Args may be None if no input exists."""

    @abc.abstractmethod
    def parseOutputArguments(self, response: bytes) -> Optional[Any]:
        """Parse output arguments from raw bytes, or return None if no output."""
