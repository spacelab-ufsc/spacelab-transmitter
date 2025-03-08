#
#  test_log.py
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

import os
import random
import string
import csv

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from spacelabtransmitter import SpaceLabTransmitter

_DIR_CONFIG_LOGFILE_LINUX   = 'spacelab_transmitter'
_DEFAULT_LOGFILE_PATH       = os.path.join(os.path.expanduser('~'), _DIR_CONFIG_LOGFILE_LINUX)
_DEFAULT_LOGFILE            = 'logfile.csv'

def test_log():
    x = SpaceLabTransmitter()

    logs = list()
    logs.append("SpaceLab Transmitter initialized!")

    n = random.randint(2, 10)
    for i in range(n):
        # Write random log messages
        m = random.randint(1, 100)
        for j in range(m):
            msg = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=random.randint(1, 100)))
            logs.append(msg)
            x.write_log(msg)

        # Verify the log messages written to the logfile
        with open(_DEFAULT_LOGFILE_PATH + '/' + _DEFAULT_LOGFILE) as logfile:
            csv_reader = csv.reader(logfile, delimiter='\t')
            for row, msg in zip(csv_reader, logs):
                assert row[1] == msg
