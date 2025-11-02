from __future__ import annotations

import dataclasses
import struct
import enum


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
        return struct.pack(cls._STRUCT_FORMAT, *dataclasses.astuple(header))

    @classmethod
    def unpack(cls, raw: bytes) -> MessageHeader:
        """Unpack raw bytes into a MessageHeader dataclass."""
        values = struct.unpack(cls._STRUCT_FORMAT, raw)
        return cls(*values)

    @classmethod
    def size(cls) -> int:
        """Return the size in bytes of the packed header."""
        return struct.calcsize(cls._STRUCT_FORMAT)
