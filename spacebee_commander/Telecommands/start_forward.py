# telecommand_template.jinja

from spacebee_commander.telecommand_interface import TelecommandInterface



class start_forward(TelecommandInterface):
    

    def __init__(self):
        self.name = "start_forward"
        
        self.help = "start_forward: No input arguments"
        self.help_input = "None"
        
        self.operation = 5
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, args):
        
        # No arguments; nothing to process
        self.body = bytes()
        self.body_length = 0
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

