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
be transmitted together with the packet payload. The used hash algorithm is the SHA-1.

Telecommands
============

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

