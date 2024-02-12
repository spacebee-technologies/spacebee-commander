from telecommand_interface import TelecommandInterface,struct


class get_timestamp(TelecommandInterface):
    def __init__(self):
        self.name="get_git_version"
        self.help="Get git version"
        self.help_input="None" 
        self.operation=10
        self.area_version=0
        self.num_inputs=0

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        self.body_length=0
        self.body=bytes()


    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        response_dict={}
        response_dict["message"] = response.decode('utf-8').strip('\x00')
        return response_dict

