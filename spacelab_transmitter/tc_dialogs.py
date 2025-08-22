#
#  tc_dialogs.py
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

import datetime
import calendar

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

        liststore_types = Gtk.ListStore(str)
        items = ["bool", "uint8", "int8", "uint16", "int16", "uint32", "int32", "uint64", "int64", "float", "double", "string"]
        for item in items:
            liststore_types.append([item])
        label3 = Gtk.Label(label="Parameter Type:")
        label3.set_halign(Gtk.Align.START)
        self.combobox_param_type = Gtk.ComboBox.new_with_model(liststore_types)
        cell = Gtk.CellRendererText()
        self.combobox_param_type.pack_start(cell, True)
        self.combobox_param_type.add_attribute(cell, "text", 0)
        self.combobox_param_type.set_active(3)

        label4 = Gtk.Label(label="Parameter Value:")
        label4.set_halign(Gtk.Align.START)
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
        grid.attach(label4, 0, 3, 1, 1)
        grid.attach(self.entry_subsys_id, 1, 0, 1, 1)
        grid.attach(self.entry_param_id, 1, 1, 1, 1)
        grid.attach(self.combobox_param_type, 1, 2, 1, 1)
        grid.attach(self.entry_param_val, 1, 3, 1, 1)

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

    def get_param_type(self):
        param_type = self.combobox_param_type.get_active()
        if param_type is not None:
            if param_type == 0:
                return str("bool")
            elif param_type == 1:
                return str("uint8")
            elif param_type == 2:
                return str("int8")
            elif param_type == 3:
                return str("uint16")
            elif param_type == 4:
                return str("int16")
            elif param_type == 5:
                return str("uint32")
            elif param_type == 6:
                return str("int32")
            elif param_type == 7:
                return str("uint64")
            elif param_type == 8:
                return str("int64")
            elif param_type == 9:
                return str("flt")
            elif param_type == 10:
                return str("dbl")
            elif param_type == 11:
                return str("str")
            else:
                return str("ukn")

    def get_param_val(self):
        return self.entry_param_val.get_text()

class DialogDataRequest(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Data Request", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Data Type ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_data_id = Gtk.Entry()

        label2 = Gtk.Label(label="Start Page:")
        label2.set_halign(Gtk.Align.START)
        self.entry_start_page = Gtk.Entry()

        label3 = Gtk.Label(label="End Page:")
        label3.set_halign(Gtk.Align.START)
        self.entry_end_page = Gtk.Entry()

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
        grid.attach(self.entry_start_page, 1, 1, 1, 1)
        grid.attach(self.entry_end_page, 1, 2, 1, 1)

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

    def get_start_page(self):
        return int(self.entry_start_page.get_text())

    def get_end_page(self):
        return int(self.entry_end_page.get_text())

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
        grid.attach(self.entry_data, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_data(self):
        return eval(self.entry_data.get_text())

class DialogEraseMemory(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Erase Memory", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Memory ID:")
        label.set_halign(Gtk.Align.START)
        self.entry_mem_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_mem_id, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_mem_id(self):
        return int(self.entry_mem_id.get_text())

class DialogUpdateTLE(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Update TLE", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="TLE Line 1:")
        label.set_halign(Gtk.Align.START)
        self.entry_tle_line_1 = Gtk.Entry()
        self.entry_tle_line_1.set_max_length(69)
        self.entry_tle_line_1.set_width_chars(69)
        self.entry_tle_line_1.set_max_width_chars(69)

        label2 = Gtk.Label(label="TLE Line 2:")
        label2.set_halign(Gtk.Align.START)
        self.entry_tle_line_2 = Gtk.Entry()
        self.entry_tle_line_2.set_max_length(69)
        self.entry_tle_line_2.set_width_chars(69)
        self.entry_tle_line_2.set_max_width_chars(69)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_tle_line_1, 1, 0, 1, 1)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_tle_line_2, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_tle_line_1(self):
        return self.entry_tle_line_1.get_text()

    def get_tle_line_2(self):
        return self.entry_tle_line_2.get_text()

class DialogCSPPeek(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="CSP Peek", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Memory Address:")
        label.set_halign(Gtk.Align.START)
        self.entry_mem_adr = Gtk.Entry()

        label2 = Gtk.Label(label="Length [bytes]:")
        label2.set_halign(Gtk.Align.START)
        self.entry_mem_len = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_mem_adr, 1, 0, 1, 1)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_mem_len, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_csp_mem_adr(self):
        return int(self.entry_mem_adr.get_text())

    def get_csp_mem_len(self):
        return int(self.entry_mem_len.get_text())

class DialogCSPPoke(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="CSP Poke", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Memory Address:")
        label.set_halign(Gtk.Align.START)
        self.entry_mem_adr = Gtk.Entry()

        label2 = Gtk.Label(label="Data:")
        label2.set_halign(Gtk.Align.START)
        self.entry_mem_data = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_mem_adr, 1, 0, 1, 1)
        grid.attach(label2, 0, 1, 1, 1)
        grid.attach(self.entry_mem_data, 1, 1, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_csp_mem_adr(self):
        return int(self.entry_mem_adr.get_text())

    def get_csp_mem_data(self):
        return eval(self.entry_mem_data.get_text())

class DialogCSPIFStat(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="CSP IF Status", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="IF Name:")
        label.set_halign(Gtk.Align.START)
        self.entry_if_name = Gtk.Entry()
        self.entry_if_name.set_max_length(11)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.add(label)
        grid.attach(self.entry_if_name, 1, 0, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_csp_if_name(self):
        return self.entry_if_name.get_text()

class DialogCSPRouteSet(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="CSP Route Set", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Destination Node:")
        label.set_halign(Gtk.Align.START)
        self.entry_dest_node = Gtk.Entry()

        label2 = Gtk.Label(label="Nest hop MAC:")
        label2.set_halign(Gtk.Align.START)
        self.entry_next_hop_mac = Gtk.Entry()

        label3 = Gtk.Label(label="Interface:")
        label3.set_halign(Gtk.Align.START)
        self.entry_if_name = Gtk.Entry()
        self.entry_if_name.set_max_length(11)

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
        grid.attach(self.entry_dest_node, 1, 0, 1, 1)
        grid.attach(self.entry_next_hop_mac, 1, 1, 1, 1)
        grid.attach(self.entry_if_name, 1, 2, 1, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.show_all()

    def get_dest_node(self):
        return int(self.entry_dest_node.get_text())

    def get_next_hop_mac(self):
        return int(self.entry_next_hop_mac.get_text())

    def get_if_name(self):
        return self.entry_if_name.get_text()

class DialogScheduleTC(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Schedule Telecommand", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Datetime:")
        label.set_halign(Gtk.Align.START)
        self.entry_ts = Gtk.Entry()

        adjustment_hour = Gtk.Adjustment(lower=0, upper=23, step_increment=1, page_increment=10)
        adjustment_min = Gtk.Adjustment(lower=0, upper=59, step_increment=1, page_increment=10)
        adjustment_sec = Gtk.Adjustment(lower=0, upper=59, step_increment=1, page_increment=10)
        adjustment_year = Gtk.Adjustment(lower=2025, upper=3000, step_increment=1, page_increment=10)
        adjustment_day = Gtk.Adjustment(lower=1, upper=31, step_increment=1, page_increment=10)

        self.spinbutton_hour = Gtk.SpinButton()
        self.spinbutton_hour.set_adjustment(adjustment_hour)
        self.spinbutton_hour.set_range(0, 23)
        self.spinbutton_hour.set_orientation(Gtk.Orientation.VERTICAL)
        self.label_hour_sep = Gtk.Label(label=":")
        self.spinbutton_min = Gtk.SpinButton()
        self.spinbutton_min.set_adjustment(adjustment_min)
        self.spinbutton_min.set_range(0, 59)
        self.spinbutton_min.set_orientation(Gtk.Orientation.VERTICAL)
        self.label_min_sep = Gtk.Label(label=":")
        self.spinbutton_sec = Gtk.SpinButton()
        self.spinbutton_sec.set_adjustment(adjustment_sec)
        self.spinbutton_sec.set_range(0, 59)
        self.spinbutton_sec.set_orientation(Gtk.Orientation.VERTICAL)
        self.label_year = Gtk.Label(label="Year:")
        self.spinbutton_year = Gtk.SpinButton()
        self.spinbutton_year.set_adjustment(adjustment_year)
        self.spinbutton_year.set_range(2025, 3000)
        self.spinbutton_year.connect("changed", self.on_spinbutton_year_changed)
        self.label_month = Gtk.Label(label="Month:")
        self.combobox_month = Gtk.ComboBoxText()
        self.combobox_month.append_text("January")
        self.combobox_month.append_text("February")
        self.combobox_month.append_text("March")
        self.combobox_month.append_text("April")
        self.combobox_month.append_text("May")
        self.combobox_month.append_text("June")
        self.combobox_month.append_text("July")
        self.combobox_month.append_text("August")
        self.combobox_month.append_text("Septembe")
        self.combobox_month.append_text("October")
        self.combobox_month.append_text("November")
        self.combobox_month.append_text("Dezember")
        self.combobox_month.set_active(0)
        self.combobox_month.connect("changed", self.on_combobox_month_changed)
        self.label_day = Gtk.Label(label="Day:")
        self.spinbutton_day = Gtk.SpinButton()
        self.spinbutton_day.set_adjustment(adjustment_day)
        self.spinbutton_day.set_range(1, 31)

        label2 = Gtk.Label(label="TC ID:")
        label2.set_halign(Gtk.Align.START)
        self.entry_tc_id = Gtk.Entry()

        label3 = Gtk.Label(label="Parameters:")
        label3.set_halign(Gtk.Align.START)
        self.entry_params = Gtk.Entry()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)

        grid.attach(label, 0, 0, 1, 3)
        grid.attach(label2, 0, 3, 1, 1)
        grid.attach(label3, 0, 4, 1, 1)
        grid.attach(self.spinbutton_hour, 1, 0, 1, 3)
        grid.attach(self.label_hour_sep, 2, 0, 1, 3)
        grid.attach(self.spinbutton_min, 3, 0, 1, 3)
        grid.attach(self.label_min_sep, 4, 0, 1, 3)
        grid.attach(self.spinbutton_sec, 5, 0, 1, 3)
        grid.attach(self.label_year, 6, 0, 1, 1)
        grid.attach(self.label_month, 6, 1, 1, 1)
        grid.attach(self.label_day, 6, 2, 1, 1)
        grid.attach(self.spinbutton_year, 7, 0, 1, 1)
        grid.attach(self.combobox_month, 7, 1, 1, 1)
        grid.attach(self.spinbutton_day, 7, 2, 1, 1)
        grid.attach(self.entry_tc_id, 1, 3, 7, 1)
        grid.attach(self.entry_params, 1, 4, 7, 1)

        box_content = self.get_content_area()
        box_content.add(grid)

        box_buttons = self.get_action_area()
        grid.set_column_spacing(10)
        box_buttons.set_margin_start(10)
        box_buttons.set_margin_end(10)
        box_buttons.set_margin_bottom(5)

        self.set_datetime(datetime.datetime.now())

        self.show_all()

    def on_spinbutton_year_changed(self, spinbutton):
        self.spinbutton_day.set_range(1, calendar.monthrange(int(self.spinbutton_year.get_value()), self.combobox_month.get_active() + 1)[1])

    def on_combobox_month_changed(self, combobox):
        self.spinbutton_day.set_range(1, calendar.monthrange(int(self.spinbutton_year.get_value()), self.combobox_month.get_active() + 1)[1])

    def set_datetime(self, dt):
        self.spinbutton_hour.set_value(dt.hour)
        self.spinbutton_min.set_value(dt.minute)
        self.spinbutton_sec.set_value(dt.second)
        self.spinbutton_year.set_value(dt.year)
        self.combobox_month.set_active(dt.month-1)
        self.spinbutton_day.set_value(dt.day)

    def get_ts(self):
        dt = datetime.datetime(int(self.spinbutton_year.get_value()),
                               self.combobox_month.get_active() + 1,
                               int(self.spinbutton_day.get_value()),
                               int(self.spinbutton_hour.get_value()),
                               int(self.spinbutton_min.get_value()),
                               int(self.spinbutton_sec.get_value()))

        return int(dt.timestamp())

    def get_tc_id(self):
        return int(self.entry_tc_id.get_text())

    def get_params(self):
        return eval(self.entry_params.get_text())

class DialogPassword(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Authentication", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        label = Gtk.Label(label="Key:")
        self.entry_password = Gtk.Entry()
        self.entry_password.set_visibility(False)

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
