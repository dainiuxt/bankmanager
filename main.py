from models.bank_base import Client, Account, Bank, Session
from sqlalchemy import func
session = Session()

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
      print('------------------------') 
      reserves = 0
      for account in bank.b_accounts:
        reserves = reserves + account.a_ballance
        print(f"Account {account.a_number} in {bank.b_name} bank with ballance of €{account.a_ballance}")
      print('------------------------') 
      print(f"Total reserves of {bank.b_name} is {round(reserves, 2)}")
      print('------------------------') 
    else:
      print('------------------------')      
      print(f"{bank.b_name} doesn't have any active accounts")
      print('------------------------')     

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
  print('------------------------') 

def list_clients():
  clients = session.query(Client)
  for client in clients:
    if len(client.c_accounts) != 0:
      print('------------------------')      
      print(f'{client.c_surname} accounts list:')
      print('------------------------') 
      reserves = 0
      for account in client.c_accounts:
        bank = session.query(Bank).get(account.bank)
        reserves = reserves + account.a_ballance
        print(f"Account {account.a_number} in {bank.b_name} bank with ballance of €{account.a_ballance}")
      print('------------------------') 
      print(f"Total reserves of {client.c_surname} is {round(reserves, 2)}")
      print('------------------------') 
    else:
      print('------------------------')      
      print(f"{client.c_surname} doesn't have any active accounts")
      print('------------------------') 

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
  print(f"You selected {client.c_name} {client.c_surname} with {client.c_security_number} security number and {client.c_phone} phone number to edit.")
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
  print(f"New client data saved: {client.c_name} {client.c_surname} with {client.c_security_number} security number and {client.c_phone} phone number.")

def client_accounts():
  clients_id()
  client_id = int(input('Select client ID you would like to inspect: '))
  client = session.query(Client).get(client_id)
  if len(client.c_accounts) != 0:
    print(f'Client {client.c_name}, {client.c_surname} accounts list.')
    print('------------------------') 
    reserves = 0
    for account in client.c_accounts:
      bank = session.query(Bank).get(account.bank)
      reserves = reserves + account.a_ballance
      print(f"Account {account.a_number} in {bank.b_name} bank with ballance of € {account.a_ballance}")
    print('------------------------') 
    print(f"{client.c_name} {client.c_surname} have €{round(reserves, 2)} total.")
    print('------------------------') 
  else:
    print(f"{client.c_name} {client.c_surname} doesn't have any active accounts")
  
def edit_account():
  clients_id()
  client_id = int(input('Select client ID you would like to inspect: '))
  client = session.query(Client).get(client_id)
  if len(client.c_accounts) != 0:
    print(f'Client {client.c_name}, {client.c_surname} accounts list.')
    print('------------------------') 
    for account in client.c_accounts:
      bank = session.query(Bank).get(account.bank)
      print(f"Account No. {account.id} in {bank.b_name} bank with ballance of €{account.a_ballance}")
    print('------------------------') 
    account_id = int(input("Enter account No to withdraw/deposit: "))
    bal_change = float(input("Enter deposit/withdraw (with minus) ammount: "))
    account = session.query(Account).get(account_id)
    account.a_ballance = account.a_ballance + bal_change
    session.commit()
    print('------------------------') 
    print(f"Account No. {account.id} in {bank.b_name} bank current ballance of €{account.a_ballance}. Ballance change: €{bal_change}")
    print('------------------------') 
  else:
    print('------------------------') 
    print(f"{client.c_name} {client.c_surname} doesn't have any active accounts")

main_menu_items = {
  1: 'Add new client',
  2: 'Change client information',
  3: 'Add new bank',
  4: 'Deposit/withdraw funds',
  5: 'Add new account',
  6: 'List all banks',
  7: 'List all accounts',
  8: 'List all clients',
  9: 'List client information',
  0: 'Quit'
}

def main_menu():
  for key in main_menu_items.keys():
    print(key, '-', main_menu_items[key])

def main():
  while True:
    main_menu()
    selection = ''
    try:
      selection = int(input('Select desired action: '))
    except ValueError:
      print('Please enter a number: ')
      continue
    if selection == 1:
      new_client()
    elif selection == 2:
      edit_client_data()
    elif selection == 3:
      new_bank()
    elif selection == 4:
      edit_account()
      pass
    elif selection == 5:
      new_account()
    elif selection == 6:
      list_banks()
    elif selection == 7:
      list_accounts()
    elif selection == 8:
      list_clients()
    elif selection == 9:
      client_accounts()
    elif selection == 0:
      print('Quitting...')
      break
    else:
      print('Select number from list!')

if __name__ == '__main__':
  main()    