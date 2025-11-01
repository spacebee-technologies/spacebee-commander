import abc

from typing import Any, Type


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
    def getInputType(cls) -> Type[Any]:
        """Return the dataclass type expected as input arguments."""

    @abc.abstractmethod
    def loadInputArguments(self, args: Any) -> None:
        """Load input arguments into the body and calculate the body length."""

    @abc.abstractmethod
    def parseOutputArguments(self, response: bytes) -> Any:
        """Parse the output arguments from the raw bytes response."""
