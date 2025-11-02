import cmd
import dataclasses
import enum
import typing

from spacebee_commander.commander import Commander
from spacebee_commander.telecommand_interface import TelecommandInterface
from spacebee_commander.message_manager import InteractionType


class SpacebeeCommander(cmd.Cmd):

    intro = 'Welcome to SpacebeeCommander vX.Y.\nType help or ? to list commands.\n'  # TODO: Get version dynamically
    prompt = '$ '

    def __init__(self, commander: Commander) -> None:
        self.commander = commander

        super().__init__()

    def preloop(self) -> None:
        for telecommand in self.commander.telecommands:
            self.create_CLI_telecommand(telecommand)

        return super().preloop()

    @classmethod
    def create_CLI_telecommand(cls, telecommand: TelecommandInterface):

        def dynamic_method(self: SpacebeeCommander, args):
            telecommand_instance = self.commander.get_telecommand(telecommand.operation)
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
                print(f"Usage: do_{telecommand.name} arg mode")
                print(f"arg: {telecommand.help_input}")
                print("mode: 1:Send 2:Submit 3:Request")

        # Attach method dynamically
        dynamic_method.__name__ = f"do_{telecommand.name}"
        dynamic_method.__doc__ = f"{telecommand.help} \n {telecommand.help_input}"
        setattr(cls, dynamic_method.__name__, dynamic_method)  # Instance method

    def do_exit(self, arg):
        'Exit the program.'
        print("Exiting...")
        return True


def parse_cli_args(dataclass_type: type, tokens: typing.List[str]):
    """Parse CLI args string into a dataclass instance."""
    fields = dataclasses.fields(dataclass_type)

    # Resolve real runtime types (handles string annotations from __future__)
    type_hints = typing.get_type_hints(dataclass_type)

    if len(tokens) != len(fields):
        raise ValueError(
            f"Expected {len(fields)} arguments but got {len(tokens)}"
        )

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
                    f"Invalid enum '{token}' for {field.name}. "
                    f"Expected one of: {valid}"
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
