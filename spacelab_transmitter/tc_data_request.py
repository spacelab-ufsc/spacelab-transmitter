#
#  tc_data_request.py
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

class DataRequest(Telecommand):
    """
    Data Request
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(0x41, "data_request")
    
    def generate(self, src_adr, data_id, start_ts, end_ts, key):

        """This telecommand is composed by four fields:

            Packet ID (1 byte = 0x41)
            Source callsign (7 bytes ASCII)
            Data type ID
            Start timestamp
            End timestamp
            HMAC hash (20 bytes)

        :param: src_adr: is the callsign of the source (ASCII string).
        :param: data_id: is the data type ID, 1 byte.
        :param: start_ts: start timestamp [ms].
        :param: end_ts: end timestamp [ms].
        :param: key: is the telecommand key (ASCII string).
        :return: The generated payload as list of integers.

        """

        pl = [self.get_id()] + self._prepare_callsign(src_adr) + [data_id]

        pl.append((start_ts >> 24) & 0xFF)
        pl.append((start_ts >> 16) & 0xFF)
        pl.append((start_ts >> 8) & 0xFF)
        pl.append((start_ts >> 0) & 0xFF)

        pl.append((end_ts >> 24) & 0xFF)
        pl.append((end_ts >> 16) & 0xFF)
        pl.append((end_ts >> 8) & 0xFF)
        pl.append((end_ts >> 0) & 0xFF)

        hashed = hmac.new(key.encode('utf-8'), bytes(pl), hashlib.sha1)

        return pl + list(hashed.digest())