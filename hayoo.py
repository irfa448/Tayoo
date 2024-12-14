import os
import pyfiglet
from colorama import Fore, init
import subprocess
import webbrowser
import time
import socket
import requests
import hashlib
import telepot

# Inisialisasi Colorama
init(autoreset=True)

# Limit run (batas jumlah eksekusi program)
MAX_RUNS = 25
current_runs = 0

# Telegram Bot Token dan ID Chat
TELEGRAM_TOKEN = '7833295057:AAFrcEke_fOMzDw8vZq9ZL-0WYVIIt37mEs'  # Ganti dengan token bot Anda
CHAT_ID = '7279041792'  # Ganti dengan ID chat Anda

# Lokasi file yang ingin dipantau
MONITORED_FILE = "hayoo.py"  # Ganti dengan nama file yang ingin dipantau

# Inisialisasi Telegram bot
bot = telepot.Bot(TELEGRAM_TOKEN)

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(message):
    try:
        bot.sendMessage(CHAT_ID, message)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

# Fungsi untuk mendapatkan IP publik perangkat
def get_ip():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except requests.exceptions.RequestException:
        return "Tidak dapat mendeteksi IP"

# Fungsi untuk mengecek perubahan pada file yang dipantau
def check_file_changes():
    try:
        with open(MONITORED_FILE, "rb") as f:
            file_content = f.read()
            file_hash = hashlib.md5(file_content).hexdigest()
        
        # Cek apakah file hash berbeda dari sebelumnya (untuk mendeteksi perubahan)
        if not os.path.isfile(f"{MONITORED_FILE}.hash"):
            with open(f"{MONITORED_FILE}.hash", "w") as hash_file:
                hash_file.write(file_hash)
        else:
            with open(f"{MONITORED_FILE}.hash", "r") as hash_file:
                stored_hash = hash_file.read()
            
            if stored_hash != file_hash:
                # Jika file hash berbeda, laporkan perubahan
                ip = get_ip()
                message = f"File {MONITORED_FILE} telah diubah!\nPerubahan dilakukan oleh IP: {ip}"
                send_telegram_message(message)
                
                # Update hash untuk file tersebut
                with open(f"{MONITORED_FILE}.hash", "w") as hash_file:
                    hash_file.write(file_hash)

    except Exception as e:
        print(f"Error checking file changes: {e}")

# Tampilkan banner seram
def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = pyfiglet.figlet_format("Web Copier", font="slant")
    print(Fore.RED + banner)
    print(Fore.YELLOW + "=== Full Website copy by irfa===\n")
    
    # Informasi Pembuat
    print(Fore.CYAN + "Program ini dibuat oleh: Irfa\n")
    print(Fore.YELLOW + "YouTube: Hellboy\n")
    print(Fore.MAGENTA + "GitHub: https://github.com/irfaf\n")
    print(Fore.GREEN + "Terima kasih telah menggunakan program ini!\n")
    
    # Mengecek jumlah eksekusi
    global current_runs
    if current_runs >= MAX_RUNS:
        print(Fore.RED + "Maaf, Anda sudah mencapai limit eksekusi!")
        print(Fore.YELLOW + "Jika Anda ingin membeli akses lebih, silakan hubungi WhatsApp: 6283852751527")
        
        # Buka WhatsApp secara otomatis
        webbrowser.open("https://wa.me/6283852751527?text=Saya%20ingin%20membeli%20lebih%20banyak%20akses%20untuk%20program%20ini")
        exit(0)
    
    current_runs += 1
    print(Fore.YELLOW + f"Jumlah eksekusi: {current_runs}/{MAX_RUNS}")

# Fungsi untuk menyalin website dengan httrack
def download_with_httrack(url, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
        print(Fore.CYAN + f"Mengunduh seluruh website: {url} dengan httrack...")
        # Menggunakan httrack untuk menyalin website
        subprocess.run(f"httrack {url} -O {output_folder}", shell=True, check=True)
        print(Fore.GREEN + f"Website berhasil disalin dengan httrack ke folder: {output_folder}")
    except Exception as e:
        print(Fore.RED + f"Gagal mengunduh website dengan httrack! Error: {e}")

# Fungsi untuk menyalin file yang belum terunduh dengan wget
def download_missing_files(url, output_folder):
    try:
        print(Fore.CYAN + f"Mengunduh file-file yang hilang dengan wget untuk: {url}...")
        # Menggunakan wget untuk mengunduh file-file terkait (gambar, CSS, JS, dll.)
        subprocess.run(f"wget --recursive --no-parent --convert-links --adjust-extension --page-requisites -P {output_folder} {url}", shell=True, check=True)
        print(Fore.GREEN + f"File yang hilang berhasil diunduh ke folder: {output_folder}")
    except Exception as e:
        print(Fore.RED + f"Gagal mengunduh file dengan wget! Error: {e}")

# Fungsi utama untuk menyalin website
def download_website(url, output_folder):
    # Gunakan HTTrack terlebih dahulu untuk menyalin website secara lengkap
    download_with_httrack(url, output_folder)
    
    # Jika ada file yang terlewat, gunakan Wget untuk mengunduh file yang hilang
    download_missing_files(url, output_folder)

# Main program
def main():
    display_banner()
    
    # Cek perubahan file sebelum melanjutkan
    check_file_changes()
    
    url = input(Fore.MAGENTA + "Masukkan URL website (contoh: https://example.com): ")
    output_folder = "downloaded_websites"
    download_website(url, output_folder)

if __name__ == "__main__":
    main()
