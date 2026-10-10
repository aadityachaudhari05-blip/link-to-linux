import sys
import gi
import socket
import qrcode
import tempfile
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

class LinkToLinuxApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.mrunu.LinkToLinux')

    def do_activate(self):
        # 1. Create the main application window
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Link to Linux")
        window.set_default_size(450, 500)

        # 2. Setup the layout container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box.set_margin_top(30)
        box.set_margin_bottom(30)
        box.set_margin_start(30)
        box.set_margin_end(30)

        # 3. Add UI Labels (Title & IP info)
        title_label = Gtk.Label(label="Link to Linux")
        box.append(title_label)

        ip_address = get_local_ip()
        ip_label = Gtk.Label(label=f"Your PC IP Address: {ip_address}")
        box.append(ip_label)

        self.status_label = Gtk.Label(label="Ready to connect. Make sure your phone is on the same Wi-Fi.")
        box.append(self.status_label)

        # 4. Add the Generation Action Button
        pair_button = Gtk.Button(label="Generate Pairing QR")
        pair_button.connect('clicked', self.on_pair_clicked)
        box.append(pair_button)

        # 5. Add the Visual QR Image (Scaled to 250px)
        self.qr_image = Gtk.Image()
        self.qr_image.set_vexpand(True)
        self.qr_image.set_hexpand(True)
        self.qr_image.set_pixel_size(250)
        box.append(self.qr_image)

        window.set_child(box)
        window.present()

    def on_pair_clicked(self, button):
        ip_address = get_local_ip()
        self.status_label.set_text("QR Code Generated! Scan this with your phone app.")
        
        # Build the internal data structure for the QR code matrix
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(f"LINK_TO_LINUX:{ip_address}")
        qr.make(fit=True)
        
        # Render and save the image out to a temporary folder location
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"{tempfile.gettempdir()}/pair_qr.png"
        img.save(img_path)
        
        # Display the crisp, scaled file natively on your app canvas
        self.qr_image.set_from_file(img_path)
        print(f"QR code successfully displayed from path: {img_path}")

if __name__ == '__main__':
    app = LinkToLinuxApp()
    sys.exit(app.run(sys.argv))
