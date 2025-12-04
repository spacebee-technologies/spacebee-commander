from spacebee_commander.telecommand_interface import TelecommandInterface
from spacebee_commander.message_header import MessageHeader, InteractionType, Service, PROTOCOL_VERSION
import logging

logger = logging.getLogger(__name__)

class MessageManager:

    __last_transaction_id = 0

    def _make_header(self, telecommand: TelecommandInterface, type: InteractionType) -> bytes:
        logger.debug(f"Creating header for telecommand: {telecommand.name}, interaction: {type.name}")
        timestamp = 0  # TODO: Implement a real timestamp
        self.__last_transaction_id += 1

        if telecommand.operation is None:
            logger.error("Telecommand operation number is not set")
            raise ValueError("Telecommand operation number is not set.")
        if telecommand.body_length is None:
            logger.error("Telecommand body length is not set")
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

        logger.debug(f"Header created: transaction_id={self.__last_transaction_id}, operation={telecommand.operation}")
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
        crc_calculated = self.make_CRC(header, body)
        crc_received = int.from_bytes(crc_check, "little")
        if crc_calculated == crc_received:
            logger.debug(f"CRC check passed (0x{crc_calculated:04x})")  # Ahora incluye el valor
            return True
        else:
            logger.error(f"CRC check failed - calculated: 0x{crc_calculated:04x}, received: 0x{crc_received:04x}")
            return False

    def make_message(self, telecommand: TelecommandInterface, type: InteractionType):
        logger.debug(f"Building message for telecommand: {telecommand.name}")
        try:
            header = self._make_header(telecommand, type)
            crc = self.make_CRC(header, telecommand.body).to_bytes(2, "little")
            message = header + telecommand.body + crc

            logger.debug(f"Message created successfully: {len(message)} bytes total")
            logger.debug(f"Message breakdown: header={len(header)}B, body={len(telecommand.body)}B, crc=2B")
            return message
        except Exception as e:
            logger.error(f"Failed to create message for {telecommand.name}: {e}", exc_info=True)
            return None

    def unpack(self, response: bytes):
        logger.debug(f"Unpacking response: {len(response)} bytes")
        try:
            if not response:
                logger.error("Empty response received")
                return None

            header_size = MessageHeader.size()
            min_size = header_size + 2

            if len(response) < min_size:
                logger.error(
                    f"Response too short: {len(response)} bytes, expected at least {min_size} bytes"
                )
                logger.debug(f"Raw data: {response.hex()}")
                return None

            header_data = response[:header_size]
            body_response = response[header_size:-2]
            crc_response = response[-2:]

            logger.debug(f"Message parts: header={len(header_data)}B, body={len(body_response)}B, crc=2B")
            try:
                header = MessageHeader.unpack(header_data)
            except Exception as e:
                logger.error(f"Failed to unpack header: {e}")
                logger.debug(f"Header data ({len(header_data)} bytes): {header_data.hex()}")
                return None

            logger.debug(
                f"Header unpacked: interaction={header.interaction_type}, "
                f"stage={header.interaction_stage}, transaction_id={header.transaction_id}"
            )

            if header.interaction_stage == 1:
                logger.error(f"Invalid interaction_stage: {header.interaction_stage} (expected != 1)")
                return None

            if header.is_error_message:
                logger.error("Response contains error flag")
                logger.debug(f"Error body: {body_response.hex()}")
                return None

            if not self.check_CRC(header_data, body_response, crc_response):
                return None

            if header.interaction_type == InteractionType.SUBMIT:
                if body_response:
                    logger.warning(f"SUBMIT ACK has non-empty body ({len(body_response)} bytes)")
                    return None
                return True

            elif header.interaction_type == InteractionType.REQUEST:
                logger.info(f"REQUEST response received: {len(body_response)} bytes")
                logger.debug(f"Response body: {body_response.hex()}")
                return body_response

            elif header.interaction_type == InteractionType.PUBSUB:
                logger.info("Received telemetry message (PUBSUB)")
                return None
            else:
                logger.warning(f"Unknown interaction_type: {header.interaction_type}")
                return None

        except Exception as e:
            logger.critical(f"Unexpected error in unpack: {e}", exc_info=True)
            logger.debug(f"Response length: {len(response) if response else 0} bytes")
            if response:
                logger.debug(f"Response data: {response.hex()}")
            return None
