*************************
Telecommands Transmission
*************************

Introduction
============

The Spacelab-Transmitter is the software for the Spacelab's Ground Station (GRS), it can transmit 14 telecommands as previously shown in the overview.    
 
In order to not depend on another software to transmit telecommands, it was implemented a GMSK modulator in the code so that the Spacelab Transmitter works alone with the Software-Defined Radio.

The default Software-Defined Radio used in Spacelab is the USRP210 so the code was written based in the integration with this specific SDR.

.. image:: img/usrp.png
   :width: 500

GMSK Implementation
===================



Integration with USRP SDR
=========================


References
==========
https://github.com/skagmo/ngham

https://github.com/mgm8/pyngham

https://pysdr.org/content/usrp.html

Viswanathan, Mathuranathan. Digital Modulations Using Python. 1st ed., vol. 1, Independently published, 2019.

