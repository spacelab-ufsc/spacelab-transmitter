#
#  tc_transmit_packet.py
#
#  Copyright The SpaceLab-Transmitter Contributors.
#
#  This file is part of SpaceLab-Transmitter.
#
#  SpaceLab-Transmitter is free software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  SpaceLab-Transmitter is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with SpaceLab-Transmitter; if not, see <http://www.gnu.org/licenses/>.
#
#

import hashlib
import hmac

from spacelab_transmitter.telecommand import Telecommand

class TransmitPacket(Telecommand):
    """
    Transmit packet
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__(0x4E, "transmit_packet")

    def generate(self, src_adr, data, key):
        """
        This telecommand is composed by three fields:

        - Packet ID (1 byte = 0x4E)
        - Source callsign (7 bytes ASCII)
        - Data (sequence of bytes, up to 45)
        - HMAC hash (20 bytes)

        :param src_adr: Is the source callsign (ASCII string).
        :type: int

        :param data: Is the data to transmit (list of integers).
        :type: list[int]

        :param key: Is the telecommand key (ASCII string).
        :type: str

        :return The generated payload as list of integers (bytes).
        """
        if len(data) > 45:
            data = data[:45]

        pl = [self.get_id()] + self._prepare_callsign(src_adr) + data

        hashed = hmac.new(key.encode('utf-8'), bytes(pl), hashlib.sha1)

        return pl + list(hashed.digest())
