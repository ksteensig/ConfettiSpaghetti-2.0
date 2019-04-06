import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

def create_label(text):
	e = Gtk.Label()
	e.set_text(text)
	return e

c_cert_assistant = Gtk.Assistant()
c_info_grid = Gtk.Grid()
c_info_grid.set_row_spacing(6)
c_info_grid.set_column_spacing(20)

c_your_name = create_label("Your name")
c_your_mail = create_label("Your email")
c_their_name = create_label("Their name")
c_their_mail = create_label("Their email")

c_enter_your_name = Gtk.Entry()
c_enter_your_mail = Gtk.Entry()
c_enter_their_name = Gtk.Entry()
c_enter_their_mail = Gtk.Entry()

c_cert_assistant.append_page(c_info_grid)

c_info_grid.attach(c_your_name, 0, 0, 1, 1)
c_info_grid.attach(c_your_mail, 0, 1, 1, 1)
c_info_grid.attach(c_their_name, 0, 2, 1, 1)
c_info_grid.attach(c_their_mail, 0, 3, 1, 1)

c_info_grid.attach(c_enter_your_name, 1, 0, 1, 1)
c_info_grid.attach(c_enter_your_mail, 1, 1, 1, 1)
c_info_grid.attach(c_enter_their_name, 1, 2, 1, 1)
c_info_grid.attach(c_enter_their_mail, 1, 3, 1, 1)

c_cert_assistant.append_page(c_info_grid)

#mail_window = Gtk.Window()

c_cert_assistant.connect("close", lambda a: Gtk.main_quit())
c_cert_assistant.connect("cancel", lambda a: Gtk.main_quit())
c_cert_assistant.show_all()
#mail_window.connect("destroy", Gtk.main_quit)
#mail_window.show_all()
Gtk.main()
