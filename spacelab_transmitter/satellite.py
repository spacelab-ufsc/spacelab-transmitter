#
#  satellite.py
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

class Satellite:
    """
    Satellite object.
    """
    def __init__(self):
        """
        Class constructor.
        """
        self._name = ""
        self._links = list()

    def set_name(self, name):
        """
        Sets the name of the satellite.

        :param name: Is the name of the satellite.
        :type: string

        :return None.
        """
        self._name = name

    def get_name(self):
        """
        Gets the name of the satellite.

        :return: The name of the satellite.
        :rtype: string
        """
        return self._name

    def set_links(self, links):
        """
        Sets the list of communication links.

        :param links: Is a list with communication links
        :type: list

        :return: None
        """
        self._links = links

    def get_links(self):
        """
        Gets the communication links.

        :return: A list with all available communication links.
        :rtype: list
        """
        return self._links
