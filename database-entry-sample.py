import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Path pointing to a downloaded private key from Project Settings > Service Accounts
credentials_path = os.path.join("authentication", "firebase-sdk.json")

# Sets up credentials and initializes realtime database URL
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://coursescheduler499-default-rtdb.firebaseio.com/'
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