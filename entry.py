from customer_app import BankApp
from agent_app import AgentApp

def launch_customer_app():
    print("Launching Customer Bank App...")
    bank_app = BankApp("data.json")
    bank_app.load_data()
    bank_app.main()

def launch_agent_app():
    print("Launching Agent App...")
    agent_app = AgentApp("data.json") 
    agent_app.load_data()
    agent_app.main()

if __name__ == "__main__":
    while True:
        print("1. Launch Customer App")
        print("2. Launch Agent App")
        print("3. Quit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            launch_customer_app()
        elif choice == "2":
            launch_agent_app()
        elif choice == "3":
            print("Thank you for using our Agent App, Goodbye")
            break
        else:
            print("Invalid choice")
