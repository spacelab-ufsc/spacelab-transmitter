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
import numpy as np
from scipy import signal
import time

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
        self._sample_rate = sample_rate
        self._pluto = adi.Pluto("ip:192.168.2.1")
        self.set_tx_gain(gain)
        self._pluto.sample_rate = int(sample_rate)
        self._pluto.tx_rf_bandwidth = int(sample_rate)

    def transmit(self, samples, dur, rate, freq):
        """
        Function to transmit IQ samples through the SDR device.

        :param samples: A NumPy array with the IQ data (complex).
        :param dur: is the time duration of the transmission (in seconds).
        :param rate: is the samples rate of the input samples.
        :param freq: is the frequency in Hz.

        :return: None.
        """
        samples = samples / np.max(np.abs(samples))
        samples = samples.astype(np.complex64)
        samples = signal.resample_poly(samples, self._sample_rate, rate)
        samples *= 2**14    # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

        self._pluto.tx_lo = int(freq)

        self._pluto.tx(samples)

        time.sleep(dur)

        return True

    def receive(self, freq, bw, num_samps, gain=50.0):
        """
        Function to receive IQ samples from the SDR device.

        :param freq: is the frequency in Hz.
        :param gain: is the RX gain in dB (between 0 and 74.5 dB).
        :param bw: is the RX filter bandwith in Hz.
        :param num_samps: is the number of samples to receive.

        :return: The received IQ samples.
        """
        self._pluto.rx_hardwaregain_chan0   = gain
        self._pluto.rx_lo                   = int(freq)
        self._pluto.rx_rf_bandwidth         = bw
        self._pluto.rx_buffer_size          = num_samps

        return self._pluto.rx()

    def set_tx_gain(self, gain):
        """
        Sets the TX gain.

        :param gain: is the desired TX gain.
        :type: int

        :return: None
        """
        self._pluto.tx_hardwaregain_chan0 = int(gain)

    def get_tx_gain(self):
        """
        Gets the TX gain.

        :return: The current TX gain.
        :rtype: int
        """
        return self._pluto.tx_hardwaregain_chan0

    def set_rx_gain_mode(self, mode):
        """
        Sets the RX gain mode.

        :param mode: is the RX gain mode (manual, slow or fast).
        :type: string

        :return: None.
        """
        if mode == 'manual':
            self._pluto.gain_control_mode_chan0 = 'manual'
        elif mode == 'slow':
            self._pluto.gain_control_mode_chan0 = 'slow_attack'
        elif mode == 'fast':
            self._pluto.gain_control_mode_chan0 = 'fast_attack'
        else:
            raise RuntimeError("Invalid RX gain mode!")

    def get_rx_gain_mode(self):
        """
        Gets the RX gain monde.

        :return: the current RX gain mode.
        :rtype: string
        """
        mode = self._pluto.gain_control_mode_chan0

        if mode == 'manual':
            return 'manual'
        elif mode == 'slow_attack':
            return 'slow'
        elif mode == 'fast_attack':
            return 'fast'
        else:
            raise RuntimeError("Invalid RX gain mode!")
