import socket
import network_parameters as np

class UdpHandler:

    def __init__(self,ip,port_send,reciver_ip,port_response):
        self.rover_ip = ip
        self.rover_port_send =port_send
        self.reciver_ip=reciver_ip
        self.rover_port_recive=port_response

    def send(self,message):
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port_send))
        socket_file_descriptor.close()

        print(f'Sent: {message.hex()}')

    def recive(self):
        print("Lisen to port...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.reciver_ip,self.rover_port_recive))


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
        self.udp=UdpHandler(np.ROVER_IP,np.ROVER_PORT_SEND,np.RECIVER_IP,np.REVICER_PORT)

    def send(self,message):
        self.udp.send(message)
    
    def recive(self):
        return self.udp.recive()
        