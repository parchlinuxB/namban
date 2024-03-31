import gi
gi.require_version("Gtk","4.0")
gi.require_version("Gdk","4.0")
from view import window
from gi.repository import Gtk
import settings
import storage
import sys
class application(Gtk.Application):
    def __init__(self, getData):
        super().__init__(
            application_id=settings.PACKAGE_NAME
        )
        self.connect('activate', self.activate)
        self._getdata = getData
        # gtksettings = Gtk.Settings.get_default()
        # print(
            # gtksettings.get_property("gtk-theme-name")
        # )
        # gtksettings.set_property("gtk-theme-name", 'Adwaita-dark')

    @property
    def data(self):
        return self._getdata()

    def activate(self,*args):
        win = window(app=self)
        win.present()

sys.exit(
    application(
        storage.read
    ).run([])
)
