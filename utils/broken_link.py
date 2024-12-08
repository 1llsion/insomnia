import requests
import os
from threading import Thread
from queue import Queue
from assets.colors import *


class BrokenLinkChecker:
    def __init__(self, links, max_threads=10):
        self.links = links
        self.results = {
            200: [],
            403: [],
            404: [],
            500: [],
            503: [],
            "error": [],
            "http_fallback": []
        }
        self.max_threads = max_threads
        self.queue = Queue()

    def worker(self):
        """Worker thread untuk memproses link dari antrian."""
        while not self.queue.empty():
            link = self.queue.get()
            print(f"[{cyan}url{white}] {magenta}{link}{white}")
            try:
                response = requests.get(link, timeout=5)
                self.process_response(response, link)
            except requests.exceptions.SSLError:
                print(f"[{red}!{white}] SSL error detected for{magenta} {link}{white}\n    -{magenta} {link} {white}Trying with HTTP...")
                self.try_http_fallback(link)
            except requests.exceptions.RequestException:
                self.results["error"].append(link)
                print(f"[{red}Error{white}] Could not reach\n    -{magenta} {link}{white} Connection issue or timeout.")
            finally:
                self.queue.task_done()

    def check_links(self):
        """Memulai thread untuk memproses link."""
        print("[*] Checking links...\n")
        for link in self.links:
            self.queue.put(link)

        threads = []
        for _ in range(self.max_threads):
            thread = Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def process_response(self, response, link):
        """Memproses respons dari server dan mengelompokkan hasilnya."""
        status = response.status_code
        if status in self.results:
            self.results[status].append(link)
            self.print_status(status, link)
        else:
            self.results["error"].append(link)
            print(f"[{red}Error{white}] Unexpected status for{magenta} {link}{white}:{cyan} {status}{white}")

    def try_http_fallback(self, link):
        """Mencoba mengakses link dengan HTTP jika HTTPS gagal."""
        if link.startswith("https://"):
            http_link = link.replace("https://", "http://", 1)
            try:
                response = requests.get(http_link, timeout=5)
                self.results["http_fallback"].append(http_link)
                self.process_response(response, http_link)
            except requests.exceptions.RequestException:
                self.results["error"].append(http_link)
                print(f"[{red}Error{white}] Could not reach\n    -{magenta} {http_link}{white} Connection issue or timeout.")
        else:
            print(f"[{red}Error{white}] Already using HTTP for{magenta} {link}{white} Cannot retry.")

    def print_status(self, status, link):
        """Mencetak status link dengan penjelasan."""
        if status == 200:
            print(f"[{green}200{white}] OK - Link valid:\n    - {magenta}{link}{white}")
        elif status == 403:
            print(f"[{red}403{white}] Forbidden - Access to the link is restricted:\n    - {magenta}{link}{white}")
        elif status == 404:
            print(f"[{red}404{white}] Not Found - Link does not exist:\n    - {magenta}{link}{white}")
        elif status == 500:
            print(f"[{red}500{white}] Internal Server Error - Server-side issue:\n    - {magenta}{link}{white}")
        elif status == 503:
            print(f"[{red}503{white}] Service Unavailable - The server is temporarily unavailable:\n    - {magenta}{link}{white}")

    def save_results(self):
        """Menyimpan hasil pengecekan ke file .txt."""
        os.makedirs("results", exist_ok=True)
        filename = f"results/broken_links_results.txt"
        with open(filename, "w") as file:
            for status, links in self.results.items():
                file.write(f"\n[{status}]\n")
                for link in links:
                    file.write(link + "\n")
        print(f"\n[{green}+{white}] Results saved to {magenta}{filename}{white}")