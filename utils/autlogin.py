import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import concurrent.futures
from assets.colors import *

class AutoLogin:
    def __init__(self, max_threads=10):
        self.session = requests.Session()
        self.max_threads = max_threads

    def detect_form(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        form = soup.find("form")

        if not form:
            print(f"[{red}Error{white}] No form detected on the page.")
            return None

        action = form.get("action")
        login_url = urljoin(url, action) if action else url

        fields = {}
        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            if name:
                fields[name] = input_tag.get("value", "")

        print(f"[{magenta}Debug{white}] Detected form fields:{cyan}", fields, f"{white}")
        print(f"[{magenta}Debug{white}] Login URL:{cyan}", login_url, f"{white}")

        return {"url": login_url, "fields": fields}

    def login(self, url, username, password):
        form = self.detect_form(url)
        if not form:
            return False

        fields = form["fields"]
        login_url = form["url"]

        # Update fields with user credentials
        fields = {**fields, "username": username, "password": password}

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

        print(f"[{magenta}Debug{white}] Sending POST request to:{cyan}", login_url, f"{white}")
        print(f"[{magenta}Debug{white}] Data sent:{cyan}", fields, f"{white}")

        response = self.session.post(login_url, data=fields, headers=headers)

        print(f"[{magenta}Debug{white}] Response status code:{cyan}", response.status_code, f"{white}")
        # print(f"[{magenta}Debug{white}] Response snippet:", response.text[:500])

        # Check if login succeeded by searching for <nav> or <ul> tags
        if re.search(r"<(nav|ul)(.*?)>", response.text, re.IGNORECASE):
            print(f"[{green}Success{white}] Login successful.")
            return True
        else:
            print(f"[{red}Failed{white}] Login failed. No navigation tag found.")
            return False

    def process_target(self, target, usernames, passwords):
        print(f"[{blue}Info{white}] Attempting to log in to {magenta} {target}")
        for username in usernames:
            for password in passwords:
                print(f"[{blue}Info{white}] Trying username:{cyan} {username}{white}, password:{cyan} {password}{white}")
                if self.login(target, username, password):
                    print(f"[{green}Success{white}] Valid credentials found for{magenta} {target}{white}: {cyan}{username}{white}:{cyan}{password}{white}")
                    return
        print(f"[{red}Failed{white}] No valid credentials found for{magenta} {target}{white}")
    def save_results(self, filename, results):
        # Save the results to a file in the results folder
        if results:
            with open(filename, "w") as file:
                file.writelines(results)
            print(f"[{blue}Info{white}] Results saved to {magenta}{filename}{white}")
        else:
            print(f"[{blue}Info{white}] No results to save.")
    def mass_login(self, target_file, username_file, password_file):
        if os.path.exists(target_file):
            with open(target_file, "r") as tfile:
                targets = [line.strip() for line in tfile.readlines()]

            if not os.path.exists(username_file) or not os.path.exists(password_file):
                print(f"[{red}Error{white}] Username or password file not found.")
                return

            with open(username_file, "r") as ufile, open(password_file, "r") as pfile:
                usernames = [line.strip() for line in ufile.readlines()]
                passwords = [line.strip() for line in pfile.readlines()]
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = []
                for target in targets:
                    futures.append(executor.submit(self.process_target, target, usernames, passwords))
                for future in concurrent.futures.as_completed(futures):
                    pass  
            self.save_results(os.path.join(self.results_dir, "test.txt"), results)
            print(f"[{blue}Info{white}] Mass login process complete.")
        else:
            print(f"[{red}Error{white}] Target list file not found.")