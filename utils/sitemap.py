import os
import urllib.parse
import json
from assets.colors import *

class SitemapGenerator:
    def __init__(self):
        self.sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
<!-- created with Free Online Sitemap Generator www.xml-sitemaps.com -->
{urls}
</urlset>"""

    def generate_single_page_sitemap(self, url):
        sitemap_content = f"<url>\n<loc>{url}</loc>\n</url>"
        self.save_sitemap(url, sitemap_content)

    def generate_tunnel_sitemap(self, url, params, brands):
        urls = ""
        for brand in brands:
            brand_str = urllib.parse.quote(brand.strip())
            urls += f"<url>\n<loc>{url}/{params}{brand_str}</loc>\n</url>\n"

        self.save_sitemap(url, urls)

    def save_sitemap(self, url, content):
        os.makedirs("results", exist_ok=True)
        filename = f"results/{self.clean_filename(url)}.xml"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.sitemap_template.format(urls=content))
        print(f"[{green}Success{white}] Sitemap saved as{magenta} {filename}{white}")

    def clean_filename(self, filename):
        return "".join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)

    def generate_from_config(self, config_path):
        with open(config_path, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)

        for sitemap in config["sitemaps"]:
            if sitemap["type"] == "single_page":
                self.generate_single_page_sitemap(sitemap["url"])
            elif sitemap["type"] == "tunnel":
                self.generate_tunnel_sitemap(sitemap["url"], sitemap["params"], sitemap["brands"])

