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

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/upload/"
nav = Navigation(app)
db = DataOperation()

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
    # db.generate_assignments("CS")
    return render_template('generateSchedule.html')


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
            
            # Get the list of files from the button
            files = request.files.getlist('files[]')
            numFiles = len(request.files.getlist('files[]'))
            if(numFiles != 2):
                fileError = "Must give exactly 2 files. "
                return render_template('uploadCSV.html', fileError=fileError)
            else:
                # Iterate through file list and store them in upload_folder
                for file in files:
                    filename = secure_filename(file.filename)
                    file.save(app.config['UPLOAD_FOLDER'] + filename)

                # Pop files from list
                file1 = files.pop()
                file2 = files.pop()

                # Set equal to filename
                file1 = file1.filename
                file2 = file2.filename

                # Call backend to import the CSV's into firebase
                db.importCSV(f"static/upload/{file1}", f"static/upload/{file2}", "CS")
                fileUploadSuccess = "File Uploaded Successfully!"

                # Render the template with updated text on screen
                return render_template('uploadCSV.html', fileUploadSuccess=fileUploadSuccess)

            """
            # Begin file reading
            uploadedFile = request.files['DepartmentFile']
            
            # Need to save the file in a directory so that it can be found by DataOperation
            uploadedFile.save(secure_filename(uploadedFile.filename))
            
            # IF there is something in the file then  call db with the file and Acronym
            if uploadedFile.filename!= '':
                db._importCourseCSV(uploadedFile.filename, "CS")
                # Signal to user that it was successful
                fileUploadSuccess = "File Uploaded Successfully!"
                # Render them template with the updated text on screen
                return render_template('uploadCSV.html', fileUploadSuccess=fileUploadSuccess)
        elif request.form['submit_button'] == 'Submit Manual Input':
            print("MANUAL INPUT BUTTON TEST")
            test = request.form['dept']
            print(test)
            """
            
    elif request.method == 'GET':
        return render_template('uploadCSV.html')
        
    return render_template('uploadCSV.html', error=error)

@app.post('/assignments/generate')
def generate_assignments():
    department = request.get_json()['department']

    conflicts = db.generate_assignments(department)

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
    exportFile = db.exportCSV(department)
    print(exportFile)

    return exportFile

@app.get('/empty/rooms')
def get_empty_rooms():
    department = request.args["department"]
    emptyRooms = db.getEmptyRooms(department)
    print(emptyRooms)
    return emptyRooms
    


if __name__ == '__main__':
    app.run(debug = True)
