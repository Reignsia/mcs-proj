#-------------------------
#   Imports
#-------------------------
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
from rich.table import Table
from simple_term_menu import TerminalMenu
from passlib.hash import pbkdf2_sha256
from getpass import getpass
import sys
import os
import random
from datetime import datetime

#-------------------------
#   Constants
#-------------------------
A_KEY, A_ID, A_USER, A_PASS, A_WALLET, A_BANK, A_CREATED = 0, 1, 2, 3, 4, 5, 6
SCREEN_WIDTH = 55
ADMIN_PASS = pbkdf2_sha256.hash("admin")
TRANSACTION_PAGE_SIZE = 10
WITHDRAW_DENOMINATIONS = [100, 500, 1000, 10000]
WITHDRAW_TAX = 0.02

#-------------------------
#   Data
#-------------------------
accounts = [
    [0, 0, "admin", ADMIN_PASS, 5000, 0, datetime.now()],
]
logs = []

#-------------------------
#   Utility Functions
#-------------------------
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def makePanel(content, title="", subtitle=None, align="center", style="white on black", border_style="bright_blue", width=SCREEN_WIDTH, box=ROUNDED):
    alignment = Align.center(content) if align=="center" else Align.left(content)
    return Panel(
        alignment,
        title=title,
        subtitle=subtitle if subtitle else "",
        title_align="center",
        subtitle_align="center",
        border_style=border_style,
        style=style,
        box=box,
        width=width
    )

def getKey(username):
    for i, acc in enumerate(accounts):
        if acc[A_USER] == username:
            return i
    return None

def pause():
    input("Press ENTER to continue...")

#-------------------------
#   Menus
#-------------------------
def mainMenu():
    print(makePanel("Welcome to BanQo", title="[bold bright_cyan]Main Menu[/]"))
    options = ["Exit", "Register", "Login", "Credits"]
    return TerminalMenu(options).show()

def userDashboard(key):
    while True:
        clear()
        print(makePanel("Dash", title="[bold bright_cyan]Dashboard[/]", subtitle=f"Welcome {accounts[key][A_USER]}!", align="center"))
        options = ["Banking Operations", "Deposit", "Withdraw", "Logout"]
        choice = TerminalMenu(options).show()
        if choice == 0:
            bankingOperations(key)
        elif choice == 3:
            break
        else:
            clear()
            print(f"You selected: {options[choice]} (logic not implemented)")
            pause()

def adminDashboard(key):
    while True:
        clear()
        print(makePanel("Admin Dashboard", title="[bold bright_cyan]Admin Panel[/]"))
        options = ["View Accounts", "Modify Account", "Transactions", "Logout"]
        choice = TerminalMenu(options).show()
        if choice == 3:
            break
        clear()
        print(f"You selected: {options[choice]} (logic not implemented)")
        pause()

#-------------------------
#   Transactions
#-------------------------
def printReceipt(user, txType, amount, balance, tax=0):
    txId = random.randint(100000, 999999)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clear()
    info = (
        f"[bold bright_cyan]BanQo Bank[/bold bright_cyan]\n"
        f"Date: {now}\n"
        f"Transaction ID: {txId}\n\n"
        f"Account: {user}\n"
        f"Transaction: {txType}\n"
        f"Amount: ₱{amount:,.2f}\n"
        + (f"Tax: ₱{tax:,.2f}\n" if tax > 0 else "")
        + f"Balance: ₱{balance:,.2f}\n"
        + f"{'-'*SCREEN_WIDTH}"
    )
    print(makePanel(info, title="[bold bright_green]Transaction Receipt[/bold bright_green]", align="left"))
    pause()

def bankingOperations(key):
    subtitle = None
    while True:
        clear()
        print(makePanel("Banking Operations", title="[bold bright_cyan]Banking Operations[/]", subtitle=subtitle))
        options = ["Account Info", "Deposit", "Withdraw", "Transaction Logs", "Back"]
        choice = TerminalMenu(options).show()

        #-------------------------
        #   Account Info
        #-------------------------
        if choice == 0:
            clear()
            acc = accounts[key]
            info = (
                f"[bold cyan]Username:[/bold cyan] {acc[A_USER]}\n"
                f"[bold cyan]User ID:[/bold cyan] {acc[A_ID]}\n"
                f"[bold cyan]Wallet Balance:[/bold cyan] ₱{acc[A_WALLET]:,.2f}\n"
                f"[bold cyan]Bank Balance:[/bold cyan] ₱{acc[A_BANK]:,.2f}\n"
                f"[bold cyan]Account Created:[/bold cyan] {acc[A_CREATED].strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            print(makePanel(info, title="[bold bright_cyan]Account Info[/bold bright_cyan]", align="left"))
            pause()

        #-------------------------
        #   Deposit
        #-------------------------
        elif choice == 1:
            subtitle = None
            while True:
                clear()
                print(makePanel("Enter amount to deposit (q to quit)", title="[bold bright_cyan]Deposit[/]", subtitle=subtitle))
                userInput = input(">> ")
                if userInput.lower() == "q":
                    break
                try:
                    amount = float(userInput)
                    if amount <= 0:
                        subtitle = "[bold bright_red]Amount must be greater than 0[/]"
                    else:
                        accounts[key][A_WALLET] += amount
                        logs.append([accounts[key][A_USER], "Deposit", amount, datetime.now()])
                        printReceipt(accounts[key][A_USER], "Deposit", amount, accounts[key][A_WALLET])
                        break
                except ValueError:
                    subtitle = "[bold bright_red]Enter a valid number[/]"

        #-------------------------
        #   Withdraw
        #-------------------------
        elif choice == 2:
            subtitle = None
            while True:
                clear()
                print(makePanel(f"Enter amount to withdraw (q to quit). {WITHDRAW_DENOMINATIONS}", title="[bold bright_cyan]Withdraw[/]", subtitle=subtitle))
                userInput = input(">> ")
                if userInput.lower() == "q":
                    break
                try:
                    amount = int(userInput)
                    if amount <= 0:
                        subtitle = "[bold bright_red]Amount must be greater than 0[/]"
                    elif not any(amount % d == 0 for d in WITHDRAW_DENOMINATIONS):
                        subtitle = "[bold bright_red]Invalid denomination[/]"
                    else:
                        tax = amount * WITHDRAW_TAX
                        total = amount + tax
                        if total > accounts[key][A_WALLET]:
                            subtitle = f"[bold bright_red]Insufficient balance including tax ₱{tax:,.2f}[/]"
                        else:
                            accounts[key][A_WALLET] -= total
                            logs.append([accounts[key][A_USER], "Withdraw", amount, datetime.now()])
                            printReceipt(accounts[key][A_USER], "Withdraw", amount, accounts[key][A_WALLET], tax)
                            break
                except ValueError:
                    subtitle = "[bold bright_red]Enter a valid number[/]"

        #-------------------------
        #   Transaction Logs
        #-------------------------
        elif choice == 3:
            userLogs = [log for log in logs if log[0] == accounts[key][A_USER]]
            if not userLogs:
                clear()
                print(makePanel("No transactions yet", title="[bold yellow]Info[/]"))
                pause()
                continue
            page = 0
            while True:
                clear()
                table = Table(title=f"{accounts[key][A_USER]}'s Transaction Logs", box=ROUNDED)
                table.add_column("Type", justify="center", style="cyan")
                table.add_column("Amount", justify="right", style="green")
                table.add_column("Time", justify="center", style="magenta")
                start = page * TRANSACTION_PAGE_SIZE
                end = start + TRANSACTION_PAGE_SIZE
                pageLogs = userLogs[start:end]
                for log in pageLogs:
                    table.add_row(log[1], f"₱{log[2]:,.2f}", log[3].strftime("%Y-%m-%d %H:%M:%S"))
                print(table)
                options = ["Next", "Back", "Quit"]
                action = TerminalMenu(options).show()
                if action == 0:
                    if end >= len(userLogs):
                        print(makePanel("No more pages", title="[bold yellow]Info[/]"))
                        pause()
                    else:
                        page += 1
                elif action == 1:
                    if page > 0:
                        page -= 1
                else:
                    break

        elif choice == 4:  # Back
            break

#-------------------------
#   Registration
#-------------------------
def register():
    subtitle = None
    while True:
        clear()
        print(makePanel("Type your desired username", title="[bold bright_cyan]Register[/]", subtitle=subtitle))
        username = input(">> ")
        if username.lower() == "q":
            return
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
        print(makePanel("Type your desired password", title="[bold bright_cyan]Register[/]", subtitle=subtitle))
        password = getpass(">> ")
        if password.lower() == "q":
            return
        hasLetter = any(x.isalpha() for x in password)
        hasDigit = any(x.isdigit() for x in password)
        hasSymbol = any(not x.isalnum() for x in password)
        if not (hasLetter and hasDigit and hasSymbol):
            subtitle = "[bold bright_red]Password must contain letters, numbers, and symbols[/]"
        elif len(password) < 8:
            subtitle = "[bold bright_red]Password must be at 8 characters long[/]"
        else:
            randomId = int("".join([str(random.randint(0,9)) for _ in range(5)]))
            hashedPassword = pbkdf2_sha256.hash(password)
            accounts.append([len(accounts), randomId, username, hashedPassword, 5000, 0, datetime.now()])
            clear()
            print(makePanel(f"{username} registered", title="[bold white]Registration Successful[/]", border_style="bright_green"))
            pause()
            return

#-------------------------
#   Login
#-------------------------
def login():
    subtitle = None
    while True:
        clear()
        print(makePanel("Type your username", title="[bold bright_cyan]Login[/]", subtitle=subtitle))
        username = input(">> ")
        if username.lower() == "q":
            return None
        if any(username == acc[A_USER] for acc in accounts):
            subtitle = None
            break
        else:
            subtitle = "[bold bright_red]Invalid username[/]"

    while True:
        clear()
        print(makePanel("Type your password", title="[bold bright_cyan]Login[/]", subtitle=subtitle))
        password = getpass(">> ")
        if password.lower() == "q":
            return None
        if any(pbkdf2_sha256.verify(password, acc[A_PASS]) for acc in accounts):
            break
        else:
            subtitle = "[bold bright_red]Password doesn't match[/]"
    return username

#-------------------------
#   Credits
#-------------------------
def credits():
    content = (
        "Reign Hart B. Sia\n"
        "Katrice R. De Guzman\n"
        "Christian Karl B. Leoncio\n"
        "Charie Denielle D. Gatmaitan\n"
        "Dhenver S. Baguio\n"
        "Clein Jerson T. Valentin\n"
        "Elden Pascual\n"
        "Hiroshi Sean K. Gallardo"
    )
    print(makePanel(content, title="[bold bright_cyan]Credits[/]"))
    pause()

#-------------------------
#   Exit
#-------------------------
def exitProgram():
    clear()
    print(makePanel("Babyee :p", title="[bold white on bright_red]You have exited[/]"))
    sys.exit()

#-------------------------
#   Main Loop
#-------------------------
def main():
    while True:
        clear()
        choice = mainMenu()
        match choice:
            case 0:
                exitProgram()
            case 1:
                register()
            case 2:
                username = login()
                if username is None:
                    continue
                key = getKey(username)
                if key == 0:
                    adminDashboard(key)
                else:
                    userDashboard(key)
            case 3:
                clear()
                credits()
            case _:
                clear()
                print("Invalid option. Try again.")
                pause()

main()