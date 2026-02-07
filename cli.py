import sqlite3

def flight_menu():
    print("\n Flight Menu")
    print("\n 1. View Upcoming Flights")
    print("\n 2. Add a New Flight")
    print("\n 3. Search for Flights")
    print("\n 4. Remove a Flight")
    print("\n 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        flight_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")
    
def pilot_menu():
    print("\n Pilot Menu")
    print("\n 1. View Pilot Roster")
    print("\n 2. Search for a Pilot")
    print("\n 3. Add a pilot")
    print("\n 4. Remove a pilot")
    print("\n 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        flight_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")
    
def destination_menu():
    print("\n Destination Menu")
    print("\n 1. View Destinations")
    print("\n 2. Search for a Destination")
    print("\n 3. Add a Destination")
    print("\n 4. Remove a Destination")
    print("\n 0. Return to Main Menu")
    
    menu_option = input("\nEnter menu option: ")
    if menu_option == 1:
        flight_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")

def main_menu():
    while True:
        print("\n Welcome to the Flight Management Database")
        print(" -----------------------------------------")
        print(" Please select one of the following options")
        print("\n1. Flights Menu")
        print("2. Pilot Menu")
        print("3. Destination Menu")
        print("0. Exit")
    
        menu_option = int(input("\nEnter menu option: "))

        if menu_option == 1:
            flight_menu()
        elif menu_option == 2:
            pilot_menu()
        elif menu_option == 3:
            destination_menu()  
        elif menu_option == 0:
            print("\nLogging Off...")
            print("Goodbye")
            exit(0)
        else:
            print("\n Invalid Input")

main_menu()