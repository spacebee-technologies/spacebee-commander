from message_manager import MessageManager 
from Telecommands import all_telecommands
from communcation import Comunication

class Commander:


    telecommands = [cls() for cls in all_telecommands]
    messageManager = MessageManager()
    communication = Comunication()

    def __init__(self):
        pass


    def getTelecommand(self,id):
        "Retrieve the telecommand using its telecommand ID."
        for telecommand in self.telecommands:
            if telecommand.getOperationNumber() == id:
                return telecommand
    

    def send(self, telecommand):
        "SEND. Consists of a single message sent without expecting a response."
        interaction_tpye=1
        message = self.messageManager.make_message(telecommand,interaction_tpye)
        self.communication.send(message)


    def submit(self, telecommand):
        "SUBMIT. It consists of a message with an acknowledgement response. It return True if ACK is okay and False otherwise " 
        interaction_tpye=2
        message = self.messageManager.make_message(telecommand,interaction_tpye)
        self.communication.send(message)
        response=self.communication.recive()

        ack=unpack_respose=self.messageManager.unpack(response)
        if ack:
            print("ACK")


            
    
    def request(self, telecommand):
        "REQUEST. In of a message with a response message. It returns the message if everything is okay, False otherwise"
        
        interaction_tpye=3
        message = self.messageManager.make_message(telecommand,interaction_tpye)
        self.communication.send(message)

        response=self.communication.recive()
        
        if response!= None:
            unpack_respose=self.messageManager.unpack(response)
            response_dict=telecommand.parseOutputArguments(unpack_respose)
            print(f"Response_dict: {response_dict}")
            return response_dict
        else:
            return False


    def send_message(self,telecommand,interaction_type):
        "Recive a telecommand and interaction type and then send the corresponding interaction."
        if interaction_type==1:
            self.send(telecommand)
        elif interaction_type==2:
            self.submit(telecommand)
        elif interaction_type==3:
            self.request(telecommand)