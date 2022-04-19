#!/usr/bin/env python

#
#  __main__.py
#  
#  Copyright (C) 2022, Universidade Federal de Santa Catarina
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


import os
import sys
import pathlib

sys.path.append(str(pathlib.Path(os.path.realpath(__file__)).parents[1]))

from spacelab_transmitter.spacelabtransmitter import SpaceLabTransmitter

#def main(args):
def main():
    """Main function.

    Args:

    Returns:
        The code uppon termination.
    """
    app = SpaceLabTransmitter()
    return app.run()


if __name__ == '__main__':
    import sys
#    sys.exit(main(sys.argv))
    sys.exit(main())
