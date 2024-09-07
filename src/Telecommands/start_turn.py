# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class start_turn(TelecommandInterface):
    
    enum_map_turnDirection = {0: "LEFT",1: "RIGHT"}

    def __init__(self):
        self.name = "start_turn"
        self.help = "start_turn: input args= turnDirection:0:LEFT, 1:RIGHT"
        self.help_input = "turnDirection =0:LEFT, 1:RIGHT"
        self.operation = 8
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, arg):
        arg = int(arg)
        if arg not in self.enum_map_turnDirection:
            raise ValueError(f"Invalid input for turnDirection")
        self.body = arg.to_bytes(max((arg.bit_length() + 7) // 8, 1), 'little')
        self.body_length = len(self.body)



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None
