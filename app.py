
from flask import Flask, render_template, redirect, url_for, request
from flask_navigation import Navigation #pip install flask_navigation
import firebase_admin #pip install firebase_admin
from Databasing.RoomTable import *
from Databasing.DataOperationEnums import *
from Databasing.DataOperationException import *

# connect to firebase
cred_obj = firebase_admin.credentials.Certificate('credentials/firebase-key.json') #input path to file here
default_app = firebase_admin.initialize_app(cred_obj)

app = Flask(__name__)
nav = Navigation(app)

# initializes navigations, add each url here
nav.Bar('top', [
    nav.Item('home', 'index'),
    nav.Item('aboutUs', 'about_us'),
    nav.Item('account', 'account'),
    nav.Item('FAQ', 'faq'),
    nav.Item('generateSchedule', 'generate_schedule'),
    nav.Item('Settings', 'settings'),
    nav.Item('uploadCSV', 'upload_csv'),
    nav.Item('Login', 'login'),
])


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('generate_schedule'))
    return render_template('login.html', error=error)


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/aboutUs') # make each of these for each html
def about_us():
    return render_template('aboutUs.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/generate_schedule')
def generate_schedule():
    return render_template('generateSchedule.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/uploadCSV', methods=['GET', 'POST'])
def upload_csv():
    error = 0
    if request.method == 'POST':
        if request.form['classNum'] > 999 or request.form['classNum'] < 100:
            error = 1
        else:
            error = 0
    return render_template('uploadCSV.html', error=error)


if __name__ == '__main__':
    app.run()
