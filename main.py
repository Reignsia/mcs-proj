from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
from rich.table import Table
from simple_term_menu import TerminalMenu
from passlib.hash import pbkdf2_sha256
from getpass import getpass
import sys
import time
import os
import random

# -----------------------------------
#             Constants
# -----------------------------------
A_KEY, A_ID, A_USER, A_PASS, A_WALLET_, A_BANK = 0, 1, 2, 3, 4, 5
SCREEN_WIDTH = 55
ADMIN_PASS = pbkdf2_sha256.hash("admin")

# -----------------------------------
#             Variables
# -----------------------------------
accounts = [
[0, 00000, "admin", ADMIN_PASS, 5000, 0],
]
logs = []

# -----------------------------------
#            Utility 
# -----------------------------------
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# -----------------------------------
#            Screens
# -----------------------------------
def mainMenu():
    panel = Panel(
        Align.center("Welcome to BanQo"),
        title="[bold bright_cyan]Main Menu[/]",
        title_align="center",
        border_style="bright_blue",
        style="white on black",
        box=ROUNDED,
        width=SCREEN_WIDTH
    )
    print(panel)
    
    options = ["Exit", "Register", "Login", "Credits"]
    index = TerminalMenu(options).show()
    return index

def userDashboard():
    while True:
        clear()
        panel = Panel(
            Align.center("User Dashboard"),
            title="[bold bright_cyan]User Panel[/]",
            title_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)

        options = ["View Balance", "Deposit", "Withdraw", "Logout"]
        choice = TerminalMenu(options).show()

        if choice == 3:
            break
        
        clear()
        print(f"You selected: {options[choice]} (logic not implemented)")
        input("Press Enter to continue...")

def adminDashboard():
    while True:
        clear()
        panel = Panel(
            Align.center("Admin Dashboard"),
            title="[bold bright_cyan]Admin Panel[/]",
            title_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)

        options = ["View Accounts", "Modify Account", "Transactions", "Logout"]
        choice = TerminalMenu(options).show()

        if choice == 3:  
            break
    
        clear()
        print(f"You selected: {options[choice]} (logic not implemented)")
        input("Press Enter to continue...")

def register():
    subtitle = None
    while True:
        clear()
        panel = Panel(
            Align.center("Type your desired username"),
            title="[bold bright_cyan]Register[/]",
            title_align="center",
            subtitle=subtitle,
            subtitle_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)
        username = input(">> ")

        if len(username) < 4:
            subtitle = "[bold bright_red]Username must be at least 4 letters[/]"
        elif not username.isalpha():
            subtitle = "[bold bright_red]Username must contain letters only[/]"
        elif any(acc[A_USER] == username for acc in accounts):
            subtitle = "[bold bright_red]Username is taken![/]"
        else:
            break

    subtitle = None
    while True:
        clear()
        panel = Panel(
            Align.center("Type your desired password"),
            title="[bold bright_cyan]Register[/]",
            title_align="center",
            subtitle=subtitle,
            subtitle_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)
        password = getpass(">> ")

        hasLetter = any(x.isalpha() for x in password)
        hasDigit = any(x.isdigit() for x in password)
        hasSymbol = any(not x.isalnum() for x in password)

        if not (hasLetter and hasDigit and hasSymbol):
            subtitle = "[bold bright_red]Password must contain letters, numbers, and symbols[/]"
        elif len(password) < 8:
            subtitle = "[bold bright_red]Password must be at 8 characters long[/]"            
        else:
            randomId = ""
            for i in range(5):
                randomId += str(random.randint(0,9))
            randomId = int(randomId)  
            hashedPassword = pbkdf2_sha256.hash(password)            
            accounts.append([len(accounts), randomId, username, hashedPassword, 5000, 0])
            randomId = None
            clear()
            panel = Panel(
                Align.center(f"{username} registered"),
                title=f"[bold white]Registration Succesful[/]",
                title_align="center",
                border_style="bright_green",
                style="white on black",
                box=ROUNDED,
                width=SCREEN_WIDTH
            )
            print(panel)
            time.sleep(2)
            return

def login():
    subtitle = None
    while True:
        clear()
        panel = Panel(
            Align.center("Type your username"),
            title="[bold bright_cyan]Login[/]",
            title_align="center",
            subtitle=subtitle,
            subtitle_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)
        username = input(">> ")
        
        if any(username == acc[A_USER] for acc in accounts): 
            subtitle = None
            break
        else:
            subtitle = "[bold bright_red]Invalid username[/]"
            
    while True:
        clear()
        panel = Panel(
            Align.center("Type your password"),
            title="[bold bright_cyan]Login[/]",
            title_align="center",
            subtitle=subtitle,
            subtitle_align="center",
            border_style="bright_blue",
            style="white on black",
            box=ROUNDED,
            width=SCREEN_WIDTH
        )
        print(panel)
        password = input(">> ")
        
        if any(pbkdf2_sha256.verify(password, acc[A_PASS]) for acc in accounts): 
            break
        else:
            subtitle = "[bold bright_red]Password doesn't match[/]"     

def credits():
    panel = Panel(
        Align.center(
            "Reign Hart B. Sia\n"
            "Katrice R. De Guzman\n"
            "Christian Karl B. Leoncio\n"
            "Charie Denielle D. Gatmaitan\n"
            "Dhenver S. Baguio\n"
            "Clein Jerson T. Valentin\n"
            "Elden Pascual\n"
            "Hiroshi Sean K. Gallardo"
        ),
        title="[bold bright_cyan]Credits[/]",
        title_align="center",
        border_style="bright_blue",
        style="white on black",
        box=ROUNDED,
        width=SCREEN_WIDTH
    )
    print(panel)

# -----------------------------------
#            Exit Screen
# -----------------------------------
def exit():
    clear()
    panel = Panel(
    Align.center("Babyee :p"),
    title="[bold white on bright_red]You have exited[/]",
    border_style="bright_red",
    box=ROUNDED,
    width=SCREEN_WIDTH
    )
    print(panel)
    sys.exit()
    
# -----------------------------------
#            Main Flow
# -----------------------------------
def main():
    while True:
        clear()
        choice = mainMenu()
    
        match choice:
            case 0:
                exit()
            case 1:
                register()
            case 2:
                login()
            case 3:
                clear()
                credits()
                input("Press Enter to continue...")
            case _:
                clear()
                print("Invalid option. Try again.")
                input("Press Enter to continue...")

main()
