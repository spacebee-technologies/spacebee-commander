from telecommand_interface import TelecommandInterface,struct
from datetime import timedelta


class get_timestamp(TelecommandInterface):
    def __init__(self):
        self.name="get_timestamp"
        self.help="Get timestamp"
        self.help_input="None" 
        self.operation=1
        self.area_version=0
        self.num_inputs=0

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        self.body_length=0
        self.body=bytes()


    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        response_dict={}
        response_int=int.from_bytes(response,"little")
        timestamp = timedelta(milliseconds=response_int)
        str_timestamp=str(timestamp)
        response_dict["timestamp"]=str_timestamp
        return response_dict

