#
#  test_doppler.py
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

import pytest
import ephem

from dopplershift import DopplerShift

# Sample TLE data for testing
SAMPLE_TLE = [
    "ISS (ZARYA)",
    "1 25544U 98067A   25075.85513494  .00023414  00000-0  41535-3 0  9993",
    "2 25544  51.6363  44.3412 0006353  29.6937 330.4411 15.50098504500847"
]

# Sample observer data for testing
OBSERVER_LAT = -27.600720
OBSERVER_LON = -48.517390
OBSERVER_ALT = 0

# Sample frequency for testing
SAMPLE_FREQ = 437.5e6  # 437.5 MHz

@pytest.fixture
def doppler_shift():
    ds = DopplerShift(direction="down")
    ds.set_tle(SAMPLE_TLE[1], SAMPLE_TLE[2], "ISS (ZARYA)")
    ds.set_observer_position(OBSERVER_LAT, OBSERVER_LON, OBSERVER_ALT)
    ds.set_frequency(SAMPLE_FREQ)
    return ds

def test_set_direction(doppler_shift):
    doppler_shift.set_direction("up")
    assert doppler_shift._direction == "up"

    with pytest.raises(ValueError):
        doppler_shift.set_direction("invalid")

def test_set_tle(doppler_shift):
    assert doppler_shift._satellite is not None
    assert doppler_shift._satellite.name == "ISS (ZARYA)"

def test_set_tle_from_file(tmp_path):
    tle_file = tmp_path / "test_tle.txt"
    tle_file.write_text(f"ISS (ZARYA)\n{SAMPLE_TLE[1]}\n{SAMPLE_TLE[2]}")

    ds = DopplerShift()
    ds.set_tle_from_file(tle_file)
    assert ds._satellite is not None
    assert ds._satellite.name == "ISS (ZARYA)"

def test_set_observer_position(doppler_shift):
    assert doppler_shift._observer.lat == -0.48172343992104927
    assert doppler_shift._observer.lon == -0.8467881999741717
    assert doppler_shift._observer.elevation == OBSERVER_ALT

def test_set_frequency(doppler_shift):
    assert doppler_shift._freq_hz == SAMPLE_FREQ

def test_get_current_shift(doppler_shift):
    shift = doppler_shift.get_current_shift()
    assert isinstance(shift, int)

def test_get_shifted_frequency(doppler_shift):
    shifted_freq = doppler_shift.get_shifted_frequency()
    assert isinstance(shifted_freq, int)
    assert shifted_freq == SAMPLE_FREQ + doppler_shift.get_current_shift()

def test_calculate_velocity(doppler_shift):
    velocity = doppler_shift._calculate_velocity()
    assert isinstance(velocity, float)
