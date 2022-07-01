#
#  test_telecommands.py
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


import random
import string

from spacelab_transmitter.tc_ping import Ping

def test_tc_ping():
    x = Ping()

    for i in range(100):
        # Random callsign
        src_adr = ''.join(random.choice(string.ascii_uppercase) for i in range(random.randint(1, 7)))

        # Convert callsign from string to list of bytes
        src_adr_as_list = [ord(i) for i in src_adr]

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Generate ping command
        res = x.generate(src_adr)

        assert res == [0x40] + spaces + src_adr_as_list

def test_tc_broadcast():
    pass

def test_tc_enter_hibernation():
    pass
