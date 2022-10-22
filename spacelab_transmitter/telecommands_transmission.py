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
