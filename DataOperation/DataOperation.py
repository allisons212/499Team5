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
#                           Harrison Matthews
# 
# NOTES:
#
########################################################################


import csv
import re

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from configparser import ConfigParser

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

        # Loads config file
        conf_file = 'DataOperation/firebase-auth.ini'
        config = ConfigParser()
        config.read(conf_file)


        # Reads in path pointing to firebase key, url to Realtime Database
        credentials_path, database_url = config['firebase']['credentials_path'], config['firebase']['database_url']

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
                
                
                                    
                # No real need to check faculty name, but input must be sanitized
                faculty_assignment = row[ColumnHeaders.FAC_ASSIGN.value] # e.g., Dr. Goober
                match = re.findall(r"^[A-Za-z.' ]{1,40}", str(faculty_assignment))
                if not match or len(faculty_assignment) > 40: # Caps character length for names at 40
                    raise ImportFormatError(f"Row {row_num} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.FAC_ASSIGN.value}:\n" +
                                            "40 characters or less using only letters, periods, and apostrophes\n")

                
                
                # Check building code and room number
                room_pref = row[ColumnHeaders.ROOM_PREF.value] # e.g., OKT203, SST123, MOR
                match = True#match = re.findall(r"^(?[0-9]{3}[A-Z]{3}[0-9]{3}|[A-Z]{3})$", str(room_pref))
                if not match:
                    raise ImportFormatError(f"Row {row_num} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.ROOM_PREF.value}:\n" +
                                            "[3 Capital Letters][Optional: 3-digit integer]\n")
                
                
                time_pref = row[ColumnHeaders.TIME_PREF.value] # e.g., ABCDEFG; designating class time blocks throughout the day
                day_pref = row[ColumnHeaders.DAY_PREF.value] # e.g., MTWRF (R = Thursday)
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
        department_dict = {department_abbr : dict_of_section_dicts}
        ref = db.reference(f'/{DatabaseHeaders.COURSES.value}')
        ref.update(department_dict)
        
    # End of importCSV



    def getDB(self, database_path):
        """
        Returns information based on the database_path query.
        Query must be a path denoting a database section followed by
        appropriately cascading fields.
        
        Example database paths: Department Courses/CS
                                Department Courses/CS/CS100-01
                                Department Courses/ECE/ECE100-01
                                Accounts/CSDeptChair

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



    def updateDB(self, new_database_entry, database_path):
        """
        Creates or updates a database entry with the new entry.
        Database path must be a path denoting a database section followed by
        appropriately cascading fields.
        
        Example database paths: Department Courses/CS
                                Department Courses/CS/CS100-01
                                Department Courses/ECE/ECE100-01
                                Accounts/CSDeptChair

        Args:
            new_database_entry (Dictionary): Must contain all keys from csv header
            database_path (string): Realtime Database path that will be updated by new_database_entry
        
        Raises:
            ImproperDBPathError: When database_path does not address one of the Database Headers
        """
        
        # Checks the path to ensure it consists of one of the Database Headers
        check_passed = False
        for header in DatabaseHeaders:
            if header.value in database_path:
                check_passed = True
                break
        
        if not check_passed:
            raise ImproperDBPathError()

        # Updates the database at the path if checks are passed
        ref = db.reference(f'/{database_path}')
        ref.update(new_database_entry)
        
    # End of update DB
    
# End of DataOperation
