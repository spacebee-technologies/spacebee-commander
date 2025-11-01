import struct
import enum

from spacebee_commander.telecommand_interface import TelecommandInterface


class InteractionType(enum.IntEnum):
    SEND = 1
    SUBMIT = 2
    REQUEST = 3
    INVOKE = 4
    PROGRESS = 5
    PUBSUB = 6


class MessageManager:

    __header_format='<QHBQHHHBH'
    __last_transaction_id=0

    def _make_header(self, telecommand: TelecommandInterface, type: InteractionType):
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

    def make_CRC(self, header, body):
        "Make CRC with 16 bits CTC-16-CCITT with polynomial x^16+x^12+x^5+1."
        data=header+body
        crc = 0xFFFF
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1

        return crc & 0xFFFF

    def check_CRC(self,header,body,crc_check):
        crc=self.make_CRC(header,body).to_bytes(2, 'little')
        if crc == crc_check:
            return True
        else:
            return False

    def make_message(self, telecommand: TelecommandInterface, type: InteractionType):
        header = self._make_header(telecommand, type)
        crc = self.make_CRC(header, telecommand.body).to_bytes(2, 'little')
        return header + telecommand.body + crc

    def unpack(self, response: bytes):
        header_size = struct.calcsize(self.__header_format)
        header_data = response[:header_size]
        timestamp, interaction_type, interaction_stage, transaction_id, service, operation, area_version, is_error_message, body_length = struct.unpack(self.__header_format, header_data)
        body_response = response[header_size:-2]
        crc_response = response[-2:]

        if interaction_stage != 1:  # Check for a command response
            if not is_error_message:

                if self.check_CRC(header_data,body_response,crc_response):

                    if interaction_type == InteractionType.SUBMIT:
                        print(f"body:{body_response}")
                        if not body_response:
                            return True
                        else:
                            return False  # ACK has empty body

                    elif interaction_type == InteractionType.REQUEST:
                        return body_response

                    elif interaction_type == InteractionType.PUBSUB:
                        print("Message is telemetry")

                else:
                    print("CRC check failed. Error in the communication detected.")
            else:
                print("The message is an error")
        else:
            print("Error, interaction stage not valid")
