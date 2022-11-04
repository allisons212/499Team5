########################################################################
# Project Title:    Course Scheduling System
# Class:            CS 499-01 - Sr. Project Design
# Term:             FA 22
# 
# Team Number:      5
# Team Members:     Devin Patel
#                   Allison Sanders
#                   Faith Grimmeisen
#                   Harrison Matthews
########################################################################
# Filename:     app.py
# Purpose:      To initialize and run the flask server that drives
#               all frontend and backend operations.
#
#
# Editors of this file:     Allison Sanders
#                           Faith Grimmeisen
#                           Devin Patel
#                           Harrison Matthews
# 
# NOTES:
#
########################################################################


from flask import Flask, render_template, redirect, url_for, request
from flask_navigation import Navigation #pip install flask_navigation
from numpy import empty # pip install numpy
from RoomTable import *
from DataOperationEnums import *
from DataOperationException import *
from DataOperation import DataOperation
from werkzeug.utils import secure_filename
import os


class User:
    user_account = ""
    
    def __init__(self):
        pass
    
    def setUser(self, newUser):
        self.user_account = newUser
    
    def getUser(self):
        return self.user_account


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/upload/"
nav = Navigation(app)
db = DataOperation()
user = User()



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
        if not db.checkUserPass(request.form['username'], request.form['password']):
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            user.setUser(db.getAccountDepartment(request.form['username']))
            return redirect(url_for('generate_schedule'))
    return render_template('login.html', error=error)


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/aboutUs') # make each of these for each html
def about_us():
    return render_template('aboutUs.html', department=user.getUser())


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/faq')
def faq():
    return render_template('faq.html', department=user.getUser())


@app.route('/generate_schedule')
def generate_schedule():
    return render_template('generateSchedule.html', department=user.getUser())


@app.route('/settings')
def settings():
    return render_template('settings.html')

# POST View for uploadCSV
@app.route('/uploadCSV', methods=['POST', 'GET'])
def upload_csv():
    fileUploadSuccess = None
    fileError = None
    error = 0
    if request.method == 'POST':
        
        if request.form['submit_button'] == 'Submit CSV':

            # Request each file
            CourseFile = request.files['courses']
            RoomsFile = request.files['rooms']

            # Create a list and append the files to it
            Files = []
            Files.append(CourseFile)
            Files.append(RoomsFile)

            # iterate over the list and add them to the upload folder
            for file in Files:
                filename = secure_filename(file.filename)
                file.save(app.config['UPLOAD_FOLDER'] + filename)
            
            # Put each course file in CourseFile
            CourseFile = Files[0]

            # Put each room file in RoomsFile
            RoomsFile = Files[1]

            # CourseFile RoomsFile
            CourseFile = CourseFile.filename
            RoomsFile = RoomsFile.filename

            # Call the database to call the CourseFile
            db.importCSV(f"static/upload/{CourseFile}", f"static/upload/{RoomsFile}", user.getUser())
            fileUploadSuccess = "File Uploaded Successfully!"

            # Render the template with updated text on screen
            return render_template('uploadCSV.html', department=user.getUser(), fileUploadSuccess=fileUploadSuccess)
            
    elif request.method == 'GET':
        return render_template('uploadCSV.html', department=user.getUser())
        
    return render_template('uploadCSV.html', department=user.getUser(), error=error)

@app.post('/assignments/generate')
def generate_assignments():
    department = request.get_json()['department']

    conflicts = db.generate_assignments(user.getUser())

    return conflicts

# @app.get('/assignments/<class_id>')
# def get_url_params(class_id):
#     return {"class_id": class_id}


# @app.get('/assignments/anything')
# def get_query_params():
#     class_id = request.args["class_id"]
#     return {"class_id": class_id}

@app.get('/csv/export')
def export_csv():
    department = request.args["department"]
    exportFile = db.exportCSV(user.getUser())

    return exportFile

@app.get('/empty/rooms')
def get_empty_rooms():
    department = request.args["department"]
    emptyRooms = db.getEmptyRooms(user.getUser())
    return emptyRooms
   


if __name__ == '__main__':
    app.run(debug = True)
