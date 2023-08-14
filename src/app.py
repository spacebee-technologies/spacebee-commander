import socket
import cmd
from commander import Commander

ROVER_IP = '192.168.0.228'
ROVER_PORT = 51524


class RovertitoCommander(cmd.Cmd):

    intro = 'Welcome to RovertitoCommander v 0.1.\n Type help or ? to list commands.\n'
    prompt = '$ '
    commander = Commander()
    
    def do_set_target_velocity(self, arg):
        'Set the target velocity x in '
        
    
        telecommand=self.commander.getTelecommand(4)
        telecommand.loadInputArguments(int(arg))

        self.commander.send(telecommand)

    def do_set_mode(self, arg):

        telecommand=self.commander.getTelecommand(2)

        telecommand.loadInputArguments(int(arg))

        self.commander.send(telecommand)


    def do_set_profile_mode(self, arg):

        telecommand=self.commander.getTelecommand(3)

        telecommand.loadInputArguments(int(arg))

        self.commander.send(telecommand)

    def do_exit(self,arg):
        'Exit the program.'
        print("Exiting...")
        return True

if __name__ == '__main__':
    RovertitoCommander().cmdloop()
