import sqlite3
from tabulate import tabulate 
from datetime import datetime
from pathlib import Path
from string import Template

# Sets paths for different folders containing SQL queries
BASE_DIR = Path(__file__).resolve().parent
QUERIES_DIR = BASE_DIR / "queries"
ALTERS_DIR = BASE_DIR / "alters"

# Dictionary for use in pilot_search()
PILOT_SEARCH_FIELDS = {
    "ID":"pilot.pilot_id",
    "Name":"pilot.name",
    "Licence Number":"pilot.licence_number",
    "Aircraft Rating":"pilot.aircraft_rating",
    "Base Airport ID":"pilot.base_id",
    "Last Medical Date":"pilot.last_medical_date,"
}

# Dictionary for use in pilot_update()
PILOT_UPDATE_FIELDS = {
    "Name":("name", "TEXT"),
    "Licence Number":("licence_number", "TEXT"),
    "Aircraft Rating":("aircraft_rating", "TEXT"),
    "Base Airport ID":("base_id", "INTEGER"),
    "Last Medical Date":("last_medical_date," "TEXT"),
}

# Defines cases for use in validate_fields
INT_FIELDS = {
    "Base Airport ID",
    "Departure Airport ID",
    "Arrival Airport ID",
}
DATE_FIELDS = {
    "Last Medical Date",
}
DATE_TIME_FIELDS = {
    "Departure Date/Time",
    "Arrival Date/Time",
}

# Dictionary for use in flight_search()
FLIGHT_SEARCH_FIELDS = {
    "ID":"flight.flight_id",
    "Flight Number":"flight.flight_number",
    "Departure ID":"flight.departure_id",
    "Arrival ID":"flight.arrival_id",
    "Pilot ID":"flight.pilot_id",
    "Departure Date/Time":"departure_time_utc",
    "Arrival Date/Time":"arrival_time_utc",
}

# Dictionary for use in flight_update()
FLIGHT_UPDATE_FIELDS = {
    "Flight Number":("flight_number", "TEXT"),
    "Departure Airport ID":("departure_id", "INTEGER"),
    "Arrival Airport ID":("arrival_id", "INTEGER"),
    "Pilot ID":("pilot_id", "INTEGER"),
    "Departure Date/Time":("departure_time_utc", "TEXT"),
    "Arrival Date/Time":("arrival_time_utc", "TEXT"),
}

# Dictionary for use in destination_search()
DESTINATION_SEARCH_FIELDS = {
    "ID":"destination.destination_id",
    "Airport Name":"destination.name",
    "City":"destination.city",
    "Country":"destination.country",
    "Timezone":"destination.timezone",
}

# Dictionary for use in destination_update()
DESTINATION_UPDATE_FIELDS = {
    "Name":("name", "TEXT"),
    "City":("city", "TEXT"),
    "Country":("country", "TEXT"),
    "Timezone":("timezone", "TEXT"),
}

# Validates the fields used by the update() functions 
def validate_fields(field_label, new_value):
    # Entry validaton for ints
    if field_label in INT_FIELDS:
        try:
            return int(new_value)
        except ValueError:
            print(f"\n{field_label} must be a number.")
            print("Returning to main menu...")
            main_menu()
    # Entry validation for dates        
    if field_label in DATE_FIELDS:
        try:
            datetime.strptime(new_value.strip(), "%Y-%m-%d")
            return new_value.strip()
        except ValueError:
            print(f"\n{field_label} must be in the format YYYY-MM-DD.")
            print("Returning to main menu...")
            main_menu()
    # Entry validation for datetime fields
    if field_label in DATE_TIME_FIELDS:
        try:
            datetime.strptime(new_value.strip(), "%Y-%m-%d %HH:%MM:%SS")
            return new_value.strip()
        except ValueError:
            print(f"\n{field_label} must be in the format YYYY-MM-DD HH:MM:SS")
            print("Returning to main menu...")
            main_menu()
    return new_value.strip()
    
# Helper function to print results
def print_results(rows):
    if not rows:
        print("No results.")
        return
    if isinstance(rows[0], sqlite3.Row):
        rows = [dict(r) for r in rows]
    print(tabulate(rows, headers="keys", tablefmt="grid"))

# Reads a sql script
def load_sql(sql_dir: Path, filename: str) -> str:
    path = sql_dir / filename # uses path to allow definition of script by filename alone.
    return path.read_text().strip()

# Executes sql queries by opening files. Used for fixed queries. Prints out the results. 
def execute_sql(filename):    
    sql = load_sql(QUERIES_DIR, filename)   
    try: 
        c.execute(sql)        
        rows = c.fetchall()
        print_results(rows)
    except sqlite3.Error as e:
        print("Query error: ", e)

# Executes sql queries that search by an individual parameter e.g. pilot_id
def execute_param_sql(filename, param):
    sql = load_sql(QUERIES_DIR, filename)   
    try: 
        c.execute(sql, param)        
        rows = c.fetchall()
        print_results(rows)
    except sqlite3.Error as e:
        print("Query error: ", e)

# Executes sql queries that add or delete from a table
def execute_alter_sql(filename, params):
    sql = load_sql(ALTERS_DIR, filename)
    try:
        c.execute(sql, params)
        c.connection.commit()
    except sqlite3.Error as e:
        print("Input error: ", e)
        raise

# Pilot menu code
def pilot_menu():
    print("\n Pilot Menu")
    print(" 1. View Pilot Roster")
    print(" 2. Search for a Pilot")
    print(" 3. Add a pilot")
    print(" 4. Remove a pilot")
    print(" 5. Amend a pilot")
    print(" 0. Return to Main Menu")
    
    # Input validation of menu_option
    while True:
        try:
            menu_option = int(input("\nEnter menu option: "))
            break # breaks out of the while loop
        except ValueError:
            print("Invalid Input")
    while True: # while loop for the menu options
        if menu_option == 1:
            execute_sql("pilot_roster.sql")
            pilot_menu()
            break
        elif menu_option == 2:
            search_pilot_prompt()
            break
        elif menu_option == 3:
            add_pilot()
            break
        elif menu_option == 4:
            delete_pilot()
            break  
        elif menu_option == 5:
            update_pilot_prompt()
            break
        elif menu_option == 0:
            main_menu()
            break
        else:
            print("\n Invalid Input")

# Searches for a pilot depending on the field selected and value entered            
def search_pilot(field_label: str, value: str, *, partial: bool = False):
    column = PILOT_SEARCH_FIELDS.get(field_label) # gets the value from the dictionary for use in the query
    if not column:
        raise ValueError(f"Unsupported search field {field_label}") # raises an error if the field is not in the dictionary
    if partial:
        where_clause = f"WHERE {column} LIKE ?" # passed into the sql query and allows for partial matches when searching
        params = (f"%{value}%",) 
    else:
        where_clause = f"WHERE {column} = ?" # passed into the sql query for an exact value
        params = (value,)
    
    sql_text = load_sql(QUERIES_DIR, "pilot_search.sql") # loads the sql query
    sql = Template(sql_text).substitute(where_clause=where_clause) # passes the where clause into the sql query
    try:
        c.execute(sql, params)
        return c.fetchall()
    except sqlite3.Error as e:
        print("Query error: ", e)
        return[] # returns an empty list if there is a query error. Used by print_results() to detect negative results
 
# Prompt selected from the pilot menu to search for a pilot
def search_pilot_prompt():
    print("Search by: ")
    for i, label in enumerate(PILOT_SEARCH_FIELDS.keys(), start=1): # starts list at 1 for ease of use
        print(f"{i}. {label}") # prints out the list of search field keys and assigns each a number
    choice = int(input("Choose seach field: ")) # takes user selection
    field_label = list(PILOT_SEARCH_FIELDS.keys())[choice-1] # uses input number to define field_label. Choice-1 to account for options starting at 1 where index starts at 0.
    
    value = input(f"Enter value for {field_label}: ").strip() # takes the value to be searched for. Strips any whitespace
    
    partial = False
    if field_label not in {"Pilot ID"}: # prevents use of partial search on ID field
        use_partial = input("Partial match? (Y/N): ").lower() # allows decision of use of partial matches
        partial = (use_partial == "y")
        rows = search_pilot(field_label, value, partial=partial) # triggers the search_pilot function
        print_results(rows) # prints the results
        pilot_menu() # returns to the pilot menu
        
# Updates the pilot record based on the input from pilot_update_prompt
def update_pilot(pilot_id, field_label, new_value):
    mapping = PILOT_UPDATE_FIELDS.get(field_label)
    if not mapping:
        raise ValueError(f"Unsupported field: {field_label}")
    column, _kind = mapping # unpacks the column name from the tuple contained in the dictionary
    validated = validate_fields(field_label, new_value) # passes the data in for validation
    
    sql_text = load_sql(ALTERS_DIR, "update_pilot.sql") # loads the sql
    set_clause = f"{column} = :value" # uses column to select the table column for update
    where_clause = "WHERE pilot.pilot_id = :pilot_id" # uses pilot id to select the record for update
    sql = Template(sql_text).substitute(set_clause=set_clause, where_clause=where_clause) # passes the clauses in to the sql query
    
    try:
        c.execute(sql, {"value": validated, "pilot_id": pilot_id}) # carries out the update
        c.connection.commit() # save the database after update
        if c.rowcount == 0: # if no rows are found then prints error message
            print("No pilot updated, pilot ID not found")
            return False
        print(f"Updated {field_label} for Pilot ID {pilot_id}.")
        return True
    except sqlite3.IntegrityError as e: # error handling for value entry
        msg = str(e).lower()
        if "unique constraint failed" in msg and "pilot.licence_number" in msg:
            print("Error: licence number must be unique.")
        elif "foreign key constraint failed" in msg:
            print("Error: base id must reference an existing airport.")
        else:
            print("Integrity Error", e)
        return False

# Prompt selected from the pilot menu to update a pilot    
def update_pilot_prompt():
    while True:
        try: # Input validation 
            pilot_id = int(input("Enter Pilot ID to update: "))
            break
        except ValueError:
            print("Pilot ID must be a number.")
    
    execute_param_sql("pilot_id.sql", (pilot_id,)) # prints the pilot to be updated  
    labels = list(PILOT_UPDATE_FIELDS.keys())
    print("\nWhich field do you want to update?")
    for i, label in enumerate(labels, start=1): # prints the variables for amendment with a number allocated
        print(f"{i}. {label}")
    while True: # Input validation for choice
        try:
            choice = int(input("Enter choice: "))
            field_label = labels[choice-1]
            break
        except(ValueError, IndexError):
            print("Invalid choice.")
            
    new_value = input(f"Enter new value for {field_label}: ").strip() # takes new value for update
    
    ok = update_pilot(pilot_id, field_label, new_value) # runs the update_pilot()
    
    if ok: # prints the results
        rows = execute_param_sql("pilot_id.sql", (pilot_id,))
        print_results(rows)
        pilot_menu()

# Adds a pilot to the database
def add_pilot():
    name = input("Enter pilot name: ") # takes input
    while True:
        licence_number = input("Enter licence number: ")
        try: # validates number input
            licence_number = int(licence_number)
            break
        except ValueError:
            print("Licence Number must be a number.")            
    aircraft_rating = input("Enter aircraft rating: ")
    while True: # validates number input
        base_id = input("Enter base ID: ")
        try:
            base_id = int(base_id)
            break
        except:
            print("Base ID must be a number.")
    while True: # validates date input
        last_medical_date = input("Enter date of last medical in the format YYYY-MM-DD: ")
        format = "%Y-%m-%d"
        try:
            datetime.strptime(last_medical_date, format)
            break
        except:
            print("Ensure date is in the format: YYYY-MM-DD")
    # allows for input review        
    print("\nPlease review your input below.")
    txt = f"Name: {name}\nLicence Number: {licence_number}\nAircraft Rating: {aircraft_rating}\nBase ID: {base_id}\nLast Medical Date: {last_medical_date}"
    params = (name, licence_number, aircraft_rating, base_id, last_medical_date)
    print(txt)    
    while True:
        print("Press 1 to add the new pilot to the database")
        print("Press 2 to cancel the database entry:")
        try: # menu options to add the new pilot
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
        except ValueError: # handles non int input
            print("Invalid input, try again.")

# Deletes a pilot from the database
def delete_pilot():
    delete_id = input("Enter the Pilot ID of the pilot you wish to delete: ")
    try: # validation of id input
        delete_id = int(delete_id)
    except ValueError:
            print("Pilot ID must be a number.")
    execute_param_sql("pilot_id.sql", (delete_id,)) # prints the pilot that is about to be deleted
    print("\n Is this the pilot you want to delete?")
    while True: # confirms deletion
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

# Flight menu code
def flight_menu():
    print("\n Flight Menu")
    print("\n 1. View Upcoming Flights")
    print(" 2. Add a New Flight")
    print(" 3. Search for Flights")
    print(" 4. Remove a Flight")
    print(" 5. Update a Flight")
    print(" 0. Return to Main Menu")
    
    while True: # Input validation
        try:
            menu_option = int(input("\nEnter menu option: "))
            break
        except ValueError:
            print("Invalid Input")
    while True:
        if menu_option == 1:
            execute_sql("all_flight.sql")
            flight_menu()
            break
        elif menu_option == 2:
            add_flight()
            break
        elif menu_option == 3:
            search_flight_prompt()
            break
        elif menu_option == 4:
            delete_flight()
            break
        elif menu_option == 5:
            update_flight_prompt()
            break
        elif menu_option == 0:
            main_menu()
            break
        else:
            print("\n Invalid Input")

# Updates the flight record based on the input from flight_update_prompt
def update_flight(flight_id, field_label, new_value):
    mapping = FLIGHT_UPDATE_FIELDS.get(field_label)
    if not mapping:
        raise ValueError(f"Unsupported field: {field_label}")
    column, _kind = mapping # unpacks the column name from the tuple contained in the dictionary
    validated = validate_fields(field_label, new_value) # passes the data in for validation
    
    sql_text = load_sql(ALTERS_DIR, "update_flight.sql") # loads the sql
    set_clause = f"{column} = :value" # uses column to select the table column for update
    where_clause = "WHERE flight.flight_id = :flight_id" # uses pilot id to select the record for update
    sql = Template(sql_text).substitute(set_clause=set_clause, where_clause=where_clause) # passes the clauses in to the sql query
    
    try:
        c.execute(sql, {"value": validated, "flight_id": flight_id}) # carries out the update
        c.connection.commit() # save the database after update
        if c.rowcount == 0: # if no rows are found then prints error message
            print("No flight updated, flight ID not found")
            return False
        print(f"Updated {field_label} for Flight ID {flight_id}.")
        return True
    except sqlite3.IntegrityError as e: # error handling for value entry
        msg = str(e).lower()
        if "foreign key constraint failed" and "departure_id" in msg:
            print("Error: departure id must reference an existing airport.")
        elif "foreign key constraint failed" and "arrival_id" in msg:
            print("Error: arrival id must reference an existing airport.")
        elif "foreign key constraint failed" and "pilot" in msg:
            print("Error: pilot id must reference an existing pilot.")
        else:
            print("Integrity Error", e)
        return False

# Prompt selected from the flight menu to update a flight      
def update_flight_prompt():
    while True: # Input validation
        try:
            flight_id = int(input("Enter Flight ID to update: "))
            break
        except ValueError:
            print("Flight ID must be a number.")
    
    execute_param_sql("flight_id.sql", (flight_id,)) # prints the flight to be updated        
    labels = list(FLIGHT_UPDATE_FIELDS.keys())
    print("\nWhich field do you want to update?")
    for i, label in enumerate(labels, start=1): # prints the variables for amendment with a number allocated
        print(f"{i}. {label}")
    while True: # Input validation for choice
        try:
            choice = int(input("Enter choice: "))
            field_label = labels[choice-1]
            break
        except(ValueError, IndexError):
            print("Invalid choice.")
            
    new_value = input(f"Enter new value for {field_label}: ").strip() # takes new value for update
    
    ok = update_flight(flight_id, field_label, new_value) # runs update_flight()
    
    if ok: # prints the results
        rows = execute_param_sql("flight_id.sql", (flight_id,))
        print_results(rows)
        flight_menu()

# Searches for pilot depending on the parameter selected
def search_flight(field_label: str, value: str, *, partial: bool = False):
    column = FLIGHT_SEARCH_FIELDS.get(field_label) # gets the value from the dictionary for use in the query
    if not column: # Error handling
        raise ValueError(f"Unsupported search field {field_label}")
    if partial: # Determines whether partial matches are accepted
        where_clause = f"WHERE {column} LIKE ?"
        params = (f"%{value}%",)
    else:
        where_clause = f"WHERE {column} = ?"
        params = (value,)
    
    sql_text = load_sql(QUERIES_DIR, "flight_search.sql") # loads the sql file
    sql = Template(sql_text).substitute(where_clause=where_clause) # passes in the where clause
    try:
        c.execute(sql, params) # executes the search
        return c.fetchall()
    except sqlite3.Error as e:
        print("Query error: ", e)
        return[] # returns an empty list if there is a query error

# Prompt selected from flight menu for search
def search_flight_prompt():
    print("Search by: ")
    for i, label in enumerate(FLIGHT_SEARCH_FIELDS.keys(), start=1):
        print(f"{i}. {label}") # Prints out the list of search fields
    choice = int(input("Choose seach field: ")) # takes user selection
    field_label = list(FLIGHT_SEARCH_FIELDS.keys())[choice-1] # uses selection to define field
    value = input(f"Enter value for {field_label}: ").strip() # takes value input
    partial = False
    if field_label not in {"Flight ID"}: # determines if partial matches are allowed
        use_partial = input("Partial match? (Y/N): ").lower()
        partial = (use_partial == "y")
        rows = search_flight(field_label, value, partial=partial) # calls the search function
        print_results(rows) # prints results
        flight_menu()
            
def add_flight():
    number = input("Enter flight number: ") # takes input
    execute_sql("destinations.sql") # prints out a list of destinations
    while True:
        try: # validates number input
            departure_id = int(input("Enter departure airport ID: "))
            break
        except ValueError:
            print("Departure ID must be a number.")
    while True:
        try: # validates number input
            arrival_id = int(input("Enter arrival airport ID: "))
            break
        except ValueError:
            print("Arrival ID must be a number.")
    execute_sql("pilot_roster.sql")
    while True: # validates number input
        try:
            pilot_id = input("Enter the Pilot ID of the pilot: ")
            break
        except ValueError:
            print("Pilot ID must be a number.")
    execute_param_sql("pilot_id.sql", (pilot_id,)) # displays the pilot details
    while True: # checks formatting of dtg
        departure_date_utc = input("Enter departure date and time in the format yyyy-mm-dd hh-mm-ss: ")
        format = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.strptime(departure_date_utc, format)
            break
        except:
            print("Ensure date is in the format: YYYY-MM-DD HH:MM:SS")
    while True:
        arrival_date_utc = input("Enter arrival date and time in the format yyyy-mm-dd hh-mm-ss: ")
        format = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.strptime(arrival_date_utc, format)
            break
        except:
            print("Ensure date is in the format: YYY-MM-DD HH:MM:SS")
    print("\nPlese review your input below.")    
    txt = f"Flight Number: {number}\nDeparture Airport: {departure_id}\nArrival Aiport: {arrival_id}\nPilot ID: {pilot_id}\nDeparture time: {departure_date_utc}\nArrival time: {arrival_date_utc}"
    params = (number, departure_id, arrival_id, pilot_id, departure_date_utc, arrival_date_utc)
    print(txt) # displays input for review
    while True:
        print("Press 1 to add the new flight to the database")
        print("Press 2 to cancel the database entry")
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

# Deletes a flight from the database
def delete_flight():
    execute_sql("all_flight.sql") # Prints all flights
    delete_id = input("Enter the Flight ID of the flight you wish to delete: ")
    try: # validates the inputted id
        delete_id = int(delete_id)
    except ValueError:
            print("Flight ID must be a number.")
    execute_param_sql("flight_id.sql", (delete_id,))
    print("\n Is this the pilot you want to delete?")
    while True:
        print("If yes select 1")
        print("If no press 2")
        try:
            menu_option = int(input("Enter choice: "))
            if menu_option == 1:
                execute_alter_sql("delete_flight.sql", (delete_id,))
                print("flight deleted")
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

# Prints the destination menu    
def destination_menu():
    print("\n Destination Menu")
    print(" 1. View Destinations")
    print(" 2. Search for a Destination")
    print(" 3. Add a Destination")
    print(" 4. Remove a Destination")
    print(" 5. Update a Destination")
    print(" 0. Return to Main Menu")
    
    while True:
        try:
            menu_option = int(input("\nEnter menu option: "))
            break
        except ValueError: # input validation
            print("Invalid Input")
    while True:
        if menu_option == 1:
            execute_sql("destinations.sql")
            destination_menu()
            break
        elif menu_option == 2:
            search_destination_prompt()
            break
        elif menu_option == 3:
            add_destination()
            break
        elif menu_option == 4:
            delete_destination()
            break 
        elif menu_option == 5:
            update_destination_prompt()
            break
        elif menu_option == 0:
            main_menu()
            break
        else:
            print("\n Invalid Input")

# Updates the destination record            
def update_destination(destination_id, field_label, new_value):
    mapping = DESTINATION_UPDATE_FIELDS.get(field_label)
    if not mapping:
        raise ValueError(f"Unsupported field: {field_label}")
    column, _kind = mapping # unpacks the column name from the tuple held in the dictionary
    validated = validate_fields(field_label, new_value) # values for validation
    
    sql_text = load_sql(ALTERS_DIR, "update_destination.sql") # loads the file
    set_clause = f"{column} = :value" # uses column to select the table column for update
    where_clause = "WHERE destination.destination_id = :destination_id" # uses destination id to select the record for update
    sql = Template(sql_text).substitute(set_clause=set_clause, where_clause=where_clause) # passes field and value into the sql file
    
    try:
        c.execute(sql, {"value": validated, "destination_id": destination_id}) # executes the update
        c.connection.commit() # saves the update
        if c.rowcount == 0: # reports on a failed update
            print("No destination updated, destination ID not found")
            return False
        print(f"Updated {field_label} for Destination ID {destination_id}.") # prints the updated record
        return True
    except sqlite3.IntegrityError as e:
            print("Integrity Error", e)
            return False

# Prompt selected from the destination menu to update destination    
def update_destination_prompt():
    while True:
        try: # input validation
            destination_id = int(input("Enter Destination ID to update: "))
            break
        except ValueError:
            print("Flight ID must be a number.")
    
    execute_param_sql("destination_id.sql", (destination_id,)) # prints the record to be updated       
    labels = list(DESTINATION_UPDATE_FIELDS.keys())
    print("\nWhich field do you want to update?") # prints the options with a number for selection
    for i, label in enumerate(labels, start=1):
        print(f"{i}. {label}")
    while True:
        try: # input validation of choice
            choice = int(input("Enter choice: "))
            field_label = labels[choice-1]
            break
        except(ValueError, IndexError):
            print("Invalid choice.")
            
    new_value = input(f"Enter new value for {field_label}: ").strip() # takes in the new value to be added to the record
    
    ok = update_destination(destination_id, field_label, new_value) # executes the update
    
    if ok: # prints the result
        rows = execute_param_sql("destination_id.sql", (destination_id,))
        print_results(rows)
        flight_menu()

# Searches for a destination
def search_destination(field_label: str, value: str, *, partial: bool = False):
    column = DESTINATION_SEARCH_FIELDS.get(field_label) # gets the field from the dictionary
    if not column:
        raise ValueError(f"Unsupported search field {field_label}") # raises an error if the value is not found
    if partial:
        where_clause = f"WHERE {column} LIKE ?" # passed into the sql query for partial matches
        params = (f"%{value}%",)
    else:
        where_clause = f"WHERE {column} = ?" # passes into the sql file for exact matches
        params = (value,)
    
    sql_text = load_sql(QUERIES_DIR, "destination_search.sql")
    sql = Template(sql_text).substitute(where_clause=where_clause) # passes the values in to search by
    try:
        c.execute(sql, params) # executes the search
        return c.fetchall()
    except sqlite3.Error as e:
        print("Query error: ", e)
        return[]

# Prompt for search from search menu
def search_destination_prompt():
    print("Search by: ")
    for i, label in enumerate(DESTINATION_SEARCH_FIELDS.keys(), start=1):
        print(f"{i}. {label}") # prints list of fields to search by
    while True:
        try:
            choice = int(input("Choose seach field: ")) # takes user input
            break
        except ValueError: # input validation
            print("Menu selection must be a number. ")
    field_label = list(DESTINATION_SEARCH_FIELDS.keys())[choice-1]
    value = input(f"Enter value for {field_label}: ").strip()
    partial = False 
    if field_label not in {"Destination ID"}:
        use_partial = input("Partial match? (Y/N): ").lower() # determines if a partial match is allowed
        partial = (use_partial == "y")
        rows = search_destination(field_label, value, partial=partial) # runs the search_destination()
        print_results(rows) # prints the results
        destination_menu()

# Adds a new destination to the database
def add_destination():
    name = input("Enter airport name: ") # takes input
    city = input("Enter airport city: ")
    country = input("Enter airport country: ")
    execute_sql("timezone.sql") # prints the timezones
    timezone = input("Enter airport timezone from the above list: ")
    
    print("\n Please review your input below.")
    txt = f"Name: {name}\nCity: {city}\nCountry: {country}\nTimezone: {timezone}"
    params = (name, city, country, timezone)
    print(txt) # prints the input for review
    while True:
        print("Press 1 to add the new destination to the database")
        print("Press 2 to cancel the database entry.")
        try: # handles data validation
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

# Deletes a destination from the database            
def delete_destination():
    execute_sql("destinations.sql") # prints the destinations for selection
    delete_id = input("Enter the Destination ID of the destination you wish to delete: ")
    try: # validates entry
        delete_id = int(delete_id)
    except ValueError:
            print("Destination ID must be a number.")
    execute_param_sql("destination_id.sql", (delete_id,)) # prints the entry to be deleted
    print("\n Is this the destination you want to delete?")
    while True:
        print("If yes select 1")
        print("If no press 2")
        try: # menu selection 
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
    
# prints the main menu
def main_menu():
    print("\n Welcome to the Flight Management Database")
    print(" -----------------------------------------")
    print(" Please select one of the following options")
    print("\n1. Flights Menu")
    print("2. Pilot Menu")
    print("3. Destination Menu")
    print("0. Exit")
    
    while True:
        try:
            menu_option = int(input("\nEnter menu option: "))
            break
        except ValueError:
            print("Invalid Input")
    while True:
        if menu_option == 1:
            flight_menu()
            break
        elif menu_option == 2:
            pilot_menu()
            break
        elif menu_option == 3:
            destination_menu()
            break  
        elif menu_option == 0:
            conn.close()
            print("\nDatabase Connection Closed")
            print("Logging Off...")
            print("Goodbye\n")
            exit(0)
        else:
            print("\n Invalid Input")
            main_menu()

# Used to populate an empty database by running each SQL command in the database.sql file
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
    conn = sqlite3.connect('CM500292--Databases-Coursework\database.db') # connects to the database
    print("\n Connecting to Database...")
    conn.row_factory = sqlite3.Row # allows accessing of columns by name of index
    c = conn.cursor() # initialises the cursor
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