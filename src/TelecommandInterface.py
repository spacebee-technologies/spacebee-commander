import time
import struct

class TelecommandInterface:

    timestamp = None            # Time in milliseconds
    interaction_type = None     # 16 bits	1 for SEND, 2 for SUBMIT, 3 for REQUEST and 6 for PUBSUB 
    interaction_stage = None    # 8 bits	1 or 2 according to message order
    transaction_id = None       # Unique incremental identifier
    service= None               # 0 for telemetries (TM) or 1 for telecommands (TC)
    operation=None              # 16 bits	Unique identifier for a given telemetry or telecommand
    area_version=None           # 16 bits	Protocol version
    is_error_message=None       # 8 bit	Boolean value to indicate if is an error message (0x1 for true, 0x0 for false)
    body_length = None          # 16 bits	Longitude in bytes of the message body
    
    __last_transaction_id=0
    __header_format='<QHBQHHHBH'
    body= None
    crc= None                   # 16 bits CTC-16-CCITT with polynomial x^16+x^12+x^5+1.
    header= None

    def __init__(self):
        TelecommandInterface.__last_transaction_id += 1
        self.transaction_id = TelecommandInterface.__last_transaction_id

    def loadInputArguments(self,arg):
        self.body=arg.to_bytes(self.body_length, 'little')
        self.CRC()

    def CRC(self):
        data=self.header+self.body
        self.crc = bytes.fromhex('0000')

    def getOperationNumber(self):
        return self.operation
    
    def make_header(self):
        self.header = struct.pack(self.__header_format, self.timestamp,
                                self.interaction_type,
                                self.interaction_stage,
                                self.transaction_id,
                                self.service,
                                self.operation,
                                self.area_version,
                                self.is_error_message,
                                self.body_length)

    def get_message(self):
        return self.header + self.body + self.crc

    def parseOutputArguments(self,response):
        header_size = struct.calcsize(self.__header_format)
        header_data = response[:header_size]
        timestamp, interaction_type, interaction_stage, transaction_id, service, operation, area_version, is_error_message, body_length = struct.unpack(self.__header_format, header_data)

        body = response[header_size:-2]  
        crc = response[-2:] 

        if not is_error_message:
            #TODO check CRC
            return body
        else:
            raise "There is an error"




class set_mode(TelecommandInterface):
    def __init__(self):
        super().__init__() 
        self.timestamp=int(time.time() * 1000)
        self.interaction_type=2
        self.interaction_stage=1
        self.service=1
        self.operation=2
        self.area_version=0
        self.is_error_message=0
        self.body_length=1

        self.make_header()

class set_profile_mode(TelecommandInterface):
    def __init__(self):
        super().__init__() 
        self.timestamp=int(time.time() * 1000)
        self.interaction_type=2
        self.interaction_stage=1
        self.service=1
        self.operation=3
        self.area_version=0
        self.is_error_message=0
        self.body_length=1

class set_target_velocity(TelecommandInterface):
    def __init__(self):
        super().__init__() 
        self.timestamp=int(time.time() * 1000)
        self.interaction_type=2
        self.interaction_stage=1
        self.service=1
        self.operation=4
        self.area_version=0
        self.is_error_message=0
        self.body_length=4

