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
from datetime import datetime
import json
import socket
import time
import struct

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib

import spacelab_transmitter.version

from spacelab_transmitter.tc_dialogs import DialogDataRequest, DialogDeactivatePayload, DialogEnterHibernation, DialogActivatePayload, DialogGetPayloadData, DialogSetParameter, DialogDeactivateModule, DialogActivateModule, DialogGetParameter, DialogBroadcastMessage, DialogTransmitPacket, DialogEraseMemory, DialogUpdateTLE, DialogCSPPeek, DialogCSPPoke, DialogCSPIFStat, DialogCSPRouteSet, DialogScheduleTC, DialogPassword

from spacelab_transmitter.gmsk import GMSK
from spacelab_transmitter.usrp import USRP
from spacelab_transmitter.pluto import Pluto
from spacelab_transmitter.csp import CSP, CSP_PRIO_NORM
from spacelab_transmitter.ax100 import AX100Mode5
from spacelab_transmitter.satellite import Satellite
from spacelab_transmitter.link import Link
from spacelab_transmitter.slp import SLP
from spacelab_transmitter.dopplershift import DopplerShift
from spacelab_transmitter.log import Log

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
_DEFAULT_LATITUDE               = '-27.600719'
_DEFAULT_LONGITUDE              = '-48.517392'
_DEFAULT_ALTITUDE               = '15'
_DEFAULT_CSP_MY_ADDRESS         = 10
_DEFAULT_CSP_DST_ADDRESS        = 1
_DEFAULT_DOPPLER_ADDRESS        = '127.0.0.1'
_DEFAULT_DOPPLER_PORT           = 7356
_DEFAULT_FREQUENCY              = 437000000
_DEFAULT_FREQ_OFFSET            = 0
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
                                   ["Catarina-A1", "catarina-a1.json"],
                                   ["Catarina-A2", "catarina-a2.json"]]

# Modulations
_MODULATION_GMSK                = "GMSK"

# Protocols
_PROTOCOL_SLP                   = "SLP"
_PROTOCOL_CSP                   = "CSP"
_PROTOCOL_NGHAM                 = "NGHam"
_PROTOCOL_AX100MODE5            = "AX100-Mode5"

# Available telecommands
_TELECOMMANDS                   = ["ping", "data_request", "broadcast_msg", "enter_hibernation",
                                   "leave_hibernation", "activate_module", "deactivate_module",
                                   "activate_payload", "deactivate_payload", "erase_memory", "force_reset",
                                   "get_payload_data", "set_param", "get_param", "transmit_pkt", "update_tle",
                                   "time_sync", "csp_services"]

# SDRs
_SDR_MODELS                     = ['USRP', 'Pluto SDR']

# SLP IDs
SLP_ID_PING                     = 0x40
SLP_ID_DATA_REQUEST             = 0x41
SLP_ID_BROADCAST_MESSAGE        = 0x42
SLP_ID_ENTER_HIBERNATION        = 0x43
SLP_ID_LEAVE_HIBERNATION        = 0x44
SLP_ID_ACTIVATE_MODULE          = 0x45
SLP_ID_DEACTIVATE_MODULE        = 0x46
SLP_ID_ACTIVATE_PAYLOAD         = 0x47
SLP_ID_DEACTIVATE_PAYLOAD       = 0x48
SLP_ID_ERASE_MEMORY             = 0x49
SLP_ID_FORCE_RESET              = 0x4A
SLP_ID_GET_PAYLOAD_DATA         = 0x4B
SLP_ID_SET_PARAMETER            = 0x4C
SLP_ID_GET_PARAMETER            = 0x4D
SLP_ID_TRANSMIT_PACKET          = 0x4E
SLP_ID_UPDATE_TLE               = 0x4F
SLP_ID_SCHEDULE_TC              = 0x50

# CSP Ports
CSP_PORT_DATA_REQUEST           = 35
CSP_PORT_UPDATE_TLE             = 37
CSP_PORT_BROADCAST_MSG          = 39
CSP_PORT_ENTER_HIBERNATION      = 40
CSP_PORT_LEAVE_HIBERNATION      = 41
CSP_PORT_ERASE_MEMORY           = 43
CSP_PORT_FORCE_RESET            = 44
CSP_PORT_GET_PAYLOAD_DATA       = 45
CSP_PORT_SET_PARAM              = 46
CSP_PORT_GET_PARAM              = 47
CSP_PORT_TIME_SYNC              = 48

class SpaceLabTransmitter:

    def __init__(self):
        self.builder = Gtk.Builder()
        # UI file from Glade
        if os.path.isfile(_UI_FILE_LOCAL):
            self.builder.add_from_file(_UI_FILE_LOCAL)
        else:
            self.builder.add_from_file(_UI_FILE_LINUX_SYSTEM)

        self._satellite = Satellite()

        self._client_socket = None
        self._tcp_cb_id = None

        self.builder.connect_signals(self)

        self._build_widgets()
        self._log = Log(_DEFAULT_LOGFILE, _DEFAULT_LOGFILE_PATH)
        self.write_log("SpaceLab Transmitter initialized!")
        self._load_preferences()

    def _build_widgets(self):
        # Main window
        self.window = self.builder.get_object("window_main")
        if os.path.isfile(_ICON_FILE_LOCAL):
            self.window.set_icon_from_file(_ICON_FILE_LOCAL)
        else:
            self.window.set_icon_from_file(_ICON_FILE_LINUX_SYSTEM)
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
        self.entry_sdr_freq_offset = self.builder.get_object("entry_sdr_freq_offset")
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

        # Link type combobox
        self.liststore_link = self.builder.get_object("liststore_link")
        self.combobox_link = self.builder.get_object("combobox_link")
        self.combobox_link.pack_start(cell, True)
        self.combobox_link.add_attribute(cell, "text", 0)
        self.combobox_link.connect("changed", self.on_combobox_link_changed)

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
        self.entry_preferences_general_latitude = self.builder.get_object("entry_preferences_general_latitude")
        self.entry_preferences_general_longitude = self.builder.get_object("entry_preferences_general_longitude")
        self.entry_preferences_general_altitude = self.builder.get_object("entry_preferences_general_altitude")

        self.entry_preferences_protocols_csp_my_adr = self.builder.get_object("entry_preferences_protocols_csp_my_adr")
        self.entry_preferences_protocols_csp_dst_adr = self.builder.get_object("entry_preferences_protocols_csp_dst_adr")
        self.switch_preferences_protocols_csp_hmac = self.builder.get_object("switch_preferences_protocols_csp_hmac")

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

        # Time Sync
        self.button_time_sync = self.builder.get_object("button_time_sync")
        self.button_time_sync.connect("clicked", self.on_button_time_sync_clicked)

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
        self.button_csp_cmp_set_clock = self.builder.get_object("button_csp_cmp_set_clock")
        self.button_csp_cmp_set_clock.connect("clicked", self.on_button_csp_cmp_set_clock_clicked)
        self.button_csp_cmp_get_clock = self.builder.get_object("button_csp_cmp_get_clock")
        self.button_csp_cmp_get_clock.connect("clicked", self.on_button_csp_cmp_get_clock_clicked)
        self.button_csp_reboot = self.builder.get_object("button_csp_reboot")
        self.button_csp_reboot.connect("clicked", self.on_button_csp_reboot_clicked)
        self.button_csp_shutdown = self.builder.get_object("button_csp_shutdown")
        self.button_csp_shutdown.connect("clicked", self.on_button_csp_shutdown_clicked)

        # Schedule TC
        self.button_schedule_tc = self.builder.get_object("button_schedule_tc")
        self.button_schedule_tc.connect("clicked", self.on_button_schedule_tc_clicked)

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_main_window_destroy(self, window):
        if self._client_socket:
            self._client_socket.close()

        Gtk.main_quit()

    def on_button_ping_request_command_clicked(self, button):
        pkt = list()
        if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
            slp = SLP()
            pkt = slp.encode(SLP_ID_PING, self.entry_preferences_general_callsign.get_text(), list())
        self._transmit_tc(pkt, "Ping")

    def on_button_enter_hibernation_clicked(self, button):
        dialog = DialogEnterHibernation(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                hbn_hours = dialog.get_hours()
                if hbn_hours <= 0 or hbn_hours > 2**16-1:
                    raise ValueError("The hibernation duration must be greater than zero and lesser than 65536!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        pl = struct.pack('>H', hbn_hours)
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_ENTER_HIBERNATION, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                        pl = struct.pack('>I', hbn_hours)
                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                        pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_ENTER_HIBERNATION, CSP_PORT_ENTER_HIBERNATION, False, True, False, False, False, pl, dialog_pw.get_key())
                    self._transmit_tc(pkt, "Enter Hibernation")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Enter Hibernation\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_activate_module_clicked(self, button):
        dialog = DialogActivateModule(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                mod_id = dialog.get_ac_mod_id()
                if mod_id < 0 or mod_id > 255:
                    raise ValueError("The module ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_ACTIVATE_MODULE, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), [mod_id])
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Activate Module")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Activate Module\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_deactivate_module_clicked(self, button):
        dialog = DialogDeactivateModule(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                mod_id = dialog.get_deac_mod_id()
                if mod_id < 0 or mod_id > 255:
                    raise ValueError("The module ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_DEACTIVATE_MODULE, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), [mod_id])
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Deactivate Module")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Deactivate Module\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_deactivate_payload_clicked(self, button):
        dialog = DialogDeactivatePayload(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                pl_id = dialog.get_deac_pl_id()
                if pl_id < 0 or pl_id > 255:
                    raise ValueError("The payload ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_DEACTIVATE_PAYLOAD, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), [pl_id])
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Deactivate Payload")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Deactivate Payload\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_activate_payload_clicked(self, button):
        dialog = DialogActivatePayload(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                pl_id = dialog.get_ac_pl_id()
                if pl_id < 0 or pl_id > 255:
                    raise ValueError("The payload ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_ACTIVATE_PAYLOAD, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), [pl_id])
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Activate Payload")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Activate Module\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_erase_memory_clicked(self, button):
        dialog = DialogEraseMemory(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                mem_id = dialog.get_mem_id()
                if mem_id < 0 or mem_id > 255:
                    raise ValueError("The memory ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_ERASE_MEMORY, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), [mem_id])
                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                        pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_ERASE_MEMORY, CSP_PORT_ERASE_MEMORY, False, True, False, False, False, [], dialog_pw.get_key())
                    self._transmit_tc(pkt, "Erase Memory")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Erase Memory\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_set_parameter_clicked(self, button):
        dialog = DialogSetParameter(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                subsys_id = dialog.get_subsys_id()
                param_id = dialog.get_param_id()
                param_type = dialog.get_param_type()
                param_val_str = dialog.get_param_val()
                if subsys_id < 0 or subsys_id > 255:
                    raise ValueError("The subsystem ID must be between 0 and 255!")

                if param_id < 0 or param_id > 255:
                    raise ValueError("The parameter ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pl = [subsys_id, param_id]

                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        param_val = int(param_val_str)
                        if param_val < 0 or param_val > 2**32-1:
                            raise ValueError("The parameter value must be between 0 and 4294967295!")

                        pl += list(struct.pack(">I", param_val))

                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_SET_PARAMETER, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                        if param_type == "bool":
                            param_val = int(param_val_str)
                            if param_val < 0 or param_val > 1:
                                raise ValueError("The parameter value must be 0 or 1!")
                            pl.append(1)
                            pl.append(param_val)
                        elif param_type == "uint8":
                            param_val = int(param_val_str)
                            if param_val < 0 or param_val > 2**8-1:
                                raise ValueError("The parameter value must be between 0 and 255!")
                            pl.append(1)
                            pl += list(struct.pack(">B", param_val))
                        elif param_type == "int8":
                            param_val = int(param_val_str)
                            if param_val < -128 or param_val > 127:
                                raise ValueError("The parameter value must be between -128 and 127!")
                            pl.append(1)
                            pl += list(struct.pack(">b", param_val))
                        elif param_type == "uint16":
                            param_val = int(param_val_str)
                            if param_val < 0 or param_val > 2**16-1:
                                raise ValueError("The parameter value must be between 0 and 65535!")
                            pl.append(2)
                            pl += list(struct.pack(">H", param_val))
                        elif param_type == "int16":
                            param_val = int(param_val_str)
                            if param_val < -32768 or param_val > 32767:
                                raise ValueError("The parameter value must be between -32768 and 32767!")
                            pl.append(2)
                            pl += list(struct.pack(">h", param_val))
                        elif param_type == "uint32":
                            param_val = int(param_val_str)
                            if param_val < 0 or param_val > 2**32-1:
                                raise ValueError("The parameter value must be between 0 and 4294967295!")
                            pl.append(4)
                            pl += list(struct.pack(">I", param_val))
                        elif param_type == "int32":
                            param_val = int(param_val_str)
                            if param_val < -2147483648 or param_val > 2147483647:
                                raise ValueError("The parameter value must be between -2147483648 and 2147483647!")
                            pl.append(4)
                            pl += list(struct.pack(">i", param_val))
                        elif param_type == "uint64":
                            param_val = int(param_val_str)
                            if param_val < 0 or param_val > 2**64-1:
                                raise ValueError("The parameter value must be between 0 and 18446744073709551615!")
                            pl.append(8)
                            pl += list(struct.pack(">Q", param_val))
                        elif param_type == "int64":
                            param_val = int(param_val_str)
                            if param_val < -9223372036854775808 or param_val > 9223372036854775807:
                                raise ValueError("The parameter value must be between -9223372036854775808 and 9223372036854775807!")
                            pl.append(8)
                            pl += list(struct.pack(">q", param_val))
                        elif param_type == "flt":
                            param_val = float(param_val_str)
                            pl.append(4)
                            pl += list(struct.pack(">f", param_val))
                        elif param_type == "dbl":
                            param_val = float(param_val_str)
                            pl.append(8)
                            pl += list(struct.pack(">d", param_val))
                        elif param_type == "str":
                            pl.append(len(param_val_str))
                            pl += [ord(c) for c in param_val_str]
                        else:
                            raise ValueError("Unknown parameter type!")

                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                        pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_SET_PARAM, CSP_PORT_SET_PARAM, False, True, False, False, False, pl, dialog_pw.get_key())

                    self._transmit_tc(pkt, "Set Parameter")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Set Parameter\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_data_request_clicked(self, button):
        dialog = DialogDataRequest(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                data_id = dialog.get_data_id()
                start_page = dialog.get_start_page()
                end_page = dialog.get_end_page()
                if data_id < 0 or data_id > 255:
                    raise ValueError("The data ID must be between 0 and 255!")

                if start_page < 0 or start_page > 2**32-1:
                    raise ValueError("The start timestamp must be between 0 and 4294967295!")

                if end_page < 0 or end_page > 2**32-1:
                    raise ValueError("The end timestamp must be between 0 and 4294967295!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pl = [data_id]
                    pl.append((start_page >> 24) & 0xFF)
                    pl.append((start_page >> 16) & 0xFF)
                    pl.append((start_page >> 8) & 0xFF)
                    pl.append((start_page >> 0) & 0xFF)
                    pl.append((end_page >> 24) & 0xFF)
                    pl.append((end_page >> 16) & 0xFF)
                    pl.append((end_page >> 8) & 0xFF)
                    pl.append((end_page >> 0) & 0xFF)

                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_DATA_REQUEST, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Data Request")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Data Request\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()
    
    def on_button_leave_hibernation_clicked(self, button):
        dialog = DialogPassword(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            pkt = list()
            if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                slp = SLP()
                pkt = slp.encode_private(SLP_ID_LEAVE_HIBERNATION, self.entry_preferences_general_callsign.get_text(), dialog.get_key(), list())
            elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_LEAVE_HIBERNATION, CSP_PORT_LEAVE_HIBERNATION, False, True, False, False, False, list(), dialog.get_key())
            self._transmit_tc(pkt, "Leave Hibernation")

        dialog.destroy()

    def on_button_force_reset_clicked(self, button):
        dialog = DialogPassword(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            pkt = list()
            if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                slp = SLP()
                pkt = slp.encode_private(SLP_ID_FORCE_RESET, self.entry_preferences_general_callsign.get_text(), dialog.get_key(), list())
#            elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                pkt = csp.encode()
            self._transmit_tc(pkt, "Force Reset")

        dialog.destroy()

    def on_button_get_parameter_clicked(self, button):
        dialog = DialogGetParameter(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                subsys_id = dialog.get_subsys_id()
                param_id = dialog.get_param_id()
                if subsys_id < 0 or subsys_id > 255:
                    raise ValueError("The subsystem ID must be between 0 and 255!")

                if param_id < 0 or param_id > 255:
                    raise ValueError("The parameter ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pl = [subsys_id, param_id]
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_GET_PARAMETER, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Get Parameter")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Get Parameter\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_get_payload_data_clicked(self, button):
        dialog = DialogGetPayloadData(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                pl_id = dialog.get_pl_id()
                pl_args = dialog.get_pl_args()
                if pl_id < 0 or pl_id > 255:
                    raise ValueError("The payload ID must be between 0 and 255!")

                if len(pl_args) == 0:
                    raise ValueError("The payload arguments cannot be empty!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pl = [pl_id]
                    pl += pl_args
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_GET_PAYLOAD_DATA, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Get Payload Data")

                dialog_pw.destroy()
            except (ValueError, SyntaxError) as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Get Payload\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_broadcast_message_clicked(self, button):
        dialog = DialogBroadcastMessage(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                dst_adr = dialog.get_dst_callsign()
                msg = dialog.get_message()
                if len(dst_adr) == 0 or len(dst_adr) > 7:
                    raise ValueError("The destination callsign must be between 0 and 7 characters long!")

                if len(msg) == 0 or len(msg) > 38:
                    raise ValueError("The message must be between 0 and 38 characters long!")

                pl = list()
                n = 7 - len(dst_adr)
                if n != 7:
                    dst_adr = n*" " + dst_adr
                pl += [ord(i) for i in dst_adr]
                pl += [ord(i) for i in msg]
                pkt = list()
                if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                    slp = SLP()
                    pkt = slp.encode(SLP_ID_BROADCAST_MESSAGE, self.entry_preferences_general_callsign.get_text(), pl)
                elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                    pl.clear()
                    pl += list(struct.pack('>I', len(msg)))
                    pl += [ord(i) for i in msg]
                    csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                    pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_BROADCAST_MSG, CSP_PORT_BROADCAST_MSG, False, False, False, False, False, pl)

                    dialog_pw = DialogPassword(self.window)

                    response_key = dialog_pw.run()
                    if response_key == Gtk.ResponseType.OK:
                        pkt = csp.append_hmac(pkt, dialog_pw.get_key())

                    dialog_pw.destroy()

                self._transmit_tc(pkt, "Broadcast Message")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Broadcast Message\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_tx_pkt_clicked(self, button):
        dialog = DialogTransmitPacket(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                data = dialog.get_data()
                if len(data) == 0 or len(data) > 45:
                    raise ValueError("The data length must be greater than 0 and lesser than 45!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_TRANSMIT_PACKET, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), data)
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Transmit Packet")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Transmit Packet\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_update_tle_clicked(self, button):
        dialog = DialogUpdateTLE(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                line1 = dialog.get_tle_line_1()
                line2 = dialog.get_tle_line_2()
                if (len(line1) != 69) or (len(line2) != 69):
                    raise ValueError("The TLE lines must have 69 characters!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        epoch_year          = int(line1[18:20])         # Extract last two digits of the year
                        epoch_day           = float(line1[20:32])       # Fractional day of the year
                        eccentricity_str    = line2[26:33].lstrip("0")  # Remove leading zeros
                        eccentricity        = int(eccentricity_str) if eccentricity_str else 0  # Convert to int
                        mean_anomaly        = float(line2[43:51])
                        argument_of_perigee = float(line2[34:42])
                        bstar_drag_term     = (1.0e-5 * float(line1[53:59])) / (10 ** int(line1[60]))  # Convert scientific notation
                        inclination         = float(line2[8:16])
                        right_ascension     = float(line2[17:25])
                        mean_motion         = float(line2[52:63])
                        packed_data = struct.pack('>H d I f f f d d d',
                            epoch_year, epoch_day, eccentricity,
                            mean_anomaly, argument_of_perigee, bstar_drag_term,
                            inclination, right_ascension, mean_motion)
                        pl = list(packed_data)
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_UPDATE_TLE, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                        pl = [ord(c) for c in line1]
                        pl += [ord(c) for c in line2]
                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                        pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_UPDATE_TLE, CSP_PORT_UPDATE_TLE, False, True, False, False, False, pl, dialog_pw.get_key())
                    self._transmit_tc(pkt, "Update TLE")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Update TLE\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_time_sync_clicked(self, button):
        dialog = DialogPassword(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                ts = int(time.time())

                pl = list()
                pl.append((ts >> 24) & 0xFF)
                pl.append((ts >> 16) & 0xFF)
                pl.append((ts >> 8) & 0xFF)
                pl.append((ts >> 0) & 0xFF)

                pkt = list()
                if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                    # There is no Time Sync TC for the SLP protocol, instead, we use a Set Parameter TC
                    pl = [0, 0] + pl
                    slp = SLP()
                    pkt = slp.encode_private(SLP_ID_SET_PARAMETER, self.entry_preferences_general_callsign.get_text(), dialog.get_key(), pl)
                elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
                    csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                    pkt = csp.encode(CSP_PRIO_NORM, int(self.entry_preferences_protocols_csp_dst_adr.get_text()), CSP_PORT_TIME_SYNC, CSP_PORT_TIME_SYNC, False, True, False, False, False, pl, dialog.get_key())

                self._transmit_tc(pkt, "Time Sync")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Time Sync\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_csp_services_clicked(self, button):
        response = self.dialog_csp_services.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.dialog_csp_services.hide()

    def on_button_csp_ping_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_ping(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Ping")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Ping\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_ps_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_ps(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP PS")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP PS\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_memfree_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_memfree(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Mem. Free")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Mem. Free\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_bufferfree_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_buf_free(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Buffer Free")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Buffer Free\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_uptime_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_uptime(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Uptime")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Uptime\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_cmp_ident_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_cmp_ident(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP CMP Ident")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Ident\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_route_set_clicked(self, button):
        dialog = DialogCSPRouteSet(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if (dialog.get_dest_node() < 0) or (dialog.get_dest_node() > 255):
                    raise ValueError("The destination node must be between 0 and 255!")

                if (dialog.get_next_hop_mac() < 0) or (dialog.get_next_hop_mac() > 255):
                    raise ValueError("The next hop MAC must be between 0 and 255!")

                if len(dialog.get_if_name()) > 11:
                    raise ValueError("The IF name must have up to 11 characters!")

                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                csp_pkt = csp.encode_cmp_set_route(int(self.entry_preferences_protocols_csp_dst_adr.get_text()), dialog.get_dest_node(), dialog.get_next_hop_mac(), dialog.get_if_name())

                if self.switch_preferences_protocols_csp_hmac.get_active():
                    dialog_pw = DialogPassword(self.window)

                    response_key = dialog_pw.run()
                    if response_key == Gtk.ResponseType.OK:
                        csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                    dialog_pw.destroy()

                self._transmit_tc(csp_pkt, "CSP CMP Route Set")
            except Exception as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Route Set\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_csp_cmp_if_stat_clicked(self, button):
        dialog = DialogCSPIFStat(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if len(dialog.get_csp_if_name()) > 11:
                    raise ValueError("The IF name must have up to 11 characters!")

                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                csp_pkt = csp.encode_cmp_if_stat(int(self.entry_preferences_protocols_csp_dst_adr.get_text()), dialog.get_csp_if_name())

                if self.switch_preferences_protocols_csp_hmac.get_active():
                    dialog_pw = DialogPassword(self.window)

                    response_key = dialog_pw.run()
                    if response_key == Gtk.ResponseType.OK:
                        csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                    dialog_pw.destroy()

                self._transmit_tc(csp_pkt, "CSP CMP IF Status")
            except Exception as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP IF Stat\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_csp_cmp_peek_clicked(self, button):
        dialog = DialogCSPPeek(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_csp_mem_adr() < 0 or dialog.get_csp_mem_adr() > 2**32-1:
                    raise ValueError("The memory address must be between 0 and 4294967295!")

                if dialog.get_csp_mem_len() < 0 or dialog.get_csp_mem_len() > 2**32-1:
                    raise ValueError("The memory length must be between 0 and 4294967295!")

                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                csp_pkt = csp.encode_cmp_peek(int(self.entry_preferences_protocols_csp_dst_adr.get_text()), dialog.get_csp_mem_adr(), dialog.get_csp_mem_len())

                if self.switch_preferences_protocols_csp_hmac.get_active():
                    dialog_pw = DialogPassword(self.window)

                    response_key = dialog_pw.run()
                    if response_key == Gtk.ResponseType.OK:
                        csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                    dialog_pw.destroy()

                self._transmit_tc(csp_pkt, "CSP Peek")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Peek\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_csp_cmp_poke_clicked(self, button):
        dialog = DialogCSPPoke(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                if dialog.get_csp_mem_adr() < 0 or dialog.get_csp_mem_adr() > 2**32-1:
                    raise ValueError("The memory address must be between 0 and 4294967295!")

                if len(dialog.get_csp_mem_data()) > 200:
                    raise ValueError("The memory length must be between 0 and 200!")

                csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
                csp_pkt = csp.encode_cmp_poke(int(self.entry_preferences_protocols_csp_dst_adr.get_text()), dialog.get_csp_mem_adr(), dialog.get_csp_mem_data())

                if self.switch_preferences_protocols_csp_hmac.get_active():
                    dialog_pw = DialogPassword(self.window)

                    response_key = dialog_pw.run()
                    if response_key == Gtk.ResponseType.OK:
                        csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                    dialog_pw.destroy()

                self._transmit_tc(csp_pkt, "CSP Poke")
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Poke\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def on_button_csp_cmp_set_clock_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_cmp_set_clock(int(self.entry_preferences_protocols_csp_dst_adr.get_text()), int(time.time()), 0)

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP CMP Set Clock")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Set Clock\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_cmp_get_clock_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_cmp_get_clock(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP CMP Get Clock")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP CMP Get Clock\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_reboot_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_reboot(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Reboot")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Reboot\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_csp_shutdown_clicked(self, button):
        try:
            csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
            csp_pkt = csp.encode_shutdown(int(self.entry_preferences_protocols_csp_dst_adr.get_text()))

            if self.switch_preferences_protocols_csp_hmac.get_active():
                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    csp_pkt = csp.append_hmac(csp_pkt, dialog_pw.get_key())

                dialog_pw.destroy()

            self._transmit_tc(csp_pkt, "CSP Shutdown")
        except Exception as err:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"CSP Shutdown\" telecommand!")
            error_dialog.format_secondary_text(str(err))
            error_dialog.run()
            error_dialog.destroy()

    def on_button_schedule_tc_clicked(self, button):
        dialog = DialogScheduleTC(self.window)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                tc_ts = dialog.get_ts()
                tc_id = dialog.get_tc_id()
                tc_par = dialog.get_params()
                if tc_ts < 0 or tc_ts > 2**32-1:
                    raise ValueError("The timestamp must be between 0 and "+ str(2**32-1) + "!")

                if tc_id < 0 or tc_id > 255:
                    raise ValueError("The telecommand ID must be between 0 and 255!")

                dialog_pw = DialogPassword(self.window)

                response_key = dialog_pw.run()
                if response_key == Gtk.ResponseType.OK:
                    pl = list(struct.pack('>I', tc_ts))
                    pl += [tc_id]
                    callsign = self.entry_preferences_general_callsign.get_text()
                    for i in range(7 - len(callsign)):
                        pl += [ord(' ')]
                    pl += [ord(i) for i in callsign]
                    pl += tc_par
                    pkt = list()
                    if self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_SLP:
                        slp = SLP()
                        pkt = slp.encode_private(SLP_ID_SCHEDULE_TC, self.entry_preferences_general_callsign.get_text(), dialog_pw.get_key(), pl)
#                    elif self._satellite.get_active_link().get_network_protocol() == _PROTOCOL_CSP:
#                        csp = CSP(int(self.entry_preferences_protocols_csp_my_adr.get_text()))
#                        pkt = csp.encode()
                    self._transmit_tc(pkt, "Schedule TC")

                dialog_pw.destroy()
            except ValueError as err:
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error generating the \"Schedule TC\" telecommand!")
                error_dialog.format_secondary_text(str(err))
                error_dialog.run()
                error_dialog.destroy()
            finally:
                dialog.destroy()

        dialog.destroy()

    def _transmit_tc(self, pkt, tc_name):
        carrier_frequency = int(self.entry_carrier_frequency.get_text())
        tx_gain = self.spinbutton_tx_gain.get_text()
        callsign = self.entry_preferences_general_callsign.get_text()

        mod_name = self._satellite.get_active_link().get_modulation()
        freq = self._satellite.get_active_link().get_frequency()
        baud = self._satellite.get_active_link().get_baudrate()
        sync = self._satellite.get_active_link().get_sync_word()
        prot_link = self._satellite.get_active_link().get_link_protocol()

        prot = None
        if prot_link == _PROTOCOL_NGHAM:
            prot = PyNGHam()
        elif prot_link == _PROTOCOL_AX100MODE5:
            prot = AX100Mode5()
        else:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a " + tc_name + " telecommand!")
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
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a " + tc_name + " telecommand!")
                error_dialog.format_secondary_text("The " + mod_name + " modulation is not supported yet!")
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
                error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a " + tc_name + " telecommand!")
                error_dialog.format_secondary_text("SDR device not supported yet!")
                error_dialog.run()
                error_dialog.destroy()

                return

            if self.switch_doppler.get_active():
                if self.radiobutton_doppler_tle_file.get_active():
                    doppler = DopplerShift("up")

                    lat = float(self.entry_preferences_general_latitude.get_text())
                    lon = float(self.entry_preferences_general_longitude.get_text())
                    alt = int(self.entry_preferences_general_altitude.get_text())

                    tle_file = self.filechooser_doppler_tle_file.get_filename()

                    if tle_file != "":
                        doppler.set_tle_from_file(tle_file)
                        doppler.set_observer_position(lat, lon, alt)
                        doppler.set_frequency(carrier_frequency)

                        carrier_frequency = doppler.get_shifted_frequency()
                    else:
                        raise RuntimeError("No TLE file provided!")

            carrier_frequency += int(self.entry_sdr_freq_offset.get_text())
            if sdr.transmit(samples, duration_s, sample_rate, carrier_frequency):
                self.write_log(tc_name + " transmitted to " + self._satellite.get_name() + " from " + callsign + " in " + str(carrier_frequency) + " Hz with a gain of " + tx_gain + " dB")
            else:
                self.write_log("Error transmitting a " + tc_name + " telecommand!")
        else:
            if self._client_socket:
                try:
                    self._client_socket.send(bytearray(enc_pkt))  # Send message to server
                    self.write_log(tc_name + " transmitted to " + self._satellite.get_name() + " from " + callsign + " via " + self.entry_tcp_address.get_text() + ":" + self.entry_tcp_port.get_text())
                except socket.error as e:
                    error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error transmitting a " + tc_name + " telecommand!")
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
            self.entry_preferences_general_latitude.set_text(config["latitude"])
            self.entry_preferences_general_longitude.set_text(config["longitude"])
            self.entry_preferences_general_altitude.set_text(config["altitude"])
            self.entry_preferences_protocols_csp_my_adr.set_text(config["csp_my_adr"]),
            self.entry_preferences_protocols_csp_dst_adr.set_text(config["csp_dst_adr"]),
            self.switch_preferences_protocols_csp_hmac.set_active(config["csp_hmac"])
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
            self.entry_sdr_freq_offset.set_text(config["sdr_freq_offset"])
            self.entry_sample_rate.set_text(config["sdr_sample_rate"])
        except:
            self._load_default_preferences()
            self._save_preferences()

    def _load_default_preferences(self):
        self.entry_preferences_general_callsign.set_text(_DEFAULT_CALLSIGN)
        self.entry_preferences_general_location.set_text(_DEFAULT_LOCATION)
        self.entry_preferences_general_country.set_text(_DEFAULT_COUNTRY)
        self.entry_preferences_general_latitude.set_text(_DEFAULT_LATITUDE)
        self.entry_preferences_general_longitude.set_text(_DEFAULT_LONGITUDE)
        self.entry_preferences_general_altitude.set_text(_DEFAULT_ALTITUDE)

        self.entry_preferences_protocols_csp_my_adr.set_text(str(_DEFAULT_CSP_MY_ADDRESS))
        self.entry_preferences_protocols_csp_dst_adr.set_text(str(_DEFAULT_CSP_DST_ADDRESS))
        self.switch_preferences_protocols_csp_hmac.set_active(False)

        self.filechooser_doppler_tle_file.set_filename("")
        self.radiobutton_doppler_network.set_active(True)
        self.entry_doppler_address.set_text(_DEFAULT_DOPPLER_ADDRESS)
        self.entry_doppler_port.set_text(str(_DEFAULT_DOPPLER_PORT))

        self.logfile_chooser_button.set_filename(_DEFAULT_LOGFILE_PATH)

        self.combobox_sdr.set_active(0)
        self.entry_carrier_frequency.set_text(str(_DEFAULT_FREQUENCY))
        self.entry_sdr_freq_offset.set_text(str(_DEFAULT_FREQ_OFFSET))
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
                       "latitude": self.entry_preferences_general_latitude.get_text(),
                       "longitude": self.entry_preferences_general_longitude.get_text(),
                       "altitude": self.entry_preferences_general_altitude.get_text(),
                       "csp_my_adr": self.entry_preferences_protocols_csp_my_adr.get_text(),
                       "csp_dst_adr": self.entry_preferences_protocols_csp_dst_adr.get_text(),
                       "csp_hmac": self.switch_preferences_protocols_csp_hmac.get_active(),
                       "doppler_from_network": self.radiobutton_doppler_network.get_active(),
                       "tle_file": self.filechooser_doppler_tle_file.get_filename(),
                       "doppler_address": self.entry_doppler_address.get_text(),
                       "doppler_port": self.entry_doppler_port.get_text(),
                       "logfile_path": self.logfile_chooser_button.get_filename(),
                       "sdr_dev": self.combobox_sdr.get_active(),
                       "sdr_freq": self.entry_carrier_frequency.get_text(),
                       "sdr_freq_offset": self.entry_sdr_freq_offset.get_text(),
                       "sdr_sample_rate": self.entry_sample_rate.get_text()}, f, ensure_ascii=False, indent=4)

    def on_toolbutton_about_clicked(self, toolbutton):
        response = self.aboutdialog.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            self.aboutdialog.hide()

    def write_log(self, msg):
        event = [str(datetime.now()), msg]

        self.listmodel_events.append(event)

        self._log.write(msg, event[0])

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
        self.button_time_sync.set_sensitive(False)
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
        self.button_csp_cmp_set_clock.set_sensitive(False)
        self.button_csp_cmp_get_clock.set_sensitive(False)
        self.button_csp_reboot.set_sensitive(False)
        self.button_csp_shutdown.set_sensitive(False)
        self.button_schedule_tc.set_sensitive(False)

        avail_pkts = self._satellite.get_active_link().get_packets()

        if "ping" in avail_pkts:                self.button_ping_request.set_sensitive(state)
        if "enter_hibernation" in avail_pkts:   self.button_enter_hibernation.set_sensitive(state)
        if "deactivate_module" in avail_pkts:   self.button_deactivate_module.set_sensitive(state)
        if "erase_memory" in avail_pkts:        self.button_erase_memory.set_sensitive(state)
        if "set_param" in avail_pkts:           self.button_set_parameter.set_sensitive(state)
        if "data_request" in avail_pkts:        self.button_data_request.set_sensitive(state)
        if "leave_hibernation" in avail_pkts:   self.button_leave_hibernation.set_sensitive(state)
        if "activate_payload" in avail_pkts:    self.button_activate_payload.set_sensitive(state)
        if "force_reset" in avail_pkts:         self.button_force_reset.set_sensitive(state)
        if "get_param" in avail_pkts:           self.button_get_parameter.set_sensitive(state)
        if "broadcast_msg" in avail_pkts:       self.button_broadcast_message.set_sensitive(state)
        if "activate_module" in avail_pkts:     self.button_activate_module.set_sensitive(state)
        if "deactivate_payload" in avail_pkts:  self.button_deactivate_payload.set_sensitive(state)
        if "get_payload_data" in avail_pkts:    self.button_get_payload_data.set_sensitive(state)
        if "update_tle" in avail_pkts:          self.button_update_tle.set_sensitive(state)
        if "time_sync" in avail_pkts:           self.button_time_sync.set_sensitive(state)
        if "transmit_pkt" in avail_pkts:        self.button_tx_pkt.set_sensitive(state)
        if "csp_services" in avail_pkts:
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
            self.button_csp_cmp_set_clock.set_sensitive(state)
            self.button_csp_cmp_get_clock.set_sensitive(state)
            self.button_csp_reboot.set_sensitive(state)
            self.button_csp_shutdown.set_sensitive(state)
        if "schedule_tc" in avail_pkts:         self.button_schedule_tc.set_sensitive(state)

    def on_combobox_satellite_changed(self, combobox):
        sat_filename = _SATELLITES[self.combobox_satellite.get_active()][1]
        sat_config_file = str()

        if os.path.isfile(_SAT_JSON_LOCAL_PATH + sat_filename):
            sat_config_file = _SAT_JSON_LOCAL_PATH + sat_filename
        else:
            sat_config_file = _SAT_JSON_SYSTEM_PATH + sat_filename

        try:
            self._satellite.load_from_file(sat_config_file)

            self.liststore_link.clear() # Clear the list of link types

            for lk in self._satellite.get_links():
                self.liststore_link.append([lk.get_name()])

            self._load_tooltips(sat_config_file)
        except (FileNotFoundError, RuntimeError) as e:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error opening the satellite configuration file!")
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()

            self.combobox_link.set_active(-1)
        except:
            error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error opening the satellite configuration file!")
            error_dialog.format_secondary_text("Is the configuration file correct?")
            error_dialog.run()
            error_dialog.destroy()
        finally:
            # Sets the first packet type as the active packet type
            self.combobox_link.set_active(0)

    def on_combobox_link_changed(self, combobox):
        self._satellite.set_active_link(self.combobox_link.get_active())

        self.entry_carrier_frequency.set_text(str(self._satellite.get_active_link().get_frequency()))

        if self.switch_button.get_active() == False:
            self._update_tc_buttons(False)
        elif self.switch_button.get_active() == True:
            self._update_tc_buttons(True)

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

            if self._client_socket:
                self.write_log("Connected to " + adr + ":" + str(port))

                # Create an IOChannel for the client socket and watch for incoming data
                self._tcp_client_socket_io_channel = GLib.IOChannel(self._client_socket.fileno())
                self._tcp_client_socket_io_channel.set_encoding(None)   # Binary mode
                self._tcp_cb_id = GLib.io_add_watch(self._tcp_client_socket_io_channel, GLib.IO_IN, self._handle_tcp_data)

                self.combobox_sdr.set_sensitive(False)
                self.entry_carrier_frequency.set_sensitive(False)
                self.entry_sdr_freq_offset.set_sensitive(False)
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
        self._close_tcp_socket()

    def _close_tcp_socket(self):
        self.write_log("Disconnected from " + self.entry_tcp_address.get_text() + ":" + self.entry_tcp_port.get_text())

        self._client_socket.close()
        self._client_socket = None

        self.combobox_sdr.set_sensitive(True)
        self.entry_carrier_frequency.set_sensitive(True)
        self.entry_sdr_freq_offset.set_sensitive(True)
        self.entry_sample_rate.set_sensitive(True)
        self.spinbutton_tx_gain.set_sensitive(True)
        self.entry_tcp_address.set_sensitive(True)
        self.entry_tcp_port.set_sensitive(True)
        self.button_tcp_connect.set_sensitive(True)
        self.button_tcp_disconnect.set_sensitive(False)

    def _handle_tcp_data(self, source, condition):
        if condition == GLib.IO_IN:
            try:
                data = self._client_socket.recv(1024)   # Receive data from the server
                if data:
                    self._write_log("Data received from TCP server!")
                else:
                    # Server has closed the connection
                    self._write_log("TCP server closed the connection!")
                    self._close_tcp_socket()
                    return False    # Stop the IO watch for this socket
            except socket.error as e:
                self._write_log("Error receiving data from TCP server: " + str(e))
                self._close_tcp_socket()
                return False  # Stop the IO watch for this socket
        return True  # Keep the handler active

    def _load_tooltips(self, filename):
        self.button_ping_request.set_tooltip_text("")
        self.button_data_request.set_tooltip_text("")
        self.button_broadcast_message.set_tooltip_text("")
        self.button_enter_hibernation.set_tooltip_text("")
        self.button_leave_hibernation.set_tooltip_text("")
        self.button_activate_module.set_tooltip_text("")
        self.button_deactivate_module.set_tooltip_text("")
        self.button_activate_payload.set_tooltip_text("")
        self.button_deactivate_payload.set_tooltip_text("")
        self.button_erase_memory.set_tooltip_text("")
        self.button_force_reset.set_tooltip_text("")
        self.button_get_payload_data.set_tooltip_text("")
        self.button_set_parameter.set_tooltip_text("")
        self.button_get_parameter.set_tooltip_text("")
        self.button_tx_pkt.set_tooltip_text("")
        self.button_update_tle.set_tooltip_text("")
        self.button_time_sync.set_tooltip_text("")
        self.button_csp_services.set_tooltip_text("")
        self.button_schedule_tc.set_tooltip_text("")

        with open(filename) as f:
            sat_info = json.load(f)

            lk_idx = self.combobox_link.get_active()
            if 'links' in sat_info:
                if 'tooltips' in sat_info['links'][lk_idx]:
                    if 'ping' in sat_info['links'][lk_idx]['packets']:
                        self.button_ping_request.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['ping'])
                    if 'data_request' in sat_info['links'][lk_idx]['packets']:
                        self.button_data_request.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['data_request'])
                    if 'broadcast_msg' in sat_info['links'][lk_idx]['packets']:
                        self.button_broadcast_message.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['broadcast_msg'])
                    if 'enter_hibernation' in sat_info['links'][lk_idx]['packets']:
                        self.button_enter_hibernation.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['enter_hibernation'])
                    if 'leave_hibernation' in sat_info['links'][lk_idx]['packets']:
                        self.button_leave_hibernation.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['leave_hibernation'])
                    if 'activate_module' in sat_info['links'][lk_idx]['packets']:
                        self.button_activate_module.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['activate_module'])
                    if 'deactivate_module' in sat_info['links'][lk_idx]['packets']:
                        self.button_deactivate_module.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['deactivate_module'])
                    if 'activate_payload' in sat_info['links'][lk_idx]['packets']:
                        self.button_activate_payload.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['activate_payload'])
                    if 'deactivate_payload' in sat_info['links'][lk_idx]['packets']:
                        self.button_deactivate_payload.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['deactivate_payload'])
                    if 'erase_memory' in sat_info['links'][lk_idx]['packets']:
                        self.button_erase_memory.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['erase_memory'])
                    if 'force_reset' in sat_info['links'][lk_idx]['packets']:
                        self.button_force_reset.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['force_reset'])
                    if 'get_payload_data' in sat_info['links'][lk_idx]['packets']:
                        self.button_get_payload_data.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['get_payload_data'])
                    if 'set_param' in sat_info['links'][lk_idx]['packets']:
                        self.button_set_parameter.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['set_param'])
                    if 'get_param' in sat_info['links'][lk_idx]['packets']:
                        self.button_get_parameter.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['get_param'])
                    if 'transmit_pkt' in sat_info['links'][lk_idx]['packets']:
                        self.button_tx_pkt.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['transmit_pkt'])
                    if 'update_tle' in sat_info['links'][lk_idx]['packets']:
                        self.button_update_tle.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['update_tle'])
                    if 'time_sync' in sat_info['links'][lk_idx]['packets']:
                        self.button_update_tle.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['time_sync'])
                    if 'csp_services' in sat_info['links'][lk_idx]['packets']:
                        self.button_csp_services.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['csp_services'])
                    if 'schedule_tc' in sat_info['links'][lk_idx]['packets']:
                        self.button_schedule_tc.set_tooltip_text(sat_info['links'][lk_idx]['tooltips']['schedule_tc'])
