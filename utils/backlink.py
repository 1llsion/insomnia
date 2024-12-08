import os
import urllib.parse
from assets.colors import *
class BacklinkGenerator:
    def __init__(self):
        self.backlinks = []

    def generate_backlinks(self, base_url, params, items):
        backlinks_content = []
        for item in items:
            item_str = urllib.parse.quote(item.strip())
            backlinks_content.append(f"{base_url}{params}{item_str}")
        
        self.save_backlinks(base_url, backlinks_content)

    def save_backlinks(self, url, content):
        filename = f"results/backlinks_{self.clean_filename(url)}.txt"
        os.makedirs("results", exist_ok=True)

        with open(filename, "w", encoding="utf-8") as file:
            for backlink in content:
                file.write(backlink + "\n")
        
        print(f"[{green}+{white}] Backlinks saved to {magenta}{filename}{white}")

    def clean_filename(self, filename):
        return "".join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)
