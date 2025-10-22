# telecommand_template.jinja
from commander.telecommand_interface import TelecommandInterface



class enable_telemetry(TelecommandInterface):
    
    enum_map_action = {0: "DISABLE",1: "ENABLE"}

    def __init__(self):
        self.name = "enable_telemetry"
        
        self.help = "enable_telemetry: input args= operationId(uint16_t),  action(enum:0:DISABLE, 1:ENABLE)"
        self.help_input = " operationId=(uint16_t),  action=(enum:0:DISABLE, 1:ENABLE)"
        
        self.operation = 7
        self.area_version = 0
        self.num_inputs = 2

    def loadInputArguments(self, args):
        
        if not isinstance(args, (list, tuple)) or len(args) != 2:
            raise ValueError("Expected 2 arguments, but got {}".format(len(args)))

        self.body = b""
        
        
        arg_0 = args[0]
        self.body += int(arg_0).to_bytes(2, 'little')
        
        arg_1 = args[1]
        arg_1 = int(arg_1)
        if arg_1 not in self.enum_map_action:
            raise ValueError(f"Invalid input for action")
        self.body += arg_1.to_bytes(max((arg_1.bit_length() + 7) // 8, 1), 'little')
        

        self.body_length = len(self.body)
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

