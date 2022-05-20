#
#  gmsk.py
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


import numpy as np
from scipy.signal import upfirdn, lfilter

class GMSK:

    def __init__(self, bt, baud):
        self._bt = bt
        self._baudrate = baud

    def modulate(self, data, fc):
        """
        Function to modulate a binary stream using GMSK modulation
        Parameters:
        data : input integer list to modulate (bytes as integers)
        enable_plot: True = plot transmitter waveforms (default False)
        Returns:
        (s_t,s_complex) : tuple containing the following variables
        s_t : GMSK modulated signal with carrier s(t)
        s_complex : baseband GMSK signal (I+jQ)
        """
        L = 40
        fs = L*fc
        Ts = 1/fs
        Tb = L*Ts                                   # Derived waveform timing parameters
        data = self._int_list_to_bit_list(data)
        data = np.array(data)
        c_t = upfirdn(h=[1]*L, x=2*data-1, up = L)  # NRZ pulse train c(t)
        k = 1                                       # Truncation length for Gaussian LPF
        h_t = self._gaussian_lpf(Tb, L, k)          # Gaussian LPF with BT=0.25
        b_t = np.convolve(h_t, c_t, 'full')         # Convolve c(t) with Gaussian LPF to get b(t)
        bnorm_t = b_t/max(abs(b_t))                 # Normalize the output of Gaussian LPF to +/-1
        h = 0.5                                     # Modulation index (GMSK = 0,5)
        # Integrate to get phase information
        phi_t = lfilter(b = [1], a=[1,-1], x=bnorm_t*Ts) * h*np.pi/Tb
        I = np.cos(phi_t)
        Q = np.sin(phi_t)                           # Cross-correlated baseband I/Q signals
        s_complex = I - 1j*Q                        # Complex baseband representation
        t = Ts*np.arange(start=0, stop=len(I))      # Time base for RF carrier
        sI_t = I*np.cos(2*np.pi*fc*t)
        sQ_t = Q*np.sin(2*np.pi*fc*t)
        s_t = sI_t - sQ_t                           # s(t) - GMSK with RF carrier

        return (s_t, s_complex)

    def _gaussian_lpf(self, Tb, L, k):
        """
        Generate filter coefficients of Gaussian low pass filter (used in gmsk_mod)
        Parameters:
        Tb : bit period
        L : oversampling factor (number of samples per bit)
        k : span length of the pulse (bit interval)
        Returns:
        h_norm : normalized filter coefficients of Gaussian LPF
        """
        B = self._bt/Tb     # Bandwidth of the filter
        # Truncated time limits for the filter
        t = np.arange(start = -k*Tb, stop = k*Tb + Tb/L, step = Tb/L)
        h = B*np.sqrt(2*np.pi/(np.log(2)))*np.exp(-2 * (t*np.pi*B)**2 /(np.log(2)))
        h_norm = h / np.sum(h)
        return h_norm

    def _int_list_to_bit_list(self, n):
        res = list()
        for i in n:
            res = res + [int(digit) for digit in bin(i)[2:].zfill(8)]

        return res
