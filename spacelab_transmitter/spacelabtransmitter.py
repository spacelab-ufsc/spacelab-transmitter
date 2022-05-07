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
from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from pyngham import PyNGHam

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

_DEFAULT_CALLSIGN               = 'PP5UF'
_DEFAULT_LOCATION               = 'Florianópolis'
_DEFAULT_COUNTRY                = 'Brazil'

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
        self._load_preferences()

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

        #Ping 
        self.ping_request = self.builder.get_object("ping_request")
        self.ping_request.connect("clicked", self.on_ping_request_command_clicked)

        #Entry_preferences_general_callsign builder
        self.entry_preferences_general_callsign = self.builder.get_object("entry_preferences_general_callsign")

        # Events treeview
        self.treeview_events = self.builder.get_object("treeview_events")
        self.listmodel_events = Gtk.ListStore(str, str)
        self.treeview_events.set_model(self.listmodel_events)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Datetime", cell, text=0)
        column.set_fixed_width(250)
        self.treeview_events.append_column(column)
        column = Gtk.TreeViewColumn("Event", cell, text=1)
        self.treeview_events.append_column(column)

        #About dialog
        self.aboutdialog = self.builder.get_object("aboutdialog_spacelab_transmitter")
        self.aboutdialog.set_version(spacelab_transmitter.version.__version__)
        if os.path.isfile(_LOGO_FILE_LOCAL):
            self.aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(_LOGO_FILE_LOCAL))
        else:
            self.aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(_LOGO_FILE_LINUX_SYSTEM))

        # About toolbutton
        self.toolbutton_about = self.builder.get_object("toolbutton_about")
        self.toolbutton_about.connect("clicked", self.on_toolbutton_about_clicked)

        #Preferences dialog
        self.button_preferences = self.builder.get_object("button_preferences")
        self.button_preferences.connect("clicked", self.on_button_preferences_clicked)

        self.dialog_preferences = self.builder.get_object("dialog_preferences")
        self.button_preferences_ok = self.builder.get_object("button_preferences_ok")
        self.button_preferences_ok.connect("clicked", self.on_button_preferences_ok_clicked)
        self.button_preferences_default = self.builder.get_object("button_preferences_default")
        self.button_preferences_default.connect("clicked", self.on_button_preferences_default_clicked)
        self.button_preferences_cancel = self.builder.get_object("button_preferences_cancel")
        self.button_preferences_cancel.connect("clicked", self.on_button_preferences_cancel_clicked)

        self.entry_preferences_general_callsign = self.builder.get_object("entry_preferences_general_callsign")
        self.entry_preferences_general_location = self.builder.get_object("entry_preferences_general_location")
        self.entry_preferences_general_country = self.builder.get_object("entry_preferences_general_country")

    def run(self):

        self.window.show_all()
        Gtk.main()

    def destroy(window, self):
        Gtk.main_quit()


    def on_ping_request_command_clicked(self, button):
        pngh = PyNGHam()
        callsign = self.entry_preferences_general_callsign.get_text()

        string_callsign = len(callsign) 
        print(string_callsign)
        n = 7 - string_callsign 
        print(n)
        if n != 7: 
            final_callsign = n*" " + callsign
        print(final_callsign)
        x = [ord(i) for i in final_callsign] 

        pl = [0x40] + x
        self.pkt = pngh.encode(pl)
        print("Encoded packet:", self.pkt)

        self.listmodel_events.append([str(datetime.now()), "Ping Resquest initial string"])
        
    def on_button_preferences_clicked(self, button):
        response = self.dialog_preferences.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self._load_preferences()
            self.dialog_preferences.hide()

    def on_button_preferences_ok_clicked(self, button):
        self._save_preferences()
        self.dialog_preferences.hide()

    def on_button_preferences_default_clicked(self, button):
        self._load_default_preferences()

    def on_button_preferences_cancel_clicked(self, button):
        self._load_preferences()
        self.dialog_preferences.hide()

    def _load_preferences(self):
        home = os.path.expanduser('~')
        location = os.path.join(home, _DIR_CONFIG_LINUX)

    def _load_default_preferences(self):
        self.entry_preferences_general_callsign.set_text(_DEFAULT_CALLSIGN)
        self.entry_preferences_general_location.set_text(_DEFAULT_LOCATION)
        self.entry_preferences_general_country.set_text(_DEFAULT_COUNTRY)

    def _save_preferences(self):
        home = os.path.expanduser('~')
        location = os.path.join(home, _DIR_CONFIG_LINUX)

        if not os.path.exists(location):
            os.mkdir(location)

    def on_toolbutton_about_clicked(self, toolbutton):
        response = self.aboutdialog.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.aboutdialog.hide()
