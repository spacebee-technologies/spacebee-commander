import socket

from spacebee_commander.communication import Communication


class UdpHandler(Communication):

    def __init__(self, ip, port_send, receiver_ip, port_response):
        self.rover_ip = ip
        self.rover_port_send = port_send
        self.receiver_ip = receiver_ip
        self.rover_port_receive = port_response

    def send(self, message):
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port_send))
        socket_file_descriptor.close()

        print(f'Sent: {message.hex()}')

    def receive(self):
        print("Listen to port...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.receiver_ip,self.rover_port_receive))

        timeout_seconds = 1
        sock.settimeout(timeout_seconds)

        try:
            data, addr = sock.recvfrom(1024)
            if addr[0] == self.rover_ip:
                print(f"Received message from {addr}: {data.hex()}")
                return data
        except socket.timeout:
            print("No response received within the timeout.")
            return None
        finally:
            sock.close()
