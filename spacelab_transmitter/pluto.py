#
#  pluto.py
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


import adi

class Pluto:
    """
    PlutoSDR handler.
    """
    def __init__(self, sample_rate, gain):
        """
        Constructor.

        :param sample_rate: Sample rate in S/s
        :param gain: gain in dB (valid range is -90 to 0 dB)
        """
        self._pluto = adi.Pluto("ip:192.168.2.1")
        self._pluto.sample_rate = int(sample_rate)
        self._pluto.tx_rf_bandwidth = int(sample_rate)
        self._pluto.tx_hardwaregain_chan0 = int(gain)

    def transmit(self, samples, dur, rate, freq):
        """
        Function to transmit IQ samples through the SDR device.

        :param: samples: A NumPy array with the IQ data (complex).
        :param: dur: is the time duration of the transmission (in seconds).
        :param: rate: is the samples rate of the input samples.
        :param: freq: is the frequency in Hz.

        :return: None.
        """
        samples *= 2**14    # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
        self._pluto.tx_lo = int(freq)

        self._pluto.tx(samples)
