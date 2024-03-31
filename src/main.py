import gi
gi.require_version("Gtk","4.0")
gi.require_version("Gdk","4.0")
from view import window
from gi.repository import Gtk
import settings
import storage
import sys
import control
class application(Gtk.Application, control.control, storage.storage):
    def __init__(self):
        Gtk.Application.__init__(self,
            application_id=settings.PACKAGE_NAME
        )
        self.connect('activate', self.activate)

    @property
    def data(self):
        return self.read()

    def activate(self,*args):
        win = window(app=self)
        win.present()

sys.exit(
    application()
    .run([])
)
