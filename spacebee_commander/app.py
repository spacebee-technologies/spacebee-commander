import cmd

import spacebee_commander.network_parameters as np
from spacebee_commander.commander import Commander
from spacebee_commander.communication import UdpHandler


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
    def create_CLI_telecommand(cls, telecommand):

        def dynamic_method(self, args):
            telecommand_instance = self.commander.getTelecommand(telecommand.operation)
            try:
                args_array = args.split()
                print(args_array)
                if len(args_array) != telecommand.num_inputs + 1:
                    print(f"Invalid arguments: {args_array}")
                    raise ValueError("Incorrect number of arguments.")

                mode = int(args_array[-1])
                inputs = args_array[:-1]

                telecommand_instance.loadInputArguments(inputs)
                self.commander.send_message(telecommand_instance, mode)

            except ValueError as e:
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


def main():
    transport = UdpHandler(np.ROVER_IP, np.ROVER_PORT_SEND, np.RECEIVER_IP, np.RECEIVER_PORT)
    commander = Commander(transport)
    cli = SpacebeeCommander(commander)
    cli.cmdloop()


if __name__ == '__main__':
    main()
