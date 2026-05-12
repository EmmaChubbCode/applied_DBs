# Applied Databases - Conference Management System
### Higher Diploma in Science in Data Analytics
**Student:** Emma Chubb  
**Module:** Applied Databases  

---

## Overview
This is a command-line conference management application built in Python. It uses two databases:
- **MySQL** — stores attendees, companies, sessions, rooms and registrations
- **Neo4j** — stores connections (relationships) between attendees

---

## Requirements

### Software
- Python 3.12 or earlier (see note below)
- MySQL Server 8.0
- Neo4j Community Edition 5.x
- Git

> **Important:** This application uses `mysql-connector-python==8.0.33` which is not compatible with Python 3.14. If you are on Python 3.14, you must downgrade the connector to version 8.0.33 as specified in `requirements.txt`.

### Python Packages
All required packages are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
```

The packages used are:
- `mysql-connector-python==8.0.33` — connects Python to MySQL
- `neo4j` — connects Python to Neo4j

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/EmmaChubbCode/applied_DBs.git
cd applied_DBs
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database
1. Open MySQL Workbench and connect to your local instance
2. Go to **Server → Data Import**
3. Select **Import from Self-Contained File**
4. Browse to `appdbproj.sql.txt` in the project folder
5. Under **Default Schema**, click **New** and type `appdbproj`
6. Click **Start Import**

### 4. Set Up Neo4j Database
1. Start your Neo4j instance
2. Open the Neo4j Browser at `http://localhost:7474`
3. Copy the contents of `appdbprojNeo4j.json` and paste into the query bar
4. Run the queries — you should see green ticks for each statement

### 5. Configure Database Connections
Open `config.py` and update the details to match your local setup:

```python
# MySQL settings
mysql_host = "localhost"
mysql_port = 3306        # change to 3308 if needed
mysql_user = "root"
mysql_password = "root"  # change to your MySQL root password
mysql_database = "appdbproj"

# Neo4j settings
neo4j_uri = "neo4j://127.0.0.1:7687"
neo4j_user = ""          # blank on VM
neo4j_password = ""      # leave blank if authentication is disabled
```

> **Note on ports:** The default MySQL port is 3306. If you installed MySQL and it assigned a different port (e.g. 3308), update `mysql_port` accordingly. You can check your port in MySQL Workbench by running `SHOW VARIABLES LIKE 'port';`

> **Note on Neo4j password:** If your Neo4j instance has authentication disabled, leave `neo4j_password` as an empty string and ensure the driver in `main_prog.py` uses `auth=None`.

---

## Running on the ATU Virtual Machine (Azure Lab Services)

The `config.py` is pre-configured for the ATU VM with the following settings:
- MySQL port: **3306**
- MySQL password: **root**
- Neo4j password: **blank** (authentication disabled on VM)

Before running on the VM, make sure:
1. **MySQL** is running — check via Services or run `net start MySQL80` in an Admin command prompt
2. **Neo4j** is started — navigate to the Neo4j installation folder and run:
```bash
bin\neo4j-admin server console
```
Wait for the "Started." message before running the application.

3. Then run the application:
```bash
python main_prog.py
```

---

## How to Use

The application displays a menu with the following options:

```
Conference Management
--------------------

MENU
====
1 - View Speakers & Sessions
2 - View Attendees by Company
3 - Add New Attendee
4 - View Connected Attendees
5 - Add Attendee Connection
6 - View Rooms
x - Exit application
```

### Option 1 — View Speakers & Sessions
Enter a speaker name or part of a name to search. Displays the speaker name, session title and room for all matching speakers.

### Option 2 — View Attendees by Company
Enter a company ID to view all attendees from that company and the sessions they attended. Must be a number greater than 0.

### Option 3 — Add New Attendee
Add a new attendee to the MySQL database. You will be prompted for:
- Attendee ID
- Name
- Date of Birth (format: YYYY-MM-DD)
- Gender (Male or Female)
- Company ID

### Option 4 — View Connected Attendees
Enter an attendee ID to view all other attendees they are connected to in the Neo4j database.

### Option 5 — Add Attendee Connection
Enter two attendee IDs to create a CONNECTED_TO relationship between them in Neo4j. Both attendees must exist in the MySQL database.

### Option 6 — View Rooms
Displays all rooms with their ID, name and capacity. Room data is cached on first load — any rooms added to MySQL after this option is first chosen will not appear until the application is restarted.

### x — Exit
Exits the application.

---

## Project Structure
```
applied_DBs/
├── main_prog.py          # main application file
├── config.py             # database connection settings
├── requirements.txt      # Python dependencies
├── appdbproj.sql.txt     # MySQL database import file
├── appdbprojNeo4j.json   # Neo4j database import file
├── GitLink.pdf           # link to GitHub repository
└── README.md             # this file
```
