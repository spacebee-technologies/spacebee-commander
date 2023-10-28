from telecommand_interface import TelecommandInterface,struct

class start_turn(TelecommandInterface):
    def __init__(self):
        self.name="start_turn"
        self.help=""
        self.help_input="0: LEFT 1: RIGHT"
        self.operation=8
        self.area_version=0
        self.num_inputs=1

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=int(arg)
        self.body_length=(arg.bit_length() + 7) // 8
        self.body=arg.to_bytes(self.body_length, 'little')

    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None