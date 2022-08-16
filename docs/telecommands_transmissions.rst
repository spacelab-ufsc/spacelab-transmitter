*************************
Telecommands Transmission
*************************

Introduction
============

The Spacelab-Transmitter is the software for the Spacelab's Ground Station (GRS), it can transmit 14 telecommands as previously shown in the overview.    
 
In order to not depend on another software to transmit telecommands, it was implemented a GMSK modulator in the code so that the Spacelab Transmitter works alone with the Software-Defined Radio.

The default Software-Defined Radio used in Spacelab is the USRP B210 so the code was written based in the integration with this specific SDR, and the modulation is the GMSK. In the code we have a class for USRP and for GMSK and also in every telecommand transmission function in the SpacelabTransmitter class we have implemented both of their codes.

.. image:: img/usrp.png
   :width: 500

GMSK Implementation
===================

Modulation and GMSK
*******************


**In the code of the gmsk class:**

**In the code of the telecommands transmission:**


Integration with USRP SDR
=========================

Software-Defined Radio
**********************

The IEEE considers Software defined to be refered to the use of software processing within the radio
system or device to implement operating (but not control) functions and Software-Defined Radio (SDR) a radio in which some or all of the physical layer functions are software
defined. [1]_ 

As said before,the SDR used in Spacelab transmissions to satellites is the USRP B210 and the modulation used is the GMSK. 

USRP
****

Means Universal Software Radio Peripheral, it's a family os SDRs designed by the Ettus Research and NI. The B210 has a continuous frequency coverage from 70 MHz to 6 GHz [2]_, which covers the frequencies used by the Spacelab's satellites.

USRP Integration 
****************

The USRP hardware driver (UHD) is the driver provided to the USRP radios. Since the Spacelab Transmitter code is in Python, it's necessary to install UHD and Python API and test them [3]_.

The folder has a specific file for usrp class, where it has a constructor function and the transmit function. To transmit it's necessary to have the:

- samples;
- duration;
- center frequency;
- sample rate;
- gain.

**In the code of the usrp class:**

 ``samples = signal.resample_poly(samples, self._sample_rate, rate)``

 ``if self._usrp.send_waveform(samples, dur, freq, self._sample_rate, [0], self._gain):``
    ``return True``
 ``else:``
    ``return False``

And the true/false return is for if it was successfull or not.

**In the code of the telecommands transmission:**

The previous parameters are set in the software and the code extracts the user inputs from the UI (GTK) to assign to the usrp values. 

 ``carrier_frequency = self.entry_carrier_frequency.get_text()``
 
 ``tx_gain = self.spinbutton_tx_gain.get_text()``
 
 ``samples, sample_rate, duration_s = mod.modulate(pkt, 1000)``
 
 ``sdr = USRP(int(self.entry_sample_rate.get_text()), int(tx_gain))``
 
 ``if sdr.transmit(samples, duration_s, sample_rate, int(carrier_frequency)):``

  ``self.write_log("Set Parameter transmitted to " + sat_json + " from" + callsign + " in " + carrier_frequency + " Hz with a gain of " + tx_gain + " dB")``

 ``else:``

  ``self.write_log("Error transmitting a Set Parameter telecommand!")``
            
References
==========

Viswanathan, Mathuranathan. Digital Modulations Using Python. 1st ed., vol. 1, Independently published, 2019.

.. [1] IEEE Project 1900.1 - Standard Definitions and Concepts for Dynamic Spectrum Access: Terminology Relating to Emerging Wireless Networks, System Functionality, and Spectrum Management https://standards.ieee.org/develop/project/1900.1.html.
.. [2] https://www.ettus.com/all-products/ub210-kit/
.. [3] https://pysdr.org/content/usrp.html
