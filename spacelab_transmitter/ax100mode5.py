#
#  ax100mode5.py
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

class AX100Mode5:
    """
    AX100-Mode5 Protocol.
    """
    def __init__(self):
        """
        Constructor.
        """
        pass

    def encode(self, data):
        """
        Encodes a given data in AX100-Mode5 format.

        :param data: data to be encoded using the AX100-Mode5 protocol.
        :type: list[int]

        :return: The encoded AX100-Mode5 packet.
        :rtype: list[int]
        """
        return data

    def decode(self):
        """
        :return: .
        """
        pass
