from telecommand_interface import TelecommandInterface,struct

class set_target_velocity(TelecommandInterface):
    def __init__(self):
        self.name="Set target velocity"
        self.help=""
        self.interaction_stage=1
        self.service=1
        self.operation=4
        self.area_version=0

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=float(arg)
        self.body=struct.pack('<f', arg)    # <f float to little-endian bytes
        self.body_length=len(self.body)

    def parseOutputArguments(self,response):
        print("No output arguments!")
        return None