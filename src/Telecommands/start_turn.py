# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class start_turn(TelecommandInterface):
    
    enum_map_turnDirection = {0: "LEFT",1: "RIGHT"}

    def __init__(self):
        self.name = "start_turn"
        
        self.help = "start_turn: input args= turnDirection(enum:0:LEFT, 1:RIGHT)"
        self.help_input = " turnDirection=(enum:0:LEFT, 1:RIGHT)"
        
        self.operation = 8
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, args):
        
        if not isinstance(args, (list, tuple)) or len(args) != 1:
            raise ValueError("Expected 1 arguments, but got {}".format(len(args)))

        self.body = b""
        
        
        arg_0 = args[0]
        arg_0 = int(arg_0)
        if arg_0 not in self.enum_map_turnDirection:
            raise ValueError(f"Invalid input for turnDirection")
        self.body += arg_0.to_bytes(max((arg_0.bit_length() + 7) // 8, 1), 'little')
        

        self.body_length = len(self.body)
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

