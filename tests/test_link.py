#
#  test_slp.py
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

from link import Link

@pytest.fixture
def link():
    """Fixture to create a Link instance for testing."""
    return Link()

def test_set_name(link):
    """Test the set_name method."""
    link.set_name("Link1")
    assert link.get_name() == "Link1"

def test_get_name(link):
    """Test the get_name method."""
    link.set_name("Link2")
    assert link.get_name() == "Link2"

def test_set_direction_valid(link):
    """Test the set_direction method with valid values."""
    link.set_direction("up")
    assert link.get_direction() == "up"
    link.set_direction("down")
    assert link.get_direction() == "down"

def test_set_direction_invalid(link):
    """Test the set_direction method with invalid values."""
    with pytest.raises(ValueError):
        link.set_direction("invalid")

def test_set_frequency(link):
    """Test the set_frequency method."""
    link.set_frequency(145800000)
    assert link.get_frequency() == 145800000

def test_get_frequency(link):
    """Test the get_frequency method."""
    link.set_frequency(435000000)
    assert link.get_frequency() == 435000000

def test_set_modulation(link):
    """Test the set_modulation method."""
    link.set_modulation("FM")
    assert link.get_modulation() == "FM"

def test_get_modulation(link):
    """Test the get_modulation method."""
    link.set_modulation("PSK")
    assert link.get_modulation() == "PSK"

def test_set_baudrate(link):
    """Test the set_baudrate method."""
    link.set_baudrate(9600)
    assert link.get_baudrate() == 9600

def test_get_baudrate(link):
    """Test the get_baudrate method."""
    link.set_baudrate(1200)
    assert link.get_baudrate() == 1200

def test_set_preamble(link):
    """Test the set_preamble method."""
    preamble = [0xAA, 0x55, 0xAA, 0x55]
    link.set_preamble(preamble)
    assert link.get_preamble() == preamble

def test_get_preamble(link):
    """Test the get_preamble method."""
    preamble = [0x55, 0xAA, 0x55, 0xAA]
    link.set_preamble(preamble)
    assert link.get_preamble() == preamble

def test_set_sync_word(link):
    """Test the set_sync_word method."""
    sync_word = [0xDE, 0xAD, 0xBE, 0xEF]
    link.set_sync_word(sync_word)
    assert link.get_sync_word() == sync_word

def test_get_sync_word(link):
    """Test the get_sync_word method."""
    sync_word = [0xBE, 0xEF, 0xCA, 0xFE]
    link.set_sync_word(sync_word)
    assert link.get_sync_word() == sync_word

def test_set_link_protocol(link):
    """Test the set_link_protocol method."""
    link.set_link_protocol("AX.25")
    assert link.get_link_protocol() == "AX.25"

def test_get_link_protocol(link):
    """Test the get_link_protocol method."""
    link.set_link_protocol("KISS")
    assert link.get_link_protocol() == "KISS"

def test_set_network_protocol(link):
    """Test the set_network_protocol method."""
    link.set_network_protocol("IP")
    assert link.get_network_protocol() == "IP"

def test_get_network_protocol(link):
    """Test the get_network_protocol method."""
    link.set_network_protocol("TCP")
    assert link.get_network_protocol() == "TCP"

def test_set_packets(link):
    """Test the set_packets method."""
    packets = [{"type": "data", "size": 128}, {"type": "command", "size": 64}]
    link.set_packets(packets)
    assert link.get_packets() == packets

def test_get_packets(link):
    """Test the get_packets method."""
    packets = [{"type": "beacon", "size": 32}]
    link.set_packets(packets)
    assert link.get_packets() == packets

def test_initial_state(link):
    """Test the initial state of the Link instance."""
    assert link.get_name() == ""
    assert link.get_direction() == ""
    assert link.get_frequency() == 0
    assert link.get_modulation() == ""
    assert link.get_baudrate() == 0
    assert link.get_preamble() == []
    assert link.get_sync_word() == []
    assert link.get_link_protocol() == ""
    assert link.get_network_protocol() == ""
    assert link.get_packets() == []
