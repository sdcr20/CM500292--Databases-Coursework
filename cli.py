import sqlite3
from tabulate import tabulate 
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUERIES_DIR = BASE_DIR / "queries"
ALTERS_DIR = BASE_DIR / "alters"

class DuplicateLicenceNumberException:
    """Raised when a licence number already exists"""
    pass

def load_sql(sql_dir: Path, filename: str) -> str:
    path = sql_dir / filename
    return path.read_text().strip()

# executes sql queries by opening files. Used for fixed queries. Prints out the results. 
def execute_sql(filename):    
    sql = load_sql(QUERIES_DIR, filename)   
    try: 
        c.execute(sql)        
        if c.description is not None:    
            column_names = [description[0] for description in c.description]
            rows = c.fetchall()
            table = tabulate(rows, headers=column_names, tablefmt="grid")
            print(table)
        else:
            print("The query did not return any results.")
    except sqlite3.Error as e:
        print("Query error: ", e)

def execute_param_sql(filename, param):
    sql = load_sql(QUERIES_DIR, filename)   
    try: 
        c.execute(sql, param)        
        if c.description is not None:    
            column_names = [description[0] for description in c.description]
            rows = c.fetchall()
            table = tabulate(rows, headers=column_names, tablefmt="grid")
            print(table)
        else:
            print("The query did not return any results.")
    except sqlite3.Error as e:
        print("Query error: ", e)

def execute_alter_sql(filename, params):
    sql = load_sql(ALTERS_DIR, filename)
    try:
        c.execute(sql, params)
        c.connection.commit()
    except sqlite3.Error as e:
        print("Input error: ", e)
        raise

def pilot_menu():
    print("\n Pilot Menu")
    print(" 1. View Pilot Roster")
    print(" 2. Search for a Pilot")
    print(" 3. Add a pilot")
    print(" 4. Remove a pilot")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        execute_sql("pilot_roster.sql")
        pilot_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        add_pilot()
    elif menu_option == 4:
        delete_pilot()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")

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
    params = (name, licence_number, aircraft_rating, base_id, last_medical_date)
    print(txt)    
    while True:
        print("Press 1 to add the new pilot to the database")
        print("Press 2 to cancel the database entry:")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("add_pilot.sql", params)
                break
            elif menu_option == 2:
                print("\n Transaction Cancelled.")
                pilot_menu()
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again.")
    
def delete_pilot():
    delete_id = input("Enter the Pilot ID of the pilot you wish to delete: ")
    try:
        delete_id = int(delete_id)
    except ValueError:
            print("Pilot ID must be a number.")
    execute_param_sql("pilot_id.sql", (delete_id,))
    print("\n Is this the pilot you want to delete?")
    while True:
        print("If yes select 1")
        print("If no press 2")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("delete_pilot.sql", (delete_id,))
                print("Pilot deleted")
                pilot_menu()
                break
            elif menu_option == 2:
                print("\n Transaction Cancelled.")
                pilot_menu()
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again.")

def flight_menu():
    print("\n Flight Menu")
    print("\n 1. View Upcoming Flights")
    print(" 2. Add a New Flight")
    print(" 3. Search for Flights")
    print(" 4. Remove a Flight")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))

    if menu_option == 1:
        execute_sql("all_flight.sql")
        flight_menu()
    elif menu_option == 2:
        add_flight()
    elif menu_option == 3:
        destination_menu()  
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")
        
def add_flight():
    number = input("Enter flight number: ")
    execute_sql("destinations.sql")
    while True:
        departure_id = int(input("Enter departure airport ID: "))
        try:
            departure_id = int(departure_id)
            break
        except:
            print("Departure ID must be a number.")
    while True:
        arrival_id = int(input("Enter arrival airport ID: "))
        try:
            arrival_id = int(arrival_id)
            break
        except:
            print("Arrival ID must be a number.")
    execute_sql("pilot_roster.sql")
    pilot_id = input("Enter the Pilot ID of the pilot: ")
    try:
        pilot_id = int(pilot_id)
    except ValueError:
            print("Pilot ID must be a number.")
    execute_param_sql("pilot_id.sql", (pilot_id,))
    while True:
        departure_date_utc = input("Enter departure date and time in the format yyyy-mm-dd hh-mm-ss")
        format = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.strptime(departure_date_utc, format)
            break
        except:
            print("Ensure date is in the format: YYYY-MM-DD HH:MM:SS")
    while True:
        arrival_date_utc = input("Enter arrival date and time in the format yyyy-mm-dd hh-mm-ss")
        format = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.strptime(arrival_date_utc, format)
            break
        except:
            print("Ensure date is in the format: YYY-MM-DD HH:MM:SS")
    print("\nPlese review your input below.")    
    txt = f"Flight Number: {number}\nDeparture Airport: {departure_id}\nArrival Aiport: {arrival_id}\nPilot ID: {pilot_id}\nDeparture time: {departure_date_utc}\nArrival time: {arrival_date_utc}"
    params = (number, departure_id, arrival_id, pilot_id, departure_date_utc, arrival_date_utc)
    print(txt)
    while True:
        print("Press 1 to add the new flight to the database")
        print("Press 2 to cancel the database entry:")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("add_flight.sql", params)
                flight_menu()
                break
            elif menu_option == 2:
                print("\n Transaction Cancelled.")
                flight_menu()
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again.")
    

    
def destination_menu():
    print("\n Destination Menu")
    print(" 1. View Destinations")
    print(" 2. Search for a Destination")
    print(" 3. Add a Destination")
    print(" 4. Remove a Destination")
    print(" 0. Return to Main Menu")
    
    menu_option = int(input("\nEnter menu option: "))
    if menu_option == 1:
        execute_sql("destinations.sql")
        destination_menu()
    elif menu_option == 2:
        pilot_menu()
    elif menu_option == 3:
        add_destination()
    elif menu_option == 4:
        delete_airport() 
    elif menu_option == 0:
        main_menu()
    else:
        print("\n Invalid Input")
        
def add_destination():
    name = input("Enter airport name: ")
    city = input("Enter airport city: ")
    country = input("Enter airport country: ")
    execute_sql("timezone.sql")
    timezone = input("Enter airport timezone from the above list: ")
    
    print("\n Please review your input below.")
    txt = f"Name: {name}\nCity: {city}\nCountry: {country}\nTimezone: {timezone}"
    params = (name, city, country, timezone)
    print(txt)
    while True:
        print("Press 1 to add the new destination to the database")
        print("Press 2 to cancel the database entry.")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("add_destination.sql", params)
                destination_menu()
                break
            elif menu_option == 2:
                print("\nTransaction Cancelled.")
                destination_menu()
                break
            else:
                print("Invalid input, try again.")
        except ValueError:
            print("Invalid input, try again.")
            
def delete_airport():
    execute_sql("destinations.sql")
    delete_id = input("Enter the Destination ID of the destination you wish to delete: ")
    try:
        delete_id = int(delete_id)
    except ValueError:
            print("Destination ID must be a number.")
    execute_param_sql("destination_id.sql", (delete_id,))
    print("\n Is this the destination you want to delete?")
    while True:
        print("If yes select 1")
        print("If no press 2")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("delete_destination.sql", (delete_id,))
                print("Destination deleted")
                destination_menu()
                break
            elif menu_option == 2:
                print("\n Transaction Cancelled.")
                destination_menu()
                break
            else:
                print("Invalid input, try again")
        except ValueError:
            print("Invalid input, try again.")
    

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

# Used to populate an empty database by running each SQL command in the database.sql file
# Based on https://stackoverflow.com/questions/19472922/reading-external-sql-script-in-python
def populate_database():
    # opens and reads the sql file to a buffer
    sql = load_sql(BASE_DIR, 'database.sql')
    # executes all the commands in sequence
    try:
        c.executescript(sql)
        # handles any errors
    except sqlite3.Error as e:
        print("Population Error: ", e)

try:
    # Connects to the database
    conn = sqlite3.connect('CM500292--Databases-Coursework\database.db')
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