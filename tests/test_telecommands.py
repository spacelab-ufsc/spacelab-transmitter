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


import sys
import random
import string
import hashlib
import hmac

sys.path.append(".")

from spacelab_transmitter.tc_ping import Ping
from spacelab_transmitter.tc_broadcast import Broadcast

from spacelab_transmitter.tc_activate_module import ActivateModule
from spacelab_transmitter.tc_deactivate_module import DeactivateModule
from spacelab_transmitter.tc_set_parameter import SetParameter

def test_tc_ping():
    x = Ping()

    for i in range(100):
        # Random callsign
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))

        # Convert callsign from string to list of bytes
        src_adr_as_list = [ord(j) for j in src_adr]

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Generate ping command
        res = x.generate(src_adr)

        assert res == [0x40] + spaces + src_adr_as_list

def test_tc_broadcast():
    pass

def test_tc_enter_hibernation():
    pass

def test_tc_activate_module():
    x = ActivateModule()

    for i in range(100):
        # Random callsign
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))

        # Random module ID
        mod_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        # Convert callsign from string to list of bytes
        src_adr_as_list = [ord(j) for j in src_adr]

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Generate activate module command
        res = x.generate(src_adr, mod_id, key)

        exp_pl = [0x45] + spaces + src_adr_as_list + [mod_id]

        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        exp_res = exp_pl + list(hashed.digest())

        assert res == exp_res

def test_tc_deactivate_module():
    x = DeactivateModule()

    for i in range(100):
        # Random callsign
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))

        # Random module ID
        mod_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        # Convert callsign from string to list of bytes
        src_adr_as_list = [ord(j) for j in src_adr]

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Generate deactivate module command
        res = x.generate(src_adr, mod_id, key)

        exp_pl = [0x46] + spaces + src_adr_as_list + [mod_id]

        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        exp_res = exp_pl + list(hashed.digest())

        assert res == exp_res

def test_tc_set_parameter():
    x = SetParameter()

    # Random callsign
    src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))

    # Random subsystem ID
    s_id = random.randint(0, 255)

    # Random parameter ID
    param_id = random.randint(0, 255)

    # Random parameter value
    param_val = random.randint(0, 2**32 - 1)

    # Random key
    key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

    res = x.generate(src_adr, s_id, param_id, param_val, key)

    # Convert callsign from string to list of bytes
    src_adr_as_list = [ord(j) for j in src_adr]

    # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
    spaces = (7 - len(src_adr)) * [ord(" ")]

    exp_pl = [0x4C] + spaces + src_adr_as_list + [s_id] + [param_id] + [(param_val >> 24) & 0xFF, (param_val >> 16) & 0xFF, (param_val >> 8) & 0xFF, param_val & 0xFF]

    hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

    exp_res = exp_pl + list(hashed.digest())

    assert res == exp_res
