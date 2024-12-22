import time
import requests
from concurrent.futures import ThreadPoolExecutor
import sys
from colorama import Fore, Style, init
from datetime import datetime, timedelta

# Inisialisasi colorama
init(autoreset=True)

# Fungsi Menampilkan Credit dengan Warna
def show_credit():
    credit_text = f"""
    {Fore.RED}┌────────────────────────────────────────────────────────────────────┐
    {Fore.RED}│                                                                    │
    {Fore.BLUE}│  █████╗ ██╗   ██╗████████╗ █████╗     ██████╗██████╗  ██████╗      │
    {Fore.BLUE}│ ██╔══██╗██║   ██║╚══██╔══╝██╔══██╗    ██╔══████╔══██╗██╔═══██╗     │
    {Fore.YELLOW}│ ███████║██║   ██║   ██║   ███████║    ██║  ████║  ██║██║   ██║     │
    {Fore.YELLOW}│ ██╔══██║██║   ██║   ██║   ██╔══██║    ██║  ████║  ██║██║   ██║     │
    {Fore.RED}│ ██║  ██║╚██████╔╝   ██║   ██║  ██║    ██████╔██████╔╝╚██████╔╝     │
    {Fore.RED}│ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝    ╚═════╝╚═════╝  ╚═════╝      │
    {Fore.YELLOW}│                                                                    │
    {Fore.BLUE}│           Auto Cronjob by c1k4dutz666 | Version 1.0                │
    {Fore.RED}└────────────────────────────────────────────────────────────────────┘
    """
    print(credit_text)

# Fungsi untuk memverifikasi password
def verify_password():
    correct_password = "admin666"  # Ganti dengan kata sandi yang Anda inginkan
    password = input("Masukkan kata sandi untuk melanjutkan: ")
    if password != correct_password:
        print("Kata sandi salah! Akses ditolak.")
        sys.exit(1)  # Menghentikan program jika kata sandi salah
    print("Kata sandi benar. Akses diterima.\n")

# Konfigurasi Target
target_file = input("Masukkan nama file target (contoh: urls.txt): ") or "urls.txt"
num_threads = int(input("Masukkan jumlah thread yang diinginkan (contoh: 50): ") or 5)
check_interval = int(input("Masukkan waktu jeda antara pengecekan ulang (dalam detik, contoh: 30): ") or 30)

def current_time():
    # Mendapatkan waktu saat ini di zona waktu Bangkok (WIB)
    bangkok_time = datetime.utcnow() + timedelta(hours=7)
    return bangkok_time.strftime("%H:%M WIB")

def check_link(url):
    try:
        response = requests.get(url)
        # Cek apakah status code 200 (OK)
        if response.status_code == 200:
            status = f"{Fore.GREEN}[SUCCESS] {current_time()} - {url} - Status Code: {response.status_code}"
        else:
            status = f"{Fore.RED}[FAILED] {current_time()} - {url} - Status Code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        status = f"{Fore.YELLOW}[ERROR] {current_time()} - {url} - Exception: {e}"

    # Tampilkan status secara realtime
    print(status)

def load_urls_from_file(filename):
    try:
        with open(filename, 'r') as file:
            # Membaca setiap baris sebagai URL dan menghapus karakter whitespace di akhir
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")
        return []

def main():
    # Menampilkan credit dan verifikasi password
    show_credit()
    verify_password()
    
    urls = load_urls_from_file(target_file)

    if not urls:
        print("Daftar URL kosong atau file tidak ditemukan.")
        return

    while True:
        # Simpan posisi kursor di bawah kredit
        print("\nMemulai pengecekan semua URL...\n")
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Mengeksekusi fungsi check_link untuk setiap URL secara paralel
            executor.map(check_link, urls)
        
        print(f"\nSelesai memeriksa semua URL, menunggu {check_interval} detik untuk pengecekan ulang...\n")
        time.sleep(check_interval)  # Tunggu selama waktu jeda yang ditentukan sebelum mengulangi pengecekan semua URL

if __name__ == "__main__":
    main()
