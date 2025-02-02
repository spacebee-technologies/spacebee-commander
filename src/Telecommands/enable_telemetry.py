# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class enable_telemetry(TelecommandInterface):
    
    enum_map_action = {0: "DISABLE",1: "ENABLE"}

    def __init__(self):
        self.name = "enable_telemetry"
        self.help = "enable_telemetry"
        self.help_input = "operationId=(uint16_t)"
        self.help = "enable_telemetry: input args= action:0:DISABLE, 1:ENABLE"
        self.help_input = "action =0:DISABLE, 1:ENABLE"
        self.operation = 7
        self.area_version = 0
        self.num_inputs = 2

    def loadInputArguments(self, arg):
        self.body = arg.to_bytes(2, 'little')
        self.body_length = len(self.body)
        arg = int(arg)
        if arg not in self.enum_map_action:
            raise ValueError(f"Invalid input for action")
        self.body = arg.to_bytes(max((arg.bit_length() + 7) // 8, 1), 'little')
        self.body_length = len(self.body)



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

