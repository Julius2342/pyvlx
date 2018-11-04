"""Module for Serial Line Internet Protocol (SLIP)."""

SLIP_END = 0xC0
SLIP_ESC = 0xDB
SLIP_ESC_END = 0xDC
SLIP_ESC_ESC = 0xDD


def is_slip(raw):
    """Check if raw is a SLIP packet."""
    if len(raw) < 2:
        return False
    return raw[0] == SLIP_END and SLIP_END in raw[1:]


def decode(raw):
    """Decode SLIP message."""
    return raw \
        .replace(bytes([SLIP_ESC, SLIP_ESC_END]), bytes([SLIP_END])) \
        .replace(bytes([SLIP_ESC, SLIP_ESC_ESC]), bytes([SLIP_ESC]))


def encode(raw):
    """Encode SLIP message."""
    return raw \
        .replace(bytes([SLIP_ESC]), bytes([SLIP_ESC, SLIP_ESC_ESC])) \
        .replace(bytes([SLIP_END]), bytes([SLIP_ESC, SLIP_ESC_END]))


def get_next_slip(raw):
    """
    Get the next slip packet from raw data.

    Returns the extracted packet plus the raw data with the remaining data stream.
    """
    if not is_slip(raw):
        return None, raw
    length = raw[1:].index(SLIP_END)
    slip_packet = decode(raw[1:length+1])
    new_raw = raw[length+2:]
    return slip_packet, new_raw


def slip_pack(raw):
    """Pack raw message to complete slip message."""
    return bytes([SLIP_END]) + encode(raw) + bytes([SLIP_END])
