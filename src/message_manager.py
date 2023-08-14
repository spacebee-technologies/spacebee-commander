from telecommand_interface import TelecommandInterface
import struct
import time


class MessageManager:

    __header_format='<QHBQHHHBH'
    __last_transaction_id=0


    def make_header(self, telecommand: TelecommandInterface, type):
        timestamp=0
        MessageManager.__last_transaction_id += 1

        return struct.pack(self.__header_format, timestamp,
                                type,
                                telecommand.interaction_stage,
                                MessageManager.__last_transaction_id,
                                telecommand.service,
                                telecommand.operation,
                                telecommand.area_version,
                                telecommand.is_error_message,
                                telecommand.body_length)
        
    def make_CRC(self,telecommand: TelecommandInterface, header):
            data=header+telecommand.body
            return bytes.fromhex('0000') # 16 bits CTC-16-CCITT with polynomial x^16+x^12+x^5+1.

    def make_message(self,telecommand, type):
        header= self.make_header(telecommand,type)
        crc=self.make_CRC(telecommand,header)
        return header+telecommand.body+crc 
        
    def unpack(self,response):
        header_size = struct.calcsize(self.__header_format)
        header_data = response[:header_size]
        timestamp, interaction_type, interaction_stage, transaction_id, service, operation, area_version, is_error_message, body_length = struct.unpack(self.__header_format, header_data)

        body = response[header_size:-2]  
        crc = response[-2:] 

        if interaction_type!=1:   #Hay que checkearlo? o ya suponemos que nunca se va a enviar una respuesta de una interaccion
            if not is_error_message:
                #TODO check CRC

                if interaction_type==2:
                    return body            #ACK is empty body
                
                if interaction_type==3:
                    #Search for a telecomand with operation and execute the function parseOutputArguments
                    print('')
                if interaction_type==6:
                    #It is telemetry
                    #Separar la telemetria a parte. no lo veo yo
                    print("")
            else:
                raise "There is an error"

    