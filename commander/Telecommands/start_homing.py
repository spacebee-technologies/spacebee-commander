from telecommand_interface import TelecommandInterface,struct

class start_homing(TelecommandInterface):
    def __init__(self):
        self.name="start_homing"
        self.help=""
        self.help_input="None"
        self.operation=12
        self.area_version=0
        self.num_inputs=0
    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        self.body_length=0
        self.body=bytes()

    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None