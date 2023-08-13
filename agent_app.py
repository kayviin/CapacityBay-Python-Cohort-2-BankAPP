import json

class AgentApp:
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


    def display_customer_database(self):
        self.load_data()
        for user in self.users:
            print(user)
            
    def get_account(self, account_number):
        for user in self.users:
            if user["account_number"] == account_number:
                return user

    def reset_customers_pin(self, account_number):

        account_number = int(account_number)

        self.load_data()

        for user in self.users:  
            if user["account_number"] == account_number:
                
                print(f"Account found for: {user['first_name']} {user['last_name']}")
                confirm = input("Are you sure you want to reset PIN? (yes/no): ")
                if confirm.lower() == "yes":
                    new_pin = input("Enter new PIN:")
                    user["pin"] = new_pin 
        
        self.save_data()
        print("Reset successful!")

    def deposit_money(self):
        account_number = input("Enter customer's account number: ")
        account_number = int(account_number)
        user = self.get_account(account_number)
        if user:
            print(f"Depositing money into {user['first_name']} {user['last_name']}'s account")
            amount = float(input("Enter amount to deposit: "))
            confirm = input("Confirm deposit? (yes/no): ")
            if confirm.lower() == "yes":
                user["balance"] += amount
                self.save_data()
                print("Deposit successful!")
            else:
                print("Deposit canceled")
        else:
            print("User not found")
            
    def perform_customer_transaction(self):
        sender_acct = input("Enter sender account:")
        sender_acct = int(sender_acct)
        sender = self.get_account(sender_acct)

        if sender:
            print(f"Sender: {sender['first_name']} {sender['last_name']}")
            confirm_sender = input("Confirm sender? (yes/no): ")

            if confirm_sender.lower() == 'yes':
                recipient_acct = input("Enter recipient account:")
                recipient_acct = int(recipient_acct)
                recipient = self.get_account(recipient_acct)

                if recipient:
                    print(f"Recipient: {recipient['first_name']} {recipient['last_name']}")
                    confirm_recipient = input("Confirm recipient? (yes/no): ")

                    if confirm_recipient.lower() == 'yes':
                        amount = float(input("Enter transfer amount:"))

                        if amount > sender['balance']:
                            print("Insufficient funds!")
                        else:
                            sender['balance'] -= amount
                            recipient['balance'] += amount

                        self.save_data()

                        print("Transfer complete!")

                    else:
                        print("Transfer canceled (recipient not confirmed)")

                else:
                    print("Recipient not found")

            else:
                print("Transfer canceled (sender not confirmed)")

        else:
            print("Sender not found")


    def save_data(self):
        data = {"users": self.users}
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=2)

    def main(self):
        print("Welcome to the Agent App")

        while True:
            print("\nMenu:")
            print("1. Display Customer Database")
            print("2. Reset Customer PIN")
            print("3. Deposit Money")
            print("4. Perform Customer Transaction")
            print("5. Quit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                self.display_customer_database()
            elif choice == "2":
                account_number = input("Enter customer's account number: ")
                self.reset_customers_pin(account_number)
            elif choice == "3":
                self.deposit_money()
            elif choice == "4":
                self.perform_customer_transaction()
            elif choice == "5":
                print("Thank you for using the Agent App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    

if __name__ == "__main__":
    app = AgentApp("data.json")
    app.main()