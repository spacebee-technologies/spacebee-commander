# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class set_target_velocity(TelecommandInterface):
    

    def __init__(self):
        self.name = "set_target_velocity"
        self.help = "set_target_velocity"
        self.help_input = "targetVelocity=(float)"
        self.operation = 4
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, arg):
        arg = float(arg)
        self.body = struct.pack('f', arg)
        self.body_length = len(self.body)



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

