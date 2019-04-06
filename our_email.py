import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from watermark import *
from certificate import *


mail_whitelist = ["mail1@lego.com", "mail2@lego.com"]

serial_number = {
    "12345" : False,
    "54321" : True,
    "99999" : True,
    "11111" : True,
}

mail_window = Gtk.Window()

receiver_field = Gtk.Entry()
receiver_field.set_hexpand(True)
subject_field = Gtk.Entry()
subject_field.set_hexpand(True)
text_field = Gtk.TextView()
text_field.set_vexpand(True)
attach_button = Gtk.Button("Attach")
send_button = Gtk.Button("Send")
label_receiver = Gtk.Label("Receiver: ")
label_subject = Gtk.Label("Subject:   ")

email_info = []
serial_numbers = []
img_names = []
watermark = None

load_images = []

cert = ""

def attach_file(button):
	image_filter = Gtk.FileFilter()
	image_filter.set_name("png/jpg")
	image_filter.add_mime_type("image/jpeg")
	image_filter.add_mime_type("image/png")
	cert_filter = Gtk.FileFilter()
	cert_filter.set_name("certificate")
	cert_filter.add_mime_type("text/plain")
	c_file_chooser =  Gtk.FileChooserDialog("Please choose a certificate", mail_window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
	c_file_chooser.add_filter(cert_filter)
	c_file_chooser.add_filter(image_filter)
	response = c_file_chooser.run()
	filename = ""
	if response == Gtk.ResponseType.OK and c_file_chooser.get_filter() == cert_filter:
		global cert
		cert = c_file_chooser.get_filename()
		cert = readfile(cert)
	if response == Gtk.ResponseType.OK and c_file_chooser.get_filter() == image_filter:
		global load_images
		load_images.append(c_file_chooser.get_filename())
		print(load_images)
	else:
		c_file_chooser.destroy()
		return
	c_file_chooser.destroy()

def send_file(button):
	print(cert)
	(b, s) = certify(cert, [receiver_field.get_text()])
	print(s)

hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
hbox1.add(label_receiver)
hbox1.add(receiver_field)
hbox1.add(attach_button)
hbox1.add(send_button)

hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
hbox2.add(label_subject)
hbox2.add(subject_field)

box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
box.add(hbox1)
box.add(hbox2)
box.add(text_field)

attach_button.connect("clicked", attach_file)
send_button.connect("clicked", send_file)

mail_window.add(box)
mail_window.show_all()
mail_window.connect("destroy", Gtk.main_quit)