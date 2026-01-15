#
#  beacon_sim.py
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
import time

sys.path.append("../")

from pyngham import PyNGHam
from pymodulation import GMSK

from spacelab_transmitter.pluto import Pluto

# Signal Config.
bitrate = 1200
freq    = 435000000
pwr     = -10

# Variables
pkt_id                  = 0
sat_callsign            = " PY0EFS"
eps_mcu_ts              = int(time.time())
eps_mcu_temp            = random.randrange(-40, 80,     1)
eps_mcu_current         = random.randrange(0,   100,    1)
eps_mcu_reset_counter   = random.randrange(0,   2**16,  1)
eps_sp_volt_mypx        = random.randrange(0,   5000,   1)
eps_sp_volt_mxpz        = random.randrange(0,   5000,   1)
eps_sp_volt_mzpy        = random.randrange(0,   5000,   1)
eps_sp_curr_mx          = random.randrange(0,   500,    1)
eps_sp_curr_px          = random.randrange(0,   500,    1)
eps_sp_curr_my          = random.randrange(0,   500,    1)
eps_sp_curr_py          = random.randrange(0,   500,    1)
eps_sp_curr_mz          = random.randrange(0,   500,    1)
eps_sp_curr_pz          = random.randrange(0,   500,    1)
eps_mppt_1_dc           = random.randrange(0,   100,    1)
eps_mppt_2_dc           = random.randrange(0,   100,    1)
eps_mppt_3_dc           = random.randrange(0,   100,    1)
eps_mppt_output_volt    = random.randrange(0,   5000,   1)
eps_main_bus_volt       = random.randrange(0,   8400,   1)
eps_rtd_0_temp          = random.randrange(-40, 80,     1)
eps_rtd_1_temp          = random.randrange(-40, 80,     1)
eps_rtd_2_temp          = random.randrange(-40, 80,     1)
eps_rtd_3_temp          = random.randrange(-40, 80,     1)
eps_rtd_4_temp          = random.randrange(-40, 80,     1)
eps_rtd_5_temp          = random.randrange(-40, 80,     1)
eps_rtd_6_temp          = random.randrange(-40, 80,     1)
eps_bat_volt            = random.randrange(0,   8400,   1)
eps_bat_curr            = random.randrange(0,   1000,   1)
eps_bat_charge          = random.randrange(0,   5000,   1)
eps_bat_heater_1_dc     = random.randrange(0,   100,    1)
eps_bat_heater_2_dc     = random.randrange(0,   100,    1)

print("===============================================")
print("Packet Data:")
print("===============================================")
print("ID:",                            pkt_id)
print("Source Callsign:",               sat_callsign)
print("MCU Timesatmp:",                 eps_mcu_ts,             "sec")
print("MCU Temperature:",               eps_mcu_temp,           "°C")
print("MCU Current:",                   eps_mcu_current,        "mA")
print("MCU Reset Counter:",             eps_mcu_reset_counter)
print("Solar Panel -Y+X Voltage:",      eps_sp_volt_mypx,       "mV")
print("Solar Panel -X+Z Voltage:",      eps_sp_volt_mxpz,       "mV")
print("Solar Panel -Z+Y Voltage:",      eps_sp_volt_mzpy,       "mV")
print("Solar Panel -X Current:",        eps_sp_curr_mx,         "mA")
print("Solar Panel +X Current:",        eps_sp_curr_px,         "mA")
print("Solar Panel -Y Current:",        eps_sp_curr_my,         "mA")
print("Solar Panel +Y Current:",        eps_sp_curr_py,         "mA")
print("Solar Panel -Z Current:",        eps_sp_curr_mz,         "mA")
print("Solar Panel +Z Current:",        eps_sp_curr_pz,         "mA")
print("MPPT 1 Duty Cycle:",             eps_mppt_1_dc,          "%")
print("MPPT 2 Duty Cycle:",             eps_mppt_2_dc,          "%")
print("MPPT 3 Duty Cycle:",             eps_mppt_3_dc,          "%")
print("MPPT Output Voltage:",           eps_mppt_output_volt,   "mV")
print("Main Bus Voltage:",              eps_main_bus_volt,      "mV")
print("RTD 0 Temperature:",             eps_rtd_0_temp,         "°C")
print("RTD 1 Temperature:",             eps_rtd_1_temp,         "°C")
print("RTD 2 Temperature:",             eps_rtd_2_temp,         "°C")
print("RTD 3 Temperature:",             eps_rtd_3_temp,         "°C")
print("RTD 4 Temperature:",             eps_rtd_4_temp,         "°C")
print("RTD 5 Temperature:",             eps_rtd_5_temp,         "°C")
print("RTD 6 Temperature:",             eps_rtd_6_temp,         "°C")
print("Battery Voltage:",               eps_bat_volt,           "mV")
print("Battery Current:",               eps_bat_curr,           "mA")
print("Battery Charge:",                eps_bat_charge,         "mAh")
print("Battery Heater 1 Duty Cycle:",   eps_bat_heater_1_dc,    "%")
print("Battery Heater 2 Duty Cycle:",   eps_bat_heater_2_dc,    "%")

pl = list()

# Packet ID
pl.append(pkt_id)

# Source Address
for i in sat_callsign:
    pl.append(ord(i))

# Timestamp
pl.append((eps_mcu_ts >> 24) & 0xFF)
pl.append((eps_mcu_ts >> 16) & 0xFF)
pl.append((eps_mcu_ts >> 8) & 0xFF)
pl.append(eps_mcu_ts & 0xFF)

# MCU Temperature
eps_mcu_temp += 273 # Convert to Kelvin
pl.append(eps_mcu_temp >> 8)
pl.append(eps_mcu_temp & 0xFF)

# EPS Current
pl.append(eps_mcu_current >> 8)
pl.append(eps_mcu_current & 0xFF)

# Reset Counter
pl.append(eps_mcu_reset_counter >> 8)
pl.append(eps_mcu_reset_counter & 0xFF)

# Solar Panels Voltages
pl.append(eps_sp_volt_mypx >> 8)
pl.append(eps_sp_volt_mypx & 0xFF)

pl.append(eps_sp_volt_mxpz >> 8)
pl.append(eps_sp_volt_mxpz & 0xFF)

pl.append(eps_sp_volt_mzpy >> 8)
pl.append(eps_sp_volt_mzpy & 0xFF)

# Solar Panels Currents
pl.append(eps_sp_curr_my >> 8)
pl.append(eps_sp_curr_my & 0xFF)

pl.append(eps_sp_curr_py >> 8)
pl.append(eps_sp_curr_py & 0xFF)

pl.append(eps_sp_curr_mx >> 8)
pl.append(eps_sp_curr_mx & 0xFF)

pl.append(eps_sp_curr_px >> 8)
pl.append(eps_sp_curr_px & 0xFF)

pl.append(eps_sp_curr_mz >> 8)
pl.append(eps_sp_curr_mz & 0xFF)

pl.append(eps_sp_curr_pz >> 8)
pl.append(eps_sp_curr_pz & 0xFF)

# MPPT Duty Cycle
pl.append(eps_mppt_1_dc)
pl.append(eps_mppt_2_dc)
pl.append(eps_mppt_3_dc)

# MPPT Voltage
pl.append(eps_mppt_output_volt >> 8)
pl.append(eps_mppt_output_volt & 0xFF)

# Main Bus Voltage
pl.append(eps_main_bus_volt >> 8)
pl.append(eps_main_bus_volt & 0xFF)

# RTDs Temperature
eps_rtd_0_temp += 273
eps_rtd_1_temp += 273
eps_rtd_2_temp += 273
eps_rtd_3_temp += 273
eps_rtd_4_temp += 273
eps_rtd_5_temp += 273
eps_rtd_6_temp += 273

pl.append(eps_rtd_0_temp >> 8)
pl.append(eps_rtd_0_temp & 0xFF)

pl.append(eps_rtd_1_temp >> 8)
pl.append(eps_rtd_1_temp & 0xFF)

pl.append(eps_rtd_2_temp >> 8)
pl.append(eps_rtd_2_temp & 0xFF)

pl.append(eps_rtd_3_temp >> 8)
pl.append(eps_rtd_3_temp & 0xFF)

pl.append(eps_rtd_4_temp >> 8)
pl.append(eps_rtd_4_temp & 0xFF)

pl.append(eps_rtd_5_temp >> 8)
pl.append(eps_rtd_5_temp & 0xFF)

pl.append(eps_rtd_6_temp >> 8)
pl.append(eps_rtd_6_temp & 0xFF)

# Battery Voltage
pl.append(eps_bat_volt >> 8)
pl.append(eps_bat_volt & 0xFF)

# Battery Current
pl.append(eps_bat_curr >> 8)
pl.append(eps_bat_curr & 0xFF)

# Battery Charge
pl.append(eps_bat_charge >> 8)
pl.append(eps_bat_charge & 0xFF)

# Battery Heater Duty Cycle
pl.append(eps_bat_heater_1_dc)
pl.append(eps_bat_heater_2_dc)

# Encode using NGHam
prot = PyNGHam()

pkt = prot.encode(pl)

# Modulate using GMSK
gmsk = GMSK(0.5, bitrate)

samples, fs, dur = gmsk.modulate(pkt, 1000)

# Transmit with Adalm Pluto
sdr = Pluto(1000000, pwr - 10)

x = sdr.transmit(samples, dur, fs, freq)
