import uuid
import time
import os

_supported_formats = ["v4", "v7"]

def v4() -> uuid.UUID:
    """Standard random UUID for general entities."""
    return uuid.uuid4()


def v7() -> uuid.UUID:
    """Time-sortable UUID for database keys, logs, and events."""
    # Uses built-in uuid7 if available (Python 3.14+), otherwise falls back
    if hasattr(uuid, 'uuid7'):
        return uuid.uuid7()
    
    # Fallback pure-python implementation
    timestamp_ms = int(time.time() * 1000)
    uuid_bytes = bytearray(16)
    uuid_bytes[0:6] = timestamp_ms.to_bytes(6, byteorder='big')
    uuid_bytes[6:16] = os.urandom(10)
    uuid_bytes[6] = (uuid_bytes[6] & 0x0F) | 0x70
    uuid_bytes[8] = (uuid_bytes[8] & 0x3F) | 0x80
    return uuid.UUID(bytes=bytes(uuid_bytes))
