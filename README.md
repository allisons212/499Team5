# UAH Course Scheduling System

Course: CS 499 - 01  
Term: FA 22  
Team: 5  

Team Members:
- Devin Patel
- Allison Sanders
- Faith Grimmeisen
- Harrison Matthews

Purpose: To create a scheduling system that will assign courses and faculty to a classroom and a time period without conflicts.  

## Dependencies

Python:  
- Flask - Used as a web framework
- flask_navigation - Used for framework navigation by Flask
- werkzeug - WSGI web application library used by Flask
- firebase-admin - Used for access to Google Firebase Realtime Database
- configparser - Used for loading API keys for Firebase
- gunicorn - Used to run the Flask app

Javascript:  
- ky - Used to integrate Flask and Javascript

## User Accounts

By default, the following accounts are in the database. The default password for each account is its own username.  
`CSChair`  
`ECEChair`

## Run from source

1. Create an account with Google Firebase and start a project.
2. Go to project settings and generate an API keys json for python. **Keep these keys private.**
3. Create a folder called `credentials` and place the keys json in it.
4. In the same folder, create a file `firebase-auth.ini` and format it according to the following:  
**Note the lack of quotation marks, replace only the angle bracketed fields with your relevant information.**
```
[firebase]
credentials_path = credentials/<API keys json>.json
database_url = <Realtime Database URL>
```
5. Run the following command to start the server:  
`gunicorn --bind :8080 --workers 1 --threads 8 app:app`  
6. By default, the app will run on `host 0.0.0.0` and `port 8080`, but this can be changed in `app.py` and in the `gunicorn` command.
7. Connect to the host and port specified in `app.py` on a web browser.

## Run from docker

1. Ensure docker is installed and an account is created with [docker hub](https://hub.docker.com/).
2. The container image repository is [devinpate1/cs499-course-scheduler](https://hub.docker.com/r/devinpate1/cs499-course-scheduler).
3. Run `docker pull devinpate1/cs499-course-scheduler`
4. Start the container image to start the server.

## Access from Google Cloud Run

Pending the status of our Google Cloud account, the website may or may not be accessible from [scheduler-bjdaal7iia-uc.a.run.app/](https://scheduler-bjdaal7iia-uc.a.run.app/).
