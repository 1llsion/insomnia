from utils.broken_link import *
from utils.sitemap import *
from utils.backlink import *
from utils.kw_sg import *
from utils.nawala import *
from utils.autlogin import *
from utils.ojs import *
from utils.xmlrpc_bf import *


################ BROKEN LINK CHECKER ######################

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


################ SITEMAP GENERATOR #################################

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


################## BACKLINK GENERATOR ##############################

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
        
############### KEYWORD SUGGESTION #####################

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

################## NAWALA CHECKER ##########################

def Nawala():
    target_domain = "internetbaik.telkomsel.com"  # Target domain to validate
    default_threads = 10
    checker = NawalaChecker(target_domain, threads=default_threads)
    print("[1] Check Single URL")
    print("[2] Check URLs from File")
    choice = input(f"{magenta}INSOMNIA [{white}Nawala Checker{magenta}]{white} > ")

    if choice == "1":
        url = input("Enter the URL to check: ")
        result = checker.check_url(url)
        print(result)
    elif choice == "2":
        filename = input("Enter the filename (e.g., urls.txt): ")
        if os.path.exists(filename):
            with open(filename, "r") as file:
                urls = [line.strip() for line in file.readlines()]
            results = checker.process_urls(urls)
            checker.save_results("nawala_results.txt", results)
        else:
            print(f"[{red}ERROR{white}] File not found!")
    else:
        print(f"[{red}ERROR{white}] Invalid choice!")

############## AUTO BYPASS LOGIN #####################

def AutLogin():
    auto_login = AutoLogin()
    print(f"{magenta} INSOMNIA HACKING TOOLS {white}[{cyan}AUTO LOGIN{white}]")
    target_file = input(f"Enter the target file => ")
    username_file = input(f"Enter the username file => ")
    password_file = input(f"Enter the password file => ")

    auto_login.mass_login(target_file, username_file, password_file)

############## OJS ######################

def OJS():
    print(f"[{magenta}+{white}] {magenta}INSOMNIA [{white}OJS SHELL FINDER ({cyan}ONLY FOR ETHOPIA SHELL{white}){magenta}]")
    target_url = input(f"enter target => ").strip()
    filename = input(f"Enter filename ({magenta}12157-61983-2-SM.phtml{white}) => ").strip()

    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    parsed_url = urlparse(target_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    print(f"[{blue}INFO{white}] Checking Version website....")
    version = check_version(base_url)
    print(f"[{blue}INFO{white}] Website Version on = {version}")

    print(f"[{blue}INFO{white}] Searching shell.......")
    results = []
    result_dir = "results"
    ensure_dir(result_dir)
    result_file = f"{result_dir}/ojs_shell_{parsed_url.netloc}.txt"

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for journal_id in range(101):  # ID 0–100
            article_id = filename.split("-")[0]  
            futures.append(executor.submit(check_file, base_url, journal_id, article_id, filename))
        
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    if results:
        with open(result_file, "w") as f:
            for result in results:
                f.write(result + "\n")
        print(f"[{blue}INFO{white}] Results saved to {result_file}")
    else:
        print(f"[{blue}INFO{white}] No shells found.")
        

################ XMLRPC BRUTE FORCE #####################


def xmlrpc_Bf():
    print(f"{magenta} INSOMNIA HACKING TOOLS {white}[{cyan}XMLRPC BRUTE FORCE{white}]")
    target_type = input(f"[{magenta}+{white}] Menu \n{cyan}1. Single Target\n2. Multiple Target\n{white}[{magenta}+{white}] Choice your input => ").strip().lower()
    
    if target_type == "1":
        target = input("Enter target domain (e.g., https://example.com): ").strip()
        usernames = input("Enter path to username file: ").strip()
        passwords = input("Enter path to password file: ").strip()
        brute_force(target, usernames, passwords)

    elif target_type == "2  ":
        target_file = input("Enter path to target list file: ").strip()
        usernames = input("Enter path to username file: ").strip()
        passwords = input("Enter path to password file: ").strip()

        with open(target_file, "r") as file:
            targets = [line.strip() for line in file]

        for target in targets:
            brute_force(target, usernames, passwords)
    
    else:
        print("Invalid option. Please choose 'single' or 'multiple'.")
