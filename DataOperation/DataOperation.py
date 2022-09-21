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
import re

import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from DataOperationException import * # Custom exceptions
from DataOperationEnums import * # Custom enums


class DataOperation:
    """
    This class holds all the methods that are necessary for database operations
    """
    
    def __init__(self):
        """
        Authenticates credentials so access to the database is established.
        """
        
        self.authenticate_credentials()
    # End of init        



    def authenticate_credentials(self):
        """
        Authenticate Firebase Database credentials so that edits can be
        made to the database.
        """
        
        # Loads virtual .env variables
        load_dotenv()

        # Path pointing to firebase key
        credentials_path = os.environ.get('credentials_path')

        # Reads in url to Realtime Database
        database_url = os.environ.get('database_url')

        # Sets up credentials and initializes realtime database URL
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL' : database_url
        })
    # End of authenticate_credentials


    def importCSV(self, filename, department_abbr):
        """
        Reads CSV file with schedule data and checks for formatting.
        Afterwards, it creates database entries for each class section.

        Args:
            filename (string): Path directed to csv file to import
            department_abbr (string): Abbreviation of the department (e.g., CS, ECE) classes to update
            
        Raises:
            FileNotFoundError: If filename does not get resolved to a csv file.
            ImportFormatError: If imported CSV file does not adhere to specified formatting guidelines.
        """
                
        # Each row of the csv input will be reorganized as a nested dictionary with
        # 'Course Section' being the key to another dictionary containing the rest
        # of the csv row fields.
        # Each of these rows will be appended to the following list
        dict_of_section_dicts = {}
                
        f = filename
        with open(f, mode='r', encoding='utf-8-sig') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
            
            row_num = 1 # Current row number
            
            # Reads in each row of csv file, 'row' is a dictionary keyed by the column headers
            for row in csv_dict_reader:
                row_num += 1
                # Checking for improper fields
                
                # Check course section
                course = row[ColumnHeaders.COURSE_SEC.value] # e.g., CS103-01
                match = re.findall(r"^[A-Z]{2,3}[0-9]{3}[-][0-9]{2}$", str(course)) # Regex to check input
                if not match:
                    raise ImportFormatError(f"Row {row_num} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.COURSE_SEC.value}:\n" +
                                            "[2-3 Capital Letters][3-digit integer]-[2-digit integer]\n")
                
                                    
                # No need to check faculty name
                faculty_assignment = row[ColumnHeaders.FAC_ASSIGN.value] # e.g., Dr. Goober
                
                
                # Check building number
                #NOTE: Should we make them recreate the csv or throw up errors in GUI for building numbers that aren't open?
                classroom_pref = row[ColumnHeaders.CLASS_PREF.value] # e.g., OKT203, SST123, MOR
                
                
                
                time_pref = row[ColumnHeaders.TIME_PREF.value] # e.g., A, B, C, D, E, F, G; designating class time blocks throughout the day
                day_pref = row[ColumnHeaders.DAY_PREF.value] # e.g., M, T, W, R, F (R = Thursday)
                seats_open = row[ColumnHeaders.SEATS_OPEN.value] # Positive integer denoting max number of students for that section
                
                
                # Creates nested dictionary with course section as the key
                course_dict = row
                course = course_dict.pop(ColumnHeaders.COURSE_SEC.value)
                
                # Appends three key-value pairs for assignments
                course_dict[ColumnHeaders.ROOM_ASS.value] = ""
                course_dict[ColumnHeaders.TIME_ASS.value] = ""
                course_dict[ColumnHeaders.DAY_ASS.value] = ""

                
                # Appends Course Section dictionary to cumulative dictionary of sections
                dict_of_section_dicts[course] = course_dict
                
            # End for loop
        # End of file reading
        
        # Updates the department's database tree
        department_dict = {f"{department_abbr}": dict_of_section_dicts}
        ref = db.reference('/')
        ref.update(department_dict)
        
    # End of importCSV





    def getDB(self, database_path):
        """
        Returns information based on the database_path query.
        Query must be a path denoting a department abbreviation
        (e.g., CS, ECE) followed by the course section
        (e.g., CS100-01, ECE100-01).
        
        Example database paths: CS
                                ECE
                                CS/CS100-01
                                ECE/ECE100-01

        Args:
            database_path (string): Realtime Database path

        Returns:
            Dictionary: All info in Realtime Database is stored as dictionary
        
        Raises:
            QueryNotFoundError: database_path doesn't return data
        """
        
        ref = db.reference(f'/{database_path}')
        retrieved = ref.get()
        
        if retrieved:
            return retrieved
        else:
            raise QueryNotFoundError()
    # End of getDB



    def updateDB(database_path):
        pass
    # End if update DB
    
# End of DataOperation
