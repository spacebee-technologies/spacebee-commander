import socket

class UdpHandler:

    def __init__(self,ip,port):
        self.rover_ip = ip
        self.rover_port =port

    def send(self,message):
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port))
        socket_file_descriptor.close()

        print(f'Sent: {message.hex()}')

class Comunication:
    def __init__(self):
        self.udp=UdpHandler('192.168.0.228',51524)

    def send(self,message):
        self.udp.send(message)
    
    def recive(self):
        print("Lisen to port...")
        