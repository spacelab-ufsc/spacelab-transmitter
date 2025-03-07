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
import hashlib
import hmac

from spacelab_transmitter.tc_ping import Ping
from spacelab_transmitter.tc_broadcast import Broadcast
from spacelab_transmitter.tc_enter_hibernation import Enter_hibernation
from spacelab_transmitter.tc_leave_hibernation import LeaveHibernation
from spacelab_transmitter.tc_activate_module import ActivateModule
from spacelab_transmitter.tc_deactivate_module import DeactivateModule
from spacelab_transmitter.tc_set_parameter import SetParameter
from spacelab_transmitter.tc_erase_memory import EraseMemory
from spacelab_transmitter.tc_force_reset import ForceReset
from spacelab_transmitter.tc_get_payload_data import GetPayloadData
from spacelab_transmitter.tc_data_request import DataRequest
from spacelab_transmitter.tc_get_parameter import GetParameter
from spacelab_transmitter.tc_get_parameter import GetParameter
from spacelab_transmitter.tc_activate_payload import ActivatePayload
from spacelab_transmitter.tc_deactivate_payload import DeactivatePayload
from spacelab_transmitter.tc_update_tle import UpdateTLE

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
    x = Broadcast()

    for i in range(100):

        #Random callsign 
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1,7)))

        # Convert callsign from string to list of bytes
        src_adr_as_list = [ord(j) for j in src_adr]

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        src_adr_spaces = (7 - len(src_adr)) * [ord(" ")]

        #dst_adr
        dst_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1,7)))

        # Compute the number spaces for padding (the callsign field is fixed as 7 bytes long)
        dst_adr_spaces = (7 - len(dst_adr)) * [ord(" ")]

        #convert destination callsign from string to list of bytes
        dst_adr_as_list = [ord(j) for j in dst_adr]

        #msg 
        msg = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1,38)))

        #convert destination callsign from string to list of bytes
        msg_as_list = [ord(j) for j in msg]

        #generate
        res = x.generate(src_adr, dst_adr, msg)

        assert res == [0x42] + src_adr_spaces + src_adr_as_list + dst_adr_spaces + dst_adr_as_list + msg_as_list

def test_tc_enter_hibernation():
    x = Enter_hibernation()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #hbn_hours
        hbn_hours = random.randint(0, 2**16)
        hbn_hours_as_list = [(hbn_hours >> 8) & 0xFF, (hbn_hours >> 0) & 0xFF]

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        #hash
        exp_pl = [0x43] + spaces + src_adr_as_list + hbn_hours_as_list
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)


        #generate 
        res = x.generate(src_adr, hbn_hours, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_leave_hibernation():
    x = LeaveHibernation()
        
    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))
        exp_pl = [0x44] + spaces + src_adr_as_list

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, key)
        assert res == exp_pl + list(hashed.digest())


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

def test_tc_erase_memory():
    x = EraseMemory()

    for i in range(100):
        # Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Random Memory ID
        mem_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))
        exp_pl = [0x49] + spaces + src_adr_as_list + [mem_id]

        # Hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        # Generate
        res = x.generate(src_adr, mem_id, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_force_reset():
    x = ForceReset()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))
        exp_pl = [0x4A] + spaces + src_adr_as_list

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_get_payload_data():
    x = GetPayloadData()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #Random pl_id
        pl_id = random.randint(0, 255)

        #Random pl_args 
        #pl_args = random.sample(range(0, 255), 12)
        pl_args = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1,12)))
        pl_args_as_list = [ord(j) for j in pl_args]

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))
        
        exp_pl = [0x4B] + spaces + src_adr_as_list + [pl_id] + pl_args_as_list

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, pl_id, pl_args_as_list, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_data_request():
    x = DataRequest()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #Random data_id
        data_id = random.randint(0, 255)

        #Random start_ts and end_ts
        start_ts = random.randint(0, 2**32 - 1)
        end_ts = random.randint(0, 2**32 - 1)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        start_ts_list = [(start_ts >> 24) & 0xFF,
        (start_ts >> 16) & 0xFF,
        (start_ts >> 8) & 0xFF, 
        start_ts & 0xFF] 

        end_ts_list = [(end_ts >> 24) & 0xFF,
        (end_ts >> 16) & 0xFF,
        (end_ts >> 8) & 0xFF, 
        end_ts & 0xFF] 

        exp_pl = [0x41] + spaces + src_adr_as_list + [data_id] + start_ts_list + end_ts_list

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, data_id, start_ts ,end_ts, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_get_parameter():
    x = GetParameter()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #Random ids
        subsys_id = random.randint(0, 255)
        param_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        exp_pl = [0x4D] + spaces + src_adr_as_list + [subsys_id] + [param_id] 

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, subsys_id, param_id, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_activate_payload():
    x = ActivatePayload()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #Random id
        pl_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        exp_pl = [0x47] + spaces + src_adr_as_list + [pl_id] 

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, pl_id, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_dactivate_payload():
    x = DeactivatePayload()

    for i in range(100):
        #Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        #Random id
        pl_id = random.randint(0, 255)

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))

        exp_pl = [0x48] + spaces + src_adr_as_list + [pl_id] 

        #hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        #generate 
        res = x.generate(src_adr, pl_id, key)
        assert res == exp_pl + list(hashed.digest())

def test_tc_update_tle():
    x = UpdateTLE()

    for i in range(100):
        # Callsign and conversion
        src_adr = ''.join(random.choice(string.ascii_uppercase) for j in range(random.randint(1, 7)))
        src_adr_as_list = [ord(j) for j in src_adr]
        spaces = (7 - len(src_adr)) * [ord(" ")]

        # Random TLE Line Number
        tle_line_num = random.randint(0, 2)

        # TLE Line
        tle_line = ''.join(random.choice(string.ascii_uppercase) for j in range(69))
        tle_line_list = [ord(j) for j in tle_line]

        # Random key
        key = ''.join(random.choice(string.ascii_uppercase) for j in range(16))
        exp_pl = [0x4F] + spaces + src_adr_as_list + [tle_line_num] + tle_line_list

        # Hash
        hashed = hmac.new(key.encode('utf-8'), bytes(exp_pl), hashlib.sha1)

        # Generate
        res = x.generate(src_adr, tle_line_num, tle_line, key)
        assert res == exp_pl + list(hashed.digest())
