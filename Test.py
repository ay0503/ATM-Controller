from ATM import *

bank = Bank() # create Bank instance
# add accounts
bank.new_account("Andrew", 1234, 67891123, "2000", 100)
bank.new_account("Andrew", 1234, 67891124, "2000", 1000)
bank.new_account("Bryan", 4321, 67123843, "2003", 500)
# run ATM
ATM(bank)