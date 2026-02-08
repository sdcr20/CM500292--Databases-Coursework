import sqlite3
from string import Template
from tabulate import tabulate 
from datetime import datetime

def add_pilot():
    name = input("Enter pilot name: ")
    while True:
        licence_number = input("Enter licence number: ")
        try:
            licence_number = int(licence_number)
            break
        except ValueError:
            print("Licence Number must be a number.")
            
    aircraft_rating = input("Enter aircraft rating: ")
    while True:
        base_id = input("Enter base ID: ")
        try:
            base_id = int(base_id)
            break
        except:
            print("Base ID must be a number.")
    while True:
        last_medical_date = input("Enter date of last medical in the format YYYY-MM-DD.")
        format = "%Y-%m-%d"
        try:
            datetime.strptime(last_medical_date, format)
            break
        except:
            print("Ensure date is in the format: YYYY-MM-DD")
            
    print("\nPlease review your input below.")
    txt = f"Name: {name}\nLicence Number: {licence_number}\nAircraft Rating: {aircraft_rating}\nBase ID: {base_id}\nLast Medical Date: {last_medical_date}"
    print(txt)    
    while True:
        print("Press 1 to add the new pilot to the database")
        print("Press 2 to cancel the database entry:")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                main_menu()
                break
            elif menu_option == 2:
                print("\n Transaction Cancelled.")
                pilot_menu()
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again.")
    


# executes sql queries by opening files. Used for fixed queries. Prints out the results. 
def execute_sql(filename):    
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()    
    try: 
        c.execute(sqlFile)        
        if c.description is not None:    
            column_names = [description[0] for description in c.description]
            rows = c.fetchall()
            table = tabulate(rows, headers=column_names, tablefmt="grid")
            print(table)
        else:
            print("The query did not return any results.")
    except sqlite3.Error as e:
        print("Query error: ", e) 
    
# Used to populate an empty database by running each SQL command in the database.sql file
# Based on https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
def populate_database():
    # opens and reads the sql file to a buffer
    fd = open('database.sql', 'r')
    sqlFile = fd.read()
    fd.close()  
    # executes all the commands in sequence
    try:
        c.executescript(sqlFile)
        # handles any errors
    except sqlite3.Error as e:
        print("Population Error: ", e)

def flight_menu():
    print("\n Flight Menu")
    print("\n 1. View Upcoming Flights")
    print(" 2. Add a New Flight")
    print(" 3. Search for Flights")
    print(" 4. Remove a Flight")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        execute_sql("queries/all_flight.sql")
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
    print(" 1. View Pilot Roster")
    print(" 2. Search for a Pilot")
    print(" 3. Add a pilot")
    print(" 4. Remove a pilot")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        execute_sql("queries/pilot_roster.sql")
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        add_pilot()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")
    
def destination_menu():
    print("\n Destination Menu")
    print(" 1. View Destinations")
    print(" 2. Search for a Destination")
    print(" 3. Add a Destination")
    print(" 4. Remove a Destination")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))
    if menu_option == 1:
        execute_sql("queries/destinations.sql")
        destination_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")

def main_menu():
    print("\n Welcome to the Flight Management Database")
    print(" -----------------------------------------")
    print(" Please select one of the following options")
    print("\n1. Flights Menu")
    print("2. Pilot Menu")
    print("3. Destination Menu")
    print("4. Test")
    print("0. Exit")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        flight_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        conn.close()
        print("\nDatabase Connection Closed")
        print("Logging Off...")
        print("Goodbye\n")
        exit(0)
    elif menu_option == 4:
        sqlfile = input("Enter filename: ")
        execute_sql(sqlfile)
    else:
        print("\n Invalid Input")
        main_menu()

try:
    # Connects to the database
    conn = sqlite3.connect('database.db')
    print("\n Connecting to Database...")
    c = conn.cursor()
    # Checks whether the database is populated
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    # populates an empty database
    if not tables:
        print("Populating database")
        populate_database()
        print("Connected")
        main_menu()
    else:
        print(" Connected")
        main_menu()
except sqlite3.DatabaseError:
    print("Database error detected")