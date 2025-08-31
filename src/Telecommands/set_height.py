# telecommand_template.jinja

from telecommand_interface import TelecommandInterface, struct



class set_height(TelecommandInterface):
    

    def __init__(self):
        self.name = "set_height"
        
        self.help = "set_height: input args= targetAngleDegrees(float)"
        self.help_input = " targetAngleDegrees=(float)"
        
        self.operation = 3
        self.area_version = 0
        self.num_inputs = 1

    def loadInputArguments(self, args):
        
        if not isinstance(args, (list, tuple)) or len(args) != 1:
            raise ValueError("Expected 1 arguments, but got {}".format(len(args)))

        self.body = b""
        
        
        arg_0 = args[0]
        arg_0 = float(arg_0)
        self.body += struct.pack('f', arg_0)
        

        self.body_length = len(self.body)
        


    def parseOutputArguments(self, response):
        print("No output arguments!")
        return None

