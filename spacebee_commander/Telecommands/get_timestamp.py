# telecommand_template.jinja

from spacebee_commander.telecommand_interface import TelecommandInterface
from datetime import timedelta


class get_timestamp(TelecommandInterface):
    

    def __init__(self):
        self.name = "get_timestamp"
        
        self.help = "get_timestamp: No input arguments"
        self.help_input = "None"
        
        self.operation = 1
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, args):
        
        # No arguments; nothing to process
        self.body = bytes()
        self.body_length = 0
        


    def parseOutputArguments(self, response):
        response_dict = {}
        response_int = int.from_bytes(response, 'little')
        timestamp = timedelta(milliseconds=response_int)
        response_dict['Date'] = str(timestamp)
    
        return response_dict

