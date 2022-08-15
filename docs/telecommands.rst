************
Telecommands
************

Introduction
============

The Spacelab Transmitter has 14 available telecommands that interact with the lab's satellites, two of them are classified as public, that can be transmitted by any amateur radio.

Authentication
==============

All the telecommands classified as private use an HMAC authentication scheme. Every
type of private telecommand has a unique 16-digit ASCII character key that with the
telecommand sequence (or message) generates an 160-bits (20-bytes) hash sequence to
be transmitted together with the packet payload. The used hash algorithm is the SHA-1. [3]_

.. image:: img/hmac.png
   :width: 500

Telecommands Available
======================

+-------------------+------------+
| Telecommand       |    Type    |  
+===================+============+
| Ping Request      |   Public   | 
+-------------------+------------+
| Data Request      |   Private  |
+-------------------+------------+
| Broadcast Message |   Public   | 
+-------------------+------------+ 
| Enter Hibernation |   Private  | 
+-------------------+------------+
| Leave Hibernation |   Private  |
+-------------------+------------+
| Activate Module   |   Private  |
+-------------------+------------+
| Deactivate Module |   Private  |
+-------------------+------------+
| Activate Payload  |   Private  |
+-------------------+------------+
| Deactivate Payload|   Private  |
+-------------------+------------+
| Erase Memory      |   Private  |
+-------------------+------------+
| Force Reset       |   Private  |
+-------------------+------------+
| Get Payload Data  |   Private  |
+-------------------+------------+
| Set Parameter     |   Private  |
+-------------------+------------+
| Get Parameter     |   Private  |
+-------------------+------------+

Structure of the packages 
=========================

Every package payload countains its ID [1 byte], the source callsign (source address of the ground station) [7 bytes] and the package content (data) [up to 212 bytes]. This las tone can either have none or many parameters depending on the funtion of the telecommand.

The communication protocol used is a python variation of the NGHam [1]_: the PyNGHam [2]_.

.. image:: img/ngham.png
   :width: 300

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

References
==========


.. [1] https://github.com/skagmo/ngham
.. [2] https://github.com/mgm8/pyngham
.. [3] https://github.com/spacelab-ufsc/floripasat2-doc