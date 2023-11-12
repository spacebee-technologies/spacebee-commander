from telecommand_interface import TelecommandInterface,struct

class tm_enable(TelecommandInterface):
    def __init__(self):
        self.name="tm_enable"
        self.help="Enable TM"
        self.help_input="TM id= (int) ; state= 0:False 1:True"
        self.operation=7
        self.area_version=0
        self.num_inputs=2

    def loadInputArguments(self,arg):
        "Load input arguments into the body and calculate the body length."
        tm, state = arg.split()
        
        tm=int(tm)
        state=int(state)
        if tm<0 or (state!=0 and state!=1):
            raise ValueError

        tm_length_bytes = max((tm.bit_length() + 7) // 8, 1)
        tm_bytes = tm.to_bytes(tm_length_bytes, 'little')
        state_length_bytes=max((state.bit_length() + 7) // 8, 1)
        state_bytes=state.to_bytes(state_length_bytes, 'little')

        self.body=tm_bytes+state_bytes
        self.body_length=tm_length_bytes+state_length_bytes



    def parseOutputArguments(self,response):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        print("No output arguments!")
        return None