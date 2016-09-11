# PennApps XIV

# imports
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from app import app
import sqlite3 as lite
import sys
import cgi
import socket
import dbops #db operations
import random
from funfacts import *


# encoding=utf8  
reload(sys)  
sys.setdefaultencoding('utf8')

# create database
con = lite.connect('test.db')

# toggles - ordering, logging in/out
loggedIn = False
table = 'Nothing'

@app.route('/')
@app.route('/index')
def index():
    global table
    quote = random.choice(facts)
    return render_template('index.html', quote = quote, userState = loggedIn, table = table)

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
    
    return render_template('database.html', userState = loggedIn, table = table, title = "no", user = "no", rcolumns = runames, rposts=ruser_list, fposts=fuser_list, fcolumns = funames, oposts = ouser_list, ocolumns = ounames, cposts = cuser_list, ccolumns = cunames)

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
    global loggedIn, table

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
    return render_template('about.html', title='About', userState = loggedIn, table = table)

@app.route('/order')
def order():
    global loggedIn

    if loggedIn:
        dbops.addOrder()

        return render_template('index.html', ordered = True, userState = loggedIn, table = table)
    else:
        return redirect('/index')

@app.route('/receive')
def receive():
    global loggedIn

    if loggedIn:
        return render_template('index.html', userState = loggedIn, table = table, connectLyft = True)

@app.route('/orderpage')
def orderpage():
    return render_template('givefood.html')

@app.route('/receivepage')
def receivepage():
    return render_template('receivefood.html')

# Lyft 

token = 'gAAAAABX1H1ioNNoziiNADp4Sy4_UHMt-AhLoaAKUg4K29JWHkYZC_2Z5YuDApZErtqLqyBH6csNNaXIdff6c6KN_gXrSKqzjqC7kgcDu3XGgWEFnqmppcp_5RCTNmeDaEK5xD0XgLcopD-7xDKS5Tg_ejIwajSyu6BMQs9DloyvpJKgFR3IQb8='

def unwrap(data):
    s = []
    i = 0
    j = 0
    while i < len(data):
        if data[i]=="[":
            j = i+2
            break
        i += 1
    s1 = ""
    while j < len(data):
        if data[j]=="}":
            s.append(s1)
            j += 4
            break
        else: s1 = s1+data[j]
        j += 1
    s2 = ""
    while j < len(data):
        if data[j] == "}":
            s.append(s2)
            j += 4
            break
        else:
            s2 = s2 + data[j]
        j += 1
    s3 = ""
    while j < len(data):
        if data[j] == "}":
            s.append(s3)
            j += 4
            break
        else:
            s3 = s3 + data[j]
        j += 1
    return s

def get_nearby_driver_cost(start_lat,start_lng,end_lat,end_lng):
    global token

    url = 'https://api.lyft.com/v1/cost'
    header = {'Authorization': 'Bearer %s' % token}
    params = {'start_lat':start_lat,'start_lng':start_lng,'end_lat':end_lat,'end_lng':end_lng}
    response = request.get(url,headers=header,params=params) #requests
    response = response.text
    import unicodedata
    response = unicodedata.normalize('NFKD', response).encode('ascii','ignore')
    response = response[1:-1]
    return unwrap(response)

@app.route('/connectlyftpage')
def connectlyftpage():
    return render_template('connectToLyft.html')

@app.route('/connectToLyft', methods=['POST'])
def connectToLyft():
    start_lat, start_lng, end_lat, end_lng = request.form['curaddresslat'], request.form['curaddresslon'], request.form['destinationlat'], request.form['destinationlon']

    text = get_nearby_driver_cost(start_lat,start_lng,end_lat,end_lng)

    return render_template('moreLyft.html', text = text)




