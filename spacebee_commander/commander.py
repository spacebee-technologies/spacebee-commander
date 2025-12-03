from spacebee_commander.message_manager import MessageManager, InteractionType
from spacebee_commander.communication import Communication
from spacebee_commander.commands_loader import load_commands
from spacebee_commander.telecommand_interface import TelecommandInterface
import logging

logger = logging.getLogger(__name__)

class Commander:

    telecommands = load_commands().values()
    message_manager = MessageManager()

    def __init__(self, transport: Communication):
        self.communication = transport
        logger.info("Commander initialized")
        logger.debug(f"Loaded {len(self.telecommands)} telecommands")

    def get_telecommand_by_id(self, id: int) -> TelecommandInterface | None:
        """Retrieve the telecommand using its telecommand ID."""
        logger.debug(f"Searching telecommand by ID: {id}")
        for telecommand in self.telecommands:
            if telecommand.get_operation_number() == id:
                logger.debug(f"Found telecommand: {telecommand.get_name()} (ID: {id})")
                return telecommand
        logger.warning(f"Telecommand with ID {id} not found")
        return None

    def get_telecommand_by_name(self, name: str) -> TelecommandInterface | None:
        """Retrieve the telecommand by its name."""
        logger.debug(f"Searching telecommand by name: {name}")
        for telecommand in self.telecommands:
            if telecommand.get_name() == name:
                logger.debug(f"Found telecommand: {name} (ID: {telecommand.get_operation_number()})")
                return telecommand
        logger.warning(f"Telecommand with name '{name}' not found")
        return None

    def send(self, telecommand: TelecommandInterface):
        """Consists of a single message sent without expecting a response."""
        logger.info(f"Sending telecommand: {telecommand.get_name()} (SEND mode)")
        try:
            message = self.message_manager.make_message(telecommand, InteractionType.SEND)
            logger.debug(f"Message created: {len(message)} bytes")
            self.communication.send(message)
            logger.info(f"Telecommand '{telecommand.get_name()}' sent successfully")

        except Exception as e:
            logger.error(f"Failed to send telecommand '{telecommand.get_name()}': {e}", exc_info=True)
            raise

    def submit(self, telecommand: TelecommandInterface):
        """It consists of a message with an acknowledgement response. It return True if ACK is okay and False otherwise."""
        logger.debug(f"Submitting telecommand: {telecommand.get_name()} (SUBMIT mode)")
        try:
            message = self.message_manager.make_message(telecommand, InteractionType.SUBMIT)
            logger.debug(f"Message created: {len(message)} bytes")

            self.communication.send(message)
            logger.debug("Message sent, waiting for ACK...")

            response = self.communication.receive()

            if response is not None:
                logger.debug(f"Response received: {len(response)} bytes")
                ack = self.message_manager.unpack(response)

                if ack:
                    logger.info(f"ACK received for telecommand '{telecommand.get_name()}'")
                    return True
                else:
                    logger.warning(f"NACK received for telecommand '{telecommand.get_name()}'")
                    return False
            else:
                logger.error("No response received.")
                return False

        except Exception as e:
            logger.error(f"Failed to submit telecommand '{telecommand.get_name()}': {e}", exc_info=True)
            return False

    def request(self, telecommand: TelecommandInterface):
        """In of a message with a response message. It returns the message if everything is okay, False otherwise."""
        logger.debug(f"Requesting telecommand: {telecommand.get_name()} (REQUEST mode)")

        try:
            message = self.message_manager.make_message(telecommand, InteractionType.REQUEST)
            logger.debug(f"Message created: {len(message)} bytes")

            self.communication.send(message)
            logger.debug("Message sent, waiting for response...")

            response = self.communication.receive()

            if response is not None:
                logger.debug(f"Response received: {len(response)} bytes")
                unpack_response = self.message_manager.unpack(response)

                if unpack_response is None:
                    logger.error("Failed to unpack response")
                    return False

                if isinstance(unpack_response, bytes):
                    logger.debug("Parsing output arguments...")
                    parsed_response = telecommand.parse_output_arguments(unpack_response)
                    logger.info(f"Command '{telecommand.get_name()}' response: {parsed_response}")
                    return parsed_response
                else:
                    logger.error(f"Invalid response type: {type(unpack_response)}")
                    return False
            else:
                logger.error("No response received.")
                return False

        except Exception as e:
            logger.error(f"Failed to request telecommand '{telecommand.get_name()}': {e}", exc_info=True)
            return False

    def send_message(self, telecommand: TelecommandInterface, interaction_type: InteractionType):
        """Receive a telecommand and interaction type and then send the corresponding interaction."""
        logger.debug(f"Send message: {telecommand.get_name()} with {interaction_type.name}")
        if interaction_type == InteractionType.SEND:
            return self.send(telecommand)
        elif interaction_type == InteractionType.SUBMIT:
            return self.submit(telecommand)
        elif interaction_type == InteractionType.REQUEST:
            return self.request(telecommand)
        else:
            logger.error(f"Unknown interaction type: {interaction_type}")
            return False
