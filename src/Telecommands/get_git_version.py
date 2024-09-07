# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class get_git_version(TelecommandInterface):
    

    def __init__(self):
        self.name = "get_git_version"
        self.help = "get_git_version"
        self.help_input = "None"
        self.operation = 10
        self.area_version = 0
        self.num_inputs = 0

    def loadInputArguments(self, arg):
        self.body = bytes()
        self.body_length = 0



    def parseOutputArguments(self, response):
        response_dict = {}
        response_dict['version'] = response.decode('utf-8').strip()
    
        return response_dict
