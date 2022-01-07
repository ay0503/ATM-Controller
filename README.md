Simple ATM Controller

- Used Python 3.10.1
- Bank, Card, Opaque PIN, Receipt implmentation
- Additional Features: PIN Locking, Transfer, Receipts

Test Case

    bank = Bank()
    bank.new_account("Andrew", 1234, 67891123, "2000", 100)
    bank.new_account("Andrew", 1234, 67891124, "2000", 1000)
    bank.new_account("Bryan", 4321, 67123843, "2003", 500)
    ATM(bank)

Command Line

    1234
    N
    Y
    2001
    2000
    Deposit
    300
    Y
    Withdrawl
    200
    Y
    Transfer
    67123843
    300
    N
