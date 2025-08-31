# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class set_mode(TelecommandInterface):
    
    enum_map_mode = {0: "OFF",1: "MANUAL",2: "AUTO"}

    def __init__(self):
        self.name = "set_mode"
        
        self.help = "set_mode: input args= mode(enum:0:OFF, 1:MANUAL, 2:AUTO)"
        self.help_input = " mode=(enum:0:OFF, 1:MANUAL, 2:AUTO)"
        
        self.operation = 2
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, args):
        
        if not isinstance(args, (list, tuple)) or len(args) != 1:
            raise ValueError("Expected 1 arguments, but got {}".format(len(args)))

        self.body = b""
        
        
        arg_0 = args[0]
        arg_0 = int(arg_0)
        if arg_0 not in self.enum_map_mode:
            raise ValueError(f"Invalid input for mode")
        self.body += arg_0.to_bytes(max((arg_0.bit_length() + 7) // 8, 1), 'little')
        

        self.body_length = len(self.body)
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

