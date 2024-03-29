import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class DialogEnterHibernation(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Enter Hibernation", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Hibernation duration in hours:")
        self.entry_hours = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_hours, 0, 1, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_hours(self):
        return int(self.entry_hours.get_text())

class DialogDeactivateModule(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Deactivate Module", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Module ID:")
        self.entry_deactivate_mod_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_deactivate_mod_id, 0, 1, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_deac_mod_id(self):
        return int(self.entry_deactivate_mod_id.get_text())

class DialogActivateModule(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Activate Module", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Module ID:")
        self.entry_activate_mod_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_activate_mod_id, 0, 1, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_ac_mod_id(self):
        return int(self.entry_activate_mod_id.get_text())

class DialogDeactivatePayload(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Deactivate Payload", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Payload ID:")
        self.entry_deactivate_pl_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_deactivate_pl_id, 0, 1, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_deac_pl_id(self):
        return int(self.entry_deactivate_pl_id.get_text())

class DialogActivatePayload(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Activate Payload", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Payload ID:")
        self.entry_activate_pl_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(self.entry_activate_pl_id, 0, 1, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_ac_pl_id(self):
        return int(self.entry_activate_pl_id.get_text())


class DialogGetParameter(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Get Parameter", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Subsystem ID:")
        self.entry_subsys_id = Gtk.Entry()

        label2 = Gtk.Label(label="Parameter ID:")
        self.entry_param_id = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(label2, 0, 2, 1, 1)
        grid.attach(self.entry_subsys_id, 0, 1, 1, 1)
        grid.attach(self.entry_param_id, 0, 3, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_subsys_id(self):
        return int(self.entry_subsys_id.get_text())

    def get_param_id(self):
        return int(self.entry_param_id.get_text())

    
class DialogSetParameter(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Set Parameter", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Subsystem ID:")
        self.entry_subsys_id = Gtk.Entry()

        label2 = Gtk.Label(label="Parameter ID:")
        self.entry_param_id = Gtk.Entry()

        label3 = Gtk.Label(label="Parameter Value:")
        self.entry_param_val = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(label2, 0, 2, 1, 1)
        grid.attach(label3, 0, 4, 1, 1)
        grid.attach(self.entry_subsys_id, 0, 1, 1, 1)
        grid.attach(self.entry_param_id, 0, 3, 1, 1)
        grid.attach(self.entry_param_val, 0, 5, 1, 1)

        box = self.get_content_area()
        box.add(grid)

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
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Data Type ID:")
        self.entry_data_id = Gtk.Entry()

        label2 = Gtk.Label(label="Start Timestamp:")
        self.entry_start_ts = Gtk.Entry()

        label3 = Gtk.Label(label="End Timestamp:")
        self.entry_end_ts = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(label2, 0, 2, 1, 1)
        grid.attach(label3, 0, 4, 1, 1)
        grid.attach(self.entry_data_id, 0, 1, 1, 1)
        grid.attach(self.entry_start_ts, 0, 3, 1, 1)
        grid.attach(self.entry_end_ts, 0, 5, 1, 1)

        box = self.get_content_area()
        box.add(grid)

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
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="Payload ID:")
        self.entry_pl_id = Gtk.Entry()

        label2 = Gtk.Label(label="Payload Arguments:")
        self.entry_pl_args = Gtk.Entry()

        grid = Gtk.Grid()
        grid.add(label)
        grid.attach(label2, 0, 2, 1, 1)
        grid.attach(self.entry_pl_id, 0, 1, 1, 1)
        grid.attach(self.entry_pl_args, 0, 3, 1, 1)

        box = self.get_content_area()
        box.add(grid)

        self.show_all()

    def get_pl_id(self):
        return int(self.entry_pl_id.get_text())

    def get_pl_args(self):
        return eval(self.entry_pl_args.get_text())