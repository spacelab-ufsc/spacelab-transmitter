#
#  usrp.py
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


import uhd
from scipy import signal
import numpy as np

class USRP:
    """
    Ettus USRP SDR handler.
    """
    def __init__(self, sample_rate, gain):
        """
        Constructor.

        :param sample_rate: Sample rate in S/s
        :param gain: gain in dB
        """
        self._sample_rate = sample_rate
        self._gain = gain

        self._usrp = uhd.usrp.MultiUSRP()

    def transmit(self, samples, dur, rate, freq):
        """
        Function to transmit IQ samples through the SDR device.

        :param: samples: A NumPy array with the IQ data (complex).
        :param: dur: is the time duration of the transmission (in seconds).
        :param: rate: is the samples rate of the input samples.
        :param: freq: is the frequency in Hz.

        :return: True/False if successful or not.
        """
        samples = samples.astype(np.complex64)
        samples = signal.resample_poly(samples, self._sample_rate, rate)

        if self._usrp.send_waveform(samples, dur, freq, self._sample_rate, [0], self._gain):
            return True
        else:
            return False
