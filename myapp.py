import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket
import datetime
from plyer import notification
from tkinter import PhotoImage
import os

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        self.icon = self.resize_icon("YAŞAR.png", (64, 64))  # İkona yeni boyutu uygulayın
        self.root.iconphoto(False, self.icon)

        self.setup_ui()

    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur."""
        # Arka Plan Görseli
        self.bg_image = Image.open("b.jpg")
        self.bg_image = self.bg_image.resize((800, 400), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Çerçeve
        self.main_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.75, relheight=0.5)

        # Ortadaki Yeşil Çizgi
        self.green_line = tk.Frame(self.main_frame, bg='#4CAF50', width=2)
        self.green_line.place(relx=0.5, rely=0, relheight=1)

        # Sol taraf logo
        self.setup_logo_frame()

        # Sağ taraf giriş alanı
        self.setup_login_frame()

    def setup_logo_frame(self):
        """Logo çerçevesini oluşturur."""
        self.logo_frame = tk.Frame(self.main_frame, bg='#ffffff', padx=20, pady=20)
        self.logo_frame.place(relx=0.25, rely=0.5, anchor='center')
        self.logo_image = Image.open("YAŞAR.png")  # Logo dosya yolu
        self.logo_image = self.logo_image.resize((200, 200), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.logo_frame, image=self.logo_photo, bg='#ffffff')
        self.logo_label.pack()

    def setup_login_frame(self):
        """Giriş çerçevesini oluşturur."""
        self.login_frame = tk.Frame(self.main_frame, bg='#ffffff', padx=20, pady=20)
        self.login_frame.place(relx=0.75, rely=0.5, anchor='center')

        # Başlık
        self.title_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 14), bg='#ffffff')
        self.title_label.pack(pady=(10, 5))

        # Kullanıcı Adı Giriş Alanı
        self.entry_username = tk.Entry(self.login_frame, font=("Arial", 14), bg='#f0f0f0', bd=0, highlightthickness=0)
        self.entry_username.pack()

        # Şifre Alanı
        self.label_password = tk.Label(self.login_frame, text="Password:", font=("Arial", 14), bg='#ffffff')
        self.label_password.pack(pady=(10, 5))
        self.entry_password = tk.Entry(self.login_frame, show="*", font=("Arial", 14), bg='#f0f0f0', bd=0, highlightthickness=0)
        self.entry_password.pack()

        # Giriş Butonu
        self.button_login = tk.Button(self.login_frame, text="Login", command=self.login, font=("Arial", 14), bg='#4CAF50', fg='white', bd=0, highlightthickness=0)
        self.button_login.pack(pady=20)

    def login(self):
        """Giriş butonuna tıklandığında çalıştırılır."""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "YaşarHospital" and password == "12345":
            self.open_notification_app()
        else:
            messagebox.showerror("Error", "Invalid username or password")
            # Giriş alanlarını temizle
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)

    def open_notification_app(self):
        """Bildirim uygulamasını açar."""
        self.root.destroy()
        root = tk.Tk()
        app = NotificationApp(root)
        root.mainloop()

    def resize_icon(self, filename, size):
        """İkonu yeniden boyutlandırır."""
        icon_image = Image.open(filename)
        icon_image = icon_image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(icon_image)
class NotificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yaşar Hospital")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.icon = PhotoImage(file='Adsız tasarım (1).png')
        self.root.iconphoto(False, self.icon)

        self.setup_ui()
        self.notifications = []
        self.listen_notifications()

    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur."""
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.photo_label = tk.Label(self.frame)
        self.photo_label.pack()

        self.label = tk.Label(self.frame, text="latest notifications:", font=("Arial", 14))
        self.label.pack()

        self.notification_listbox = tk.Listbox(self.frame, font=("Arial", 12), height=10)
        self.notification_listbox.pack(expand=True, fill=tk.BOTH, pady=10)

    def listen_notifications(self):
        """UDP soketi üzerinden bildirimleri dinler."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        self.receive_notification()

    def receive_notification(self):
        """Bildirim alır ve ekranda görüntüler."""
        data, addr = self.sock.recvfrom(1024)
        message = data.decode()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        message_with_time = f"[{current_time}] {message}"

        self.notifications.insert(0, message_with_time)
        self.update_notification_listbox(message)
        self.display_image_for_notification(message)

        notification.notify(
            title='Bildirim',
            message=message,
            app_name='Python Script',
            timeout=5
        )
        self.root.after(1000, self.receive_notification)

    def update_notification_listbox(self, message):
        """Bildirim listesine yeni bildirim ekler."""
        self.notification_listbox.delete(0, tk.END)
        for idx, notification in enumerate(self.notifications):
            self.notification_listbox.insert(tk.END, notification)
            if idx == 0:
                if "patient is moving" in message.lower():
                    self.notification_listbox.itemconfig(0, {'bg': 'red', 'fg': 'white'})
                else:
                    self.notification_listbox.itemconfig(0, {'bg': 'yellow', 'fg': 'black'})

    
    def display_image_for_notification(self, message):
        """Bildirime göre ilgili görüntüyü ekranda gösterir."""
        base_image_path = None

        if "patient is moving" in message.lower():
            base_image_path = "yatak_hastalı_Ayakta.png"
        elif "patient is in bed" in message.lower():
            base_image_path = "yatak_hastalı.png"

        if base_image_path:
            print(f"Base image path selected: {base_image_path}")
            img = Image.open(base_image_path)
            img = img.resize((400, 400), Image.LANCZOS)

            if "high temperature detected" in message.lower():
                print("High temperature detected. Adding fire icon.")
                img = self.overlay_image(img, "fire icon.png")
                if img:
                    print("Fire icon successfully added.")
                else:
                    print("Failed to add fire icon.")
            else:
                print("No high temperature detected. Using base image.")

            photo = ImageTk.PhotoImage(img)
            self.photo_label.config(image=photo)
            self.photo_label.image = photo
        else:
            print("No base image path selected.")

    def overlay_image(self, base_img, overlay_path):
        """Bir görüntünün üzerine başka bir görüntü ekler."""
        try:
            # Overlay görüntüsünü yükle ve boyutlandır
            overlay = Image.open(overlay_path)
            overlay = overlay.resize((100, 100), Image.LANCZOS)
            print("Overlay image opened and resized.")

            # Overlay görüntüsünün RGBA formatında olduğundan emin ol
            if overlay.mode != 'RGBA':
                overlay = overlay.convert('RGBA')
                print("Overlay image converted to RGBA.")

            # Base görüntüsünün RGBA formatında olduğundan emin ol
            if base_img.mode != 'RGBA':
                base_img = base_img.convert('RGBA')
                print("Base image converted to RGBA.")

            # Şeffaf bir görüntü oluştur
            transparent = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
            print("Transparent image created.")

            # Base görüntüsünü şeffaf görüntüye yapıştır
            transparent.paste(base_img, (0, 0))
            print("Base image pasted onto transparent image.")

            # Overlay görüntüsünü sağ üst köşeye yapıştır
            position = (base_img.width - overlay.width, 0)
            transparent.paste(overlay, position, overlay)
            print(f"Overlay image pasted at position {position}.")

            return transparent
        except Exception as e:
            print(f"Error in overlay_image: {e}")
            return None


if __name__ == "__main__":
    UDP_IP = "172.20.10.2"
    UDP_PORT = 50001

    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop() 