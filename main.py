# =========================
# PART 1: Imports & Constants (Elden)
# =========================
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

A_KEY = 0
A_ID = 1
A_USER = 2
A_PASS = 3
A_WALLET = 4
A_BANK = 5
A_CREATED = 6

SCREEN_WIDTH = 70
ADMIN_PASS = pbkdf2_sha256.hash("admin")
TRANSACTION_PAGE_SIZE = 10
WITHDRAW_DENOMINATIONS = [100, 500, 1000, 10000]
WITHDRAW_TAX = 0.02

accounts = [
    [0, "00000", "admin", ADMIN_PASS, 5000, 0, datetime.now()],
]
logs = []
# =========================
# END PART 1
# =========================

# =========================
# PART 2: Utility Functions (Charie)
# =========================
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def makePanel(content, title="", subtitle=None, align="center", style="white on black", border_style="bright_blue", width=SCREEN_WIDTH, box=ROUNDED):
    alignment = Align.center(content) if align == "center" else Align.left(content)
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
    for i in range(len(accounts)):
        if str(accounts[i][index]) == str(value):
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

def addLog(user, action, amount=0):
    actionStr = str(action).upper()
    isAdmin = user == accounts[0][A_USER]
    if isAdmin:
        if "DELETE ACCOUNT" in actionStr:
            act = "DELETE ACCOUNT"
        elif "EDIT ACCOUNT" in actionStr or "USERNAME" in actionStr or "PASSWORD" in actionStr or "WALLET" in actionStr or "BANK" in actionStr or actionStr.startswith("EDIT"):
            act = "EDIT ACCOUNT"
        elif "UPDATE TAX" in actionStr or "TAX RATE" in actionStr:
            act = "UPDATE TAX RATE"
        elif "DENOMINATIONS" in actionStr:
            act = "UPDATE DENOMINATIONS"
        elif "LOG PAGE SIZE" in actionStr or "PAGE SIZE" in actionStr:
            act = "UPDATE LOG PAGE SIZE"
        else:
            act = actionStr
        logs.append([user, act, 0, datetime.now()])
    else:
        logs.append([user, actionStr, amount, datetime.now()])

def reindexAccounts():
    for i in range(len(accounts)):
        accounts[i][A_KEY] = i
# =========================
# END PART 2
# =========================

# =========================
# PART 3: AI ChatBot (Dhenver)
# =========================
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
# =========================
# END PART 3
# =========================

# =========================
# PART 4: Main Menus & Navigation (CJ)
# =========================
def mainMenu():
    makePanel("Welcome to BanQo", title="[bold bright_cyan]Main Menu[/]")
    options = ["Exit", "Register", "Login", "Credits"]
    return TerminalMenu(options).show()

def userDashboard(key):
    while True:
        clear()
        makePanel(f"Welcome {accounts[key][A_USER]}!", title="[bold bright_cyan]User Dashboard[/]", align="center")
        options = ["Banking Operations", "Customer Support", "Change Password", "Logout"]
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                bankingOperations(key)
            case 1:
                customerSupport(key)
            case 2:
                changePassword(key)
            case 3:
                addLog(accounts[key][A_USER], "LOGOUT", 0)
                break

def adminDashboard(key):
    while True:
        clear()
        makePanel(f"Welcome {accounts[key][A_USER]}!", title="[bold bright_cyan]Admin Dashboard[/]")
        options = [
            "Account Management",
            "Activity Logs",
            "Configuration",
            "Logout"
        ]
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                accountManagement(key)
            case 1:
                viewActivityLogs(key)
            case 2:
                systemSettings(key)
            case 3:
                addLog(accounts[key][A_USER], "LOGOUT", 0)
                break
# =========================
# END PART 4
# =========================

# =========================
# PART 5: Admin Account Management (Reign)
# =========================
def accountManagement(adminKey):
    while True:
        clear()
        options = ["View Accounts", "Search Account", "Edit Account", "Delete Account", "Logout"]
        makePanel("Account Management", title="[bold bright_cyan]Admin Dashboard[/]", align="center")
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                clear()
                table = Table(title="All Accounts", box=ROUNDED, width=SCREEN_WIDTH, title_justify="center")
                table.add_column("Key", justify="center", style="magenta")
                table.add_column("ID", justify="center", style="magenta")
                table.add_column("Username", justify="center", style="yellow")
                table.add_column("Wallet", justify="right", style="green")
                table.add_column("Bank", justify="right", style="green")
                table.add_column("Created", justify="center", style="bright_blue")
                for acc in accounts:
                    table.add_row(
                        str(acc[A_KEY]),
                        str(acc[A_ID]),
                        str(acc[A_USER]),
                        f"₱{acc[A_WALLET]:,.2f}",
                        f"₱{acc[A_BANK]:,.2f}",
                        acc[A_CREATED].strftime("%Y-%m-%d %H:%M:%S")
                    )
                clear()
                print(table)
                pause()
            case 1:
                subtitle = None
                while True:
                    clear()
                    makePanel("Enter account ID to search (q to cancel)", title="[bold bright_cyan]Search Account[/]", subtitle=subtitle, align="center")
                    userInput = input(">> ")
                    if userInput.lower() == "q":
                        break
                    key = getKey(A_ID, userInput)
                    if key is None:
                        subtitle = "[bold bright_red]Account not found[/]"
                        continue
                    acc = accounts[key]
                    clear()
                    makePanel(
                        f"Id: {acc[A_ID]}\nUsername: {acc[A_USER]}\nWallet: ₱{acc[A_WALLET]:,.2f}\nBank: ₱{acc[A_BANK]:,.2f}\nCreated: {acc[A_CREATED].strftime('%Y-%m-%d %H:%M:%S')}",
                        title="[bold bright_cyan]Account Details[/]",
                        align="center"
                    )
                    pause()
                    break
            case 2:
                subtitle = None
                while True:
                    clear()
                    makePanel("Enter account ID to edit (q to cancel)", title="[bold bright_cyan]Edit Account[/]", subtitle=subtitle, align="center")
                    userInput = input(">> ")
                    if userInput.lower() == "q":
                        break
                    key = getKey(A_ID, userInput)
                    if key is None:
                        subtitle = "[bold bright_red]Account not found[/]"
                        continue
                    acc = accounts[key]
                    editOptions = ["Username", "Wallet Balance", "Bank Balance", "Password", "Cancel"]
                    editChoice = TerminalMenu(editOptions).show()
                    match editChoice:
                        case 0:
                            newSubtitle = None
                            clear()
                            makePanel(f"Enter new username for {acc[A_USER]} (q to cancel)", title="[bold bright_cyan]Edit Username[/]", subtitle=newSubtitle, align="center")
                            newUsername = input(">> ")
                            if newUsername.lower() != "q" and newUsername.isalpha() and all(a[A_USER] != newUsername for a in accounts):
                                updateAccount(key, A_USER, newUsername)
                                addLog(accounts[adminKey][A_USER], f"EDIT ACCOUNT USERNAME {acc[A_USER]} -> {newUsername}", 0)
                                clear()
                                makePanel("Username updated!", title="[bold bright_green]Success[/]", align="center")
                                pause()
                        case 1:
                            newSubtitle = None
                            clear()
                            makePanel(f"Enter new wallet balance for {acc[A_USER]} (q to cancel)", title="[bold bright_cyan]Edit Wallet[/]", subtitle=newSubtitle, align="center")
                            newWallet = input(">> ")
                            try:
                                if newWallet.lower() != "q":
                                    amount = float(newWallet)
                                    updateAccount(key, A_WALLET, amount)
                                    addLog(accounts[adminKey][A_USER], f"EDIT ACCOUNT WALLET {acc[A_USER]}", amount)
                                    clear()
                                    makePanel("Wallet updated!", title="[bold bright_green]Success[/]", align="center")
                                    pause()
                            except:
                                pass
                        case 2:
                            newSubtitle = None
                            clear()
                            makePanel(f"Enter new bank balance for {acc[A_USER]} (q to cancel)", title="[bold bright_cyan]Edit Bank[/]", subtitle=newSubtitle, align="center")
                            newBank = input(">> ")
                            try:
                                if newBank.lower() != "q":
                                    amount = float(newBank)
                                    updateAccount(key, A_BANK, amount)
                                    addLog(accounts[adminKey][A_USER], f"EDIT ACCOUNT BANK {acc[A_USER]}", amount)
                                    clear()
                                    makePanel("Bank updated!", title="[bold bright_green]Success[/]", align="center")
                                    pause()
                            except:
                                pass
                        case 3:
                            clear()
                            makePanel(f"Enter new password for {acc[A_USER]} (q to cancel)", title="[bold bright_cyan]Edit Password[/]", align="center")
                            newPass = getpass(">> ")
                            if newPass and newPass.lower() != "q":
                                updateAccount(key, A_PASS, pbkdf2_sha256.hash(newPass))
                                addLog(accounts[adminKey][A_USER], f"EDIT ACCOUNT PASSWORD {acc[A_USER]}", 0)
                                clear()
                                makePanel("Password updated!", title="[bold bright_green]Success[/]", align="center")
                                pause()
                        case 4:
                            break
                    break
            case 3:
                subtitle = None
                while True:
                    clear()
                    makePanel("Enter account ID to delete (q to cancel)", title="[bold bright_cyan]Delete Account[/]", subtitle=subtitle, align="center")
                    userInput = input(">> ")
                    if userInput.lower() == "q":
                        break
                    key = getKey(A_ID, userInput)
                    if key is None or accounts[key][A_ID] == "00000":
                        subtitle = "[bold bright_red]Cannot delete this account[/]"
                        continue
                    clear()
                    makePanel(f"Are you sure you want to delete {accounts[key][A_USER]}? (y/n)", title="[bold bright_cyan]Confirm Delete[/]", align="center")
                    confirm = input(">> ")
                    if confirm.lower() == "y":
                        addLog(accounts[adminKey][A_USER], f"DELETE ACCOUNT {accounts[key][A_USER]}", 0)
                        del accounts[key]
                        reindexAccounts()
                        clear()
                        makePanel("Account deleted!", title="[bold bright_green]Success[/]", align="center")
                        pause()
                        break
                    else:
                        break
            case 4:
                break
# =========================
# END PART 5
# =========================

# =========================
# PART 6: User Operations (Hiroshi)
# =========================
def customerSupport(key):
    content = "Gemmy: Hello! I'm Gemmy, I'll be your assistant today. How can I help you?"
    while True:
        clear()
        makePanel(f"{content}", title="[bold bright_cyan]Customer Support[/]")
        userInput = input(">> ")
        if userInput.lower() in ["q", "quit", "exit"]:
            break
        clear()
        makePanel("Gemmy is typing...", title="[bold bright_cyan]Customer Support[/]")
        aiResponse = chatBot(userInput)
        content = str(aiResponse)
        clear()
        makePanel(f"Gemmy: {aiResponse}", title="[bold bright_cyan]Customer Support[/]")
       

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
    makePanel(info, title="[bold bright_green]Transaction Receipt[/]", align="left")
    pause()

def bankingOperations(key):
    subtitle = None
    while True:
        clear()
        makePanel(f"Wallet: ₱{accounts[key][A_WALLET]}", title="[bold bright_cyan]Banking Operations[/]", subtitle=subtitle)
        options = ["Account Info", "Deposit", "Withdraw", "Transfer Funds", "Transaction Logs", "Back"]
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                clear()
                acc = accounts[key]
                info = (
                    f"[bold cyan]Username:[/bold cyan] {acc[A_USER]}\n"
                    f"[bold cyan]User ID:[/bold cyan] {acc[A_ID]}\n"
                    f"[bold cyan]Wallet Balance:[/bold cyan] ₱{acc[A_WALLET]:,.2f}\n"
                    f"[bold cyan]Bank Balance:[/bold cyan] ₱{acc[A_BANK]:,.2f}\n"
                    f"[bold cyan]Account Created:[/bold cyan] {acc[A_CREATED].strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                makePanel(info, title="[bold bright_cyan]Account Info[/]", align="left")
                pause()
            case 1:
                subtitle = None
                while True:
                    clear()
                    makePanel("Enter amount to deposit (q to quit)", title="[bold bright_cyan]Deposit[/]", subtitle=subtitle)
                    userInput = input(">> ")
                    try:
                        if userInput.lower() == "q":
                            break
                        amount = float(userInput)
                        if amount <= 0:
                            subtitle = "[bold bright_red]Amount must be greater than 0[/]"
                        else:
                            accounts[key][A_WALLET] += amount
                            addLog(accounts[key][A_USER], "DEPOSIT", amount)
                            printReceipt(accounts[key][A_USER], "Deposit", amount, accounts[key][A_WALLET])
                            break
                    except:
                        subtitle = "[bold bright_red]Enter a valid number[/]"
            case 2:
                subtitle = None
                while True:
                    clear()
                    makePanel(f"Enter amount to withdraw (q to quit). {WITHDRAW_DENOMINATIONS}", title="[bold bright_cyan]Withdraw[/]", subtitle=subtitle)
                    userInput = input(">> ")
                    try:
                        if userInput.lower() == "q":
                            break
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
                                addLog(accounts[key][A_USER], "WITHDRAW", amount)
                                printReceipt(accounts[key][A_USER], "Withdraw", amount, accounts[key][A_WALLET], tax)
                                break
                    except:
                        subtitle = "[bold bright_red]Enter a valid number[/]"
            case 3:
                subtitle = None
                while True:
                    clear()
                    makePanel("Enter recipient account ID (q to quit)", title="[bold bright_cyan]Transfer Funds[/]", subtitle=subtitle)
                    targetInput = input(">> ")
                    if targetInput.lower() == "q":
                        break
                    targetKey = getKey(A_ID, targetInput)
                    if targetKey is None:
                        subtitle = "[bold bright_red]Account not found[/]"
                        continue
                    if targetKey == key:
                        subtitle = "[bold bright_red]You cannot transfer to yourself[/]"
                        continue
                    clear()
                    makePanel(f"Enter amount to transfer to {getAccount(targetKey, A_USER)} (q to quit)", title="[bold bright_cyan]Transfer Funds[/]", subtitle=subtitle)
                    amountInput = input(">> ")
                    try:
                        if amountInput.lower() == "q":
                            break
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
                            addLog(accounts[key][A_USER], f"TRANSFER TO {accounts[targetKey][A_USER]}", amount)
                            addLog(accounts[targetKey][A_USER], f"RECEIVED FROM {accounts[key][A_USER]}", amount)
                            printReceipt(accounts[key][A_USER], f"Transfer to {accounts[targetKey][A_USER]}", amount, senderBalance)
                            break
                    except:
                        subtitle = "[bold bright_red]Enter a valid amount[/]"
            case 4:
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
                    for log in userLogs[start:end]:
                        table.add_row(log[1], f"₱{log[2]:,.2f}", log[3].strftime("%Y-%m-%d %H:%M:%S"))
                    print(table)
                    options = ["Next", "Back", "Quit"]
                    action = TerminalMenu(options).show()
                    match action:
                        case 0:
                            if end >= len(userLogs):
                                makePanel("No more pages", title="[bold yellow]Info[/]")
                                pause()
                            else:
                                page += 1
                        case 1:
                            if page > 0:
                                page -= 1
                        case 2:
                            break
            case 5:
                break
# =========================
# END PART 6
# =========================

# =========================
# PART 7: Registration, Login, Password, Credits, Exit (Karl)
# =========================
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
            subtitle = "[bold bright_red]Password must be at least 8 characters long[/]"
        else:
            randomId = "".join(str(random.randint(0, 9)) for _ in range(5))
            hashedPassword = pbkdf2_sha256.hash(password)
            accounts.append([len(accounts), randomId, username, hashedPassword, 5000, 0, datetime.now()])
            addLog(username, "REGISTER", 0)
            clear()
            makePanel(f"{username} registered", title="[bold white]Registration Successful[/]")
            pause()
            return

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
        valid = False
        for acc in accounts:
            try:
                if pbkdf2_sha256.verify(password, acc[A_PASS]) and acc[A_USER] == username:
                    valid = True
            except:
                continue
        if valid:
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
        try:
            if not pbkdf2_sha256.verify(currentPass, getAccount(key, A_PASS)):
                subtitle = "[bold bright_red]Incorrect current password[/]"
                continue
        except:
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
        addLog(getAccount(key, A_USER), "PASSWORD CHANGE", 0)
        pause()
        return

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

def exitProgram():
    clear()
    makePanel("Babyee :p", title="[bold white on bright_red]You have exited[/]")
    sys.exit()
# =========================
# END PART 7
# =========================

# =========================
# PART 8: Logs, Settings, Main Loop (Kathrice)
# =========================
def viewActivityLogs(adminKey):
    if not logs:
        clear()
        makePanel("No activity logs yet", title="[bold yellow]Info[/]")
        pause()
        return
    page = 0
    while True:
        clear()
        table = Table(title="System Activity Logs", box=ROUNDED)
        table.add_column("User", justify="center", style="magenta")
        table.add_column("Action", justify="center", style="cyan")
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Time", justify="center", style="bright_blue")
        start = page * TRANSACTION_PAGE_SIZE
        end = start + TRANSACTION_PAGE_SIZE
        for log in logs[start:end]:
            table.add_row(log[0], log[1], f"₱{log[2]:,.2f}", log[3].strftime("%Y-%m-%d %H:%M:%S"))
        print(table)
        options = ["Next", "Back", "Quit"]
        action = TerminalMenu(options).show()
        match action:
            case 0:
                if end >= len(logs):
                    makePanel("No more pages", title="[bold yellow]Info[/]")
                    pause()
                else:
                    page += 1
            case 1:
                if page > 0:
                    page -= 1
            case 2:
                break

def systemSettings(adminKey):
    global WITHDRAW_TAX, WITHDRAW_DENOMINATIONS, TRANSACTION_PAGE_SIZE
    while True:
        clear()
        makePanel("Configure system settings", title="[bold bright_cyan]Configuration[/]")
        options = ["Edit Tax Rate", "Edit Denominations", "Edit Log Page Size", "Back"]
        choice = TerminalMenu(options).show()
        match choice:
            case 0:
                subtitle = None
                while True:
                    clear()
                    makePanel(f"Current tax rate: {WITHDRAW_TAX}\nEnter new tax rate as decimal (e.g. 0.02) (q to cancel)", title="[bold bright_cyan]Edit Tax Rate[/]", subtitle=subtitle)
                    userInput = input(">> ")
                    try:
                        if userInput.lower() == "q":
                            break
                        newTax = float(userInput)
                        if newTax < 0 or newTax > 1:
                            subtitle = "[bold bright_red]Enter a decimal between 0 and 1[/]"
                        else:
                            WITHDRAW_TAX = newTax
                            addLog(accounts[adminKey][A_USER], f"UPDATE TAX RATE TO {WITHDRAW_TAX}", 0)
                            clear()
                            makePanel("Tax rate updated!", title="[bold bright_green]Success[/]")
                            pause()
                            break
                    except:
                        subtitle = "[bold bright_red]Enter a valid decimal number[/]"
            case 1:
                subtitle = None
                while True:
                    clear()
                    denomsStr = ",".join(str(d) for d in WITHDRAW_DENOMINATIONS)
                    makePanel(f"Current denominations: {denomsStr}\nEnter comma-separated denominations (e.g. 100,500,1000) (q to cancel)", title="[bold bright_cyan]Edit Denominations[/]", subtitle=subtitle)
                    userInput = input(">> ")
                    if userInput.lower() == "q":
                        break
                    parts = [p.strip() for p in userInput.split(",") if p.strip() != ""]
                    try:
                        if not parts or not all(p.isdigit() for p in parts):
                            subtitle = "[bold bright_red]Denominations must be integers[/]"
                        else:
                            WITHDRAW_DENOMINATIONS = [int(p) for p in parts]
                            addLog(accounts[adminKey][A_USER], f"UPDATE DENOMINATIONS TO {WITHDRAW_DENOMINATIONS}", 0)
                            clear()
                            makePanel("Denominations updated!", title="[bold bright_green]Success[/]")
                            pause()
                            break
                    except:
                        subtitle = "[bold bright_red]Denominations must be integers[/]"
            case 2:
                subtitle = None
                while True:
                    clear()
                    makePanel(f"Current page size: {TRANSACTION_PAGE_SIZE}\nEnter new page size (number) (q to cancel)", title="[bold bright_cyan]Edit Log Page Size[/]", subtitle=subtitle)
                    userInput = input(">> ")
                    try:
                        if userInput.lower() == "q":
                            break
                        newSize = int(userInput)
                        if newSize <= 0:
                            subtitle = "[bold bright_red]Page size must be greater than 0[/]"
                        else:
                            TRANSACTION_PAGE_SIZE = newSize
                            addLog(accounts[adminKey][A_USER], f"UPDATE LOG PAGE SIZE TO {TRANSACTION_PAGE_SIZE}", 0)
                            clear()
                            makePanel("Log page size updated!", title="[bold bright_green]Success[/]")
                            pause()
                            break
                    except:
                        subtitle = "[bold bright_red]Enter a valid number[/]"
            case 3:
                break

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
                if key is None:
                    continue
                addLog(username, "LOGIN", 0)
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
# =========================
# END PART 8
# =========================