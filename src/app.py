import socket
import struct
import cmd


ROVER_IP = '192.168.0.228'
ROVER_PORT = 51524


class RovertitoCommander(cmd.Cmd):

    intro = 'Welcome to RovertitoCommander. Type help or ? to list commands.\n'
    prompt = '$ '

    def do_set_target_velocity(self, arg):
        target_velocity = float(arg)
        timestamp = 11
        interaction_type = 2  # SUBMIT
        interaction_stage = 1
        transaction_id = 14
        service = 1  # TC
        operation = 4  # SetTargetVelocity telecommand
        area_version = 0
        is_error_message = 0
        body_length = 4
        header = struct.pack('<QHBQHHHBH', timestamp,
                                        interaction_type,
                                        interaction_stage,
                                        transaction_id,
                                        service,
                                        operation,
                                        area_version,
                                        is_error_message,
                                        body_length)
        body = struct.pack('f', target_velocity)
        crc = bytes.fromhex('0000')
        message = header + body + crc
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')

    def do_set_mode(self, arg):
        mode = int(arg)
        timestamp = 11
        interaction_type = 2  # SUBMIT
        interaction_stage = 1
        transaction_id = 14
        service = 1  # TC
        operation = 2  # SetMode telecommand
        area_version = 0
        is_error_message = 0
        body_length = 1
        header = struct.pack('<QHBQHHHBH', timestamp,
                                        interaction_type,
                                        interaction_stage,
                                        transaction_id,
                                        service,
                                        operation,
                                        area_version,
                                        is_error_message,
                                        body_length)
        body = mode.to_bytes(1, 'little')
        crc = bytes.fromhex('0000')
        message = header + body + crc
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')

    def do_set_profile_mode(self, arg):
        profile_mode = int(arg)
        timestamp = 11
        interaction_type = 2  # SUBMIT
        interaction_stage = 1
        transaction_id = 14
        service = 1  # TC
        operation = 3  # SetProfileMode telecommand
        area_version = 0
        is_error_message = 0
        body_length = 1
        header = struct.pack('<QHBQHHHBH', timestamp,
                                        interaction_type,
                                        interaction_stage,
                                        transaction_id,
                                        service,
                                        operation,
                                        area_version,
                                        is_error_message,
                                        body_length)
        body = profile_mode.to_bytes(1, 'little')
        crc = bytes.fromhex('0000')
        message = header + body + crc
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (ROVER_IP, ROVER_PORT))
        socket_file_descriptor.close()
        print(f'Sent: {message.hex()}')


if __name__ == '__main__':
    RovertitoCommander().cmdloop()
