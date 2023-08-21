import socket
ROVER_IP= '192.168.0.228'
ROVER_PORT_SEND= 51524
ROVER_PORT_RECIVE= 51525

class UdpHandler:

    def __init__(self,ip,port_send,port_response):
        self.rover_ip = ip
        self.rover_port_send =port_send
        self.rover_port_recive=port_response

    def send(self,message):
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port))
        socket_file_descriptor.close()

        print(f'Sent: {message.hex()}')

    def recive(self):
        print("Lisen to port...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.rover_ip,51525))


        sock.settimeout(1)

        try:
            data, addr = sock.recvfrom(1024)

            print(f"Recibido mensaje de {addr}: {data.hex()}")

            return data
        except socket.timeout:

            print("No response received within the timeout.")

            return None
        finally:
            sock.close()

       

class Comunication:
    def __init__(self):
        self.udp=UdpHandler(ROVER_IP,ROVER_PORT_SEND,ROVER_PORT_RECIVE)

    def send(self,message):
        self.udp.send(message)
    
    def recive(self):
        return self.udp.recive()
        