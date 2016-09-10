# database operations
import sqlite3 as lite
import sys

# create database
con = lite.connect('test.db')

def createInitialTables(con):
    # Restaurants, FoodPantries
     with con:
        
        cur = con.cursor()    
        
    # Create Restaurants
        cur.execute("DROP TABLE IF EXISTS Restaurants")
        cur.execute("CREATE TABLE Restaurants(Id INTEGER PRIMARY KEY ASC, Organization TEXT, PersonName TEXT, Email TEXT, Pword TEXT, FoodGivenTimes INT)")

        #cur.executemany("INSERT INTO Users (FirstName, LastName, Email, Pword) VALUES(?, ?, ?, ?)", submits)
        cur.execute("INSERT INTO Restaurants (Organization, PersonName, Email, Pword, FoodGivenTimes) VALUES ('Bill Eats', 'Billy Bob', 'bill@bill.com', '12354', 0)")

    # Create FoodPantries
        cur.execute("DROP TABLE IF EXISTS FoodPantries")
        cur.execute("CREATE TABLE FoodPantries(Id INTEGER PRIMARY KEY ASC, Organization TEXT, PersonName TEXT, Email TEXT, Pword TEXT)")

        #cur.executemany("INSERT INTO Users (FirstName, LastName, Email, Pword) VALUES(?, ?, ?, ?)", submits)
        cur.execute("INSERT INTO FoodPantries (Organization, PersonName, Email, Pword) VALUES ('The Hungry', 'Hungry Bill', 'hungrybill@bill.com', '12354')")


        #treats row as a dictionary (column is key)
        con.row_factory = lite.Row
           
        cur = con.cursor() 
        cur.execute("SELECT * FROM Restaurants")

        rows = cur.fetchall()

        for row in rows:
            print ("Restaurants: %d %s %s %s %s %d" % (row["Id"], row["Organization"], row["PersonName"], row["Email"], row["Pword"], row["FoodGivenTimes"]))

con = lite.connect('test.db')
createInitialTables(con)