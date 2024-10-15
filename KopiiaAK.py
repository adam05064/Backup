import os
import shutil
import time
import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, smtp_server, port, sender_email, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, subject, body, recipient_email):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            print("Wiadomość została wysłana pomyślnie!")
        except Exception as e:
            print(f"Błąd podczas wysyłania e-maila: {e}")


def copy_files(src, dst):
    """
    Funkcja kopiuje pliki z katalogu źródłowego do katalogu docelowego, nie nadpisując istniejących plików.
    """
    for root, dirs, files in os.walk(src):
        relative_path = os.path.relpath(root, src)
        destination_path = os.path.join(dst, relative_path)

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(destination_path, file)

            # Sprawdzenie, czy plik już istnieje, jeśli tak - dodajemy timestamp do nazwy
            if os.path.exists(dst_file):
                base, ext = os.path.splitext(file)
                timestamp = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
                dst_file = os.path.join(destination_path, f"{base}_{timestamp}{ext}")

            shutil.copy2(src_file, dst_file)  # Kopiowanie pliku z zachowaniem metadanych


def backup(source, destination, email_sender):
    try:
        # Sprawdzenie, czy katalog źródłowy istnieje i czy zawiera pliki
        if not os.path.exists(source):
            raise Exception(f"Katalog źródłowy {source} nie istnieje.")

        if not os.listdir(source):
            raise Exception(f"Katalog źródłowy {source} jest pusty.")

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Rozpoczęcie kopii zapasowej: {start_time}")

        copy_files(source, destination)

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Kopia zapasowa zakończona pomyślnie o: {end_time}")
        email_sender.send_email(
            "Kopia zapasowa",
            f"Kopia została wykonana pomyślnie o {end_time}",
            "adam.korzepa98@gmail.com"
        )

    except Exception as e:
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Błąd w trakcie wykonywania kopii zapasowej: {e}")
        email_sender.send_email(
            "Błąd kopii zapasowej",
            f"Błąd w trakcie wykonywania kopii zapasowej o {end_time}: {e}",
            "adam.korzepa98@gmail.com"
        )


if __name__ == "__main__":
    # Konfiguracja serwera e-mail
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "pythonprojektautomat@gmail.com"
    password = "nzpayfsabkktgxgo"

    # Tworzenie obiektu EmailSender
    email_sender = EmailSender(smtp_server, port, sender_email, password)

    # Ścieżki do katalogów
    source = "C:\\Kopia"
    destination = "C:\\Kopia2"

    # Wykonywanie kopii zapasowej
    backup(source, destination, email_sender)
