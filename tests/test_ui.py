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
    window                  = builder.get_object("window_main")
    button_preferences      = builder.get_object("button_preferences")
    toolbutton_about        = builder.get_object("toolbutton_about")
    liststore_satellite     = builder.get_object("liststore_satellite")
    liststore_packet_type   = builder.get_object("liststore_packet_type")
    button_ping_request            = builder.get_object("button_ping_request")
    button_enter_hibernation       = builder.get_object("button_enter_hibernation")
    button_deactivate_module       = builder.get_object("button_deactivate_module")
    button_erase_memory            = builder.get_object("button_erase_memory")
    button_set_parameter           = builder.get_object("button_set_parameter")
    button_data_request            = builder.get_object("button_data_request")
    button_leave_hibernation       = builder.get_object("button_leave_hibernation")
    button_activate_payload        = builder.get_object("button_activate_payload")
    button_force_reset             = builder.get_object("button_force_reset")
    button_get_parameter           = builder.get_object("button_get_parameter")
    button_broadcast_message       = builder.get_object("button_broadcast_message")
    button_activate_module         = builder.get_object("button_activate_module")
    button_deactivate_payload      = builder.get_object("button_deactivate_payload")
    button_get_payload_data        = builder.get_object("button_get_payload_data")
    treeview_events         = builder.get_object("treeview_events")

    assert window                   != None
    assert button_preferences       != None
    assert toolbutton_about         != None
    assert liststore_satellite      != None
    assert liststore_packet_type    != None
    assert button_ping_request             != None
    assert button_enter_hibernation        != None
    assert button_deactivate_module        != None
    assert button_erase_memory             != None
    assert button_set_parameter            != None
    assert button_data_request             != None
    assert button_leave_hibernation        != None
    assert button_activate_payload         != None
    assert button_force_reset              != None
    assert button_get_parameter            != None
    assert button_broadcast_message        != None
    assert button_activate_module          != None
    assert button_deactivate_payload       != None
    assert button_get_payload_data         != None
    assert treeview_events          != None

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
    filechooserbutton_logfile           = builder.get_object("logfile_chooser_button")

    assert dialog_preferences                   != None
    assert button_preferences_ok                != None
    assert button_preferences_default           != None
    assert button_preferences_cancel            != None
    assert entry_preferences_general_country    != None
    assert entry_preferences_general_location   != None
    assert entry_preferences_general_callsign   != None
    assert filechooserbutton_logfile            != None
