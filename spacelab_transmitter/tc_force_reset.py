#
#  tc_force_reset.py
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

class ForceReset(Telecommand):
    """
    Force Reset
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(0x4A, "force_reset")
    
    def generate(self, src_adr, key):

        """This telecommand is composed by three fields:
            Packet ID (1 byte = 0x4A)
            Source callsign (7 bytes ASCII)
            HMA C hash (20 bytes)

        :param: src_adr: is the callsign of the source (ASCII string).
        :param: key: is the telecommand key (ASCII string).
        :return: The generated payload as list of integers.

        """
        
        pl = [self.get_id()] + self._prepare_callsign(src_adr)

        hashed = hmac.new(key.encode('utf-8'), bytes(pl), hashlib.sha1)

        return pl + list(hashed.digest())