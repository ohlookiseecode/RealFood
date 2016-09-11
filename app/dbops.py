# database operations
import sqlite3 as lite
import sys
# create database
db = 'test.db'

def createInitialTables(): # run once to create Tables with test
    # Restaurants, FoodPantries, Orders
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

    # Create Orders 
        cur.execute("DROP TABLE IF EXISTS Orders")
        cur.execute("CREATE TABLE Orders(OrderId INTEGER PRIMARY KEY ASC, Id INT, Organization TEXT, OrderDate DATE, OrderType INT DEFAULT 0, OrderSize INT DEFAULT 0)")

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

def createCurUser(Table, Email, Pword):
    # make usertable specific?
    global db
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS CurrentUser")
        cur.execute("CREATE TABLE CurrentUser (Id INT, Organization TEXT)")

        con.row_factory = lite.Row
        cur = con.cursor()
        stmt = "SELECT * FROM " + Table + " WHERE Email = '" + Email + "' AND Pword = '" + Pword + "'"
        cur.execute(stmt)

        Id, Organization = 0, 'None'
        rows = cur.fetchall()
        for row in rows:
            Id, Organization = row["Id"], row["Organization"]

        stmt = "INSERT INTO CurrentUser (Id, Organization) VALUES (?, ?)"
        user = [(Id, Organization)]
        cur.executemany(stmt, user)

def clearCurUser():
    global db
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("DELETE FROM CurrentUser")

def verifyUser(Table, Email, Pword):
    global db
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        stmt = "SELECT COUNT(*) FROM " + Table + "  WHERE Email = '" + Email + "' AND Pword = '" + Pword + "'"
        cur.execute(stmt)
        if cur.fetchone()[0] == 0:
            return False
        return True

def addOrder():
    global db
    con = lite.connect(db)
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        stmt = "INSERT INTO Orders (Id, Organization, OrderDate) SELECT Id, Organization, date('now') FROM CurrentUser"
        cur.execute(stmt)

#createInitialTables()
