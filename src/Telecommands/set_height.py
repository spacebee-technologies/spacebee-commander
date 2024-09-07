# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class set_height(TelecommandInterface):
    

    def __init__(self):
        self.name = "set_height"
        self.help = "set_height"
        self.help_input = "targetAngleDegrees=(float)"
        self.operation = 3
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, arg):
        arg = float(arg)
        self.body = struct.pack('f', arg)
        self.body_length = len(self.body)



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None
