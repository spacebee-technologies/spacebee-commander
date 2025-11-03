import abc

from typing import Any, Type, Optional


class TelecommandInterface(abc.ABC):

    operation: int = 0
    name = ""

    body_length: int = 0
    body = b''

    # TODO: Shall be CLI level attributes?
    help = ""
    help_input = ""

    def get_operation_number(self) -> int:
        return self.operation

    def get_name(self) -> str:
        return self.name

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
