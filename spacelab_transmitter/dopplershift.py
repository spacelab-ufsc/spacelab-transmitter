#
#  dopplershift.py
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

from datetime import datetime, UTC

import ephem

class DopplerShift:
    """
    Doppler shift computation.
    """
    def __init__(self, direction="down"):
        """
        Constructor.

        :return: None.
        """
        self._observer = ephem.Observer()
        self._direction = str()

        self.set_direction(direction)

    def set_direction(self, direction):
        """
        Sets the direction of the link ("up" or "down").

        :param direction: Is the direction of the link.
        :type: str

        :return: None
        """
        if direction == "down" or direction == "up":
            self._direction = direction
        else:
            raise ValueError("The direction to compute the Doppler shift must be \"up\" or \"down\"!")

    def set_tle(self, line1: str, line2: str, sat_name="Satellite"):
        """
        Sets the TLE of the satellite.

        :param line1: Is the first line of the TLE.
        :type: str

        :param line2: Is the second line of the TLE.
        :type: str

        :param sat_name: Is the name of the satellite.
        :type: str

        :return:
        """
        self._satellite = ephem.readtle(sat_name, line1, line2)

    def set_tle_from_file(self, tle_filename: str):
        """
        Loads the TLE from a text file.

        :param tle_filename: Is the file with TLE data.

        :return: None.
        """
        lines = list()
        with open(tle_filename) as f:
            lines = [line.rstrip() for line in f]

        if len(lines) == 2:
            self.set_tle(lines[0], lines[1])
        elif len(lines) == 3:
            self.set_tle(lines[1], lines[2], lines[0])
        else:
            raise RuntimeError("Error reading the TLE file!")

    def set_observer_position(self, lat: float, lon: float, alt: float):
        """
        Sets the position of the observer.

        :param lat: Is the latitude of the observer in degrees.
        :type: float

        :param lon: Is the longitude of the observer in degrees.
        :type: float

        :param alt: Is the altitude of the observer in meters.
        :type: float

        :return: None.
        """
        self._observer.lat = str(lat)
        self._observer.lon = str(lon)
        self._observer.elevation = alt

    def set_frequency(self, freq: float):
        """
        Sets the reference frequency.

        :param freq: Is the frequency, in Hertz, to compute the Doppler shift.
        :type: float

        :return: None.
        """
        self._freq_hz = freq

    def get_current_shift(self):
        """
        Computes the current Doppler shift for the given data.

        :return: The computed Doppler shift in Hertz.
        """
        cur_shift = self._freq_hz * (1-self._calculate_velocity()/ephem.c) - self._freq_hz

        if self._direction == "down":
            return int(cur_shift)
        elif self._direction == "up":
            return int(cur_shift)*(-1)

    def get_shifted_frequency(self):
        """
        Computes the shifted frequency.

        :return: The computed shifted frequency in Hertz.
        :rtype: float
        """
        return int(self._freq_hz + self.get_current_shift())

    def _calculate_velocity(self):
        """
        Computes the velocity of the satellite.

        :return: The current velocity of the satellite.
        :rtype: float
        """
        self._observer.date = datetime.now(UTC)

        self._satellite.compute(self._observer)

        return self._satellite.range_velocity
