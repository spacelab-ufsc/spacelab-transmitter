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


from datetime import datetime

import ephem

class DopplerShift:
    """
    Doppler shift computation.
    """
    def __init__(self):
        """
        Constructor.

        :return: None.
        """
        self._observer = ephem.Observer()

    def set_tle_from_file(self, tle_filename : str):
        """
        Sets the TLE file.

        :param tle_filename: is the file with TLE data.

        :return: None.
        """
        tle_file = open(tle_filename, 'r')

        tle_lines = tle_file.readlines()

        self._satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])

    def set_observer_local(self, lat : float, lon : float, altitude : float):
        """
        Sets the position of the observer.

        :param lat: is the latitude of the observer.
        :param lon: is the longitude of the oberser.
        :param atitude: is the altitude of the observer.

        :return: None.
        """
        self._observer.lat = str(lat)
        self._observer.lon = str(lon)
        self._observer.elevation = altitude

    def set_freq(self, freq : float):
        """
        Sets the reference frequency.

        :param freq: is the frequency, in Hertz, to compute the Doppler shift.

        :return: None.
        """
        self._freq_hz = freq

    def get_current_shift(self):
        """
        Computes the current Doppler shift for the given data.

        :return: The computed Doppler shift in Hertz.
        """
        return self._freq_hz * (1-self._calculate_velocity()/ephem.c) - self._freq_hz

    def get_shifted_freq(self):
        """
        Computes the shifted frequency.

        :return: The computed shifted frequency in Hertz.
        """
        return self._freq_hz + self.get_current_shift()

    def _calculate_velocity(self):
        """
        Computes the velocity of the satellite.

        :return: The current velocity of the satellite.
        """
        self._observer.date = datetime.timestamp(datetime.now())

        self._satellite.compute(self._observer)

        return self._satellite.range_velocity
