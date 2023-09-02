from telecommand_interface import TelecommandInterface,struct
from datetime import timedelta

class set_mode(TelecommandInterface):
    def __init__(self):
        self.name="get_timestamp"
        self.help="Get timestamp"
        self.help_input="None" #Para que no se rompa en otro lado
        self.interaction_stage=1
        self.service=1
        self.operation=1
        self.area_version=0
        self.num_inputs=0

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=int(arg)
        self.body_length=(arg.bit_length() + 7) // 8
        self.body=arg.to_bytes(self.body_length, 'little')


    def parseOutputArguments(self,response):
        timestamp = timedelta(milliseconds=response)
        return timestamp

