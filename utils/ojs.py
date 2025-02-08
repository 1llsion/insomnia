import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from assets.colors import *

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def check_version(target_url):
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code == 200:
            match = re.search(r'OJS ([\d\.]+)', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"[{red}ERROR{white}] Failed to check version")
    return "Unknown"

def check_file(base_url, journal_id, article_id, filename):
    file_url = f"{base_url}/files/journals/{journal_id}/articles/{article_id}/submission/original/{filename}"
    try:
        response = requests.get(file_url, timeout=10)
        if response.status_code == 200 and re.search(r'<ethopia>', response.text):
            print(f"[{green}Found Shell{white}] {file_url}")
            return file_url
        else:
            print(f"[{red}404{white}] {file_url}")
    except Exception:
        print(f"[{red}ERROR{white}] {file_url}")
    return None