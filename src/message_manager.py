from telecommand_interface import TelecommandInterface
import struct


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
            "Make CRC with 16 bits CTC-16-CCITT with polynomial x^16+x^12+x^5+1."
            
           
            data=header+telecommand.body

            #TODO check CRC
            return bytes.fromhex('0000') 

    def check_CRC(self,header,body,crc):
        #TODO check CRC
        return True

    def make_message(self,telecommand, type):
        header= self.make_header(telecommand,type)
        crc=self.make_CRC(telecommand,header)
        return header+telecommand.body+crc 
        
    def unpack(self,response):
        header_size = struct.calcsize(self.__header_format)
        header_data = response[:header_size]
        timestamp, interaction_type, interaction_stage, transaction_id, service, operation, area_version, is_error_message, body_length = struct.unpack(self.__header_format, header_data)
        body_response = response[header_size:-2]  
        crc_response = response[-2:] 
        

        if interaction_stage!=1:   #Checkea que el interaction type es una respuesta del mensaje
            if not is_error_message:
                
                if self.check_CRC(header_data,body_response,crc_response):

                    if interaction_type==2:
                        if body_response == None:
                            return True
                        else:
                            return False          #ACK is empty body

                    elif interaction_type==3:
                        #Search for a telecomand with operation and execute the function parseOutputArguments
                        return body_response
                    
                    elif interaction_type==6:
                        #It is telemetry
                        print("Error is telemetry")
                
                else:
                    print("CRC check failed. Error in the communication detected.")
            else:
                print("The message is an error")

    