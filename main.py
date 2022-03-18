from models.bank_base import Client, Account, Bank, Session
from sqlalchemy import func
session = Session()
'''
OK įvesti asmenis,
OK keisti asmens informaciją
OK bankus,
OK sąskaitas.
OK Leistų vartotojui peržiūrėti savo sąskaitas ir jų informaciją,
OK pridėti arba nuimti iš jų pinigų.
OK Taip pat leistų bendrai peržiūrėti visus bankus,
vartotojus,
OK sąskaitas ir jų informaciją
'''

def clients_id():
  print('Select client ID from list.')
  clients = session.query(Client)
  for client in clients:
    print(client.id, client.c_surname)

def new_client():
  c_name = input("Enter client name: ")
  c_surname = input("Enter client surname: ")
  c_security_number = int(input("Enter client social security No: "))
  c_phone = int(input("Enter client phone: "))
  client = Client(c_name = c_name, c_surname = c_surname, c_security_number = c_security_number, c_phone = c_phone)
  session.add(client)
  session.commit()
  print(f"Client {client.c_name} {client.c_surname} created.")

def new_bank():
  b_name = input("Enter bank name: ")
  b_address = input("Enter bank address: ")
  b_code = int(input("Enter bank code: "))
  swift = input("Enter SWIFT code: ")
  bank = Bank(b_name = b_name, b_address = b_address, b_code = b_code, swift = swift)
  session.add(bank)
  session.commit()
  print(f'{bank.b_name} bank record created.')

def list_banks():
  banks = session.query(Bank)
  for bank in banks:
    if len(bank.b_accounts) != 0:
      print('------------------------')      
      print(f'{bank.b_name} accounts list:')
      reserves = 0
      for account in bank.b_accounts:
        reserves = reserves + account.a_ballance
        print(f"Account {account.a_number} in {bank.b_name} bank with ballance of €{account.a_ballance}")
      print(f"Total reserves of {bank.b_name} is {round(reserves, 2)}")
    else:
      print('------------------------')      
      print(f"{bank.b_name} doesn't have any active accounts")      

def list_accounts():
  accounts = session.query(Account)
  resources = 0
  for account in accounts:
    client = session.query(Client).get(account.client)
    bank = session.query(Bank).get(account.bank)
    resources = resources + account.a_ballance
    print(bank.b_name, client.c_surname, account.a_ballance)
  print('------------------------')      
  print(f"Total money in the market: €{resources}") 

def list_clients():
  clients = session.query(Client)
  for client in clients:
    if len(client.c_accounts) != 0:
      print('------------------------')      
      print(f'{client.c_surname} accounts list:')
      reserves = 0
      for account in client.c_accounts:
        bank = session.query(Bank).get(account.bank)
        reserves = reserves + account.a_ballance
        print(f"Account {account.a_number} in {bank.b_name} bank with ballance of €{account.a_ballance}")
      print(f"Total reserves of {client.c_surname} is {round(reserves, 2)}")
    else:
      print('------------------------')      
      print(f"{client.c_surname} doesn't have any active accounts")    

def new_account():
  a_number = input("Enter account No: ")
  a_ballance = float(input("Enter account ballance: "))
  clients_id()
  client_id = int(input("Enter client id: "))
  print('Select bank ID from list.')
  banks = session.query(Bank)
  for bank in banks:
    print(bank.id, bank.b_name)
  bank_id = int(input("Enter bank id: "))
  account = Account(a_number = a_number, a_ballance = a_ballance, client = client_id, bank = bank_id)
  session.add(account)
  session.commit()

def edit_client_data():
  clients_id()
  client_id = int(input('Select client ID you would like to edit (return to skip): '))
  client = session.query(Client).get(client_id)
  c_name = input("Enter client name: ")
  if c_name != '':
    client.c_name = c_name  
  c_surname = input("Enter client surname (return to skip): ")
  if c_surname != '':
    client.c_surname = c_surname
  c_security_number = input("Enter client social security No (return to skip): ")
  if c_security_number != '':
    client.c_security_number = int(c_security_number)
  c_phone = input("Enter client phone (return to skip): ")
  if c_phone != '':
    client.c_phone = int(c_phone)
  session.commit()

def client_accounts():
  clients_id()
  client_id = int(input('Select client ID you would like to inspect: '))
  client = session.query(Client).get(client_id)
  if len(client.c_accounts) != 0:
    print(f'Client {client.c_name}, {client.c_surname} accounts list.')
    reserves = 0
    for account in client.c_accounts:
      bank = session.query(Bank).get(account.bank)
      reserves = reserves + account.a_ballance
      print(f"Account {account.a_number} in {bank.b_name} bank with ballance of € {account.a_ballance}")
    print(f"{client.c_name} {client.c_surname} have €{round(reserves, 2)} total.")
  else:
    print(f"{client.c_name} {client.c_surname} doesn't have any active accounts")
  
def edit_account():
  clients_id()
  client_id = int(input('Select client ID you would like to inspect: '))
  client = session.query(Client).get(client_id)
  if len(client.c_accounts) != 0:
    print(f'Client {client.c_name}, {client.c_surname} accounts list.')
    for account in client.c_accounts:
      bank = session.query(Bank).get(account.bank)
      print(f"Account No. {account.id} in {bank.b_name} bank with ballance of €{account.a_ballance}")
    account_id = int(input("Enter account No to withdraw/deposit: "))
    bal_change = float(input("Enter deposit/withdraw (with minus) ammount: "))
    account = session.query(Account).get(account_id)
    account.a_ballance = account.a_ballance + bal_change
    session.commit()
    print(f"Account No. {account.id} in {bank.b_name} bank current ballance of €{account.a_ballance}. Ballance change: €{bal_change}")
  else:
    print(f"{client.c_name} {client.c_surname} doesn't have any active accounts")
