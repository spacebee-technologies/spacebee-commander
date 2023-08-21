from telecommand_interface import TelecommandInterface,struct

class set_profile_mode(TelecommandInterface):
    def __init__(self):
        self.name="Set profile mode"
        self.help="0:FORWARD 1:SET HEIGHT 2:TURN"
        self.interaction_stage=1
        self.service=1
        self.operation=3
        self.area_version=0

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=int(arg)
        self.body_length=arg.bit_length()
        self.body=arg.to_bytes(self.body_length, 'little')

    def parseOutputArguments(self,response):
        print("No output arguments!")
        return None