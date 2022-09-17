########################################################################
# Project Title:    UAH Course Scheduler
# Class:            CS 499-01 - Sr. Project Design
# Term:             FA 22
# 
# Team Number:      5
# Team Members:     Devin Patel
#                   Allison Sanders
#                   Faith Grimmeisen
#                   Harrison Matthews
########################################################################
# Filename:     DataOperation.py
# Purpose:      To establish an interface through which databasing
#               operations can be called by a web server host.
#
# Editors of this file:     Devin Patel
# 
# NOTES:
#
########################################################################


import csv

import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class DataOperation:
    """
    This class holds all the methods that are necessary for database operations
    """
    
    def __init__(self):
        """
        Authenticates credentials so access to the database is established.
        """
        
        self.authenticate_credentials()



    def authenticate_credentials(self):
        """
        Authenticate Firebase Database credentials so that edits can be
        made to the database.
        """
        
        # Loads virtual .env variables
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
        


    def importCSV(filename):
        """
        Reads CSV file with schedule data and checks for formatting.
        Afterwards, it creates database entries for each class section.

        Args:
            filename (string): Path directed to csv file to import
        """        
        
        f = filename
        
        # Each row of the csv input will be reorganized as a nested dictionary with
        # 'Course Section' being the key to another dictionary containing the rest
        # of the csv row fields.
        # Each of these rows will be appended to the following list
        list_of_section_dicts = []
        
        with open(f, mode='r', encoding='utf-8-sig') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
            
            
            # Reads in each row of csv file, 'row' is a dictionary keyed by the column headers
            for row in csv_dict_reader:            
                # Creates nested dictionary with course section as the key
                temp = row
                course = temp.pop('Course Section')
                course_dict = {}
                course_dict[course] = temp
                
                # Appends Course Section dictionary to cumulative list of rows
                list_of_section_dicts.append(course_dict)

        # Sets the full database
        ref = db.reference('/')
        ref.set(list_of_section_dicts)


#########################################
#
# Main
#
#########################################

csv_file = "path/to/file.csv"

DataOperation() # Runs constructor to authenticate credentials
DataOperation.importCSV(csv_file) # Test a csv file