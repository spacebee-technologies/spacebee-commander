from spacebee_commander.telecommand_interface import TelecommandInterface
from spacebee_commander.message_header import MessageHeader, InteractionType, Service, PROTOCOL_VERSION


class MessageManager:

    __last_transaction_id = 0

    def _make_header(self, telecommand: TelecommandInterface, type: InteractionType) -> bytes:
        timestamp = 0  # TODO: Implement a real timestamp
        self.__last_transaction_id += 1

        if telecommand.operation is None:
            raise ValueError("Telecommand operation number is not set.")
        if telecommand.body_length is None:
            raise ValueError("Telecommand body length is not set.")

        header = MessageHeader(
            timestamp=timestamp,
            interaction_type=type,
            interaction_stage=1,
            transaction_id=self.__last_transaction_id,
            service=Service.TELECOMMAND,
            operation=telecommand.operation,
            area_version=PROTOCOL_VERSION,
            is_error_message=0,
            body_length=telecommand.body_length
        )

        return MessageHeader.pack(header)

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
        header_size = MessageHeader.size()
        header_data = response[:header_size]
        header = MessageHeader.unpack(header_data)
        body_response = response[header_size:-2]
        crc_response = response[-2:]

        if header.interaction_stage != 1:  # Check for a command response
            if not header.is_error_message:

                if self.check_CRC(header_data, body_response, crc_response):

                    if header.interaction_type == InteractionType.SUBMIT:
                        print(f"body:{body_response}")
                        if not body_response:
                            return True
                        else:
                            return False  # ACK has empty body

                    elif header.interaction_type == InteractionType.REQUEST:
                        return body_response

                    elif header.interaction_type == InteractionType.PUBSUB:
                        print("Message is telemetry")

                else:
                    print("CRC check failed. Error in the communication detected.")
            else:
                print("The message is an error")
        else:
            print("Error, interaction stage not valid")
