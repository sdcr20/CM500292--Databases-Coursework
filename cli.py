import sqlite3
from string import Template
from tabulate import tabulate 

# executes sql queries by opening files. Used for fixed queries. Prints out the results. 
def execute_sql(filename):    
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()    
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        c.execute(command)
        
        if c.description is not None:    
            column_names = [description[0] for description in c.description]
            rows = c.fetchall()
            table = tabulate(rows, headers=column_names, tablefmt="grid")
            print(table)
            main_menu()
        else:
            print("The query did not return any results.")
            main_menu()
    
# Used to populate an empty database by running each SQL command in the database.sql file
# Based on https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
def populate_database():
    # opens and reads the sql file to a buffer
    fd = open('database.sql', 'r')
    sqlFile = fd.read()
    fd.close()
    # splits the file into the separate commands based on the ; 
    sqlCommands = sqlFile.split(';')
    # executes all the commands in sequence
    for command in sqlCommands:
        try:
            c.execute(command)
        # handles any errors
        except sqlite3.Error as e:
            print("Command Skipped: ", e)

def flight_menu():
    print("\n Flight Menu")
    print("\n 1. View Upcoming Flights")
    print(" 2. Add a New Flight")
    print(" 3. Search for Flights")
    print(" 4. Remove a Flight")
    print(" 0. Return to Main Menu")
    
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
    print(" 1. View Pilot Roster")
    print(" 2. Search for a Pilot")
    print(" 3. Add a pilot")
    print(" 4. Remove a pilot")
    print(" 0. Return to Main Menu")
    
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
    print(" 1. View Destinations")
    print(" 2. Search for a Destination")
    print(" 3. Add a Destination")
    print(" 4. Remove a Destination")
    print(" 0. Return to Main Menu")
    
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