# PennApps XIV

# imports
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from app import app
import sqlite3 as lite
import sys
import cgi
#import resetDB
import socket

# create database
con = lite.connect('test.db')


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/signup', methods = ['POST'])
def signup():

    if request.form['value'] == 'res':
        return render_template('index.html')
    elif request.form['value'] == 'foo':
        return render_template('signup.html')
    #else:
    # invalid action

	#first_name, last_name = request.form['first_name'], request.form['last_name']
	# name for stuff = request.form['name from form']
	# sending name/s to db

	return redirect('/') 

@app.route('/signuppage')
def signuppage():
	return render_template('signup.html')

@app.route('/login', methods = ['POST'])
def login():
	# check if user name and password are true (in db)
	return redirect('/')

@app.route('/about')
def about():
    return render_template('CREATEPAGE.html', title='About')