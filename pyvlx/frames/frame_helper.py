"""Helper module for SLIP Frames."""
from pyvlx.const import Command
from pyvlx.exception import PyVLXException


def calc_crc(raw):
    """Calculate cyclic redundancy check (CRC)."""
    crc = 0
    for sym in raw:
        crc = crc ^ int(sym)
    return crc


def extract_from_frame(data):
    """Extract payload and command from frame."""
    if len(data) <= 4:
        raise PyVLXException("could_not_extract_from_frame_too_short", data=data)
    length = data[0] * 256 + data[1] - 1
    if len(data) != length + 3:
        raise PyVLXException("could_not_extract_from_frame_invalid_length", data=data, current_length=len(data), expected_length=length + 3)
    if calc_crc(data[:-1]) != data[-1]:
        raise PyVLXException("could_not_extract_from_frame_invalid_crc", data=data, expected_crc=calc_crc(data[:-1]), current_crc=data[-1])
    payload = data[4:-1]
    try:
        command = Command(data[2] * 256 + data[3])
    except ValueError:
        raise PyVLXException("could_not_extract_from_frame_command", data=data)
    return command, payload
