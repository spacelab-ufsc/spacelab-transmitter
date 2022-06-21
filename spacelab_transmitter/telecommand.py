#
#  telecommand.py
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


class Telecommand:
    """
    Generic telecommand class.
    """
    def __init__(self, id, name):
        """
        Constructor.

        :param id: ID of the telecommand.
        :param name: name of the telecommand.
        """
        self.set_id(id)
        self.set_name(name)

    def generate(self):
        """
        Generic function to generate the payload of telecommand.

        :return: An empty list.
        """
        return list()

    def set_id(self, id):
        """
        Sets a new ID for the telecommand.

        :param id: The new ID of the telecommand.

        :return: None.
        """
        self._id = id

    def get_id(self):
        """
        Gets the ID of the telecommand.

        :return: The ID of the telecommand.
        """
        return self._id

    def set_name(self, name):
        """
        Sets a new name for the telecommand.

        :param name: The new name of the telecommand.

        :return: None;
        """
        self._name = name

    def get_name(self):
        """
        Gets the name of the telecommand.

        :return: The name of the telecommand as an string.
        """
        return self._name

    def _prepare_callsign(self, callsign):
        """
        Prepares a callsign for a transmission.

        :param callsign: Is the callsign to convert to the transmission format.

        :return: An ready to transmit callsign.
        """
        n = 7 - len(callsign)
        if n != 7:
            callsign = n*" " + callsign

        return [ord(i) for i in callsign]
