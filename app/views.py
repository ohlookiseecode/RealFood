# PennApps XIV

# imports
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from app import app
import sqlite3 as lite
import sys
import cgi
#import resetDB
import socket
import dbops #db operations
import random
from funfacts import facts

# create database
con = lite.connect('test.db')

# toggles - ordering, logging in/out
loggedIn = False

@app.route('/')
@app.route('/index')
def index():
    quote = random.choice(facts)
    return render_template('index.html', quote = quote)

@app.route('/database')
def database():

    con = lite.connect('test.db')
    with con:
        con.row_factory = lite.Row
           
        cur = con.cursor() 

        ruser_list = []
        cur.execute("SELECT * FROM Restaurants")
        runames = [description[0] for description in cur.description]
        rows = cur.fetchall()
        for row in rows:
            entire_row = ()
            for name in runames:
                entire_row += (row[name], )
            ruser_list.append(entire_row)
            #user_list.append((row["Id"], row["FirstName"], row["LastName"], row["Logins"], row["Email"], row["Pword"]))

        fuser_list = []
        cur.execute("SELECT * FROM FoodPantries")
        funames = [description[0] for description in cur.description]
        rows = cur.fetchall()
        for row in rows:
            entire_row = ()
            for name in funames:
                entire_row += (row[name], )
            fuser_list.append(entire_row)

        ouser_list = []
        cur.execute("SELECT * FROM Orders")
        ounames = [description[0] for description in cur.description]
        rows = cur.fetchall()
        for row in rows:
            entire_row = ()
            for name in ounames:
                entire_row += (row[name], )
            ouser_list.append(entire_row)

        cuser_list = []
        cur.execute("SELECT * FROM CurrentUser")
        cunames = [description[0] for description in cur.description]
        rows = cur.fetchall()
        for row in rows:
            entire_row = ()
            for name in cunames:
                entire_row += (row[name], )
            cuser_list.append(entire_row)
    
    return render_template('database.html', title = "no", user = "no", rcolumns = runames, rposts=ruser_list, fposts=fuser_list, fcolumns = funames, oposts = ouser_list, ocolumns = ounames, cposts = cuser_list, ccolumns = cunames)

@app.route('/signup', methods = ['POST'])
def signup():
    grouptype, Organization, PersonName, Email, Pword = request.form['grouptype'], request.form['group_name'], request.form['person_name'], request.form['email'], request.form['pword']
    if grouptype == 'res':
        dbops.createUser("Restaurants", Organization, PersonName, Email, Pword)

    elif grouptype == 'foo':
        #add to foo table
        dbops.createUser("FoodPantries", Organization, PersonName, Email, Pword)

    return render_template('index.html', user=Organization)

	#first_name, last_name = request.form['first_name'], request.form['last_name']
	# name for stuff = request.form['name from form']
	# sending name/s to db

@app.route('/signuppage')
def signuppage():
	return render_template('signup.html')

@app.route('/login', methods = ['POST'])
def login():
    global loggedIn

    grouptype, email, pword = request.form['grouptype'], request.form['email'], request.form['pword']

    # specify table
    if grouptype == 'res':
        table = 'Restaurants'
    elif grouptype == 'foo':
        table = 'FoodPantries'

    if dbops.verifyUser(table, email, pword):
        dbops.createCurUser(table, email, pword)
        loggedIn = True
        return redirect('/index')
    else:
        return render_template('login.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/logout')
def logout():
    global loggedIn

    dbops.clearCurUser()
    loggedIn = False
    return redirect('/')

@app.route('/aboutpage')
def aboutpage():
    return render_template('about.html', title='About')

@app.route('/order', methods = ['POST'])
def order():
    global loggedIn

    if loggedIn:
        dbops.addOrder()
        return render_template('index.html', ordered = True) #some notice saying thanks!
    else:
        return redirect('/index')

@app.route('/orderpage')
def orderpage():
    return render_template('givefood.html')