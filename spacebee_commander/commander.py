from spacebee_commander.message_manager import MessageManager, InteractionType
from spacebee_commander.communication import Communication
from spacebee_commander.commands_loader import load_commands
from spacebee_commander.telecommand_interface import TelecommandInterface


class Commander:

    telecommands = load_commands().values()
    messageManager = MessageManager()

    def __init__(self, transport: Communication):
        self.communication = transport

    def get_telecommand(self, id: int) -> TelecommandInterface | None:
        "Retrieve the telecommand using its telecommand ID."
        for telecommand in self.telecommands:
            if telecommand.get_operation_number() == id:
                return telecommand

    def send(self, telecommand: TelecommandInterface):
        "SEND. Consists of a single message sent without expecting a response."
        message = self.messageManager.make_message(telecommand, InteractionType.SEND)
        self.communication.send(message)

    def submit(self, telecommand: TelecommandInterface):
        "SUBMIT. It consists of a message with an acknowledgement response. It return True if ACK is okay and False otherwise "
        message = self.messageManager.make_message(telecommand, InteractionType.SUBMIT)
        self.communication.send(message)
        response=self.communication.receive()
        if response != None:
            ack=self.messageManager.unpack(response)

            if ack:
                print("ACK")
                return True
            else:
                print("No ACK")
                return False
        else: 
            print("Error no response receive")
            return False

    def request(self, telecommand: TelecommandInterface):
        "REQUEST. In of a message with a response message. It returns the message if everything is okay, False otherwise"

        message = self.messageManager.make_message(telecommand, InteractionType.REQUEST)
        self.communication.send(message)

        response=self.communication.receive()

        if response != None:
            unpack_response = self.messageManager.unpack(response)
            if isinstance(unpack_response, bytes):
                parsed_response = telecommand.parse_output_arguments(unpack_response)
                print(f"Command response: {parsed_response}")
                return parsed_response
            else:
                print("Error in the response")
                return False
        else:
            print("Error no response receive")
            return False

    def send_message(self, telecommand: TelecommandInterface, interaction_type: InteractionType):
        "Receive a telecommand and interaction type and then send the corresponding interaction."
        if interaction_type == InteractionType.SEND:
            return self.send(telecommand)
        elif interaction_type == InteractionType.SUBMIT:
            return self.submit(telecommand)
        elif interaction_type == InteractionType.REQUEST:
            return self.request(telecommand)
