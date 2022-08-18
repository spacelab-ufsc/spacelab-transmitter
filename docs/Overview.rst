########
Overview 
########

.. image:: enterprise.png
   :target: https://www.youtube.com/watch?v=JaDpDG2fYtY
   :width: 50px                                                                                                                                                                                                                                     
The *Spacelab-Transmitter* is a Python in-development software to transmit telecommands to satellites using an SDR (Software Defined Radio).

A list of known satellites that are planned to use this software so far are presented below:

* **FloripaSat-1** [1]_
* **GOLDS-UFSC (a.k.a. FloripaSat-2)** [2]_
* **Catarina-A1**

The satellites of the list above are developed (or in development) by the same research group: the *Space Technology Research Laboratory* (SpaceLab) [3]_, from *Universidade Federal de Santa Catarina* (Brazil).

The Software
============

.. image:: img/front_page.png
   :width: 700

The objective of this software is to become the "universal" software of the Spacelab's Satellites to transmit telecommands to any of its satellites.

As it is first focused on GOLDS-UFSC, right when we run the software we can see 14 buttons with the respective telecommands of this sattelite:

* Ping Request
* Data Request
* Broadcast Message
* Enter Hibernation
* Leave Hibernation
* Activate Module
* Deactivate Module
* Activate Payload
* Deactivate Payload
* Erase Memory
* Force Reset
* Get Payload Data
* Set Parameter
* Get Parameter

For future satellites, new types of telecommands can be added to this list.

The software also has other functionalities, like doppler correction, wav files generation, a logging system, and so on. More details are described in the next sections of this documentation.

This application is written in Python, and is based on the experience gathered in the applications developed for the FloripaSat-1 mission. For telemetry decoding, there is also another application developed by the same research group, called *SpaceLab-Decoder* [4]_.

References
==========

.. [1] Marcelino, Gabriel M.; Martinez, Sara V.; Seman, Laio O., Slongo, Leonardo K.; Bezerra, Eduardo A. *A Critical Embedded System Challenge: The FloripaSat-1 Mission*. IEEE Latin America Transactions, Vol. 18, Issue 2, 2020.
.. [2] https://github.com/spacelab-ufsc/floripasat2-doc
.. [3] https://spacelab.ufsc.br/
.. [4] https://github.com/spacelab-ufsc/spacelab-decoder
