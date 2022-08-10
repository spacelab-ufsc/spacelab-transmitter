#
#  tc_set_parameter.py
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

class SetParameter(Telecommand):
    """
    Set parameter telecommand.
    """
    def __init__(self):
        """
        Constructor.
        """
        super().__init__(0x4C, "set_parameter")

    def generate(self, src_adr, s_id, param_id, param_val, key):
        """
        Generates the telecommand's payload.

        :param src_adr: is the callsign of the source (ASCII string).
        :param s_id: is the ID of the subsystem to set a parameter.
        :param param_id: is the ID of the parameter to set.
        :param param_val: is the new value of the given parameter (32-bit integer).
        :param key: is the telecommand key (ASCII string).

        :return The generated payload as list of integers (bytes).
        """
        if (s_id > 255) or (param_id > 255):
            return list()

        pl = [self.get_id()] + self._prepare_callsign(src_adr) + [s_id] + [param_id]

        # Split 32-bit integer into 4 bytes
        pl.append((param_val >> 24) & 0xFF)
        pl.append((param_val >> 16) & 0xFF)
        pl.append((param_val >> 8) & 0xFF)
        pl.append(param_val & 0xFF)

        hashed = hmac.new(key.encode('utf-8'), bytes(pl), hashlib.sha1)

        return pl + list(hashed.digest())
