************
Telecommands
************

Introduction
============

The Spacelab-Transmitter has 14 available telecommands that interact with the lab's satellites, two of them are classified as public, that can be transmitted by any amateur radio. In the next section, these telecommands are described.

Available Telecommands
======================

The table below lists all the 14 available telecommands, including their IDs, size and type of telecommand. In the next sections, each telecommand is described.

+--------------------+-----+------------------------------------------------+--------------+---------+
| Telecommand        | ID  | Content                                        | Size (bytes) | Type    |
+====================+=====+================================================+==============+=========+
| Ping Request       | 40h | None                                           | 8            | Public  |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Data Request       | 41h | Data ID + Start ts. + End ts. + Hash           | 37           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Broadcast Message  | 42h | Dst. callsign + message                        | 15 to 53     | Public  |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Enter Hibernation  | 43h | Hibernation in hours + Hash                    | 30           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Leave Hibernation  | 44h | Hash                                           | 28           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Activate Module    | 45h | Module ID + Hash                               | 29           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Deactivate Module  | 46h | Module ID + Hash                               | 29           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Activate Payload   | 47h | Payload ID + Hash                              | 29           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Deactivate Payload | 48h | Payload ID + Hash                              | 29           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Erase Memory       | 49h | Hash                                           | 28           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Force Reset        | 4Ah | Hash                                           | 28           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Get Payload Data   | 4Bh | Payload ID + Args. + Hash                      | 41           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Set Parameter      | 4Ch | Subsystem ID + Param. ID + Param. value + Hash | 34           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+
| Get Parameter      | 4Dh | Subsystem ID + Parameter ID + Hash             | 30           | Private |
+--------------------+-----+------------------------------------------------+--------------+---------+

Ping Request
------------

TODO

Data Request
------------

TODO

Bloadcast Message
-----------------

TODO

Enter Hibernation
-----------------

TODO

Leave Hibernation
-----------------

TODO

Activate Module
---------------

TODO

Deactivate Module
-----------------

TODO

Activate Payload
----------------

TODO

Deactivate Payload
------------------

TODO

Erase Memory
------------

TODO

Force Reset
-----------

TODO

Get Payload Data
----------------

TODO

Set Parameter
-------------

TODO

Get Parameter
-------------

TODO

Authentication
==============

All the telecommands classified as private use an HMAC authentication scheme. Every type of private telecommand has a unique 16-digit ASCII character key that with the telecommand sequence (or message) generates an 160-bits (20-bytes) hash sequence to be transmitted together with the packet payload. The used hash algorithm is the SHA-1. [3]_. The below illustrates this authentication method.

.. image:: img/hmac.png
   :width: 500

Structure of the packets
========================

Every package payload countains its ID (1 byte), the source callsign (source address of the ground station, 7 bytes) and the package content (data, up to 212 bytes). This last one can either have none or many parameters depending on the function of the telecommand.

The used communication protocol is a python variation of the NGHam [1]_: the PyNGHam [2]_.

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
