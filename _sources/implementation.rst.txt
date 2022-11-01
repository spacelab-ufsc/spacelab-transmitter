**************
Implementation
**************

Telecommands Code
=================

The Spacelab Transmitter has a generic telecommand class with these functions:

- **generate**: which generate the telecommand payload;
- **set_id**: which sets a new ID for the telecommand;
- **get_id**: which gets the ID of the telecommand;
- **set_name**: which sets a new name for the telecommand;
- **get_name**: which gets the name of the telecommand;
- **_prepare_callsign**: which prepares a callsign for a transmission.

Each telecommand has its own class with the Telecommand class working as a "superclass" with 14 telecommands classes working as "subclasses" (this process is called "inheritance" in object-oriented programming).

USRP Integration
****************

The USRP hardware driver (UHD) is the driver provided to the USRP radios. Since the Spacelab Transmitter code is in Python, it's necessary to install UHD and Python API and test them [5]_.

The folder has a specific file for usrp class, where it has a constructor function and the transmit function. To transmit it's necessary to have the:

- samples;
- duration;
- center frequency;
- sample rate;
- gain.

**In the code of the usrp class:**

.. code-block:: python

   samples = signal.resample_poly(samples, self._sample_rate, rate)
   if self._usrp.send_waveform(samples, dur, freq, self._sample_rate, [0], self._gain):
      return True
   else:
      return False

And the true/false return is for if it was successfull or not.

**In the code of the telecommands transmission:**

The previous parameters are set in the software and the code extracts the user inputs from the UI (GTK) to assign to the usrp values.

.. code-block:: python

   carrier_frequency = self.entry_carrier_frequency.get_text()

   tx_gain = self.spinbutton_tx_gain.get_text()

   samples, sample_rate, duration_s = mod.modulate(pkt, 1000)

   sdr = USRP(int(self.entry_sample_rate.get_text()), int(tx_gain))

   if sdr.transmit(samples, duration_s, sample_rate, int(carrier_frequency)):
      self.write_log("Set Parameter transmitted to " + sat_json + " from" + callsign + " in " + carrier_frequency + " Hz with a gain of " + tx_gain + " dB")
   else:
      self.write_log("Error transmitting a Set Parameter telecommand!")
