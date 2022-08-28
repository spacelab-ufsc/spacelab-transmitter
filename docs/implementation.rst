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
