#
#  test_ui.py
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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def test_ui():
    builder = Gtk.Builder()
    builder.add_from_file("spacelab_transmitter/data/ui/spacelab_transmitter.glade")

    # Main window
    window                          = builder.get_object("window_main")
    button_preferences              = builder.get_object("button_preferences")
    switch_button                   = builder.get_object("switch_button")
    switch_doppler                  = builder.get_object("switch_doppler")
    toolbutton_about                = builder.get_object("toolbutton_about")
    combobox_satellite              = builder.get_object("combobox_satellite")
    combobox_packet_type            = builder.get_object("combobox_packet_type")
    liststore_satellite             = builder.get_object("liststore_satellite")
    liststore_packet_type           = builder.get_object("liststore_packet_type")
    button_ping_request             = builder.get_object("button_ping_request")
    button_enter_hibernation        = builder.get_object("button_enter_hibernation")
    button_deactivate_module        = builder.get_object("button_deactivate_module")
    button_erase_memory             = builder.get_object("button_erase_memory")
    button_set_parameter            = builder.get_object("button_set_parameter")
    button_data_request             = builder.get_object("button_data_request")
    button_leave_hibernation        = builder.get_object("button_leave_hibernation")
    button_activate_payload         = builder.get_object("button_activate_payload")
    button_force_reset              = builder.get_object("button_force_reset")
    button_get_parameter            = builder.get_object("button_get_parameter")
    button_broadcast_message        = builder.get_object("button_broadcast_message")
    button_activate_module          = builder.get_object("button_activate_module")
    button_deactivate_payload       = builder.get_object("button_deactivate_payload")
    button_get_payload_data         = builder.get_object("button_get_payload_data")
    button_tx_pkt                   = builder.get_object("button_tx_pkt")
    button_update_tle               = builder.get_object("button_update_tle")
    combobox_sdr                    = builder.get_object("combobox_sdr")
    liststore_sdr_devices           = builder.get_object("liststore_sdr_devices")
    entry_carrier_frequency         = builder.get_object("entry_carrier_frequency")
    entry_sample_rate               = builder.get_object("entry_sample_rate")
    spinbutton_tx_gain              = builder.get_object("spinbutton_tx_gain")
    entry_tcp_address               = builder.get_object("entry_tcp_address")
    entry_tcp_port                  = builder.get_object("entry_tcp_port")
    button_tcp_connect              = builder.get_object("button_tcp_connect")
    button_tcp_disconnect           = builder.get_object("button_tcp_disconnect")
    treeview_events                 = builder.get_object("treeview_events")

    assert window                           != None
    assert button_preferences               != None
    assert switch_button                    != None
    assert switch_doppler                   != None
    assert toolbutton_about                 != None
    assert combobox_satellite               != None
    assert combobox_packet_type             != None
    assert liststore_satellite              != None
    assert liststore_packet_type            != None
    assert button_ping_request              != None
    assert button_enter_hibernation         != None
    assert button_deactivate_module         != None
    assert button_erase_memory              != None
    assert button_set_parameter             != None
    assert button_data_request              != None
    assert button_leave_hibernation         != None
    assert button_activate_payload          != None
    assert button_force_reset               != None
    assert button_get_parameter             != None
    assert button_broadcast_message         != None
    assert button_activate_module           != None
    assert button_deactivate_payload        != None
    assert button_get_payload_data          != None
    assert button_tx_pkt                    != None
    assert button_update_tle                != None
    assert combobox_sdr                     != None
    assert liststore_sdr_devices            != None
    assert entry_carrier_frequency          != None
    assert entry_sample_rate                != None
    assert spinbutton_tx_gain               != None
    assert entry_tcp_address                != None
    assert entry_tcp_port                   != None
    assert button_tcp_connect               != None
    assert button_tcp_disconnect            != None
    assert treeview_events                  != None

    # About dialog
    aboutdialog_spacelab_transmitter = builder.get_object("aboutdialog_spacelab_transmitter")

    assert aboutdialog_spacelab_transmitter != None

    # Preferences dialog
    dialog_preferences                  = builder.get_object("dialog_preferences")
    button_preferences_ok               = builder.get_object("button_preferences_ok")
    button_preferences_default          = builder.get_object("button_preferences_default")
    button_preferences_cancel           = builder.get_object("button_preferences_cancel")
    entry_preferences_general_country   = builder.get_object("entry_preferences_general_country")
    entry_preferences_general_location  = builder.get_object("entry_preferences_general_location")
    entry_preferences_general_callsign  = builder.get_object("entry_preferences_general_callsign")
    radiobutton_doppler_tle_file        = builder.get_object("radiobutton_doppler_tle_file")
    filechooser_doppler_tle_file        = builder.get_object("filechooser_doppler_tle_file")
    radiobutton_doppler_network         = builder.get_object("radiobutton_doppler_network")
    entry_doppler_address               = builder.get_object("entry_doppler_address")
    entry_doppler_port                  = builder.get_object("entry_doppler_port")
    filechooserbutton_logfile           = builder.get_object("logfile_chooser_button")

    assert dialog_preferences                   != None
    assert button_preferences_ok                != None
    assert button_preferences_default           != None
    assert button_preferences_cancel            != None
    assert entry_preferences_general_country    != None
    assert entry_preferences_general_location   != None
    assert entry_preferences_general_callsign   != None
    assert radiobutton_doppler_tle_file         != None
    assert filechooser_doppler_tle_file         != None
    assert radiobutton_doppler_network          != None
    assert entry_doppler_address                != None
    assert entry_doppler_port                   != None
    assert filechooserbutton_logfile            != None

    # CSP Services Dialog
    button_csp_services             = builder.get_object("button_csp_services")
    dialog_csp_services             = builder.get_object("dialog_csp_services")
    button_csp_ping                 = builder.get_object("button_csp_ping")
    button_csp_ps                   = builder.get_object("button_csp_ps")
    button_csp_memfree              = builder.get_object("button_csp_memfree")
    button_csp_bufferfree           = builder.get_object("button_csp_bufferfree")
    button_csp_uptime               = builder.get_object("button_csp_uptime")
    button_csp_cmp_ident            = builder.get_object("button_csp_cmp_ident")
    button_csp_route_set            = builder.get_object("button_csp_route_set")
    button_csp_cmp_if_stat          = builder.get_object("button_csp_cmp_if_stat")
    button_csp_cmp_peek             = builder.get_object("button_csp_cmp_peek")
    button_csp_cmp_poke             = builder.get_object("button_csp_cmp_poke")
    button_csp_cmp_clock            = builder.get_object("button_csp_cmp_clock")

    assert button_csp_services              != None
    assert dialog_csp_services              != None
    assert button_csp_ping                  != None
    assert button_csp_ps                    != None
    assert button_csp_memfree               != None
    assert button_csp_bufferfree            != None
    assert button_csp_uptime                != None
    assert button_csp_cmp_ident             != None
    assert button_csp_route_set             != None
    assert button_csp_cmp_if_stat           != None
    assert button_csp_cmp_peek              != None
    assert button_csp_cmp_poke              != None
    assert button_csp_cmp_clock             != None
