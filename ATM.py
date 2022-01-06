import math, hashlib

class Receipt(object):
  def __init__(self, op_type, amount, account, target = None):
    if target != None:
      print(f"{op_type} to {target} of {amount} has been made. New Balance: {account.balance}")
    else:
      print(f"{op_type} of {amount} has been made. New Balance: {account.balance}")

class PIN(object):
  def __init__(self, pin_number):
    self.pin_number = pin_number

  def __hash__(self):
    return hashlib.sha256(self.pin_number.encode())

class Card(object):
  def __init__(self, ident):
    self.id = ident

class Account(object):
  def __init__(self, name, card_number, number, pin, balance = 0):
    self.name = name
    self.card_number = card_number
    self.id = number # int
    self.pin = PIN(pin)
    self.locked = False
    self.balance = balance

  def check_pin(self, input_pin):
    return PIN(input_pin) == self.pin

  def hash(self):
    return self.number

class ATM(object):

  def __init__(self, database):
    # dictionary of sets of accounts based on card number
    self.accounts = database
    self.in_account = False
    self.card_check()

  def card_check(self):
    ident = int(input("Insert Card ID: "))
    while ident not in self.accounts:
      ident = int(input("Invalid Card ID. Please Try Again: "))
    accounts = self.accounts[ident]
    for account in accounts:
      if input(f"Do you want to work with this account: {account.id}: ") == "Yes":
        self.pin_check(account)     

  def pin_check(self, account):
    attempts = 0
    if account.locked:
      print("Account is locked.")
      return
    input_pin = int(input("Insert 4-Digit PIN: "))
    while (attempts < 5 and account.check_pin(input_pin)):
      input_pin = int(input("Insert 4-Digit PIN: "))
      attempts += 1
    if attempts >= 5:
      account.locked = True
      print("Failed to check PIN. Account has been locked.")
    else:
      self.in_account = True
      self.operations(account)

  def operations(self, account):
    op_type = input("Deposit? Withdrawl? Transfer?: ")
    match op_type:
      case "Deposit":
        amount = int(input("How much would you like to deposit: "))
        self.deposit(account, amount)
      case "Withdrawl":
        print(f"Current Balance is: {account.balance}")
        amount = int(input("How much would you like to withdraw: "))
        self.withdraw(account, amount)
      case "Transfer":
        account_num = int(input("Target Transfer Account Number: "))
        while account_num in self.accounts:
          account_num = int(input("Target Transfer Account Number: "))
        amount = int(input("How much would you like to transfer: "))
        self.transfer(account, account_num, amount)
    match input("Anything Else: "):
      case "Yes":
        self.operations(account)
      case "No":
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


ATM({1234: {Account("Andrew", 1234, 67891123, 2000, 100), Account("Andrew", 1234, 67891124, 2000, 1000)}})