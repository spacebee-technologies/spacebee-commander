from telecommand_interface import TelecommandInterface,struct

class set_target_velocity(TelecommandInterface):
    def __init__(self):
        self.name="set_target_velocity"
        self.help=""
        self.help_input="target velocity= float"
        self.operation=4
        self.area_version=0
        self.num_inputs=1

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=float(arg)
        self.body=struct.pack('<f', arg)    # <f float to little-endian bytes
        self.body_length=len(self.body)

    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None