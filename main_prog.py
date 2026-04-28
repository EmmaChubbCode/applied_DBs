# STEP 1: CONNECT TO SERVERS #
# code for this section was adapted from the following:
# https://pypi.org/project/mysql-connector-python/ 

# first import config 
# Gerard can import his details into this file to match his local setup
import config

# first set up connection to MySQL
import mysql.connector

# connect to servers using details from config.py
mysql_conn = mysql.connector.connect(
    host="config.mysql_host",
    port=config.mysql_port,
    user="config.mysql_user",
    password="config.mysql_password",
    database="config.mysql_database"
)
# create cursor for MySQL connection
mysql_cursor = mysql_conn.cursor()

# now set up connection to Neo4j
from neo4j import GraphDatabase 

# import details from config.py and create driver for Neo4j connection
# see https://neo4j.com/docs/api/python-driver/current/ 
neo4j_driver = GraphDatabase.driver(
    config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password)
)

#STEP 2 CREATE USER MENU
# adapt from https://learn.modernagecoders.com/blog/how-to-build-menu-driven-program-in-python 
import mysql.connector
from neo4j import GraphDatabase

# ── Database connections ──────────────────────────────────────────
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3308,
    user="root",
    password="yourpassword",  # replace with your root password
    database="appdbproj"
)
mysql_cursor = mysql_conn.cursor()

neo4j_driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687",
    auth=("neo4j", "yourpassword")  # replace with your Neo4j password
)

# STEP 2: CREATE USER MENU
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