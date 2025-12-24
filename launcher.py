import os

def menu():
    print("==== Port Scanner ====")
    print("1. Run CLI Scanner")
    print("2. Run Web Interface")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        os.system("python scanner.py")

    elif choice == "2":
        os.system("python app.py")

    elif choice == "3":
        print("Goodbye!")
        exit()

    else:
        print("Invalid choice.")
        menu()

if __name__ == "__main__":
    menu()
