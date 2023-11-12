from telecommand_interface import TelecommandInterface,struct

class set_mode(TelecommandInterface):
    def __init__(self):
        self.name="set_mode"
        self.help="input args= 0:OFF 1:Manual 2:Automatic"
        self.help_input="mode=0:OFF 1:Manual 2:Automatic"
        self.operation=2
        self.area_version=0
        self.num_inputs=1

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        arg=int(arg)
        if arg!=0 and arg!=1 and arg!=2:
            raise ValueError
            
        self.body_length=max((arg.bit_length() + 7) // 8,1)
        self.body=arg.to_bytes(self.body_length, 'little')


    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None