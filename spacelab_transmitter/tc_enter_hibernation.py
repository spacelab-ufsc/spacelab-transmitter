#
#  tc_enter_hibernation.py
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

class Enter_hibernation(Telecommand):
    """
    Enter Hibernation
    """
    def __init__(self):
        """
        Constructor.hbn hours e hmac has
        """
        super().__init__(0x43, "enter_hibernation")
    
    def generate(self, src_adr, hbn_hours, key):

        """This telecommand is composed by four fields:

            Packet ID (1 byte = 0x43)
            Source callsign (7 bytes ASCII)
            Hibernation duration in hours (2 bytes)
            HMAC hash (20 bytes)

        :param: src_adr: is the callsign of the source (ASCII string).
        :param: hbn_hours: is how many hibernation hours it will be set.
        :param: key: is the telecommand key (ASCII string).

        :return: The generated payload as list of integers.

        """

        pl = [self.get_id()] + self._prepare_callsign(src_adr)

        pl.append((hbn_hours >> 8) & 0xFF)
        pl.append((hbn_hours >> 0) & 0xFF)

        hashed = hmac.new(key.encode('utf-8'), bytes(pl), hashlib.sha1)

        return pl + list(hashed.digest())