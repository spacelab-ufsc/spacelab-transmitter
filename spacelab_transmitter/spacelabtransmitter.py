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


import os
import threading
from datetime import datetime
import pathlib
import json
import csv

import gi
from numpy import broadcast
from spacelab_transmitter.tc_activate_module import ActivateModule
from spacelab_transmitter.tc_broadcast import Broadcast
from spacelab_transmitter.tc_data_request import DataRequest

from spacelab_transmitter.tc_deactivate_module import DeactivateModule
from spacelab_transmitter.tc_activate_payload import ActivatePayload
from spacelab_transmitter.tc_deactivate_payload import DeactivatePayload
from spacelab_transmitter.tc_erase_memory import EraseMemory
from spacelab_transmitter.tc_force_reset import ForceReset
from spacelab_transmitter.tc_get_parameter import GetParameter
from spacelab_transmitter.tc_get_payload_data import GetPayloadData
from spacelab_transmitter.tc_leave_hibernation import LeaveHibernation
from spacelab_transmitter.tc_set_parameter import SetParameter
from spacelab_transmitter.telecommands_transmission import DialogDataRequest, DialogDeactivatePayload, DialogEnterHibernation, DialogActivatePayload, DialogGetPayloadData, DialogSetParameter
from spacelab_transmitter.telecommands_transmission import DialogDeactivateModule, DialogDeactivatePayload
from spacelab_transmitter.telecommands_transmission import DialogActivateModule, DialogGetParameter


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from pyngham import PyNGHam

import spacelab_transmitter.version
from spacelab_transmitter.gmsk import GMSK
from spacelab_transmitter.usrp import USRP
from spacelab_transmitter.tc_ping import Ping
from spacelab_transmitter.tc_enter_hibernation import Enter_hibernation

# Constants
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
_SAT_JSON_GOLDS_UFSC_LOCAL      = os.path.abspath(os.path.dirname(__file__)) + '/data/satellites/golds-ufsc.json'
_SAT_JSON_GOLDS_UFSC_SYSTEM     = '/usr/share/spacelab_transmitter/golds-ufsc.json'

_DEFAULT_CALLSIGN               = 'PP5UF'
_DEFAULT_LOCATION               = 'Florianópolis'
_DEFAULT_COUNTRY                = 'Brazil'

_DIR_CONFIG_DEFAULTJSON         = 'spacelab_transmitter.json'

# Defining logfile default local
_DIR_CONFIG_LOGFILE_LINUX       = 'spacelab_transmitter'
_DEFAULT_LOGFILE_PATH           = os.path.join(os.path.expanduser('~'), _DIR_CONFIG_LOGFILE_LINUX)
_DEFAULT_LOGFILE                = 'logfile.csv'

class DialogPassword(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Authentification", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Enter the key")
        self.entry_password = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_password, 0, 1, 1, 1)
        

        box = self.get_content_area()
        box.add(grid)

        '''box.add(label)
        box.add(self.entry_password)'''
        self.show_all()

    def get_key(self):
        return self.entry_password.get_text()

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
        self.write_log("SpaceLab Transmitter initialized!")
        self._load_preferences()

        self.pkt = []
        self.label = ""

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

        # Entry_preferences_general_callsign builder
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

        # About dialog
        self.aboutdialog = self.builder.get_object("aboutdialog_spacelab_transmitter")
        self.aboutdialog.set_version(spacelab_transmitter.version.__version__)
        if os.path.isfile(_LOGO_FILE_LOCAL):
            self.aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(_LOGO_FILE_LOCAL))
        else:
            self.aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(_LOGO_FILE_LINUX_SYSTEM))

        # About toolbutton
        self.toolbutton_about = self.builder.get_object("toolbutton_about")
        self.toolbutton_about.connect("clicked", self.on_toolbutton_about_clicked)

        # Switch button transmission
        self.switch_button = self.builder.get_object("switch_button")
        self.switch_button.connect("state-set", self.on_switch_button_clicked)

        # Switch button Doppler correction
        self.switch_doppler = self.builder.get_object("switch_doppler")

        # Logfile chooser button
        self.logfile_chooser_button = self.builder.get_object("logfile_chooser_button")
        self.logfile_chooser_button.set_filename(_DEFAULT_LOGFILE_PATH)

        # SDR Parameters
        self.entry_carrier_frequency = self.builder.get_object("entry_carrier_frequency")
        self.entry_sample_rate = self.builder.get_object("entry_sample_rate")
        self.spinbutton_tx_gain = self.builder.get_object("spinbutton_tx_gain")

        # Satellite combobox
        self.liststore_satellite = self.builder.get_object("liststore_satellite")
        self.liststore_satellite.append(["FloripaSat-1"])
        self.liststore_satellite.append(["GOLDS-UFSC"])
        self.combobox_satellite = self.builder.get_object("combobox_satellite")
        cell = Gtk.CellRendererText()
        self.combobox_satellite.pack_start(cell, True)
        self.combobox_satellite.add_attribute(cell, "text", 0)

        # Preferences dialog
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

        #Ping Request
        self.button_ping_request = self.builder.get_object("button_ping_request")
        self.button_ping_request.connect("clicked", self.on_button_ping_request_command_clicked)

        #Broadcast Message
        self.button_broadcast_message = self.builder.get_object("button_broadcast_message")
        self.button_broadcast_message.connect("clicked", self.on_button_broadcast_message_clicked)

        self.dialog_broadcast = self.builder.get_object("dialog_broadcast")
        self.entry_msg = self.builder.get_object("entry_msg")
        self.entry_dst_callsign = self.builder.get_object("entry_dst_callsign")
        self.button_broadcast_send = self.builder.get_object("button_broadcast_send")
        self.button_broadcast_send.connect("clicked", self.on_button_broadcast_send_clicked)
        self.button_broadcast_cancel = self.builder.get_object("button_broadcast_cancel")
        self.button_broadcast_cancel.connect("clicked", self.on_button_broadcast_cancel_clicked)

        #Force Reset
        self.button_force_reset = self.builder.get_object("button_force_reset")
        self.button_force_reset.connect("clicked", self.on_button_force_reset_clicked)
        
        #Erase Memory
        self.button_erase_memory = self.builder.get_object("button_erase_memory")
        self.button_erase_memory.connect("clicked", self.on_button_erase_memory_clicked)
        
        #Enter Hibernation
        self.button_enter_hibernation = self.builder.get_object("button_enter_hibernation")
        self.button_enter_hibernation.connect("clicked", self.on_button_enter_hibernation_clicked)

        #Leave Hibernation
        self.button_leave_hibernation = self.builder.get_object("button_leave_hibernation")
        self.button_leave_hibernation.connect("clicked", self.on_button_leave_hibernation_clicked)

        #Activate Module
        self.button_activate_module = self.builder.get_object("button_activate_module")
        self.button_activate_module.connect("clicked", self.on_button_activate_module_clicked)
    
        #Deactivate Module
        self.button_deactivate_module = self.builder.get_object("button_deactivate_module")
        self.button_deactivate_module.connect("clicked", self.on_button_deactivate_module_clicked)

        #Activate Payload
        self.button_activate_payload = self.builder.get_object("button_activate_payload")
        self.button_activate_payload.connect("clicked", self.on_button_activate_payload_clicked)

        #Deactivate Payload
        self.button_deactivate_payload = self.builder.get_object("button_deactivate_payload")
        self.button_deactivate_payload.connect("clicked", self.on_button_deactivate_payload_clicked)

        #Get Parameter
        self.button_get_parameter = self.builder.get_object("button_get_parameter")
        self.button_get_parameter.connect("clicked", self.on_button_get_parameter_clicked)

        #Get Payload Data
        self.button_get_payload_data = self.builder.get_object("button_get_payload_data")
        self.button_get_payload_data.connect("clicked", self.on_button_get_payload_data_clicked)

        #Set Parameter
        self.button_set_parameter = self.builder.get_object("button_set_parameter")
        self.button_set_parameter.connect("clicked", self.on_button_set_parameter_clicked)

        #Data Request
        self.button_data_request = self.builder.get_object("button_data_request")
        self.button_data_request.connect("clicked", self.on_button_data_request_clicked)



    def run(self):
        self.window.show_all()          
        Gtk.main()

    def destroy(window, self):
        Gtk.main_quit()

    def on_button_ping_request_command_clicked(self, button):
        callsign = self.entry_preferences_general_callsign.get_text()

        pg = Ping()

        pl = pg.generate(callsign)

        pngh = PyNGHam()

        pkt = pngh.encode(pl)

        sat_json = str()
        if self.combobox_satellite.get_active() == 0:
            sat_json = 'FloripaSat-1'
        elif self.combobox_satellite.get_active() == 1:
            sat_json = 'GOLDS-UFSC'

        carrier_frequency = self.entry_carrier_frequency.get_text()
        tx_gain = self.spinbutton_tx_gain.get_text()

        mod = GMSK(0.5, 1200)   # BT = 0.5, 1200 bps

        samples, sample_rate, duration_s = mod.modulate(pkt, 1000)

        sdr = USRP(int(self.entry_sample_rate.get_text()), int(tx_gain))

        if sdr.transmit(samples, duration_s, sample_rate, int(carrier_frequency)):
            self.write_log("Ping request transmitted to " + sat_json + " from" + callsign + " in " + carrier_frequency + " Hz with a gain of " + tx_gain + " dB")
        else:
            self.write_log("Error transmitting a ping telecommand!")

    def on_button_enter_hibernation_clicked(self, button):
        dialog = DialogEnterHibernation(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = Enter_hibernation()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_hours(),key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Enter Hibernation"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_activate_module_clicked(self, button):
        dialog = DialogActivateModule(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = ActivateModule()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_ac_mod_id(),key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Activate Module"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_deactivate_module_clicked(self, button):
        dialog = DialogDeactivateModule(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = DeactivateModule()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_deac_mod_id(),key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Deactivate Module"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_deactivate_payload_clicked(self, button):
        dialog = DialogDeactivatePayload(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = DeactivatePayload()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_deac_pl_id(),key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Deactivate Payload"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_activate_payload_clicked(self, button):
        dialog = DialogActivatePayload(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = ActivatePayload()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_ac_pl_id(),key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Activate Payload"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_erase_memory_clicked(self, button):
        dialog = DialogPassword(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            callsign = self.entry_preferences_general_callsign.get_text()
            fr = EraseMemory()
            key = dialog.get_key()
            pl = fr.generate(callsign, key)
            pngh = PyNGHam()
            self.pkt = pngh.encode(pl)
            self.label = "Erase Memory"
            self._transmit_tc(self.pkt, self.label)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_set_parameter_clicked(self, button):
        dialog = DialogSetParameter(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = SetParameter()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_subsys_id(),dialog.get_param_id(),dialog.get_param_val(), key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Set Parameter"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_data_request_clicked(self, button):
        dialog = DialogDataRequest(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = DataRequest()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_data_id(),dialog.get_start_ts(),dialog.get_end_ts(), key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Data Request"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()
    
    def on_button_leave_hibernation_clicked(self, button):
        dialog = DialogPassword(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            callsign = self.entry_preferences_general_callsign.get_text()
            fr = LeaveHibernation()
            key = dialog.get_key()
            pl = fr.generate(callsign, key)
            pngh = PyNGHam()
            self.pkt = pngh.encode(pl)
            self.label = "Leave Hibernation"
            self._transmit_tc(self.pkt, self.label)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_force_reset_clicked(self, button_password_send):
        #response = self.dialog_password.run()
        dialog = DialogPassword(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            callsign = self.entry_preferences_general_callsign.get_text()
            fr = ForceReset()
            key = dialog.get_key()
            pl = fr.generate(callsign, key)
            pngh = PyNGHam()
            self.pkt = pngh.encode(pl)
            self.label = "Force Reset"
            self._transmit_tc(self.pkt, self.label)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_password_send_clicked(self, dialog_password):
        #response = dialog_password.run()
        dialog = DialogPassword(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        print(self.pkt, self.label)
        self._transmit_tc(self.pkt, self.label)

    def on_button_password_cancel_clicked(self, button):
        self.dialog_password.destroy()

    def on_button_get_parameter_clicked(self, button):
        dialog = DialogGetParameter(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = GetParameter()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_subsys_id(),dialog.get_param_id(), key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Get Parameter"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_get_payload_data_clicked(self, button):
        dialog = DialogGetPayloadData(self.window)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog_password = DialogPassword(self.window)
            response_key = dialog_password.run()
            if response_key == Gtk.ResponseType.OK:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = GetPayloadData()
                key = dialog_password.get_key()
                pl = fr.generate(callsign, dialog.get_pl_id(),dialog.get_pl_args(), key) 
                pngh = PyNGHam()
                self.pkt = pngh.encode(pl)
                self.label = "Get Payload Data"
                self._transmit_tc(self.pkt, self.label)
                dialog.destroy()
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.CANCEL:
                dialog_password.destroy()
            elif response_key == Gtk.ResponseType.DELETE_EVENT:
                dialog_password.destroy()
            else:
                dialog_password.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_broadcast_message_clicked(self, button): 
        response = self.dialog_broadcast.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.dialog_broadcast.hide()

    def _transmit_tc(self, pkt, tc_name):
        sat_json = str()
        if self.combobox_satellite.get_active() == 0:
            sat_json = 'FloripaSat-1'
        elif self.combobox_satellite.get_active() == 1:
            sat_json = 'GOLDS-UFSC'

        carrier_frequency = self.entry_carrier_frequency.get_text()
        tx_gain = self.spinbutton_tx_gain.get_text()
        callsign = self.entry_preferences_general_callsign.get_text()

        mod = GMSK(0.5, 1200)   # BT = 0.5, 1200 bps

        samples, sample_rate, duration_s = mod.modulate(pkt, 1000)

        sdr = USRP(int(self.entry_sample_rate.get_text()), int(tx_gain))

        if sdr.transmit(samples, duration_s, sample_rate, int(carrier_frequency)):
            self.write_log(tc_name + " transmitted to " + sat_json + " from" + callsign + " in " + carrier_frequency + " Hz with a gain of " + tx_gain + " dB")
        else:
            self.write_log("Error transmitting a " + tc_name + " telecommand!")

    def on_button_broadcast_cancel_clicked(self, button):
        self.dialog_broadcast.hide()

    def on_button_broadcast_send_clicked(self, button):
        dst_adr = self.entry_dst_callsign.get_text()
        msg = self.entry_msg.get_text()

        bm = Broadcast()

        pl = bm.generate(self.entry_preferences_general_callsign.get_text(), dst_adr, msg)

        pngh = PyNGHam()

        pkt = pngh.encode(pl)

        self._transmit_tc(pkt, "Broadcast Message")
        self.dialog_broadcast.hide()

    #CODE REGARDING PREFERENCES 

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

        if not os.path.isfile(location + "/" + _DIR_CONFIG_DEFAULTJSON):
            self._load_default_preferences()
            self._save_preferences() 

        f = open(location + "/" + _DIR_CONFIG_DEFAULTJSON, "r")
        config = json.loads(f.read())
        f.close()

        self.entry_preferences_general_callsign.set_text(config["callsign"])
        self.entry_preferences_general_location.set_text(config["location"])
        self.entry_preferences_general_country.set_text(config["country"])
        self.logfile_chooser_button.set_filename(config["logfile_path"])

    def _load_default_preferences(self):
        self.entry_preferences_general_callsign.set_text(_DEFAULT_CALLSIGN)
        self.entry_preferences_general_location.set_text(_DEFAULT_LOCATION)
        self.entry_preferences_general_country.set_text(_DEFAULT_COUNTRY)
        self.logfile_chooser_button.set_filename(_DEFAULT_LOGFILE_PATH)
        
    def _save_preferences(self):
        home = os.path.expanduser('~')
        location = os.path.join(home, _DIR_CONFIG_LINUX)

        if not os.path.exists(location):
            os.mkdir(location)

        with open(location + '/' + _DIR_CONFIG_DEFAULTJSON, 'w', encoding='utf-8') as f:
            json.dump({"callsign": self.entry_preferences_general_callsign.get_text(),
                    "location": self.entry_preferences_general_location.get_text(),
                    "country": self.entry_preferences_general_country.get_text(),
                    "logfile_path": self.logfile_chooser_button.get_filename()}, f, ensure_ascii=False, indent=4)

    def on_toolbutton_about_clicked(self, toolbutton):
        response = self.aboutdialog.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.aboutdialog.hide()

    def write_log(self, msg):
        event = [str(datetime.now()), msg]

        self.listmodel_events.append(event)

        if not os.path.exists(_DEFAULT_LOGFILE_PATH):
            os.mkdir(_DEFAULT_LOGFILE_PATH)

        with open(self.logfile_chooser_button.get_filename() + '/' + _DEFAULT_LOGFILE, 'a') as logfile:
            writer = csv.writer(logfile, delimiter='\t')
            writer.writerow(event)

    def on_switch_button_clicked(self, false, button):
        if self.switch_button.get_active() == False:
            self.button_ping_request.set_sensitive(False)
            self.button_enter_hibernation.set_sensitive(False)
            self.button_deactivate_module.set_sensitive(False)
            self.button_erase_memory.set_sensitive(False)
            self.button_set_parameter.set_sensitive(False)
            self.button_data_request.set_sensitive(False)
            self.button_leave_hibernation.set_sensitive(False)
            self.button_activate_payload.set_sensitive(False)
            self.button_force_reset.set_sensitive(False)
            self.button_get_parameter.set_sensitive(False)
            self.button_broadcast_message.set_sensitive(False)
            self.button_activate_module.set_sensitive(False)
            self.button_deactivate_payload.set_sensitive(False)
            self.button_get_payload_data.set_sensitive(False)
        elif self.switch_button.get_active() == True:
            self.button_ping_request.set_sensitive(True)
            self.button_enter_hibernation.set_sensitive(True)
            self.button_deactivate_module.set_sensitive(True)
            self.button_erase_memory.set_sensitive(True)
            self.button_set_parameter.set_sensitive(True)
            self.button_data_request.set_sensitive(True)
            self.button_leave_hibernation.set_sensitive(True)
            self.button_activate_payload.set_sensitive(True)
            self.button_force_reset.set_sensitive(True)
            self.button_get_parameter.set_sensitive(True)
            self.button_broadcast_message.set_sensitive(True)
            self.button_activate_module.set_sensitive(True)
            self.button_deactivate_payload.set_sensitive(True)
            self.button_get_payload_data.set_sensitive(True)
