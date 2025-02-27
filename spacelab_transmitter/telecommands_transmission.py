#
#  telecommands_transmission.py
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

import ast

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DialogEnterHibernation(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Enter Hibernation", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Hibernation duration in hours:")
        label.set_halign(Gtk.Align.START)
        self.entry_hours = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_hours, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_hours(self):
        return int(self.entry_hours.get_text())

class DialogDeactivateModule(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Deactivate Module", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Module ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_deactivate_mod_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_deactivate_mod_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_deac_mod_id(self):
        return int(self.entry_deactivate_mod_id.get_text())

class DialogActivateModule(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Activate Module", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Module ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_activate_mod_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_activate_mod_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_ac_mod_id(self):
        return int(self.entry_activate_mod_id.get_text())

class DialogDeactivatePayload(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Deactivate Payload", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Payload ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_deactivate_pl_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_deactivate_pl_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_deac_pl_id(self):
        return int(self.entry_deactivate_pl_id.get_text())

class DialogActivatePayload(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Activate Payload", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Payload ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_activate_pl_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_activate_pl_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_ac_pl_id(self):
        return int(self.entry_activate_pl_id.get_text())

class DialogGetParameter(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Get Parameter", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Subsystem ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_subsys_id = Gtk.Entry()

        label2 = Gtk.Label(label="Parameter ID:")
        label2.set_halign(Gtk.Align.START)
        self.entry_param_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_subsys_id, 1, 0, 1, 1)
        grid.attach(self.entry_param_id, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_subsys_id(self):
        return int(self.entry_subsys_id.get_text())

    def get_param_id(self):
        return int(self.entry_param_id.get_text())
    
class DialogSetParameter(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Set Parameter", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Subsystem ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_subsys_id = Gtk.Entry()

        label2 = Gtk.Label(label="Parameter ID:")
        label2.set_halign(Gtk.Align.START)
        self.entry_param_id = Gtk.Entry()

        label3 = Gtk.Label(label="Parameter Value:")
        label3.set_halign(Gtk.Align.START)
        self.entry_param_val = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(label3, 0, 2, 1, 1)
        grid.attach(self.entry_subsys_id, 1, 0, 1, 1)
        grid.attach(self.entry_param_id, 1, 1, 1, 1)
        grid.attach(self.entry_param_val, 1, 2, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_subsys_id(self):
        return int(self.entry_subsys_id.get_text())

    def get_param_id(self):
        return int(self.entry_param_id.get_text())

    def get_param_val(self):
        return int(self.entry_param_val.get_text())

class DialogDataRequest(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Data Request", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Data Type ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_data_id = Gtk.Entry()

        label2 = Gtk.Label(label="Start Timestamp:")
        label2.set_halign(Gtk.Align.START)
        self.entry_start_ts = Gtk.Entry()

        label3 = Gtk.Label(label="End Timestamp:")
        label3.set_halign(Gtk.Align.START)
        self.entry_end_ts = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(label3, 0, 2, 1, 1)
        grid.attach(self.entry_data_id, 1, 0, 1, 1)
        grid.attach(self.entry_start_ts, 1, 1, 1, 1)
        grid.attach(self.entry_end_ts, 1, 2, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_data_id(self):
        return int(self.entry_data_id.get_text())

    def get_start_ts(self):
        return int(self.entry_start_ts.get_text())

    def get_end_ts(self):
        return int(self.entry_end_ts.get_text())

class DialogGetPayloadData(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Get Payload Data", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Payload ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_pl_id = Gtk.Entry()

        label2 = Gtk.Label(label="Payload Arguments:")
        label2.set_halign(Gtk.Align.START)
        self.entry_pl_args = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_pl_id, 1, 0, 1, 1)
        grid.attach(self.entry_pl_args, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_pl_id(self):
        return int(self.entry_pl_id.get_text())

    def get_pl_args(self):
        return eval(self.entry_pl_args.get_text())

class DialogBroadcastMessage(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Broadcast Message", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Destination Callsign:")
        label.set_halign(Gtk.Align.START)
        self.entry_dst_callsign = Gtk.Entry()

        label2 = Gtk.Label(label="Message:")
        label2.set_halign(Gtk.Align.START)
        self.entry_message = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_dst_callsign, 1, 0, 1, 1)
        grid.attach(self.entry_message, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_dst_callsign(self):
        return self.entry_dst_callsign.get_text()

    def get_message(self):
        return self.entry_message.get_text()

class DialogTransmitPacket(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Transmit Packet", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Data:")
        label.set_halign(Gtk.Align.START)
        self.entry_data = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_deactivate_mod_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_data(self):
        return ast.literal_eval(self.entry_data.get_text())
