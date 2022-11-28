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
from RoomTable import *
from DataOperationEnums import *
from DataOperationException import *
from DataOperation import DataOperation
from werkzeug.utils import secure_filename
import os
import re



# The user account is responsible for setting and getting the user_account so we know which department is logged into the system
class User:
    user_account = ""
    
    def __init__(self):
        pass
    
    def setUser(self, newUser):
        self.user_account = newUser
    
    def getUser(self):
        return self.user_account

# Default Flask operations
app = Flask(__name__)
nav = Navigation(app)
db = DataOperation()
user = User()

# Define port number
try:
    PORT = int(os.environ.get("PORT", 8080))
except:
    PORT = 8080

#  Defines where our upload folder is
app.config["UPLOAD_FOLDER"] = "static/upload/"

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
        # If the username or password field is blank, then collect error message
        if request.form['username'] == "" or request.form['password'] == "":
            error = "No Username or password typed in. Please try again."
        # If the fields are just wrong, then collect the error message
        elif not db.checkUserPass(request.form['username'], request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        # IF the credentials are correct then redirect to homepage and set the user acronym to the users department.
        else:
            user.setUser(db.getAccountDepartment(request.form['username']))
            return redirect(url_for('generate_schedule'))
    # IF we get to this point then we need to render the error to the user
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

    # If fileUploadSuccess is successful then it is filled with a string, but by default it is None
    fileUploadSuccess = None

    # If manualUploadSuccess is successful then it is filled with a string, but by default it is None
    manualUploadSuccess =  None

    # If fileUploadFailure is not None, then it is filled with a string denoting failure
    fileUploadFailure = None

    # manualError will only be filled with a string if there is improper formatting
    # from the fields Faculty, and Class in the ManualUpload. manualErrorCount is just the number of errors
    manualError = ""
    manualErrorCount = 0

    # TemporaryList is a 2D list that is used to format the Exception errors
    temporaryList = [[]]

    # FormatErrorList is the error List that is originally used to format Exception errors if the user uploads a CSV with the wrong format.
    formatErrorList = []

    # FormatErrorList is filled with a header of how many errors were found. We want to pop this off and put
    # into headingErrorList for easier formatting in the HTML
    headingErrorList = ""

    # Manual box entrys that are dynamic
    departmentManual = user.getUser()

    # To fill the Manual rooms box we need to getEmptyRooms from database
    rooms = db.getEmptyRoomsOnly(user.getUser())

    # IF the page detects a post
    if request.method == 'POST':
        
        # If the post originated from the Submit CSV button
        if request.form['submit_button'] == 'Submit CSV':

            # Put the File object from the 'courses' and 'rooms' files into CourseFile and RoomsFile
            CourseFile = request.files['courses']
            RoomsFile = request.files['rooms']

            # Get the secure_filename and store in CourseFileName, then save the filename to the UPLOAD_FOLDER    
            CourseFileName = secure_filename(CourseFile.filename)
            CourseFile.save(app.config['UPLOAD_FOLDER'] + CourseFileName)

            # Get the secure_filename and store in RoomsFileName, then save the filename to the UPLOAD_FOLDER
            RoomsFileName = secure_filename(RoomsFile.filename)
            RoomsFile.save(app.config['UPLOAD_FOLDER'] + RoomsFileName)

            # Call the database to call the CourseFile
            try:
                db.importCSV(f"static/upload/{CourseFile.filename}", f"static/upload/{RoomsFile.filename}", user.getUser())
                fileUploadSuccess = "File Uploaded Successfully! Generate schedule on Create Schedule page."

                # Must clear temporaryList if it was a success. I think because of how it was initalized above it thinks theres at least 
                # 1 element in the List and outputs it to the frontend
                temporaryList = []
            # If the Database causes an exception for ImportFormatError
            except ImportFormatError as ife:

                # Get the exceptionMessage as 1 long string
                exceptionMessage = str(ife)

                # Split the exception by \n character
                formatErrorList = exceptionMessage.split('\n')

                # We have an extra empty elment at end of list so we need to remove it
                formatErrorList.pop()

                # pop the first element and store it in headingErrorList to send to HTML
                headingErrorList = formatErrorList.pop(0)

                # Fill the temporaryList as a 2D List
                temporaryList = [formatErrorList[i:i+3] for i in range(0, len(formatErrorList), 3)]

                # Let the user know that the upload has failed
                fileUploadFailure = "File Upload Failed! Fix errors and try uploading again."

            # Render the template with updated text on screen
            return render_template('uploadCSV.html', department=user.getUser(), fileUploadSuccess=fileUploadSuccess, departmentManual=departmentManual,
            formatErrorList=temporaryList, rooms=rooms, fileUploadFailure=fileUploadFailure,headingErrorList=headingErrorList)
        # END SUBMIT CSV IF

        # If the user selects the Submit Manual Input button 
        elif request.form['submit_button'] == "Submit Manual Input":

            # Get each piece of information from the HTML
            userClass = request.form.get("class")
            faculty = request.form.get("faculty")
            room = request.form.get("room")
            day = request.form.get("day")
            time = request.form.get("time")

            # Check userClass for proper formatting
            match = re.findall(r"^[0-9]{3}[-][0-9]{2}$", str(userClass))
            if not match:
                manualErrorCount += 1
                manualError += "CLASS ERROR: Incorrect CLASS formatting. Format: '[3-digit integer]-[2-digit integer]' EX. 102-01 where 01 indicates the section number.\n"
            
            # Check faculty for proper formatting
            match = re.findall(r"^[A-Za-z.' ]{1,40}$", str(faculty))
            if not match:
                manualErrorCount += 1
                manualError += "FACULTY ERROR: Incorrect FACULTY formatting. Format: 40 characters or less using only letters, periods, apostrophes, and spaces."
            
            # This can be Re-Written to be better ------REMINDER
            if manualErrorCount > 0:
                if(manualErrorCount == 1 and manualError.find('\n')):
                    manualError = manualError.replace('\n','')

                manualError = manualError.split('\n')

                # IF there were errors then return the render_template to reflect that to the user
                return render_template('uploadCSV.html', department=user.getUser(), departmentManual=departmentManual, rooms=rooms, manualError=manualError)
            
            # Enter the data into the database.
            # Returns a boolean to determine if the class was already in the database or not.
            inDatabase = db.manualEntryAssignment(user.getUser(), userClass, faculty, room, day, time)
            
            # IF the item was not in the database
            if(not inDatabase):
                manualUploadSuccess = "Entry is now in the database."
            # ELSE the item was in the database
            else:
                manualUploadSuccess = "Entry in database has been OVERWRITTEN!"
            
            # Return the template with the updated information if it was successful 
            return render_template('uploadCSV.html', department=user.getUser(), departmentManual=departmentManual, rooms=rooms, manualUploadSuccess=manualUploadSuccess)
    # END POST IF

    # IF there is a GET then just return the template for user
    elif request.method == 'GET':
        return render_template('uploadCSV.html', department=user.getUser(), departmentManual=departmentManual, rooms=rooms)
    
    return render_template('uploadCSV.html', department=user.getUser(), manualError=manualError)


@app.post('/assignments/generate')
def generate_assignments():
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
    exportFile = db.exportCSV(user.getUser())

    return exportFile

@app.get('/empty/rooms')
def get_empty_rooms():
    emptyRooms = db.getEmptyRooms(user.getUser())
    return emptyRooms

@app.get('/empty/faculty')
def get_empty_faculty():
    emptyFaculty = db.getEmptyFaculty(user.getUser())
    return emptyFaculty


@app.get('/get/DB')
def get_DB():
    department_path = "Department Courses/" + user.getUser()
    return db.getDB(department_path)

@app.put('/update/solution/assignments')
def update_solution_assignments():
    # department, course_number, day, time, room_number
    department = user.getUser()
    body = request.get_json()
    course_number = body["className"]
    dayAndTime = body["dayAndTime"]
    day, time = dayAndTime.split(" - ")
    room_number = body["room"]
    db.updateSolutionAssignments(department, course_number, day, time, room_number)
    return { "success": True }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
