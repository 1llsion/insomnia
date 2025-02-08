import requests
import os
from urllib.parse import urlparse, urlunparse
from assets.colors import *
from concurrent.futures import ThreadPoolExecutor

# Initialize colorama
init()

class NawalaChecker:
    def __init__(self, target_domain, threads=10):
        self.target_domain = target_domain
        self.results_dir = "results"
        self.threads = threads
        os.makedirs(self.results_dir, exist_ok=True)

    def check_url(self, url):
        try:
            # Replace HTTPS with HTTP if needed
            parsed_url = urlparse(url)
            if parsed_url.scheme == "http" or parsed_url.scheme == "https":
                if parsed_url.scheme != "https":
                    url = urlunparse(parsed_url._replace(scheme="https"))
                try:
                    response = requests.get(url, allow_redirects=True, timeout=10, verify=False)
                except requests.exceptions.SSLError:
                    url = urlunparse(parsed_url._replace(scheme="http"))
                    response = requests.get(url, allow_redirects=True, timeout=10, verify=False)
            else:
                url = f"http://{url}"
                response = requests.get(url, allow_redirects=True, timeout=10, verify=False)

            final_url = response.url
            parsed_final = urlparse(final_url)

            if response.history:
                if self.target_domain in parsed_final.netloc:
                    print(f"[{green}OK{white}] {url} redirected to {magenta}{final_url}{white}")
                    return f"{url} -> {final_url} (Redirected to Target Domain)"
                else:
                    print(f"[{red}WRONG DOMAIN{white}] {url} redirected to {magenta}{final_url}{white}")
                    return f"{url} -> {final_url} (Redirected to Non-Target Domain)"
            else:
                print(f"[{red}NO REDIRECT{white}] {url} did not redirect.")
                return f"{url} -> No Redirect"
        except requests.exceptions.RequestException as e:
            # Handle connection errors and other request issues
            return f"{url} -> Error: Connection or Request Failed"
        except Exception as e:
            # Generic error handling
            return f"{url} -> Error: {str(e)}"

    def process_urls(self, urls):
        results = []
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_url, url): url for url in urls}
            for future in futures:
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"[{red}THREAD ERROR{white}] {e}")
        return results

    def save_results(self, filename, results):
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            for line in results:
                file.write(line + "\n")
        print(f"[{cyan}SAVED{white}] Results saved to {filepath}")