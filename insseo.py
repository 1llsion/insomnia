import os
import time
import platform
from assets.menu import *
from utils.engine import *

def display_menu():
    print(menu)

def clear_screen():
    system = platform.system().lower()
    if system == 'windows':
        os.system('cls')
    else:
        os.system('clear')

while True:
    time.sleep(2)
    clear_screen()
    display_menu()
    requests.packages.urllib3.disable_warnings()
    try:
        choice = input(f"{magenta}INSOMNIA > {white}")
        if choice == "1":
            broken_link()
        elif choice == "2":
            sitemaps()
        elif choice == "3":
            generate_backlinks()
        elif choice == "4":
            keyword_suggestion()
        elif choice == "5":
            Nawala()
        elif choice == "6":
            AutLogin()
        elif choice == "7":
            OJS()
        elif choice == "8":
            xmlrpc_Bf()
        else:
            print(f"[{red}Error{white}] Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
        time.sleep(1)  
        break
