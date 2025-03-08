#
#  link.py
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

class Link:
    """
    Communication link object.
    """
    def __init__(self):
        """
        Class constructor.
        """
        self._name              = ""
        self._direction         = ""
        self._frequency         = 0
        self._modulation        = ""
        self._baudrate          = 0
        self._preamble          = list()
        self._sync_word         = list()
        self._protocol_link     = ""
        self._protocol_network  = ""
        self._packets           = list()

    def set_name(self, name):
        """
        Sets the name of the communication link.

        :param name:
        :type: str

        :return: None
        """
        self._name = name

    def get_name(self):
        """
        Gets the link name.

        :return: The name of the link.
        :rtype: str
        """
        return self._name

    def set_direction(self, dir):
        """
        Sets the direction of the communication link ("up" or "down").

        :param dir: Is the direction of the communication link.
        :type: str

        :return: None
        """
        dir = dir.lower()
        if dir == "up" or dir == "down":
            self._direction = dir
        else:
            raise ValueError('The direction of the communication link must be \"up\" or \"down\"!')

    def get_direction(self):
        """
        Gets the direction of the communication link.

        :return: The direction of the communication link.
        :rtype: str
        """
        return self._direction

    def set_frequency(self, freq):
        """
        Sets the frequency of the communication link.

        :param freq: Is the frequency in Hertz.
        :type: int

        :return: None
        """
        self._frequency = freq

    def get_frequency(self):
        """
        Gets the frequency of the communication link.

        :return: The frequency of the communication link in Hertz.
        :rtype: int
        """
        return self._frequency

    def set_modulation(self, mod):
        """
        Sets the modulation of the communication link.

        :param mod: Is the name of the modulation of the communication link.
        :type: str

        :return: None.
        """
        self._modulation = mod

    def get_modulation(self):
        """
        Gets the modulation of the communication link.

        :return: The name of the modulation.
        :rtype: str
        """
        return self._modulation

    def set_baudrate(self, baud):
        """
        Sets the baudrate of the communication link.

        :param baud: Is the new baudrate in bps.
        :type: int

        :return: None
        """
        self._baudrate = baud

    def get_baudrate(self):
        """
        Gets the baurdate of the communication link.

        :return: The baudrate of the link in bps.
        :rtype: int
        """
        return self._baudrate

    def set_preamble(self, preamb):
        """
        Sets the preamble of the communication link.

        :param preamb: Is the list with the preamble sequence as integers.
        :type: list

        :return: None
        """
        self._preamble = preamb

    def get_preamble(self):
        """
        Gets the preamble sequence of the communication link.

        :return: The preamble sequence as a list of integers
        :rtype: list
        """
        return self._preamble

    def set_sync_word(self, sw):
        """
        Sets the sync word of the communication link.

        :param sw: Is the sync word as a list of integers.
        :type: list

        :return: None
        """
        self._sync_word = sw.copy()

    def get_sync_word(self):
        """
        Gets the sync word of the communication link.

        :return: The sync word as a list of integers.
        :rtype: list
        """
        return self._sync_word

    def set_link_protocol(self, prot):
        """
        Sets the protocol of the data link layer of the communication link.

        :param prot: Is the name of the data link layer protocol.
        :type: str

        :return: None
        """
        self._protocol_link = prot

    def get_link_protocol(self):
        """
        Gets the protocol of the data link layer of the communication link.

        :return: The name of the data link layer protocol.
        :rtype: str
        """
        return self._protocol_link

    def set_network_protocol(self, prot):
        """
        Sets the protocol of the network layer of the communication link.

        :param prot: Is the name of the network layer protocol.
        :type: str

        :return: None
        """
        self._protocol_network = prot

    def get_network_protocol(self):
        """
        Gets the protocol of the network layer of the communication link.

        :return: The name of the network layer protocol.
        :rtype: str
        """
        return self._protocol_network

    def set_packets(self, pkt):
        """
        Sets the list of available packets in the communication link.

        :param pkt: Is the list of packets.
        :type: list

        :return: None
        """
        self._packets = pkt.copy()

    def get_packets(self):
        """
        Gets the list of packets available in the communication link.

        :return: The list of packets.
        :rtype: list
        """
        return self._packets
