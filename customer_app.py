import json
import random

class BankApp:

    def __init__(self, json_file):
        self.json_file = json_file
        self.users = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.json_file) as f:
                 data = json.load(f)
            self.users = data['users']
        except FileNotFoundError:  
            # File doesn't exist yet, create it
            with open(self.json_file, 'w') as f:
                data = {'users': []}
            json.dump(data, f)
            self.users = []
            
    def save_data(self):
        data = {
        "users": self.users
        }
        
        with open(self.json_file, 'w') as f:  
            json.dump(data, f, indent=2)

    def is_valid_dob(self, dob):
        if len(dob) != 10 or dob[2] != "/" or dob[5] != "/":
            return False

        day = dob[:2]
        month = dob[3:5]
        year = dob[6:]

        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return False

        return True

    def is_duplicate(self, fname, lname):
        for user in self.users:
            if user["first_name"] == fname and user["last_name"] == lname:
                return True
        return False

    def create_account(self):
      while True:
          first_name = input("Enter first name: ")
          last_name = input("Enter last name: ")

          if self.is_duplicate(first_name, last_name):
              print("Name already exists. Please try again.")
              continue

          break

      while True:
          dob = input("Enter DOB (DD/MM/YYYY): ")
          if not self.is_valid_dob(dob):
              print("Invalid format. Try again.")
              continue
          break

      pin = input("Enter 4-digit PIN: ")
      while len(pin) != 4 or not pin.isdigit():
          print("Invalid PIN. Try again.")
          pin = input("Re-enter PIN: ")

      account_number = self.generate_account_number()

      user = {
          "first_name": first_name,
          "last_name": last_name,
          "dob": dob,
          "account_number": account_number,
          "pin": pin,
          "balance": 0
      }

      self.users.append(user)
      self.save_data()

      print("Account created!")
      print("Account Number:", account_number)


    def generate_account_number(self):
        while True:
            account_number = random.randint(1000000000, 9999999999)
            if not self.is_duplicate_account(account_number):
                return account_number

    def is_duplicate_account(self, account_number):
        for user in self.users:
            if user["account_number"] == account_number:
                return True
        return False

    def authenticate(self, account_number, pin):
        self.load_data()
        account_number = int(account_number)

        for user in self.users:
            if user["account_number"] == account_number:
                if user["pin"] == pin:
                    return user
                else:
                    print("Incorrect PIN")
                    return None

        print("Invalid account number")
        return None

    def get_user(self, account_number):
        account_number = int(account_number)
        for user in self.users:
            if user["account_number"] == account_number:
                return user
        return None

    def check_balance(self, user):
        print("Balance:")
        print(user["first_name"], user["last_name"])
        print("$" + str(user["balance"]))

    def transfer(self, sender, recipient, amount):
        print(f"Transfer {amount} from {sender['first_name']} {sender['last_name']} to {recipient['first_name']} {recipient['last_name']}?")
        confirm = input("Confirm details? (yes/no): ")
        if confirm.lower() != "yes":
            return

        if amount > sender["balance"]:
            print("Insufficient balance!")
            return

        sender_pin = input("Enter your PIN to confirm: ")
        if sender_pin != sender["pin"]:
            print("Incorrect PIN!")
            return

        sender["balance"] -= amount
        recipient["balance"] += amount
        self.save_data()

        print("Transfer successful!")

    def reset_pin(self, user):
      print("Reset PIN")

      if "dob" in user:
          dob = input("Enter DOB: ")
          if dob != user["dob"]:
              print("Incorrect DOB")
              return

      confirm = input("Confirm reset (yes/no): ")
      if confirm.lower() != "yes":
          return

      new_pin = input("New PIN: ")
      while len(new_pin) != 4 or not new_pin.isdigit():
          print("Invalid PIN")
          new_pin = input("Re-enter PIN: ")

      user["pin"] = new_pin
      self.save_data()

      print("Reset successful!")

    def main(self):
        app = BankApp("data.json")

        while True:
            print()
            print("Welcome to Chuka's Bank App!")
            print("1. Create New Account")
            print("2. Login")
            print("3. Quit")

            option = input("Select option: ")

            if option == "1":
                app.create_account()

            elif option == "2":
                account_number = input("Enter account number: ")
                pin = input("Enter PIN: ")
                user = app.authenticate(account_number, pin)

                if user:
                    print(f"Welcome {user['first_name']} {user['last_name']}!")

                    while True:
                        print("1. Check Balance")
                        print("2. Transfer")
                        print("3. Reset PIN")
                        print("4. Logout")

                        option = input("Select option: ")

                        if option == "1":
                            app.check_balance(user)

                        elif option == "2":
                            recipient_account_number = input("Enter recipient's account number: ")
                            amount = float(input("Enter the amount to transfer: $"))
                            recipient = app.get_user(recipient_account_number)
                            if not recipient:
                                print("Recipient account not found.")
                                continue

                            app.transfer(user, recipient, amount)

                        elif option == "3":
                            app.reset_pin(user)

                        elif option == "4":
                            break

            # elif option == "3":
            #     break

if __name__ == "__main__":
    app = BankApp("data.json")
    app.load_data()
    app.main()