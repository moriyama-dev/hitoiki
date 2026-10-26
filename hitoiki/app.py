import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk  # noqa: E402

from hitoiki import APP_ID, APP_NAME, VERSION  # noqa: E402
from hitoiki import report  # noqa: E402


class HitoikiWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=APP_NAME)
        self.set_default_size(360, 420)

        label = Gtk.Label(label="25:00")
        label.add_css_class("title-1")

        # メインメニュー：GitHub、問題を報告、Hitoiki について
        menu = Gio.Menu()
        links = Gio.Menu()
        links.append("GitHub", "app.github")
        links.append("問題を報告", "app.report-problem")
        menu.append_section(None, links)
        menu.append("Hitoiki について", "app.about")
        menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic", menu_model=menu, tooltip_text="メニュー")

        header = Adw.HeaderBar()
        header.pack_end(menu_button)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(label)
        self.set_content(toolbar)


class HitoikiApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)
        for name, callback in (
            ("github", self.on_github),
            ("report-problem", self.on_report_problem),
            ("about", self.on_about),
        ):
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)

    def open_url(self, url):
        Gtk.UriLauncher.new(url).launch(self.props.active_window, None, None, None)

    def on_github(self, *_):
        self.open_url(report.REPOSITORY_URL)

    def on_report_problem(self, *_):
        gtk = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        adw = f"{Adw.get_major_version()}.{Adw.get_minor_version()}.{Adw.get_micro_version()}"
        self.open_url(report.issue_url(gtk, adw))

    def on_about(self, *_):
        # 「問題を報告」と「Web サイト（GitHub）」のボタンは libadwaita の情報画面が付ける
        about = Adw.AboutDialog(
            application_name=APP_NAME,
            application_icon=APP_ID,
            version=VERSION,
            developer_name="moriyama-dev",
            license_type=Gtk.License.GPL_3_0,
            website=report.REPOSITORY_URL,
            issue_url=report.issue_url(),
        )
        about.present(self.props.active_window)

    def do_activate(self):
        window = self.props.active_window or HitoikiWindow(self)
        window.present()


def main(argv):
    return HitoikiApp().run(argv)
