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
conn = sqlite3.connect('test.db')


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/signup', methods = ['POST'])
def signup():
	# name for stuff = request.form['name from form']
	# sending name/s to db

	return redirect('/') 

@app.route('/signuppageres')
def signup1():
    return render_template('CREATEPAGE.html', title='Signup/Login')

@app.route('/signuppatefoo')
def signup2():
    return render_template('CREATEPAGE.html', title='Signup/Login')

@app.route('/login', methods = ['POST'])
def login():
	# check if user name and password are true (in db)
	return redirect('/')

@app.route('/about')
def about():
    return render_template('CREATEPAGE.html', title='About')