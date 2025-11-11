import cmd
import dataclasses
import enum
import typing
from importlib.metadata import PackageNotFoundError, version

from spacebee_commander.commander import Commander
from spacebee_commander.message_manager import InteractionType
from spacebee_commander.telecommand_interface import TelecommandInterface

try:
    pkg_version = version("spacebee-commander")
except PackageNotFoundError:
    pkg_version = "0.0.0"


class SpacebeeCommander(cmd.Cmd):
    intro = f"Welcome to SpacebeeCommander v{pkg_version}.\nType help or ? to list commands.\n"
    prompt = "$ "

    def __init__(self, commander: Commander) -> None:
        self.commander = commander

        super().__init__()

    def preloop(self) -> None:
        for telecommand in self.commander.telecommands:
            self.create_CLI_telecommand(telecommand)

        return super().preloop()

    @classmethod
    def create_CLI_telecommand(cls, telecommand: TelecommandInterface):
        def autocomplete_method(
            self: SpacebeeCommander, text: str, line: str, begidx: int, endidx: int
        ):
            """Autocomplete based on cursor position"""
            input_type = telecommand.get_input_type()

            # Parse arguments
            tokens = line.split()
            command_name = tokens[0] if tokens else ""
            current_args = tokens[1:] if len(tokens) > 1 else []

            # Determine position of cursor
            if line[endidx - 1 : endidx] == " ":
                arg_index = len(current_args)
            else:
                arg_index = len(current_args) - 1

            if not input_type:
                # No arguments, only mode
                modes = [str(mode.value) for mode in InteractionType]
                return [m for m in modes if m.startswith(text)]

            fields = list(dataclasses.fields(input_type))
            type_hints = typing.get_type_hints(input_type)

            # Last argument is always the mode
            if arg_index >= len(fields):
                modes = [str(mode.value) for mode in InteractionType]
                return [m for m in modes if m.startswith(text)]

            # Verify if the current field is an enum
            field = fields[arg_index]
            field_type = type_hints[field.name]

            if isinstance(field_type, type) and issubclass(field_type, enum.Enum):
                enum_values = [e.name for e in field_type]
                # Case-insensitive matching
                return [v for v in enum_values if v.startswith(text.upper())]

            # For int, float, str there are no suggestions
            return []

        def dynamic_method(self: SpacebeeCommander, args):
            telecommand_instance = self.commander.get_telecommand_by_id(
                telecommand.operation
            )
            if telecommand_instance is None:
                print(f"Telecommand with ID {telecommand.operation} not found.")
                return
            try:
                args_array = args.split()
                input_type = telecommand.get_input_type()

                if input_type:
                    if len(args_array) != len(dataclasses.fields(input_type)) + 1:
                        print(f"Invalid arguments: {args_array}")
                        raise ValueError("Incorrect number of arguments.")

                    inputs = args_array[:-1]
                    parsed_args = parse_cli_args(input_type, inputs)
                    telecommand_instance.load_input_arguments(parsed_args)
                else:
                    if len(args_array) != 1:
                        print(f"Invalid arguments: {args_array}")
                        raise ValueError("Incorrect number of arguments.")
                    telecommand_instance.load_input_arguments(None)

                mode = InteractionType(int(args_array[-1]))
                self.commander.send_message(telecommand_instance, mode)

            except ValueError as e:
                print(e)
                print("Argument not valid!")
                print(format_telecommand_help(telecommand_instance))

        # Attach method dynamically
        dynamic_method.__name__ = f"do_{telecommand.name}"
        dynamic_method.__doc__ = format_telecommand_help(telecommand)
        setattr(cls, dynamic_method.__name__, dynamic_method)
        autocomplete_method.__name__ = f"complete_{telecommand.name}"
        setattr(cls, autocomplete_method.__name__, autocomplete_method)

    def do_exit(self, arg):
        "Exit the program."
        print("Exiting...")
        return True


def format_telecommand_help(telecommand: TelecommandInterface):
    """Generate usage help string for a telecommand."""
    input_type = telecommand.get_input_type()

    usage = f"Usage: {telecommand.name} "

    if input_type:
        type_hints = typing.get_type_hints(input_type)
        args_help = []
        for field in dataclasses.fields(input_type):
            field_type = type_hints[field.name]
            args_help.append(f"<{field.name}>")

        usage += " ".join(args_help) + " <mode>"
    else:
        usage += "<mode>"

    usage += "\n\nArguments:"

    if input_type:
        type_hints = typing.get_type_hints(input_type)
        for field in dataclasses.fields(input_type):
            field_type = type_hints[field.name]
            if isinstance(field_type, type) and issubclass(field_type, enum.Enum):
                values = ", ".join([e.name for e in field_type])
                usage += f"\n  {field.name}: {values}"
            else:
                usage += f"\n  {field.name}: {field_type.__name__}"

    mode_help = ", ".join([f"{m.value}={m.name}" for m in InteractionType])
    usage += f"\n  mode: {mode_help}"

    return usage


def parse_cli_args(dataclass_type: type, tokens: typing.List[str]):
    """Parse CLI args string into a dataclass instance."""
    fields = dataclasses.fields(dataclass_type)

    # Resolve real runtime types (handles string annotations from __future__)
    type_hints = typing.get_type_hints(dataclass_type)

    if len(tokens) != len(fields):
        raise ValueError(f"Expected {len(fields)} arguments but got {len(tokens)}")

    parsed_values = []
    for token, field in zip(tokens, fields):
        field_type = type_hints[field.name]

        # Handle enums
        if isinstance(field_type, type) and issubclass(field_type, enum.Enum):
            try:
                value = field_type[token]
            except KeyError:
                valid = ", ".join([e.name for e in field_type])
                raise ValueError(
                    f"Invalid enum '{token}' for {field.name}. Expected one of: {valid}"
                )
            parsed_values.append(value)
            continue

        # Handle integers (supports hex, e.g. 0xFF)
        if field_type is int:
            parsed_values.append(int(token, 0))
            continue

        # Default case: just cast
        parsed_values.append(field_type(token))

    return dataclass_type(*parsed_values)
