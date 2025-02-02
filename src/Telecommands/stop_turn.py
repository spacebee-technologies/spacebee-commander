# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class stop_turn(TelecommandInterface):
    

    def __init__(self):
        self.name = "stop_turn"
        self.help = "stop_turn"
        self.help_input = "None"
        self.operation = 9
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, arg):
        self.body = bytes()
        self.body_length = 0



    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

