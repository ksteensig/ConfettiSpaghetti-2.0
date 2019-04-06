import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from our_email import *
from watermark import *
from certificate import *

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
c_cert_assistant.set_page_title(c_info_grid, "Add information")

c_info_grid.attach(c_your_name, 0, 0, 1, 1)
c_info_grid.attach(c_your_mail, 0, 1, 1, 1)
c_info_grid.attach(c_their_name, 0, 2, 1, 1)
c_info_grid.attach(c_their_mail, 0, 3, 1, 1)

c_info_grid.attach(c_enter_your_name, 1, 0, 1, 1)
c_info_grid.attach(c_enter_your_mail, 1, 1, 1, 1)
c_info_grid.attach(c_enter_their_name, 1, 2, 1, 1)
c_info_grid.attach(c_enter_their_mail, 1, 3, 1, 1)

c_cert_assistant.set_page_type(c_info_grid, Gtk.AssistantPageType.INTRO)
c_cert_assistant.set_page_complete(c_info_grid, True)

c_add_file_grid = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
c_add_file_grid.set_spacing(5)

c_cert_assistant.append_page(c_add_file_grid)
c_cert_assistant.set_page_type(c_add_file_grid, Gtk.AssistantPageType.CONTENT)
c_cert_assistant.set_page_title(c_add_file_grid, "Choose images")

filename_label = Gtk.Label("Filename")
serial_no_label = Gtk.Label("Serial no.")
some_hbox_for_categories = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
some_hbox_for_categories.add(Gtk.Label("         "))
some_hbox_for_categories.add(filename_label)
some_hbox_for_categories.add(serial_no_label)
serial_no_label.set_halign(Gtk.Align.END)
serial_no_label.set_hexpand(True)

c_add_file_grid.add(some_hbox_for_categories)
c_add_file_grid.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

c_add_image = Gtk.Button("+")
c_add_file_grid.add(c_add_image)

def click_button(button):
	filters = Gtk.FileFilter()
	filters.set_name("png/jpg")
	filters.add_mime_type("image/jpeg")
	filters.add_mime_type("image/png")
	c_file_chooser =  Gtk.FileChooserDialog("Please choose an image", c_cert_assistant,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
	c_file_chooser.add_filter(filters)
	response = c_file_chooser.run()
	filename = ""
	if response == Gtk.ResponseType.OK:
		filename = c_file_chooser.get_filename()
		c_cert_assistant.set_page_complete(c_add_file_grid, True)
	else:
		c_file_chooser.destroy()
		return
	c_file_chooser.destroy()
	new_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	new_button = Gtk.Button("+")
	c_add_file_grid.remove(button)

	new_label = Gtk.Label(filename)
	delete_button = Gtk.Button("x")
	new_hbox.add(delete_button)
	new_hbox.add(new_label)
	new_entry = Gtk.Entry()
	new_entry.set_halign(Gtk.Align.END)
	new_entry.set_hexpand(True)
	new_hbox.add(new_entry)
	new_hbox.set_spacing(6)
	c_add_file_grid.add(new_hbox)

	c_add_file_grid.add(new_button)
	c_add_file_grid.show_all()
	new_button.connect("clicked", click_button)
	delete_button.connect("clicked", lambda c: c_add_file_grid.remove(new_hbox))

c_add_image.connect("clicked", click_button)

c_text_result = Gtk.TextView()
c_text_result.set_cursor_visible(False)
c_text_result.set_wrap_mode(Gtk.WrapMode.WORD)
c_text_result.set_hexpand(True)
c_text_result.set_vexpand(True)
c_text_result.set_editable(False)
c_cert_assistant.append_page(c_text_result)
c_cert_assistant.set_page_type(c_text_result, Gtk.AssistantPageType.CONFIRM)
c_cert_assistant.set_page_title(c_text_result, "Confirm certificate   ")

missing_info_g = []
missing_serial_g = []

def check_info_fields(w):
	if type(w) is Gtk.Grid:
		w.foreach(check_info_fields)
	elif type(w) is Gtk.Entry:
		email_info.append(w.get_text())
		missing_info_g.append(w.get_text() != "")

def check_sn_fields(w):
	if type(w) is Gtk.Box:
		w.foreach(check_sn_fields)
	elif type(w) is Gtk.Label:
		img_names.append(w.get_text())
	elif type(w) is Gtk.Entry:
		serial_numbers.append(w.get_text())
		missing_serial_g.append(len(w.get_text()) == 5 and w.get_text().isdigit())

def f(a, p):
	if type(p) is Gtk.TextView:
		buf = p.get_buffer()
		check_info_fields(c_info_grid)
		check_sn_fields(c_add_file_grid)

		if False in missing_info_g:
			buf.insert_at_cursor("Missing information field.\n")

		if False in missing_serial_g:
			buf.insert_at_cursor("Missing serial number field.\n")

		if not False in missing_serial_g and not False in missing_info_g:
			img_names.pop(0)
			img_names.pop(0)
			img_names.pop(0)
			watermark = Watermark(*email_info)
			
			imgs = []
			print(email_info)
			print(img_names)
			print(serial_numbers)

			for i, s in zip(img_names, serial_numbers):
				with Image(filename=i) as img:
					result = watermark(img, s, True)
					result.save(filename="wm_" + i.split('/')[-1])
				imgs.append("wm_" + i.split('/')[-1])

			cert = makecertificate(imgs, [email_info[0]])
			print('cert_imgs')
			writefile('cert_imgs', cert)

			buf.insert_at_cursor("\nYour certificate:\n")
			buf.insert_at_cursor(cert)

		
		p.set_buffer(buf)

c_cert_assistant.connect('prepare', f)
c_cert_assistant.connect("close", lambda a: Gtk.main_quit())
c_cert_assistant.connect("cancel", lambda a: Gtk.main_quit())
c_cert_assistant.set_title("Watermarker")
c_cert_assistant.show_all()

mail_window.show_all()
Gtk.main()