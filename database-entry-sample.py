import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Loads virtual environment variables
load_dotenv()

# Path pointing to a downloaded private key from Project Settings > Service Accounts
credentials_path = os.environ.get('credentials_path')

# Reads in url to Realtime Database
database_url = os.environ.get('database_url')

# Sets up credentials and initializes realtime database URL
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {
    'databaseURL' : database_url
})


# Sets the full database
ref = db.reference('/')
ref.set({
    'Employee': {
            'emp1': {
                'name':'Devin',
                'lname':'Patel',
                'age':20
            },
            
            'emp2': {
                'name':'Harrison',
                'lname':'Matthews',
                'age':22
            },
    }
})

# Run program to update database, which can be viewed in Realtime Database on the Firebase project