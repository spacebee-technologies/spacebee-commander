# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class stop_forward(TelecommandInterface):
    

    def __init__(self):
        self.name = "stop_forward"
        self.help = "stop_forward"
        self.help_input = "None"
        self.operation = 6
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, arg):
        self.body = bytes()
        self.body_length = 0



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None
