# STEP 1: CONNECT TO SERVERS #
# code for this section was adapted from the following:
# https://pypi.org/project/mysql-connector-python/ 

# first import config 
# Gerard can import his details into this file to match his local setup
import config

# first set up connection to SQL servers and neo4j using details from config.py
import mysql.connector
from neo4j import GraphDatabase

# connect to servers using details from config.py
mysql_conn = mysql.connector.connect(
    host=config.mysql_host,
    port=config.mysql_port,
    user=config.mysql_user,
    password=config.mysql_password,
    database=config.mysql_database
)
# create cursor for MySQL connection
mysql_cursor = mysql_conn.cursor()

# import details from config.py and create driver for Neo4j connection
# see https://neo4j.com/docs/api/python-driver/current/ 
neo4j_driver = GraphDatabase.driver(
    config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password)
)


# STEP 2: start defining functions before they're called by main menu

# STEP 2.1: CREATE VIEW SPEAKER FUNCTION

def view_speakers():
    # user will input a search of a name
    search = input("Enter speaker name : ")
    # squirly brackets are used to format the printed string with the user output. 
    print(f"Session Details For : {search}")
    print("-------------------")

    # now define the query to the sql db. the wildcard is a placeholder for whatever searh is entered by user. see https://www.w3schools.com/sql/sql_like.asp
    query = """
        Select s.speakerName, s.sessionTitle, r.roomName
        from session as s
        left join room as r on s.roomID = r.roomID
        where s.speakerName like %s
    """
    # replace the wildcard with user input and execute the query.adopted from https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html 
    mysql_cursor.execute(query, (f"%{search}%",))
    # fetch all the results from the query: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchall.html 
    results = mysql_cursor.fetchall()

# if there are no results, print a message to the user. otherwise, print the results.
# this is a pythonic waty to check if a list is empty.https://www.geeksforgeeks.org/python/python-if-with-not-operator/ 
    if not results:
        print("No speakers found of that name")
# otherwise print the columns returned by the query.     
    else:
        for speakerName, sessionTitle, roomName in results:
            print(f"{speakerName} | {sessionTitle} | {roomName}")

# STEP 2.1: Attendees by company function

def view_attendees_by_company():
    # start a loop because the user keeps getting asked if they enter one that doesnt exist.
    while True:
        # user will input a search of a company name
        company_id_input = input("Enter Company ID : ")
    # check the input is valid (>0 and only digits allowed)
        if not company_id_input.isdigit() or int(company_id_input) <= 0:
            print("Please enter a valid company ID (number greater than 0)")
            continue
        # input makes everything string but we need int.
        company_id = int(company_id_input)

        # i need to check the company id exists in te db
        mysql_cursor.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
       # company is whatever tuple is returned by the query
        company = mysql_cursor.fetchone()
        # if company is none, the company id isnt in there. print error statement from spec.
        if not company:
            print(f"Company with ID  {company_id}  doesn't exist")
           
            continue

        # otherwise we have a valid company id. just take the first index of the tuple otherwise it looks like "'CloudSprint', "
        company_name = company[0]

        # print company name and the word attendees.
        print(f"{company_name}  Attendees")

        # build thr query to get attendees and their sessions.
        # use inner join because we only want to return attendees that have registered. 
        query = """
        select a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, s.sessionDate, r.roomName
            from attendee a
            inner join registration reg ON a.attendeeID = reg.attendeeID
            inner join session s ON reg.sessionID = s.sessionID
            inner join room r ON s.roomID = r.roomID
            where a.attendeeCompanyID = %s
            order by a.attendeeName
        """
        mysql_cursor.execute(query, (company_id,))
        results = mysql_cursor.fetchall()
        
        # if no attendees found, print a message to the user
        if not results:
            print(f"No attendees found for  {company_name}")
            continue
        
        # otherwise print the results
        for attendeeName, attendeeDOB, sessionTitle, speakerName, sessionDate, roomName in results:
            print(f"{attendeeName} | {attendeeDOB} | {sessionTitle} | {speakerName} | {sessionDate} | {roomName}")
        break

# add new attendee function
def add_new_attendee():
    print("\nAdd New Attendee")
    print("----------------")

    # user input as per the spec
    name = input("Name : ")
    dob = input("DOB : ")
    gender = input("Gender : ")
    CompanyID = input("Company ID : ")

    # check for whether the attendee id is already there. 
    mysql_cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID = %s", (attendee_id,))
    # the opposite pof if not - check if it returns a value. 
    if mysql_cursor.fetchone():
    print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
    return

    # check for validity of gender
       # validate gender first before hitting the database
    if gender not in ("Male", "Female"):
        print("*** ERROR *** Gender must be Male/Female")
        return



# STEP 3: CREATE USER MENU
# ADAPT FROMED: https://learn.modernagecoders.com/blog/how-to-build-menu-driven-program-in-python 
def main():
    # use infinity loops to keep showing menu until user exits
    while True:
        print("\nConference Management")
        print("--------------------")
        print("\nMENU")
        print("====")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("x - Exit application")
        
        # input allows for user input. see https://www.w3schools.com/python/python_user_input.asp 
        choice = input("Choice: ")
        
        # these will be the functions that can be called by users.
        if choice == "1":
            view_speakers()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "3":
            add_new_attendee()
        elif choice == "4":
            view_connected_attendees()
        elif choice == "5":
            add_attendee_connection()
        elif choice == "6":
            view_rooms()
        elif choice == "x":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()