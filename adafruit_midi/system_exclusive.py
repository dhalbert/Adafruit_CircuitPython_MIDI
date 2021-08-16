# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.system_exclusive`
================================================================================

System Exclusive MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class SystemExclusive(MIDIMessage):
    """System Exclusive MIDI message.

    :param bool real_time: True if this is a real time SYSEX message, else False.
    :param int device_id: Device ID. If not supplied use 0x7F, which means all devices should respond.
    :param Sequence data: SYSEX data bytes.

    This message can only be parsed if it fits within the input buffer in :class:MIDI.
    """

    _STATUS = 0xF0
    _STATUSMASK = 0xFF
    LENGTH = -1
    ENDSTATUS = 0xF7

    def __init__(self, *, real_time=False, device_id=0x7F, data):
        self.real_time = real_time
        self.data = bytes(data)
        super().__init__()

    def __bytes__(self):
        return (
            bytes((self._STATUS,))
            + b"\x7F" if self.real_time else b"\x7E"
            + self.data
            + bytes((self.ENDSTATUS,))
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        # -1 on last arg is to avoid the ENDSTATUS which is passed
        return cls(msg_bytes[2] == 0x7F, msg_bytes[3], msg_bytes[4:-1])


SystemExclusive.register_message_type()
