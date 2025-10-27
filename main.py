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
from google import genai

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
    panel = Panel(
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
    print(panel)

def getKey(index, value):
    for i, acc in enumerate(accounts):
        if acc[index] == value:
            return i
    return None

def getAccount(key, index):
    if 0 <= key < len(accounts):
        return accounts[key][index]
    return None

def updateAccount(key, index, newValue):
    if 0 <= key < len(accounts):
        accounts[key][index] = newValue
        return True
    return False

def pause():
    input("Press ENTER to continue...")

def chatBot(userInput):
    client = genai.Client(api_key="AIzaSyAcfY03vSZ_jWpb-UncTgyJAFyg839oRC8")
    
    systemInstructions = """
You are Gemmy, a friendly and professional banking assistant for BanQo Bank.
Always respond politely, clearly, and concisely.
Do not reveal any sensitive user information or passwords.
Guide users on account info, wallet balance, deposits, withdrawals, and transaction logs.
Provide step-by-step instructions if necessary, and maintain a helpful and reassuring tone.
Avoid unnecessary chatter, and always ensure the user feels confident about their banking actions.
"""
    
    prompt = systemInstructions + f"\nUser: {userInput}\nAI:"
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text

#-------------------------
#   Menus
#-------------------------
def mainMenu():
    makePanel("Welcome to BanQo", title="[bold bright_cyan]Main Menu[/]")
    options = ["Exit", "Register", "Login", "Credits"]
    return TerminalMenu(options).show()

def userDashboard(key):
    while True:
        clear()
        makePanel(f"Welcome {accounts[key][A_USER]}!", title="[bold bright_cyan]Dashboard[/]", align="center")
        options = ["Banking Operations", "Customer Support", "Withdraw", "Change Password", "Logout"]
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                bankingOperations(key)
            case 1:
                customerSupport(key)
            case 2:
               
                pass
            case 3:
                changePassword(key)
            case 4:
                break

def adminDashboard(key):
    while True:
        clear()
        makePanel("Admin Dashboard", title="[bold bright_cyan]Admin Panel[/]")
        options = ["View Accounts", "Modify Account", "Transactions", "Logout"]
        choice = TerminalMenu(options).show()
        if choice == 3:
            break
        clear()
        print(f"You selected: {options[choice]} (logic not implemented)")
        pause()
        
def customerSupport(key):
    while True:
        clear()
        makePanel("Gemmy: How can I assist you today?", title="[bold bright_cyan]Customer Support[/bold bright_cyan]")
        userInput = input(">> ")
        if userInput.lower() in ["q", "quit", "exit"]:
            break
        
        clear()
        makePanel("Gemmy is typing...", title="[bold bright_cyan]Customer Support[/bold bright_cyan]")
        
        aiResponse = chatBot(userInput)
        
        clear()
        makePanel(f"Gemmy: {aiResponse}", title="[bold bright_cyan]Customer Support[/bold bright_cyan]")
        input("Press ENTER to ask another question or type 'q' to quit...")

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
    makePanel(info, title="[bold bright_green]Transaction Receipt[/bold bright_green]", align="left")
    pause()

#-------------------------
#   Banking Operations
#-------------------------
def bankingOperations(key):
    subtitle = None
    while True:
        clear()
        makePanel(f"Wallet: ₱{accounts[key][A_WALLET]}", title="[bold bright_cyan]Banking Operations[/]", subtitle=subtitle)
        options = ["Account Info", "Deposit", "Withdraw", "Transfer Funds", "Transaction Logs", "Back"]
        choice = TerminalMenu(options).show()

        
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
            makePanel(info, title="[bold bright_cyan]Account Info[/bold bright_cyan]", align="left")
            pause()

        
        elif choice == 1:
            subtitle = None
            while True:
                clear()
                makePanel("Enter amount to deposit (q to quit)", title="[bold bright_cyan]Deposit[/]", subtitle=subtitle)
                userInput = input(">> ")
                if userInput.lower() == "q":
                    break
                if not userInput.isdigit():
                    subtitle = "[bold bright_red]Enter a valid number[/]"
                else:
                    amount = float(userInput)
                    if amount <= 0:
                        subtitle = "[bold bright_red]Amount must be greater than 0[/]"
                    else:
                        accounts[key][A_WALLET] += amount
                        logs.append([accounts[key][A_USER], "Deposit", amount, datetime.now()])
                        printReceipt(accounts[key][A_USER], "Deposit", amount, accounts[key][A_WALLET])
                        break

       
        elif choice == 2:
            subtitle = None
            while True:
                clear()
                makePanel(f"Enter amount to withdraw (q to quit). {WITHDRAW_DENOMINATIONS}", title="[bold bright_cyan]Withdraw[/]", subtitle=subtitle)
                userInput = input(">> ")
                if userInput.lower() == "q":
                    break
                if not userInput.isdigit():
                    subtitle = "[bold bright_red]Enter a valid number[/]"
                else:
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

       
        elif choice == 3:
            subtitle = None
            while True:
                clear()
                makePanel("Enter recipient account ID (q to quit)", title="[bold bright_cyan]Transfer Funds[/]", subtitle=subtitle)
                targetInput = input(">> ")
                if targetInput.lower() == "q":
                    break
                if not targetInput.isdigit():
                    subtitle = "[bold bright_red]Enter a valid numeric ID[/]"
                    continue

                targetId = int(targetInput)
                targetKey = getKey(A_ID, targetId)
                if targetKey is None:
                    subtitle = "[bold bright_red]Account not found[/]"
                    continue
                if targetKey == key:
                    subtitle = "[bold bright_red]You cannot transfer to yourself[/]"
                    continue

                clear()
                makePanel(f"Enter amount to transfer to {getAccount(targetKey, A_USER)} (q to quit)", title="[bold bright_cyan]Transfer Funds[/]", subtitle=subtitle)
                amountInput = input(">> ")
                if amountInput.lower() == "q":
                    break
                if not amountInput.isdigit():
                    subtitle = "[bold bright_red]Enter a valid amount[/]"
                    continue

                amount = float(amountInput)
                if amount <= 0:
                    subtitle = "[bold bright_red]Amount must be greater than 0[/]"
                elif amount > getAccount(key, A_WALLET):
                    subtitle = "[bold bright_red]Insufficient balance[/]"
                else:
                    senderBalance = getAccount(key, A_WALLET) - amount
                    receiverBalance = getAccount(targetKey, A_WALLET) + amount
                    updateAccount(key, A_WALLET, senderBalance)
                    updateAccount(targetKey, A_WALLET, receiverBalance)
                    logs.append([accounts[key][A_USER], f"Transfer to {accounts[targetKey][A_USER]}", amount, datetime.now()])
                    logs.append([accounts[targetKey][A_USER], f"Received from {accounts[key][A_USER]}", amount, datetime.now()])
                    printReceipt(accounts[key][A_USER], f"Transfer to {accounts[targetKey][A_USER]}", amount, senderBalance)
                    break
                    
        elif choice == 4:
            userLogs = [log for log in logs if log[0] == accounts[key][A_USER]]
            if not userLogs:
                clear()
                makePanel("No transactions yet", title="[bold yellow]Info[/]")
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
                        makePanel("No more pages", title="[bold yellow]Info[/]")
                        pause()
                    else:
                        page += 1
                elif action == 1:
                    if page > 0:
                        page -= 1
                else:
                    break

        elif choice == 5:  
            break

#-------------------------
#   Registration
#-------------------------
def register():
    subtitle = None
    while True:
        clear()
        makePanel("Type your desired username (q to cancel)", title="[bold bright_cyan]Register[/]", subtitle=subtitle)
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
        makePanel("Type your desired password (q to cancel)", title="[bold bright_cyan]Register[/]", subtitle=subtitle)
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
            makePanel(f"{username} registered", title="[bold white]Registration Successful[/]", border_style="bright_green")
            pause()
            return

#-------------------------
#   Login
#-------------------------
def login():
    subtitle = None
    while True:
        clear()
        makePanel("Type your username (q to cancel)", title="[bold bright_cyan]Login[/]", subtitle=subtitle)
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
        makePanel("Type your password (q to cancel)", title="[bold bright_cyan]Login[/]", subtitle=subtitle)
        password = getpass(">> ")
        if password.lower() == "q":
            return None
        if any(pbkdf2_sha256.verify(password, acc[A_PASS]) for acc in accounts):
            break
        else:
            subtitle = "[bold bright_red]Password doesn't match[/]"
    return username

def changePassword(key):
    subtitle = None
    while True:
        clear()
        makePanel("Enter your current password (q to cancel)", title="[bold bright_cyan]Change Password[/]", subtitle=subtitle)
        currentPass = getpass(">> ")
        if currentPass.lower() == "q":
            return
        if not pbkdf2_sha256.verify(currentPass, getAccount(key, A_PASS)):
            subtitle = "[bold bright_red]Incorrect current password[/]"
            continue

        clear()
        makePanel("Enter new password (q to cancel)", title="[bold bright_cyan]Change Password[/]")
        newPass = getpass(">> ")
        if newPass.lower() == "q":
            return

        hasLetter = any(c.isalpha() for c in newPass)
        hasDigit = any(c.isdigit() for c in newPass)
        hasSymbol = any(not c.isalnum() for c in newPass)
        if len(newPass) < 8:
            subtitle = "[bold bright_red]Password must be at least 8 characters long[/]"
            continue
        if not (hasLetter and hasDigit and hasSymbol):
            subtitle = "[bold bright_red]Must contain letters, numbers, and symbols[/]"
            continue

        confirmPass = getpass("Confirm new password >> ")
        if newPass != confirmPass:
            subtitle = "[bold bright_red]Passwords do not match[/]"
            continue

        updateAccount(key, A_PASS, pbkdf2_sha256.hash(newPass))
        clear()
        makePanel("Password successfully changed!", title="[bold bright_green]Success[/]")
        logs.append([getAccount(key, A_USER), "Password Change", 0, datetime.now()])
        pause()
        return
        
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
    makePanel(content, title="[bold bright_cyan]Credits[/]")
    pause()

#-------------------------
#   Exit
#-------------------------
def exitProgram():
    clear()
    makePanel("Babyee :p", title="[bold white on bright_red]You have exited[/]")
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
                key = getKey(A_USER, username)
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