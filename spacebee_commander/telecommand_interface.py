import abc


class TelecommandInterface(abc.ABC):

    operation = None          # 16 bits: Unique identifier for a given telemetry or telecommand
    body_length = None        # 16 bits: Longitude in bytes of the message body
    body = b''
    name = ""                 # string: Name of the telecommand
    help = ""                 # string: Description and usage for the telecommand
    help_input = ""           # string: Description for the input arguments
    num_inputs = None         # int: Number of input arguments for this command

    def getOperationNumber(self):
        return self.operation

    @abc.abstractmethod
    def loadInputArguments(self, raw):
        "Load input arguments into the body and calculate the body length."
        ...

    @abc.abstractmethod
    def parseOutputArguments(self, response: bytes):
        "Parse the output argument, where the response is a byte sequence, and return a dictionary."
        ...
