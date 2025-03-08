#
#  slp.py
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

class SLP:
    """
    SpaceLab network layer protocol.
    """
    def __init__(self):
        """
        Class constructor.
        """
        pass

    def encode(self, id, src_adr, pl):
        """
        Encodes an SLP packet.

        :param id: Is the ID code of the packet.
        :type: int

        :param src_adr: Is the source address of the packet.
        :type: str

        :param pl: Is the payload of the packet.
        :type: list[int]

        :return: The SLP encoded packet.
        :rtype: list[int]
        """
        pkt = list()

        pkt.append(id)
        if len(src_adr) <= 7:
            pkt += self._prepare_callsign(src_adr)
        else:
            raise ValueError("The source address must be lesser than 7-bytes long!")
        pkt += pl

        return pkt

    def decode(self, pkt):
        """
        Decodes an SLP packet.

        :param pkt: Is an SLP packet to decode.
        :type: list[int]

        :return: The decoded SLP packet as a dict.
        :rtype: dict
        """
        if len(pkt) < 8:
            raise IndexError("An SLP packet must be at least 8-bytes long!")

        id = pkt[0]
        src_adr = ''.join(chr(i) for i in pkt[1:8]).strip()
        pl = pkt[8:]

        return {
            "id": id,
            "src_adr": src_adr,
            "payload": pl
        }

    def _prepare_callsign(self, callsign):
        """
        Prepares a callsign for a transmission.

        :param callsign: Is the callsign to convert to the transmission format.

        :return: A ready to transmit callsign.
        """
        n = 7 - len(callsign)
        if n != 7:
            callsign = n*" " + callsign

        return [ord(i) for i in callsign]
