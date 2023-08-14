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
        for telecommand in self.telecommands:
            if telecommand.getOperationNumber() == id:
                return telecommand
    
    def send(self, telecommand):
        interaction_tpye=1
        message = self.messageManager.make_message(telecommand,interaction_tpye)
        self.communication.send(message)

    def submit(self, telecommand, messageManager):
        print('submit')
    
    def request(self, telecommand, messageManager):
        print('request')

com=Commander()