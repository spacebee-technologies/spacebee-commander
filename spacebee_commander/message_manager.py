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
        data = header + body
        crc = 0xFFFF
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1

        return crc & 0xFFFF

    def check_CRC(self, header, body, crc_check):
        crc = self.make_CRC(header, body).to_bytes(2, "little")
        if crc == crc_check:
            return True
        else:
            return False

    def make_message(self, telecommand: TelecommandInterface, type: InteractionType):
        try:
            header = self._make_header(telecommand, type)
            crc = self.make_CRC(header, telecommand.body).to_bytes(2, "little")
            return header + telecommand.body + crc
        except Exception as e:
            print(f"[ERROR] Failed to create message: {e}")
            return None

    def unpack(self, response: bytes):
        try:
            if not response:
                print("[ERROR] Empty response received")
                return None

            header_size = MessageHeader.size()
            min_size = header_size + 2

            if len(response) < min_size:
                print(f"[ERROR] Response too short: {len(response)} bytes, expected at least {min_size}")
                print(f"[DEBUG] Raw data: {response.hex()}")
                return None

            header_data = response[:header_size]
            body_response = response[header_size:-2]
            crc_response = response[-2:]

            try:
                header = MessageHeader.unpack(header_data)
            except Exception as e:
                print(f"[ERROR] Failed to unpack header: {e}")
                print(f"[DEBUG] Header data ({len(header_data)} bytes): {header_data.hex()}")
                return None

            if header.interaction_stage == 1:
                print(f"[ERROR] Invalid interaction_stage: {header.interaction_stage}")
                return None

            if header.is_error_message:
                print("[ERROR] Response returned an error message")
                print(f"[DEBUG] Error body: {body_response.hex()}")
                return None

            if not self.check_CRC(header_data, body_response, crc_response):
                calculated = self.make_CRC(header_data, body_response)
                received = int.from_bytes(crc_response, "little")
                print("[ERROR] CRC check failed - communication error detected")
                print(f"[DEBUG] Calculated CRC: 0x{calculated:04x}")
                print(f"[DEBUG] Received CRC: 0x{received:04x}")
                return None

            if header.interaction_type == InteractionType.SUBMIT:
                if body_response:
                    print(f"[WARNING] SUBMIT ACK has non-empty body ({len(body_response)} bytes)")
                    return None
                return True

            elif header.interaction_type == InteractionType.REQUEST:
                return body_response

            elif header.interaction_type == InteractionType.PUBSUB:
                print("Message is telemetry")
                return None
            else:
                print(f"[WARNING] Unknown interaction_type: {header.interaction_type}")
                return None

        except Exception as e:
            print(f"[CRITICAL ERROR] Unexpected error in unpack: {e}")
            print(f"[DEBUG] Response length: {len(response) if response else 0} bytes")
            if response:
                print(f"[DEBUG] Response data: {response.hex()}")
            return None
