# database operations
import sqlite3 as lite
import sys
# create database
db = 'test.db'

def createInitialTables(): # run once to create Tables with test
    # Restaurants, FoodPantries
    global db
    con = lite.connect(db)
    with con:
        cur = con.cursor()    
        
    # Create Restaurants
        cur.execute("DROP TABLE IF EXISTS Restaurants")
        cur.execute("CREATE TABLE Restaurants(Id INTEGER PRIMARY KEY ASC, Organization TEXT, PersonName TEXT, Email TEXT, Pword TEXT, FoodGivenTimes INT DEFAULT 0)")
        cur.execute("INSERT INTO Restaurants (Organization, PersonName, Email, Pword, FoodGivenTimes) VALUES ('Bill Eats', 'Billy Bob', 'bill@bill.com', '12354', 0)")

    # Create FoodPantries
        cur.execute("DROP TABLE IF EXISTS FoodPantries")
        cur.execute("CREATE TABLE FoodPantries(Id INTEGER PRIMARY KEY ASC, Organization TEXT, PersonName TEXT, Email TEXT, Pword TEXT)")
        cur.execute("INSERT INTO FoodPantries (Organization, PersonName, Email, Pword) VALUES ('The Fredrrrick', 'Hungry Bill', 'hungrybill@bill.com', '12354')")

    # Printing Check
       # treats row as a dictionary (column is key)
        con.row_factory = lite.Row
        cur = con.cursor() 
        cur.execute("SELECT * FROM Restaurants")
        rows = cur.fetchall()
        for row in rows:
            print ("Restaurants: %d %s %s %s %s %d" % (row["Id"], row["Organization"], row["PersonName"], row["Email"], row["Pword"], row["FoodGivenTimes"])) 

def createUser(Table, Organization, PersonName, Email, Pword):
    global db
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        user = [(Organization, PersonName, Email, Pword)]
        stmt = "INSERT INTO " + Table + " (Organization, PersonName, Email, Pword) VALUES (?, ?, ?, ?)"
        cur.executemany(stmt, user)

# createInitialTables()