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
    builder.add_from_file("../spacelab-transmitter/data/ui/spacelab_transmitter.glade")

    # Main window
    window = builder.get_object("window_main")
    button_preferences = builder.get_object("button_preferences")
    toolbutton_about = builder.get_object("toolbutton_about")

    assert window != None
    assert button_preferences != None
    assert toolbutton_about != None

    # About dialog
    aboutdialog_spacelab_transmitter = builder.get_object("aboutdialog_spacelab_transmitter")

    assert aboutdialog_spacelab_transmitter != None

    # Preferences dialog
    dialog_preferences = builder.get_object("dialog_preferences")
    button_preferences_ok = builder.get_object("button_preferences_ok")
    button_preferences_default = builder.get_object("button_preferences_default")
    button_preferences_cancel = builder.get_object("button_preferences_cancel")
    entry_preferences_general_country = builder.get_object("entry_preferences_general_country")
    entry_preferences_general_location = builder.get_object("entry_preferences_general_location")
    entry_preferences_general_callsign = builder.get_object("entry_preferences_general_callsign")

    assert dialog_preferences != None
    assert button_preferences_ok != None
    assert button_preferences_default != None
    assert button_preferences_cancel != None
    assert entry_preferences_general_country != None
    assert entry_preferences_general_location != None
    assert entry_preferences_general_callsign != None
