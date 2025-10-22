# telecommand_template.jinja

from spacebee_commander.telecommand_interface import TelecommandInterface



class take_photo(TelecommandInterface):
    

    def __init__(self):
        self.name = "take_photo"
        
        self.help = "take_photo: No input arguments"
        self.help_input = "None"
        
        self.operation = 11
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, args):
        
        # No arguments; nothing to process
        self.body = bytes()
        self.body_length = 0
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

