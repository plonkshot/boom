import requests
import hashlib
import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
from tqdm import tqdm  # Progress bar
from datetime import datetime, timedelta
import time
import os

# Inisialisasi colorama untuk pewarnaan output
init(autoreset=True)

# Header untuk requests
header = {
    "user-agent": (
        "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"
    )
}
ses = requests.session()
timeout_duration = 5  # Waktu maksimum untuk setiap request dalam detik

# ASCII art credit author
def show_credit():
    print(f"""
{Fore.RED} ## ##      ##    ##  ###      ##   ### ##   ##  ###  #### ##  ### ##    ## ###   ## ###   ## ###  
{Fore.YELLOW}##   ##    ###    ##  ##     # ##    ##  ##  ##   ##  # ## ##  ##  ##   ##   ##  ##   ##  ##   ##  
{Fore.GREEN}##          ##    ## ##     ## ##    ##  ##  ##   ##    ##        ##    ##       ##       ##       
{Fore.CYAN}##          ##    ## ##    ##  ##    ##  ##  ##   ##    ##       ##     ## ###   ## ###   ## ###   
{Fore.MAGENTA}##          ##    ## ###   ### ###   ##  ##  ##   ##    ##      ##      ##   ##  ##   ##  ##   ##  
{Fore.BLUE}##   ##     ##    ##  ##       ##    ##  ##  ##   ##    ##     ##  ##   ##   ##  ##   ##  ##   ##  
{Fore.RED} ## ##     ####   ##  ###      ##   ### ##    ## ##    ####    # ####    ## ##    ## ##    ## ##   
                                                                                                   
{Fore.RED}DB Finder Version 1.1 | c1k4dutz666
""")

# Daftar IP yang diizinkan
allowed_ips = ["103.239.52.29"]  # Ganti dengan alamat IP yang diizinkan

# Fungsi untuk verifikasi IP
def verify_ip():
    current_ip = requests.get('https://api.ipify.org').text  # Mendapatkan IP publik
    if current_ip not in allowed_ips:
        print(f"{Fore.YELLOW}Login Failed, IP Anda tidak terdaftar Whitelist. Silahkan Hubungi Admin :)")
        exit()
    print(f"{Fore.GREEN}IP terverifikasi. Akses diterima.\n")

# Fungsi autentikasi password dengan MD5 hashing
def verify_password():
    correct_hash = "e10adc3949ba59abbe56e057f20f883e"  # Hash untuk "123456" sebagai contoh
    password = getpass.getpass("Masukkan password: ")
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    if hashed_password != correct_hash:
        print(f"{Fore.RED}Kata sandi salah! Akses ditolak.")
        exit()
    print(f"{Fore.GREEN}Kata sandi benar. Akses diterima.\n")

# Fungsi untuk memeriksa URL
def check(url, save_path):
    try:
        response = ses.get(url, headers=header, timeout=timeout_duration)
        if response.status_code == 200:
            with open(save_path, "a") as save:
                save.write(url + "\n")
            return "valid"
        elif response.status_code == 404:
            return "invalid"
        else:
            return "unknown"
    except requests.RequestException:
        return "timeout/error"

# Fungsi untuk menampilkan status BOT SEDANG BERJALAN
def show_running_message():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print(f"{Fore.YELLOW}BOT SEDANG BERJALAN, HARAP MENUNGGU SAMPAI SELESAI..")
    time.sleep(1)  # Delay agar tidak terlalu cepat

# Fungsi utama
def main():
    show_credit()
    verify_ip()  # Verifikasi IP sebelum melanjutkan
    verify_password()
    
    url_list = open(input("Masukan file list (.txt): "), "r").read().splitlines()
    save_path = input("Simpan dengan nama: ")
    if '.txt' not in save_path:
        save_path += '.txt'
    
    num_start = "000000"  # Set start number
    num_end = "88888"  # Set end number
    max_workers = int(input("Max workers per URL (max 500): ")) * 7
    if max_workers < 500:
        max_workers = 500
    
    num_length = len(num_start)
    dom_list = [
        [f"{x}{str(int(num_start) + y).zfill(num_length)}.csv" for y in range(int(num_start), int(num_end) + 1)]
        for x in url_list
    ]
    
    # Gabungkan semua URL dalam satu daftar
    urls = [y for x in dom_list for y in x if y != ""]

    # Tampilkan pesan BOT SEDANG BERJALAN sebelum pemindaian
    show_running_message()

    # Eksekusi pemindaian URL secara bersamaan dengan progress bar
    start_time = time.time()  # Mulai menghitung waktu
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        with tqdm(total=len(urls), desc="Scanning URLs", colour="green") as pbar:
            futures = {pool.submit(check, domain, save_path): domain for domain in urls}
            
            # Memperbarui progress bar untuk menunjukkan loading yang aktif
            pbar.update(0)  # Update awal untuk memastikan progress bar tidak terjebak di 0%

            while futures:
                for future in as_completed(futures):
                    url = futures[future]  # Ambil URL yang sedang diproses
                    result = future.result()  # Ambil hasil pemindaian
                    
                    # Update progress bar untuk setiap URL yang selesai dipindai
                    pbar.update(1)  
                    pbar.set_postfix({"URL saat ini": url})  # Tampilkan URL saat ini di postfix
                    
                    # Update estimasi waktu
                    elapsed_time = time.time() - start_time
                    remaining_time = (elapsed_time / pbar.n) * (pbar.total - pbar.n)
                    estimated_finish_time = str(timedelta(seconds=int(remaining_time)))
                    
                    # Update progress bar dengan estimasi waktu tersisa
                    pbar.set_postfix({"Estimasi waktu tersisa": estimated_finish_time})

                    # Hapus future yang telah selesai
                    del futures[future]

                    # Jika status kode 200 ditemukan, langsung lanjut ke URL berikutnya
                    if result == "valid":
                        print(f"{Fore.GREEN}URL valid ditemukan: {url}")
                        break  # Keluar dari loop untuk melanjutkan ke URL berikutnya

    # Tampilkan pesan ketika semua URL selesai dipindai
    print(f"\n{Fore.GREEN}Hasil scan sudah valid. Silakan cek hasil di file '{save_path}'.")

if __name__ == "__main__":
    main()
