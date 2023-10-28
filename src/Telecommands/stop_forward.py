from telecommand_interface import TelecommandInterface,struct

class stop_forward(TelecommandInterface):
    def __init__(self):
        self.name="stop_forward"
        self.help=""
        self.help_input="None"
        self.operation=6
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