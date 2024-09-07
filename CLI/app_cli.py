import cmd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_src_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'src/'))
sys.path.append(parent_src_dir)
from commander import Commander

class RovertitoCommander(cmd.Cmd):

    intro = 'Welcome to RovertitoCommander v 0.1.\n Type help or ? to list commands.\n'
    prompt = '$ '
    commander = Commander()

    def create_CLI_telecommand(cls, telecommand):
        method_name=f"do_{telecommand.name}"
        method_code= f"def {method_name}(self,args):\n\
                    telecommand=self.commander.getTelecommand({telecommand.operation})\n\
                    try:\n\
                        args_array=[]\n\
                        for i in range(0,{telecommand.num_inputs}):\n\
                            args_array.append(i)\n\
                        args_array.append(0)\n\
                        length_args=len(args_array)\n\
                        args_array = args.split()\n\
                        if len(args_array)!={telecommand.num_inputs}+1:\n\
                            raise ValueError\n\
                        mode=int(args_array[length_args-1])\n\
                        inputs=' '.join(args_array[0:length_args-1])\n\
                        telecommand.loadInputArguments(inputs)\n\
                        self.commander.send_message(telecommand,mode)\n\
                    except ValueError:\n\
                        print('Argument not valid!')\n\
                        print('should be: do_{telecommand.name} arg mode')\n\
                        print('arg: {telecommand.help_input}')\n\
                        print('mode: 1:Send 2:Submit 3:Request')\n\
                "
        method_globals = globals().copy()
        method_globals[cls.__name__] = cls
        exec(method_code, method_globals)
        method_func = method_globals[method_name]
        method_func.__doc__ = f"{telecommand.help} \n {telecommand.help_input}"
        setattr(cls, method_name, classmethod(method_func))

    def do_exit(self, arg):
        'Exit the program.'
        print("Exiting...")
        return True


if __name__ == '__main__':
    telecommands=RovertitoCommander.commander.telecommands
    for telecommand in telecommands:
        RovertitoCommander.create_CLI_telecommand(RovertitoCommander, telecommand)
    RovertitoCommander().cmdloop()
