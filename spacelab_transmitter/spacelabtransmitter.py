# -*- coding: utf-8 -*-

#
#  spacelab_transmitter.py
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


#MODULES 
import os
import threading
import sys
import signal
from datetime import datetime
import pathlib
import json

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import matplotlib.pyplot as plt
from scipy.io import wavfile
import zmq

#import pyngham

import spacelab_transmitter.version

#here's for importing the other files of spacelab-transmitter that are missing or not ready

#CONSTANTS
_UI_FILE_LOCAL                  = os.path.abspath(os.path.dirname(__file__)) + '/data/ui/spacelab_transmitter.glade'
_UI_FILE_LINUX_SYSTEM           = '/usr/share/spacelab_transmitter/spacelab_transmitter.glade'

_ICON_FILE_LOCAL                = os.path.abspath(os.path.dirname(__file__)) + '/data/img/spacelab_transmitter_256x256.png'
_ICON_FILE_LINUX_SYSTEM         = '/usr/share/icons/spacelab_transmitter_256x256.png'

_LOGO_FILE_LOCAL                = os.path.abspath(os.path.dirname(__file__)) + '/data/img/spacelab-logo-full-400x200.png'
_LOGO_FILE_LINUX_SYSTEM         = '/usr/share/spacelab_transmitter/spacelab-logo-full-400x200.png' 

_DIR_CONFIG_LINUX               = '.spacelab_transmitter'
_DIR_CONFIG_WINDOWS             = 'spacelab_transmitter'

_SAT_JSON_FLORIPASAT_1_LOCAL    = os.path.abspath(os.path.dirname(__file__)) + '/data/satellites/floripasat-1.json'
_SAT_JSON_FLORIPASAT_1_SYSTEM   = '/usr/share/spacelab_transmitter/floripasat-1.json'
_SAT_JSON_FLORIPASAT_2_LOCAL    = os.path.abspath(os.path.dirname(__file__)) + '/data/satellites/floripasat-2.json'
_SAT_JSON_FLORIPASAT_2_SYSTEM   = '/usr/share/spacelab_transmitter/floripasat-2.json'

#signal constants (?) such as location, country, etc. (?)

class SpaceLabTransmitter:

    def __init__(self):
        self.builder = Gtk.Builder()
        # UI file from Glade
        if os.path.isfile(_UI_FILE_LOCAL):
            self.builder.add_from_file(_UI_FILE_LOCAL)
        else:
            self.builder.add_from_file(_UI_FILE_LINUX_SYSTEM)

        self.builder.connect_signals(self)

        self._build_widgets()

        #self._load_preferences()
        #self.ngham = pyngham.PyNGHam()
        #self.decoded_packets_index = list()

    def _build_widgets(self):
        # Main window
        self.window = self.builder.get_object("window_main")
        if os.path.isfile(_ICON_FILE_LOCAL):
            self.window.set_icon_from_file(_ICON_FILE_LOCAL)
        else:
            self.window.set_icon_from_file(_ICON_FILE_LINUX_SYSTEM)
        self.window.set_wmclass(self.window.get_title(), self.window.get_title())
        self.window.connect("destroy", Gtk.main_quit)

    def run(self):

        self.window.show_all()
        Gtk.main()

    def destroy(window, self):
        Gtk.main_quit()