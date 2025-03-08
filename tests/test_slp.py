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

from slp import SLP

@pytest.fixture
def slp():
    """Fixture to create an SLP instance for testing."""
    return SLP()

def test_encode(slp):
    """Test the encode method."""
    id = 1
    src_adr = "PP5UF"
    pl = [0x01, 0x02, 0x03]

    encoded_pkt = slp.encode(id, src_adr, pl)
    assert encoded_pkt == [1, 32, 32, 80, 80, 53, 85, 70, 1, 2, 3]

def test_decode(slp):
    """Test the decode method."""
    pkt = [1, 32, 32, 80, 80, 53, 85, 70, 1, 2, 3]

    decoded_pkt = slp.decode(pkt)
    assert decoded_pkt == {
        "id": 1,
        "src_adr": "PP5UF",
        "payload": [1, 2, 3]
    }

def test_encode_short_callsign(slp):
    """Test the encode method with a short callsign."""
    id = 2
    src_adr = "ABC"
    pl = [0x04, 0x05]

    encoded_pkt = slp.encode(id, src_adr, pl)
    assert encoded_pkt == [2, 32, 32, 32, 32, 65, 66, 67, 4, 5]

def test_decode_short_callsign(slp):
    """Test the decode method with a short callsign."""
    pkt = [2, 32, 32, 32, 32, 65, 66, 67, 4, 5]

    decoded_pkt = slp.decode(pkt)
    assert decoded_pkt == {
        "id": 2,
        "src_adr": "ABC",
        "payload": [4, 5]
    }

def test_encode_empty_payload(slp):
    """Test the encode method with an empty payload."""
    id = 3
    src_adr = "PP5UF"
    pl = []

    encoded_pkt = slp.encode(id, src_adr, pl)
    assert encoded_pkt == [3, 32, 32, 80, 80, 53, 85, 70]

def test_decode_empty_payload(slp):
    """Test the decode method with an empty payload."""
    pkt = [3, 32, 32, 80, 80, 53, 85, 70]

    decoded_pkt = slp.decode(pkt)
    assert decoded_pkt == {
        "id": 3,
        "src_adr": "PP5UF",
        "payload": []
    }

def test_encode_invalid_callsign(slp):
    """Test the encode method with an invalid callsign."""
    id = 4
    src_adr = "CALLSIGN_TOO_LONG"
    pl = [0x06]

    with pytest.raises(ValueError):
        slp.encode(id, src_adr, pl)

def test_decode_invalid_packet(slp):
    """Test the decode method with an invalid packet."""
    pkt = [4]  # Packet too short

    with pytest.raises(IndexError):
        slp.decode(pkt)
