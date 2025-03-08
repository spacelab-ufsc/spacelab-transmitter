#
#  test_satellite.py
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

import pytest

from satellite import Satellite

@pytest.fixture
def satellite():
    """Fixture to create a Satellite instance for testing."""
    return Satellite()

def test_set_name(satellite):
    """Test the set_name method."""
    satellite.set_name("Satellite1")
    assert satellite.get_name() == "Satellite1"

def test_get_name(satellite):
    """Test the get_name method."""
    satellite.set_name("Satellite2")
    assert satellite.get_name() == "Satellite2"

def test_set_links(satellite):
    """Test the set_links method."""
    links = ["Link1", "Link2", "Link3"]
    satellite.set_links(links)
    assert satellite.get_links() == links

def test_get_links(satellite):
    """Test the get_links method."""
    links = ["LinkA", "LinkB"]
    satellite.set_links(links)
    assert satellite.get_links() == links

def test_initial_state(satellite):
    """Test the initial state of the Satellite instance."""
    assert satellite.get_name() == ""
    assert satellite.get_links() == []
