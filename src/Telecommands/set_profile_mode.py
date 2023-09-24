from telecommand_interface import TelecommandInterface,struct

class set_profile_mode(TelecommandInterface):
    def __init__(self):
        self.name="set_profile_mode"
        self.help="input args= 0:FORWARD 1:SET HEIGHT 2:TURN"
        self.help_input="profile mode= 0:FORWARD 1:SET HEIGHT 2:TURN"
        self.operation=3
        self.area_version=0
        self.num_inputs=1

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=int(arg)
        self.body_length=arg.bit_length()
        self.body=arg.to_bytes(self.body_length, 'little')

    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None