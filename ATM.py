import math, hashlib

# receipt prints transaction type and amount
class Receipt(object):
  def __init__(self, op_type, amount, account, target = None):
    if target != None:
      print(f"{op_type} to {target} of ${amount} has been made. New Balance: ${account.balance}")
    else:
      print(f"{op_type} of ${amount} has been made. New Balance: ${account.balance}")

# PIN is hashed to check but not expose numerical PIN number
class PIN(object):
  def __init__(self, pin_number):
    # str
    self.pin_number = hashlib.sha256(pin_number.encode()).hexdigest()

  def __eq__(self, other):
    return self.pin_number == other.pin_number

class Card(object):
  def __init__(self, num):
    self.num = num

  def __hash__(self):
    return self.num

  def __eq__(self, other):
    return self.num == other.num

# account is associated to a card number and holds an encrypted PIN object
class Account(object):
  def __init__(self, name, card_number, number, pin, balance = 0):
    self.name = name
    self.card_number = card_number
    self.id = number # int
    self.pin = PIN(pin)
    self.locked = False
    self.balance = balance

  # checks hash of PINs
  def check_pin(self, input_pin):
    return PIN(input_pin) == self.pin

  def __hash__(self):
    return self.id

class Bank(object):
  def __init__(self):
    self.cards = dict()
    self.accounts = set()

  def new_account(self, name, card_number, number, pin, balance):
    card = Card(card_number)
    account = Account(name, card_number, number, pin, balance)
    self.cards[card] = self.cards.get(card, set())
    self.cards[card].add(account)
    self.accounts.add(account) 

class ATM(object):

  def __init__(self, bank):
    # dictionary of sets of accounts based on card number
    self.bank = bank
    self.card = None
    self.in_account = False
    self.card_check()

  # checks card number against accounts
  def card_check(self):
    ident = int(input("Insert Card ID: "))
    self.card = Card(ident)
    while self.card not in self.bank.cards:
      ident = int(input("Invalid Card ID. Please Try Again: "))
    accounts = self.bank.cards[self.card]
    for account in accounts:
      if input(f"Do you want to work with this account: {account.id}? (Y/N) ") == "Y":
        self.pin_check(account)     
        return

  # validates PIN by comparing with account PIN object
  def pin_check(self, account):
    attempts = 0
    if account.locked:
      print("Account is locked.")
      self.card_check()
      return
    input_pin = input("Insert 4-Digit PIN: ")
    while (not account.check_pin(input_pin) and attempts < 4):
      input_pin = input("Incorrect PIN. Try Again: ")
      attempts += 1
    if attempts >= 4:
      account.locked = True
      print("Failed to check PIN. Account has been locked.")
      self.card_check()
    else:
      self.in_account = True
      self.operations(account)

  def operations(self, account):
    op_type = input("Deposit / Withdrawl / Transfer : ")
    match op_type:
      case "Deposit":
        amount = int(input("How much would you like to deposit: $"))
        self.deposit(account, amount)
      case "Withdrawl":
        print(f"Current Balance is: ${account.balance}")
        amount = int(input("How much would you like to withdraw: $"))
        self.withdraw(account, amount)
      case "Transfer":
        account_num = int(input("Target Transfer Account Number: $"))
        while account_num in self.accounts:
          account_num = int(input("Target Transfer Account Number: "))
        amount = int(input("How much would you like to transfer: "))
        self.transfer(account, account_num, amount)
    match input("Anything Else? (Y/N) "):
      case "Y":
        self.operations(account)
      case "N":
        print("Account will now close. Thank You")
        self.__init__(self.accounts)

  def deposit(self, account, amount):
    account.balance += amount
    return Receipt("Deposit", amount, account)
    
  def withdraw(self, account, amount):
    if account.balance < amount:
      print("Not enough funds in account.")
      self.operations(account)
    else:
      account.balance -= amount
      return Receipt("Withdrawl", amount, account)
  
  def transfer(self, account, account_num, amount):
    account.balance -= amount
    target = self.accounts[account_num]
    target.balance += amount
    return Receipt("Transfer", amount, account)

bank = Bank()
bank.new_account("Andrew", 1234, 67891123, "2000", 100)
bank.new_account("Andrew", 1234, 67891124, "2000", 1000)
ATM(bank)