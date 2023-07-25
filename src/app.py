import socket
import struct
import cmd
from TelecommandInterface import set_mode,set_profile_mode,set_target_velocity

ROVER_IP = '192.168.0.228'
ROVER_PORT = 51524


class RovertitoCommander(cmd.Cmd):

    intro = 'Welcome to RovertitoCommander v 0.1.\n Type help or ? to list commands.\n'
    prompt = '$ '
    
    def do_set_target_velocity(self, arg):
        'Set the target velocity x in '

        ##Check arg limits
        command_set_target_velocity=set_target_velocity()
        command_set_target_velocity.loadInputArguments(int(arg))

        message=command_set_target_velocity.get_message()

        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')

    def do_set_mode(self, arg):

        ##Check arg limits
        command_set_mode=set_mode()
        command_set_mode.loadInputArguments(int(arg))
        message=command_set_mode.get_message()

        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')

    def do_set_profile_mode(self, arg):

        ##Check arg limits
        command_set_profile_mode=set_profile_mode()
        command_set_profile_mode.loadInputArguments(int(arg))

        message=command_set_profile_mode.get_message()

        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')

    def do_exit(self,arg):
        'Exit the program.'
        print("Exiting...")
        return True

if __name__ == '__main__':
    RovertitoCommander().cmdloop()
