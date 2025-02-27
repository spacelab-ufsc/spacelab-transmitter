#
#  tc_broadcast.py
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

from spacelab_transmitter.telecommand import Telecommand

class Broadcast(Telecommand):
    """
    Broadcast Message
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__(0x42, "broadcast")

    def generate(self, src_adr, dst_adr, msg):
        """
        This telecommand is composed by four fields:

        - Packet ID (1 byte = 0x42)
        - Source callsign (7 bytes ASCII)
        - Destination callsign (7 bytes ASCII)
        - Message (string, up to 38 characters)

        The inputs of the "generate" method will be the source callsign (ASCII string), the destination callsign
        (ASCII string) and the message to broadcast (ASCII string).
        """
        return [self.get_id()] + self._prepare_callsign(src_adr) + self._prepare_callsign(dst_adr) + [ord(i) for i in msg]
