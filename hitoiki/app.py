import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from hitoiki import APP_ID, APP_NAME  # noqa: E402


class HitoikiWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=APP_NAME)
        self.set_default_size(360, 420)

        label = Gtk.Label(label="25:00")
        label.add_css_class("title-1")

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(Adw.HeaderBar())
        toolbar.set_content(label)
        self.set_content(toolbar)


class HitoikiApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

    def do_activate(self):
        window = self.props.active_window or HitoikiWindow(self)
        window.present()


def main(argv):
    return HitoikiApp().run(argv)
