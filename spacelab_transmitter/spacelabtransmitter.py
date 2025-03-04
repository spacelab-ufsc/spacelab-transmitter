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
import socket

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import spacelab_transmitter.version

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
from spacelab_transmitter.tc_transmit_packet import TransmitPacket
from spacelab_transmitter.tc_ping import Ping
from spacelab_transmitter.tc_enter_hibernation import Enter_hibernation
from spacelab_transmitter.tc_update_tle import UpdateTLE

from spacelab_transmitter.telecommands_transmission import DialogDataRequest, DialogDeactivatePayload, DialogEnterHibernation, DialogActivatePayload, DialogGetPayloadData, DialogSetParameter, DialogDeactivateModule, DialogActivateModule, DialogGetParameter, DialogBroadcastMessage, DialogTransmitPacket, DialogEraseMemory, DialogUpdateTLE, DialogCSPPeek, DialogCSPPoke

from spacelab_transmitter.gmsk import GMSK
from spacelab_transmitter.usrp import USRP
from spacelab_transmitter.pluto import Pluto
from spacelab_transmitter.csp import CSP
from spacelab_transmitter.ax100 import AX100Mode5

from pyngham import PyNGHam

# Constants
_UI_FILE_LOCAL                  = os.path.abspath(os.path.dirname(__file__)) + '/data/ui/spacelab_transmitter.glade'
_UI_FILE_LINUX_SYSTEM           = '/usr/share/spacelab_transmitter/spacelab_transmitter.glade'

_ICON_FILE_LOCAL                = os.path.abspath(os.path.dirname(__file__)) + '/data/img/spacelab_transmitter_256x256.png'
_ICON_FILE_LINUX_SYSTEM         = '/usr/share/icons/spacelab_transmitter_256x256.png'

_LOGO_FILE_LOCAL                = os.path.abspath(os.path.dirname(__file__)) + '/data/img/spacelab-logo-full-400x200.png'
_LOGO_FILE_LINUX_SYSTEM         = '/usr/share/spacelab_transmitter/spacelab-logo-full-400x200.png' 

_DIR_CONFIG_LINUX               = '.config/spacelab_transmitter'
_DIR_CONFIG_WINDOWS             = 'spacelab_transmitter'

_SAT_JSON_LOCAL_PATH            = os.path.abspath(os.path.dirname(__file__)) + '/data/satellites/'
_SAT_JSON_SYSTEM_PATH           = '/usr/share/spacelab_decoder/'

_DEFAULT_CALLSIGN               = 'PP5UF'
_DEFAULT_LOCATION               = 'Florianópolis'
_DEFAULT_COUNTRY                = 'Brazil'
_DEFAULT_DOPPLER_ADDRESS        = '127.0.0.1'
_DEFAULT_DOPPLER_PORT           = 7356
_DEFAULT_FREQUENCY              = 437000000
_DEFAULT_SAMPLE_RATE            = 1000000
_DEFAULT_GAIN_USRP              = 40
_DEFAULT_GAIN_PLUTO             = -30

_DIR_CONFIG_DEFAULTJSON         = 'spacelab_transmitter.json'

# Defining logfile default local
_DIR_CONFIG_LOGFILE_LINUX       = 'spacelab_transmitter'
_DEFAULT_LOGFILE_PATH           = os.path.join(os.path.expanduser('~'), _DIR_CONFIG_LOGFILE_LINUX)
_DEFAULT_LOGFILE                = 'logfile.csv'

# Satellites
_SATELLITES                     = [["FloripaSat-1", "floripasat-1.json"],
                                   ["GOLDS-UFSC", "golds-ufsc.json"],
                                   ["Aldebaran-1", "aldebaran-1.json"],
                                   ["Catarina-A1", "catarina-a1.json"],
                                   ["Catarina-A2", "catarina-a2.json"]]

# Modulations
_MODULATION_GMSK                = "GMSK"

# Protocols
_PROTOCOL_NGHAM                 = "NGHam"
_PROTOCOL_AX100MODE5            = "AX100-Mode5"

# Available telecommands
_TELECOMMANDS                   = ["ping", "data_request", "broadcast_msg", "enter_hibernation",
                                   "leave_hibernation", "activate_module", "deactivate_module",
                                   "activate_payload", "deactivate_payload", "erase_memory", "force_reset",
                                   "get_payload_data", "set_param", "get_param", "transmit_pkt", "update_tle",
                                   "csp_services"]

# SDRs
_SDR_MODELS                     = ['USRP', 'Pluto SDR']

_CSP_MY_ADDRESS                 = 10

class DialogPassword(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Authentication", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Key:")
        self.entry_password = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_password, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

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

        self._client_socket = None

        self.builder.connect_signals(self)

        self._build_widgets()
        self.write_log("SpaceLab Transmitter initialized!")
        self._load_preferences()
        self._active_tcs = list()

    def _build_widgets(self):
        # Main window
        self.window = self.builder.get_object("window_main")
        if os.path.isfile(_ICON_FILE_LOCAL):
            self.window.set_icon_from_file(_ICON_FILE_LOCAL)
        else:
            self.window.set_icon_from_file(_ICON_FILE_LINUX_SYSTEM)
        self.window.set_wmclass(self.window.get_title(), self.window.get_title())
        self.window.connect("destroy", self.on_main_window_destroy)

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

        # SDR Parameters
        self.liststore_sdr = self.builder.get_object("liststore_sdr_devices")
        for sat in _SDR_MODELS:
            self.liststore_sdr.append([sat])
        self.combobox_sdr = self.builder.get_object("combobox_sdr")
        cell = Gtk.CellRendererText()
        self.combobox_sdr.pack_start(cell, True)
        self.combobox_sdr.add_attribute(cell, "text", 0)
        self.combobox_sdr.connect("changed", self.on_combobox_sdr_changed)
        self.entry_carrier_frequency = self.builder.get_object("entry_carrier_frequency")
        self.entry_sample_rate = self.builder.get_object("entry_sample_rate")
        self.spinbutton_tx_gain = self.builder.get_object("spinbutton_tx_gain")

        # Satellite combobox
        self.liststore_satellite = self.builder.get_object("liststore_satellite")
        for sat in _SATELLITES:
            self.liststore_satellite.append([sat[0]])
        self.combobox_satellite = self.builder.get_object("combobox_satellite")
        cell = Gtk.CellRendererText()
        self.combobox_satellite.pack_start(cell, True)
        self.combobox_satellite.add_attribute(cell, "text", 0)
        self.combobox_satellite.connect("changed", self.on_combobox_satellite_changed)

        # Packet type combobox
        self.liststore_packet_type = self.builder.get_object("liststore_packet_type")
        self.combobox_packet_type = self.builder.get_object("combobox_packet_type")
        self.combobox_packet_type.pack_start(cell, True)
        self.combobox_packet_type.add_attribute(cell, "text", 0)

        # TCP socket
        self.entry_tcp_address = self.builder.get_object("entry_tcp_address")
        self.entry_tcp_port = self.builder.get_object("entry_tcp_port")
        self.button_tcp_connect = self.builder.get_object("button_tcp_connect")
        self.button_tcp_connect.connect("clicked", self.on_button_tcp_connect_clicked)
        self.button_tcp_disconnect = self.builder.get_object("button_tcp_disconnect")
        self.button_tcp_disconnect.connect("clicked", self.on_button_tcp_disconnect_clicked)

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

        self.radiobutton_doppler_tle_file = self.builder.get_object("radiobutton_doppler_tle_file")
        self.filechooser_doppler_tle_file = self.builder.get_object("filechooser_doppler_tle_file")
        self.radiobutton_doppler_network = self.builder.get_object("radiobutton_doppler_network")
        self.entry_doppler_address = self.builder.get_object("entry_doppler_address")
        self.entry_doppler_port = self.builder.get_object("entry_doppler_port")

        self.logfile_chooser_button = self.builder.get_object("logfile_chooser_button")
        self.logfile_chooser_button.set_filename(_DEFAULT_LOGFILE_PATH)

        # Ping Request
        self.button_ping_request = self.builder.get_object("button_ping_request")
        self.button_ping_request.connect("clicked", self.on_button_ping_request_command_clicked)

        # Broadcast Message
        self.button_broadcast_message = self.builder.get_object("button_broadcast_message")
        self.button_broadcast_message.connect("clicked", self.on_button_broadcast_message_clicked)

        # Force Reset
        self.button_force_reset = self.builder.get_object("button_force_reset")
        self.button_force_reset.connect("clicked", self.on_button_force_reset_clicked)
        
        # Erase Memory
        self.button_erase_memory = self.builder.get_object("button_erase_memory")
        self.button_erase_memory.connect("clicked", self.on_button_erase_memory_clicked)
        
        # Enter Hibernation
        self.button_enter_hibernation = self.builder.get_object("button_enter_hibernation")
        self.button_enter_hibernation.connect("clicked", self.on_button_enter_hibernation_clicked)

        # Leave Hibernation
        self.button_leave_hibernation = self.builder.get_object("button_leave_hibernation")
        self.button_leave_hibernation.connect("clicked", self.on_button_leave_hibernation_clicked)

        # Activate Module
        self.button_activate_module = self.builder.get_object("button_activate_module")
        self.button_activate_module.connect("clicked", self.on_button_activate_module_clicked)
    
        # Deactivate Module
        self.button_deactivate_module = self.builder.get_object("button_deactivate_module")
        self.button_deactivate_module.connect("clicked", self.on_button_deactivate_module_clicked)

        # Activate Payload
        self.button_activate_payload = self.builder.get_object("button_activate_payload")
        self.button_activate_payload.connect("clicked", self.on_button_activate_payload_clicked)

        # Deactivate Payload
        self.button_deactivate_payload = self.builder.get_object("button_deactivate_payload")
        self.button_deactivate_payload.connect("clicked", self.on_button_deactivate_payload_clicked)

        # Get Parameter
        self.button_get_parameter = self.builder.get_object("button_get_parameter")
        self.button_get_parameter.connect("clicked", self.on_button_get_parameter_clicked)

        # Get Payload Data
        self.button_get_payload_data = self.builder.get_object("button_get_payload_data")
        self.button_get_payload_data.connect("clicked", self.on_button_get_payload_data_clicked)

        # Set Parameter
        self.button_set_parameter = self.builder.get_object("button_set_parameter")
        self.button_set_parameter.connect("clicked", self.on_button_set_parameter_clicked)

        # Data Request
        self.button_data_request = self.builder.get_object("button_data_request")
        self.button_data_request.connect("clicked", self.on_button_data_request_clicked)

        # Transmit Packet
        self.button_tx_pkt = self.builder.get_object("button_tx_pkt")
        self.button_tx_pkt.connect("clicked", self.on_button_tx_pkt_clicked)

        # Update TLE
        self.button_update_tle = self.builder.get_object("button_update_tle")
        self.button_update_tle.connect("clicked", self.on_button_update_tle_clicked)

        # CSP Services
        self.button_csp_services = self.builder.get_object("button_csp_services")
        self.button_csp_services.connect("clicked", self.on_button_csp_services_clicked)
        self.dialog_csp_services = self.builder.get_object("dialog_csp_services")
        self.button_csp_ping = self.builder.get_object("button_csp_ping")
        self.button_csp_ping.connect("clicked", self.on_button_csp_ping_clicked)
        self.button_csp_ps = self.builder.get_object("button_csp_ps")
        self.button_csp_ps.connect("clicked", self.on_button_csp_ps_clicked)
        self.button_csp_memfree = self.builder.get_object("button_csp_memfree")
        self.button_csp_memfree.connect("clicked", self.on_button_csp_memfree_clicked)
        self.button_csp_bufferfree = self.builder.get_object("button_csp_bufferfree")
        self.button_csp_bufferfree.connect("clicked", self.on_button_csp_bufferfree_clicked)
        self.button_csp_uptime = self.builder.get_object("button_csp_uptime")
        self.button_csp_uptime.connect("clicked", self.on_button_csp_uptime_clicked)
        self.button_csp_cmp_ident = self.builder.get_object("button_csp_cmp_ident")
        self.button_csp_cmp_ident.connect("clicked", self.on_button_csp_cmp_ident_clicked)
        self.button_csp_route_set = self.builder.get_object("button_csp_route_set")
        self.button_csp_route_set.connect("clicked", self.on_button_csp_route_set_clicked)
        self.button_csp_cmp_if_stat = self.builder.get_object("button_csp_cmp_if_stat")
        self.button_csp_cmp_if_stat.connect("clicked", self.on_button_csp_cmp_if_stat_clicked)
        self.button_csp_cmp_peek = self.builder.get_object("button_csp_cmp_peek")
        self.button_csp_cmp_peek.connect("clicked", self.on_button_csp_cmp_peek_clicked)
        self.button_csp_cmp_poke = self.builder.get_object("button_csp_cmp_poke")
        self.button_csp_cmp_poke.connect("clicked", self.on_button_csp_cmp_poke_clicked)
        self.button_csp_cmp_clock = self.builder.get_object("button_csp_cmp_clock")
        self.button_csp_cmp_clock.connect("clicked", self.on_button_csp_cmp_clock_clicked)
        self.button_csp_reboot = self.builder.get_object("button_csp_reboot")
        self.button_csp_reboot.connect("clicked", self.on_button_csp_reboot_clicked)
        self.button_csp_shutdown = self.builder.get_object("button_csp_shutdown")
        self.button_csp_shutdown.connect("clicked", self.on_button_csp_shutdown_clicked)

    def run(self):
        self.window.show_all()          
        Gtk.main()

    def on_main_window_destroy(self, window):
        self._save_preferences()

        if self._client_socket:
            self._client_socket.close()

        Gtk.main_quit()

    def on_button_ping_request_command_clicked(self, button):
        callsign = self.entry_preferences_general_callsign.get_text()
        fr = Ping()
        pl = fr.generate(callsign)
        self._transmit_tc(pl, "Ping")

    def on_button_enter_hibernation_clicked(self, button):
        dialog = DialogEnterHibernation(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_hours() <= 0 or dialog.get_hours() > 2**16-1:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = Enter_hibernation()
                    pl = fr.generate(callsign, dialog.get_hours(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Enter Hibernation")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Enter Hibernation\" telecommand!")
                error_dialog.format_secondary_text("The hibernation duration must be greater than zero and lesser than 65536!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_ac_mod_id() < 0 or dialog.get_ac_mod_id() > 255:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = ActivateModule()
                    pl = fr.generate(callsign, dialog.get_ac_mod_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Activate Module")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Activate Module\" telecommand!")
                error_dialog.format_secondary_text("The module ID must be between 0 and 255!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_deac_mod_id() < 0 or dialog.get_deac_mod_id() > 255:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = DeactivateModule()
                    pl = fr.generate(callsign, dialog.get_deac_mod_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Deactivate Module")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Deactivate Module\" telecommand!")
                error_dialog.format_secondary_text("The module ID must be between 0 and 255!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_deac_pl_id() < 0 or dialog.get_deac_pl_id() > 255:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = DeactivatePayload()
                    pl = fr.generate(callsign, dialog.get_deac_pl_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Deactivate Payload")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Deactivate Payload\" telecommand!")
                error_dialog.format_secondary_text("The payload ID must be between 0 and 255!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_ac_pl_id() < 0 or dialog.get_ac_pl_id() > 255:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = ActivatePayload()
                    pl = fr.generate(callsign, dialog.get_ac_pl_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Activate Payload")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Activate Module\" telecommand!")
                error_dialog.format_secondary_text("The payload ID must be between 0 and 255!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_erase_memory_clicked(self, button):
        dialog = DialogEraseMemory(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_mem_id() < 0 or dialog.get_mem_id() > 255:
                    raise ValueError()

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = EraseMemory()
                    pl = fr.generate(callsign, dialog.get_mem_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Erase Memory")
                    dialog_pw.destroy()
                    dialog.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Erase Memory\" telecommand!")
                error_dialog.format_secondary_text("The memory ID must be between 0 and 255!")
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_subsys_id() < 0 or dialog.get_subsys_id() > 255:
                    raise ValueError("The subsystem ID must be between 0 and 255!")

                if dialog.get_param_id() < 0 or dialog.get_param_id() > 255:
                    raise ValueError("The parameter ID must be between 0 and 255!")

                if dialog.get_param_val() < 0 or dialog.get_param_val() > 2**32-1:
                    raise ValueError("The payload value must be between 0 and 4294967295!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = SetParameter()
                    pl = fr.generate(callsign, dialog.get_subsys_id(), dialog.get_param_id(), dialog.get_param_val(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Set Parameter")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Set Parameter\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_data_id() < 0 or dialog.get_data_id() > 255:
                    raise ValueError("The data ID must be between 0 and 255!")

                if dialog.get_start_ts() < 0 or dialog.get_start_ts() > 2**32-1:
                    raise ValueError("The start timestamp must be between 0 and 4294967295!")

                if dialog.get_end_ts() < 0 or dialog.get_end_ts() > 2**32-1:
                    raise ValueError("The end timestamp must be between 0 and 4294967295!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = DataRequest()
                    pl = fr.generate(callsign, dialog.get_data_id(), dialog.get_start_ts(), dialog.get_end_ts(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Data Request")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Data Request\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            pl = fr.generate(callsign, dialog.get_key())
            self._transmit_tc(pl, "Leave Hibernation")
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_force_reset_clicked(self, button):
        dialog = DialogPassword(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            callsign = self.entry_preferences_general_callsign.get_text()
            fr = ForceReset()
            pl = fr.generate(callsign, dialog.get_key())
            self._transmit_tc(pl, "Force Reset")
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_get_parameter_clicked(self, button):
        dialog = DialogGetParameter(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_subsys_id() < 0 or dialog.get_subsys_id() > 255:
                    raise ValueError("The subsystem ID must be between 0 and 255!")

                if dialog.get_param_id() < 0 or dialog.get_param_id() > 255:
                    raise ValueError("The parameter ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = GetParameter()
                    pl = fr.generate(callsign, dialog.get_subsys_id(), dialog.get_param_id(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Get Parameter")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Get Parameter\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
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
            try:
                if dialog.get_pl_id() < 0 or dialog.get_pl_id() > 255:
                    raise ValueError("The payload ID must be between 0 and 255!")

                if len(dialog.get_pl_args()) == 0:
                    raise ValueError("The payload arguments cannot be empty!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = GetPayloadData()
                    pl = fr.generate(callsign, dialog.get_pl_id(), dialog.get_pl_args(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Get Payload Data")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except (ValueError, SyntaxError) as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Get Payload\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_broadcast_message_clicked(self, button):
        dialog = DialogBroadcastMessage(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if len(dialog.get_dst_callsign()) == 0 or len(dialog.get_dst_callsign()) > 7:
                    raise ValueError("The destination callsign must be between 0 and 7 characters long!")

                if len(dialog.get_message()) == 0 or len(dialog.get_message()) > 38:
                    raise ValueError("The message must be between 0 and 38 characters long!")

                callsign = self.entry_preferences_general_callsign.get_text()
                fr = Broadcast()
                pl = fr.generate(callsign, dialog.get_dst_callsign(), dialog.get_message())
                self._transmit_tc(pl, "Broadcast Message")
                dialog.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Broadcast Message\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_tx_pkt_clicked(self, button):
        dialog = DialogTransmitPacket(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                callsign = self.entry_preferences_general_callsign.get_text()
                fr = TransmitPacket()
                pl = fr.generate(callsign, dialog.get_data())
                self._transmit_tc(pl, "Transmit Packet")
            except Exception as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Transmit Packet\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_update_tle_clicked(self, button):
        dialog = DialogUpdateTLE(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_tle_line_num() < 0 or dialog.get_tle_line_num() > 2:
                    raise ValueError("The TLE line number must be between 0 and 2!")

                if len(dialog.get_tle_line()) != 69:
                    raise ValueError("The TLE line must be 69 characters long!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    callsign = self.entry_preferences_general_callsign.get_text()
                    fr = UpdateTLE()
                    pl = fr.generate(callsign, dialog.get_tle_line_num(), dialog.get_tle_line(), dialog_pw.get_key())
                    self._transmit_tc(pl, "Update TLE")
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.CANCEL:
                    dialog_pw.destroy()
                elif response_key == Gtk.ResponseType.DELETE_EVENT:
                    dialog_pw.destroy()
                else:
                    dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Update TLE\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_csp_services_clicked(self, button):
        response = self.dialog_csp_services.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.dialog_csp_services.hide()

    def on_button_csp_ping_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_ping(1)    # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Ping")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Ping\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_ps_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_ps(1)  # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP PS")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP PS\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_memfree_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_memfree(1) # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Mem. Free")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Mem. Free\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_bufferfree_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_buf_free(1)    # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Buffer Free")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Buffer Free\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_uptime_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_uptime(1)  # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Uptime")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Uptime\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_cmp_ident_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_cmp_ident(1)   # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP CMP Ident")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Ident\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_route_set_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_cmp_set_route(1)   # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP CMP Route Set")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Route Set\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_cmp_if_stat_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_cmp_if_stat(1) # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP CMP IF Stat")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP IF Stat\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_cmp_peek_clicked(self, button):
        dialog = DialogCSPPeek(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_csp_mem_adr() < 0 or dialog.get_csp_mem_adr() > 2**32-1:
                    raise ValueError("The memory address must be between 0 and 4294967295!")

                if dialog.get_csp_mem_len() < 0 or dialog.get_csp_mem_len() > 2**32-1:
                    raise ValueError("The memory length must be between 0 and 4294967295!")

                csp = CSP(_CSP_MY_ADDRESS)
                csp_pkt = csp.encode_cmp_peek(1, dialog.get_csp_mem_adr(), dialog.get_csp_mem_len()) # 1 = Satellite (OBDH) address
                self._transmit_tc(csp_pkt, "CSP Peek")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Peek\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_csp_cmp_poke_clicked(self, button):
        dialog = DialogCSPPoke(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_csp_mem_adr() < 0 or dialog.get_csp_mem_adr() > 2**32-1:
                    raise ValueError("The memory address must be between 0 and 4294967295!")

                if dialog.get_csp_mem_len() < 0 or dialog.get_csp_mem_len() > 2**32-1:
                    raise ValueError("The memory length must be between 0 and 4294967295!")

                csp = CSP(_CSP_MY_ADDRESS)
                csp_pkt = csp.encode_cmp_poke(1, dialog.get_csp_mem_adr(), dialog.get_csp_mem_len()) # 1 = Satellite (OBDH) address
                self._transmit_tc(csp_pkt, "CSP Poke")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Poke\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
        elif response == Gtk.ResponseType.DELETE_EVENT:
            dialog.destroy()
        else:
            dialog.destroy()

    def on_button_csp_cmp_clock_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_cmp_get_clock(1)   # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP CMP Get Clock")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Get Clock\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_reboot_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_reboot(1)  # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Reboot")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Reboot\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_shutdown_clicked(self, button):
        try:
            csp = CSP(_CSP_MY_ADDRESS)
            csp_pkt = csp.encode_shutdown(1)    # 1 = Satellite (OBDH) address
            self._transmit_tc(csp_pkt, "CSP Shutdown")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Shutdown\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def _transmit_tc(self, pkt, tc_name):
        carrier_frequency = self.entry_carrier_frequency.get_text()
        tx_gain = self.spinbutton_tx_gain.get_text()
        callsign = self.entry_preferences_general_callsign.get_text()

        mod_name, freq, baud, sync, prot_name = self._get_link_info()

        prot = None
        if prot_name == _PROTOCOL_NGHAM:
            prot = PyNGHam()
        elif prot_name == _PROTOCOL_AX100MODE5:
            prot = AX100Mode5()
        else:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a" + tc_name + "telecommand!")
            error_dialog.format_secondary_text("The " + prot_name + " protocol is not supported yet!")
            error_dialog.run()
            error_dialog.destroy()

            return

        enc_pkt = prot.encode(pkt)

        if self.button_tcp_connect.get_sensitive():
            mod = None
            if mod_name == _MODULATION_GMSK:
                mod = GMSK(0.5, baud)   # BT = 0.5
            else:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a" + tc_name + "telecommand!")
                error_dialog.format_secondary_text("The" + mod_name + "modulation is not supported yet!")
                error_dialog.run()
                error_dialog.destroy()

                return

            samples, sample_rate, duration_s = mod.modulate(enc_pkt, 1000)

            sdr = None
            if self.combobox_sdr.get_active() == 0:   # USRP
                sdr = USRP(int(self.entry_sample_rate.get_text()), int(tx_gain))
            elif self.combobox_sdr.get_active() == 1: # Pluto SDR
                sdr = Pluto(int(self.entry_sample_rate.get_text()), int(tx_gain))
            else:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a" + tc_name + "telecommand!")
                error_dialog.format_secondary_text("SDR device not supported yet!")
                error_dialog.run()
                error_dialog.destroy()

                return

            if sdr.transmit(samples, duration_s, sample_rate, int(carrier_frequency)):
                self.write_log(tc_name + " transmitted to " + _SATELLITES[self.combobox_satellite.get_active()][0] + " from" + callsign + " in " + carrier_frequency + " Hz with a gain of " + tx_gain + " dB")
            else:
                self.write_log("Error transmitting a " + tc_name + " telecommand!")
        else:
            if self._client_socket:
                try:
                    self._client_socket.send(bytearray(enc_pkt))  # Send message to server
                    self.write_log(tc_name + " transmitted to " + _SATELLITES[self.combobox_satellite.get_active()][0] + " from" + callsign + " via " + self.entry_tcp_address.get_text() + ":" + self.entry_tcp_port.get_text())
                except socket.error as e:
                    error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a" + tc_name + "telecommand!")
                    error_dialog.format_secondary_text(str(e))
                    error_dialog.run()
                    error_dialog.destroy()

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

        try:
            self.entry_preferences_general_callsign.set_text(config["callsign"])
            self.entry_preferences_general_location.set_text(config["location"])
            self.entry_preferences_general_country.set_text(config["country"])
            if config["doppler_from_network"]:
                self.radiobutton_doppler_network.set_active(True)
            else:
                self.radiobutton_doppler_tle_file.set_active(True)
            self.filechooser_doppler_tle_file.set_filename(config["tle_file"] if config["tle_file"] != None else "")
            self.entry_doppler_address.set_text(config["doppler_address"])
            self.entry_doppler_port.set_text(config["doppler_port"])
            self.logfile_chooser_button.set_filename(config["logfile_path"])
            self.combobox_sdr.set_active(config["sdr_dev"])
            self.entry_carrier_frequency.set_text(config["sdr_freq"])
            self.entry_sample_rate.set_text(config["sdr_sample_rate"])
        except:
            self._load_default_preferences()
            self._save_preferences()

    def _load_default_preferences(self):
        self.entry_preferences_general_callsign.set_text(_DEFAULT_CALLSIGN)
        self.entry_preferences_general_location.set_text(_DEFAULT_LOCATION)
        self.entry_preferences_general_country.set_text(_DEFAULT_COUNTRY)

        self.filechooser_doppler_tle_file.set_filename("")
        self.radiobutton_doppler_network.set_active(True)
        self.entry_doppler_address.set_text(_DEFAULT_DOPPLER_ADDRESS)
        self.entry_doppler_port.set_text(str(_DEFAULT_DOPPLER_PORT))

        self.logfile_chooser_button.set_filename(_DEFAULT_LOGFILE_PATH)

        self.combobox_sdr.set_active(-1)
        self.entry_carrier_frequency.set_text(str(_DEFAULT_FREQUENCY))
        self.entry_sample_rate.set_text(str(_DEFAULT_SAMPLE_RATE))

    def _save_preferences(self):
        home = os.path.expanduser('~')
        location = os.path.join(home, _DIR_CONFIG_LINUX)

        if not os.path.exists(location):
            os.mkdir(location)

        with open(location + '/' + _DIR_CONFIG_DEFAULTJSON, 'w', encoding='utf-8') as f:
            json.dump({"callsign": self.entry_preferences_general_callsign.get_text(),
                       "location": self.entry_preferences_general_location.get_text(),
                       "country": self.entry_preferences_general_country.get_text(),
                       "doppler_from_network": self.radiobutton_doppler_network.get_active(),
                       "tle_file": self.filechooser_doppler_tle_file.get_filename(),
                       "doppler_address": self.entry_doppler_address.get_text(),
                       "doppler_port": self.entry_doppler_port.get_text(),
                       "logfile_path": self.logfile_chooser_button.get_filename(),
                       "sdr_dev": self.combobox_sdr.get_active(),
                       "sdr_freq": self.entry_carrier_frequency.get_text(),
                       "sdr_sample_rate": self.entry_sample_rate.get_text()}, f, ensure_ascii=False, indent=4)

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
            self._update_tc_buttons(False)
        elif self.switch_button.get_active() == True:
            self._update_tc_buttons(True)

    def _update_tc_buttons(self, state):
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
        self.button_update_tle.set_sensitive(False)
        self.button_tx_pkt.set_sensitive(False)
        self.button_csp_services.set_sensitive(False)
        self.button_csp_ping.set_sensitive(False)
        self.button_csp_ps.set_sensitive(False)
        self.button_csp_memfree.set_sensitive(False)
        self.button_csp_bufferfree.set_sensitive(False)
        self.button_csp_uptime.set_sensitive(False)
        self.button_csp_cmp_ident.set_sensitive(False)
        self.button_csp_route_set.set_sensitive(False)
        self.button_csp_cmp_if_stat.set_sensitive(False)
        self.button_csp_cmp_peek.set_sensitive(False)
        self.button_csp_cmp_poke.set_sensitive(False)
        self.button_csp_cmp_clock.set_sensitive(False)
        self.button_csp_reboot.set_sensitive(False)
        self.button_csp_shutdown.set_sensitive(False)

        if "ping" in self._active_tcs: self.button_ping_request.set_sensitive(state)
        if "enter_hibernation" in self._active_tcs: self.button_enter_hibernation.set_sensitive(state)
        if "deactivate_module" in self._active_tcs: self.button_deactivate_module.set_sensitive(state)
        if "erase_memory" in self._active_tcs: self.button_erase_memory.set_sensitive(state)
        if "set_param" in self._active_tcs: self.button_set_parameter.set_sensitive(state)
        if "data_request" in self._active_tcs: self.button_data_request.set_sensitive(state)
        if "leave_hibernation" in self._active_tcs: self.button_leave_hibernation.set_sensitive(state)
        if "activate_payload" in self._active_tcs: self.button_activate_payload.set_sensitive(state)
        if "force_reset" in self._active_tcs: self.button_force_reset.set_sensitive(state)
        if "get_param" in self._active_tcs: self.button_get_parameter.set_sensitive(state)
        if "broadcast_msg" in self._active_tcs: self.button_broadcast_message.set_sensitive(state)
        if "activate_module" in self._active_tcs: self.button_activate_module.set_sensitive(state)
        if "deactivate_payload" in self._active_tcs: self.button_deactivate_payload.set_sensitive(state)
        if "get_payload_data" in self._active_tcs: self.button_get_payload_data.set_sensitive(state)
        if "update_tle" in self._active_tcs: self.button_update_tle.set_sensitive(state)
        if "transmit_pkt" in self._active_tcs: self.button_tx_pkt.set_sensitive(state)
        if "csp_services" in self._active_tcs:
            self.button_csp_services.set_sensitive(state)
            self.button_csp_ping.set_sensitive(state)
            self.button_csp_ps.set_sensitive(state)
            self.button_csp_memfree.set_sensitive(state)
            self.button_csp_bufferfree.set_sensitive(state)
            self.button_csp_uptime.set_sensitive(state)
            self.button_csp_cmp_ident.set_sensitive(state)
            self.button_csp_route_set.set_sensitive(state)
            self.button_csp_cmp_if_stat.set_sensitive(state)
            self.button_csp_cmp_peek.set_sensitive(state)
            self.button_csp_cmp_poke.set_sensitive(state)
            self.button_csp_cmp_clock.set_sensitive(state)
            self.button_csp_reboot.set_sensitive(state)
            self.button_csp_shutdown.set_sensitive(state)

    def on_combobox_satellite_changed(self, combobox):
        # Clear the list of packet types
        self.liststore_packet_type.clear()

        sat_filename = _SATELLITES[self.combobox_satellite.get_active()][1]
        sat_config_file = str()

        if os.path.isfile(_SAT_JSON_LOCAL_PATH + sat_filename):
            sat_config_file = _SAT_JSON_LOCAL_PATH + sat_filename
        else:
            sat_config_file = _SAT_JSON_SYSTEM_PATH + sat_filename

        try:
            with open(sat_config_file) as f:
                sat_info = json.load(f)

                if 'links' in sat_info:
                    for i in range(len(sat_info['links'])):
                        self.liststore_packet_type.append([sat_info['links'][i]['name']])
                else:
                    self.liststore_packet_type.append(['Uplink'])

            self._active_tcs = list()
            if 'telecommands' in sat_info:
                for tc in sat_info["telecommands"]:
                    for tc_avail in _TELECOMMANDS:
                        if tc == tc_avail:
                            self._active_tcs.append(tc)
            else:
                self._active_tcs = _TELECOMMANDS.copy()

            if self.switch_button.get_active() == False:
                self._update_tc_buttons(False)
            elif self.switch_button.get_active() == True:
                self._update_tc_buttons(True)

            modulation, frequency, baudrate, sync_word, protocol = self._get_link_info()
            self.entry_carrier_frequency.set_text(str(int(frequency)))
        except FileNotFoundError as e:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error opening the satellite configuration file!")
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()

            self.combobox_packet_type.set_active(-1)
        except:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error opening the satellite configuration file!")
            error_dialog.format_secondary_text("Is the configuration file correct?")
            error_dialog.run()
            error_dialog.destroy()
        else:
            # Sets the first packet type as the active packet type
            self.combobox_packet_type.set_active(0)

    def on_combobox_sdr_changed(self, combobox):
        if self.combobox_sdr.get_active() == 0:   # USRP
            self.spinbutton_tx_gain.set_range(0, 90)
            self.spinbutton_tx_gain.set_value(_DEFAULT_GAIN_USRP)
        elif self.combobox_sdr.get_active() == 1: # Pluto SDR
            self.spinbutton_tx_gain.set_range(-90, 0)
            self.spinbutton_tx_gain.set_value(_DEFAULT_GAIN_PLUTO)
        else:
            self.spinbutton_tx_gain.set_range(0, 90)
            self.spinbutton_tx_gain.set_value(_DEFAULT_GAIN_USRP)

    def on_button_tcp_connect_clicked(self, button):
        try:
            adr = self.entry_tcp_address.get_text()
            port = int(self.entry_tcp_port.get_text())
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect((adr, port))
            self.write_log("Connected to " + adr + ":" + str(port))

            self.combobox_sdr.set_sensitive(False)
            self.entry_carrier_frequency.set_sensitive(False)
            self.entry_sample_rate.set_sensitive(False)
            self.spinbutton_tx_gain.set_sensitive(False)
            self.entry_tcp_address.set_sensitive(False)
            self.entry_tcp_port.set_sensitive(False)
            self.button_tcp_connect.set_sensitive(False)
            self.button_tcp_disconnect.set_sensitive(True)
        except socket.error as e:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error connecting to server!")
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_tcp_disconnect_clicked(self, button):
        self._client_socket.shutdown(socket.SHUT_RDWR)
        self._client_socket.close()

        self.write_log("Disconnected from " + self.entry_tcp_address.get_text() + ":" + self.entry_tcp_port.get_text())

        self.combobox_sdr.set_sensitive(True)
        self.entry_carrier_frequency.set_sensitive(True)
        self.entry_sample_rate.set_sensitive(True)
        self.spinbutton_tx_gain.set_sensitive(True)
        self.entry_tcp_address.set_sensitive(True)
        self.entry_tcp_port.set_sensitive(True)
        self.button_tcp_connect.set_sensitive(True)
        self.button_tcp_disconnect.set_sensitive(False)

    def _get_link_info(self):
        sat_config_file = str()

        for i in range(len(_SATELLITES)):
            if self.combobox_satellite.get_active() == i:
                if os.path.isfile(_SAT_JSON_LOCAL_PATH + _SATELLITES[i][1]):
                    sat_config_file = _SAT_JSON_LOCAL_PATH + _SATELLITES[i][1]
                else:
                    sat_config_file = _SAT_JSON_SYSTEM_PATH + _SATELLITES[i][1]

        with open(sat_config_file) as f:
            sat_info = json.load(f)
            modulation  = sat_info['modulation']
            frequency   = sat_info['frequency']
            baudrate    = sat_info['baudrate']
            sync_word   = sat_info['sync_word']
            protocol    = sat_info['protocol']

            return modulation, frequency, baudrate, sync_word, protocol
