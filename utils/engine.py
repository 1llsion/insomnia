from utils.broken_link import *
from utils.sitemap import *
from utils.backlink import *
from utils.kw_sg import *


def broken_link():
    input_file = input(f"{magenta}INSOMNIA [{white}Broken Link Checker{magenta}]{white} > ")

    try:
        with open(input_file, "r") as file:
            links = [line.strip() for line in file.readlines() if line.strip()]
        
        max_threads = 10  
        checker = BrokenLinkChecker(links, max_threads=max_threads)
        checker.check_links()
        checker.save_results()
    except FileNotFoundError:
        print(f"[{red}-{white}] File {red}{input_file}{white} not found. Please check the file name and try again.")

def sitemaps():
    generator = SitemapGenerator()
    display = f"""
[{magenta}1{white}] Single Page
[{magenta}2{white}] Tunnel
[{magenta}3{white}] Json
    """
    print(display)
    user_choice = input(f"{magenta}INSOMNIA [{white}Sitemap Generator{magenta}]{white} > ").lower()

    if user_choice == "1":
        single_page_url = input("Enter single page URL: ")
        generator.generate_single_page_sitemap(single_page_url)
    elif user_choice == "2":
        tunnel_url = input("Enter tunnel URL: ")
        tunnel_params = input("Enter tunnel params: ")
        tunnel_brands = input("Enter path to brands file: ")

        with open(tunnel_brands, "r", encoding="utf-8") as brands_file:
            brands_list = [brand.strip() for brand in brands_file.readlines()]

        generator.generate_tunnel_sitemap(tunnel_url, tunnel_params, brands_list)
    elif user_choice == "3":
        config_path = input("Enter path to config file: ")
        generator.generate_from_config(config_path)
    else:
        print(f"[{red}Error{white}] Invalid choice. Please try again.")

def generate_backlinks():
    generator = BacklinkGenerator()
    display = f"""
    [{magenta}1{white}] mass
        """
    print(display)
    user_choice = input(f"{magenta}INSOMNIA [{white}Backlink Generator{magenta}]{white} > ").lower()
    if user_choice == "1":
        tunnel_base_url = input("Enter base URL : ")
        tunnel_params = input("Enter URL params : ")
        tunnel_items_file = input("Enter path to items file (e.g., brands.txt): ")

        with open(tunnel_items_file, "r", encoding="utf-8") as file:
            items_list = [item.strip() for item in file.readlines()]

        generator.generate_backlinks(tunnel_base_url, tunnel_params, items_list)
    else:
        print(f"[{red}Error{white}] Invalid choice. Please try again.")
        
def keyword_suggestion():
    suggestion_tool = GoogleSuggestion()
    display = f"""
[{magenta}1{white}] Single Keyword
[{magenta}2{white}] Multiple Keywords
    """
    print(display)
    choice = input(f"{magenta}INSOMNIA [{white}Keyword Suggestion{magenta}]{white} > ")
    if choice == '1':
        user_keyword = input(f"Input your keyword : ")
        suggestion_tool.get_suggestions(user_keyword)
    
    elif choice == '2':
        filename = input(f"Input your list keyword : ")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                keywords = file.readlines()
                keywords = [kw.strip() for kw in keywords]
                
                for keyword in keywords:
                    print(f"\n[{green}+{white}] Processing keyword: {cyan}{keyword}{white}")
                    suggestion_tool.get_suggestions(keyword)
        else:
            print(f"[{red}!{white}] File not found. Please check the file path.")
    
    else:
        print(f"[{red}!{white}] Invalid choice. Please try again")