import socket
ROVER_IP= '192.168.0.228'
RECIVER_IP='192.168.0.185'
ROVER_PORT_SEND= 51524
REVICER_PORT= 51525

class UdpHandler:

<<<<<<< HEAD
    def __init__(self,ip,port_send,reciver_ip,port_response):
        self.rover_ip = ip
        self.rover_port_send =port_send
        self.reciver_ip=reciver_ip
        self.rover_port_recive=port_response
=======
    def __init__(self,ip,port_send,reciver_ip,reciver_port):
        self.rover_ip = ip
        self.rover_port_send =port_send
        self.reciver_ip=reciver_ip
        self.reciver_port=reciver_port

>>>>>>> refs/remotes/origin/1-draft-cli

    def send(self,message):
        socket_file_descriptor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_file_descriptor.sendto(message, (self.rover_ip, self.rover_port_send))
        socket_file_descriptor.close()

        print(f'Sent: {message.hex()}')

    def recive(self):
        print("Lisen to port...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
<<<<<<< HEAD
        sock.bind((self.reciver_ip,self.rover_port_recive))
=======
        sock.bind((self.reciver_ip,self.reciver_port))
>>>>>>> refs/remotes/origin/1-draft-cli


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
<<<<<<< HEAD
        self.udp=UdpHandler(ROVER_IP,ROVER_PORT_SEND,RECIVER_IP,ROVER_PORT_RECIVE)
=======
        self.udp=UdpHandler(ROVER_IP,ROVER_PORT_SEND,RECIVER_IP,REVICER_PORT)
>>>>>>> refs/remotes/origin/1-draft-cli

    def send(self,message):
        self.udp.send(message)
    
    def recive(self):
        return self.udp.recive()
        