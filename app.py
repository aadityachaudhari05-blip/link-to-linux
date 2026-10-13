import sys
import socket
import tempfile
from pathlib import Path

import gi
import qrcode

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


SERVER_PORT = 8765


def get_local_ip():
    """Find the laptop's local network IP address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


class LinkToLinuxApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.mrunu.LinkToLinux")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Link to Linux")
        window.set_default_size(450, 550)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=15,
        )
        box.set_margin_top(30)
        box.set_margin_bottom(30)
        box.set_margin_start(30)
        box.set_margin_end(30)

        title = Gtk.Label(label="Link to Linux")
        title.set_markup("<span size='xx-large' weight='bold'>Link to Linux</span>")
        box.append(title)

        self.ip_address = get_local_ip()
        ip_label = Gtk.Label(
            label=f"Laptop IP address: {self.ip_address}"
        )
        box.append(ip_label)

        self.status_label = Gtk.Label(
            label="Connect your phone to the same Wi-Fi network."
        )
        self.status_label.set_wrap(True)
        box.append(self.status_label)

        pair_button = Gtk.Button(label="Generate Pairing QR")
        pair_button.connect("clicked", self.on_pair_clicked)
        box.append(pair_button)

        self.qr_image = Gtk.Image()
        self.qr_image.set_pixel_size(250)
        self.qr_image.set_vexpand(True)
        box.append(self.qr_image)

        window.set_child(box)
        window.present()

    def on_pair_clicked(self, button):
        self.ip_address = get_local_ip()

        # The QR code contains a real URL that opens the laptop's server.
        pairing_url = (
            f"http://{self.ip_address}:{SERVER_PORT}/pair"
        )

        qr = qrcode.QRCode(
            version=None,
            box_size=8,
            border=4,
        )
        qr.add_data(pairing_url)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        image_path = Path(tempfile.gettempdir()) / "link-to-linux-qr.png"
        image.save(image_path)

        self.qr_image.set_from_file(str(image_path))
        self.status_label.set_text(
            "QR code ready! Scan it with your phone while both devices "
            "are connected to the same Wi-Fi network."
        )

        print(f"Pairing URL: {pairing_url}", flush=True)


if __name__ == "__main__":
    app = LinkToLinuxApp()
    sys.exit(app.run(sys.argv))
