from __future__ import annotations

import dataclasses
import struct
import enum
import logging

logger = logging.getLogger(__name__)

PROTOCOL_VERSION = 1


class InteractionType(enum.IntEnum):
    SEND = 1
    SUBMIT = 2
    REQUEST = 3
    INVOKE = 4
    PROGRESS = 5
    PUBSUB = 6


class Service(enum.IntEnum):
    TELEMETRY = 0
    TELECOMMAND = 1


@dataclasses.dataclass
class MessageHeader:
    timestamp: int
    interaction_type: InteractionType
    interaction_stage: int
    transaction_id: int
    service: Service
    operation: int
    area_version: int
    is_error_message: int
    body_length: int

    _STRUCT_FORMAT = "<Q H B Q H H H B H"  # little-endian layout

    @classmethod
    def pack(cls, header: MessageHeader) -> bytes:
        """Pack a MessageHeader dataclass into raw bytes."""
        logger.debug(
            f"Packing header: interaction={header.interaction_type.name}, "
            f"service={header.service.name}, operation={header.operation}, "
            f"transaction_id={header.transaction_id}, body_length={header.body_length}"
        )

        try:
            packed = struct.pack(cls._STRUCT_FORMAT, *dataclasses.astuple(header))
            logger.debug(f"Header packed successfully: {len(packed)} bytes")
            return packed
        except struct.error as e:
            logger.error(f"Failed to pack header: {e}", exc_info=True)
            raise

    @classmethod
    def unpack(cls, raw: bytes) -> MessageHeader:
        """Unpack raw bytes into a MessageHeader dataclass."""
        logger.debug(f"Unpacking header from {len(raw)} bytes")

        expected_size = cls.size()
        if len(raw) != expected_size:
            logger.error(
                f"Invalid header size: expected {expected_size} bytes, got {len(raw)} bytes"
            )
            raise ValueError(f"Expected {expected_size} bytes for header, got {len(raw)}")

        try:
            values = struct.unpack(cls._STRUCT_FORMAT, raw)
            header = cls(*values)
            logger.debug(
                f"Header unpacked: interaction={header.interaction_type}, "
                f"service={header.service}, operation={header.operation}, "
                f"transaction_id={header.transaction_id}, body_length={header.body_length}"
            )
            return header
        except struct.error as e:
            logger.error(f"Failed to unpack header: {e}", exc_info=True)
            raise
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid header values after unpacking: {e}", exc_info=True)
            raise

    @classmethod
    def size(cls) -> int:
        """Return the size in bytes of the packed header."""
        size = struct.calcsize(cls._STRUCT_FORMAT)
        logger.debug(f"Header size: {size} bytes")
        return size
