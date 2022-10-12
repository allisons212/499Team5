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
import os.path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from configparser import ConfigParser

from RoomTable import *

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
        self._authenticate_credentials()
    # End of init        



    def _authenticate_credentials(self):
        """
        Authenticate Firebase Database credentials so that edits can be
        made to the database.
        """

        # Loads config file
        conf_file = 'credentials/firebase-auth.ini'
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
    
    def importRoomsCSV(self, filename):
        """
        Reads CSV file AvailableRooms.csv with data and checks it for formatting.
        After it is error checked, it creates database entries for the given Department

        Args:
            filename (string): Path directed to csv file to import
            department_abbr (string): Abbreviation of the building (e.g., CS, ECE) classes to update
        """
        
        from collections import defaultdict
        
        # Each row of the csv input will be reorganized as a nested dictionary with
        # 'Available Classrooms' being the key to another dictionary containing the rest
        # of the csv row fields.
        # Each of these rows will be appended to the list 
        
        building_dictionary = {}
        row_number = 1
        
        # Counts all format errors before raising the exception
        format_error_count = 0 
        
        # Cumulative string to store all exception/error messages for each wrongly formatted entry
        format_error_msg = "" 
        
        # Set f equal to filename and open the csv file as read_obj
        f = filename
        with open(f, mode='r', encoding='utf-8-sig') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
        
            
        # Pre-process the dictionary and find all unique buildings and put into list
            for row in csv_dict_reader:
                # Track the row_number
                row_number = row_number + 1
                
                # ERROR CHECKING (BUILDING)
                building = row[ColumnHeaders.BUILD.value]
                match = re.findall("^[A-Z]{3}$", str(building))
                if not match:
                    format_error_count += 1
                    format_error_msg = (f"Row {row_number} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.BUILD.value}:\n" +
                                            "[3 Capital Letters]\n\n")
                
                # ERROR CHECKING (ROOM NUMBER)
                room_number = row[ColumnHeaders.ROOM_NUM.value]
                match = re.findall("^[0-9]{3}$", str(room_number))
                if not match:
                    format_error_count += 1
                    format_error_msg = (f"Row {row_number} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.ROOM_NUM.value}:\n" +
                                            "[3-digit integer]\n\n")
                
                # No need to do the rest of the row operations if a format error is found
                if format_error_count > 0:
                    continue
                
                
                # IF the building is in the dictionary then just append to exising dictionary
                # ELSE create a new key pair with that room number
                if row['Building'] in building_dictionary.keys():
                    building_dictionary[row['Building']].append(row['Room Number'])
                else:
                    building_dictionary[row['Building']] = [row['Room Number']]
            
           
        # If errors are found, raise the exception
        if format_error_count > 0:
            raise ImportFormatError(f"{format_error_count} errors have been found:\n"
                                    + format_error_msg)
        
        
        # Now that we have the dictionary that has each building as a key, and 
        # has the values as a list of the room numbers we need to put into database
        ref = db.reference(f'/{DatabaseHeaders.ROOMS.value}')
        ref.update(building_dictionary)
            
            
            
            
            
        
            

    def importCourseCSV(self, filename, department_abbr):
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
        dict_of_course_dicts = {}
        
        format_error_count = 0 # Counts all format errors before raising the exception
        format_error_msg = ""  # Cumulative string to store all exception/error messages for each wrongly formatted entry
        
        f = filename
        filename = os.path.split(filename)[1] # Extracts file name from path, if applicable
        
        with open(f, mode='r', encoding='utf-8-sig') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
            
            row_num = 1            # Current row number
            
            # Reads in each row of csv file, 'row' is a dictionary keyed by the column headers
            for row in csv_dict_reader:
                row_num += 1
                # Checking for improper fields
                
                # Check course section
                course = row[ColumnHeaders.COURSE_SEC.value] # e.g., CS103-01
                match = re.findall(r"^[A-Z]{2,3}[0-9]{3}[-][0-9]{2}$", str(course)) # Regex to check input
                if not match:
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.COURSE_SEC.value}:\n" +
                                            "[2-3 Capital Letters][3-digit integer]-[2-digit integer]\n\n")
                
                                                    
                # No real need to check faculty name, but input must be sanitized
                faculty_assignment = row[ColumnHeaders.FAC_ASSIGN.value] # e.g., Dr. Goober
                match = re.findall(r"^[A-Za-z.' ]{1,40}$", str(faculty_assignment))
                if not match or len(faculty_assignment) > 40: # Caps character length for names at 40
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.FAC_ASSIGN.value}:\n" +
                                            "40 characters or less using only letters, periods, apostrophes, and spaces.\n\n")

                
                # Check building code and room number
                room_pref = row[ColumnHeaders.ROOM_PREF.value] # e.g., OKT203, SST123, MOR
                match = re.findall(r"^[A-Z]{3}([0-9]{3}|)$", str(room_pref))
                if not match:
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.ROOM_PREF.value}:\n" +
                                            "[3 Capital Letters][Optional: 3-digit integer]\n\n")
                
                
                # Check time block preferences
                time_pref = row[ColumnHeaders.TIME_PREF.value] # e.g., ABCDEFG; designating class time blocks throughout the day
                match = re.findall(r"^[A]{0,1}[B]{0,1}[C]{0,1}[D]{0,1}[E]{0,1}[F]{0,1}[G]{0,1}$", str(time_pref))
                if not match:
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.TIME_PREF.value}:\n" +
                                            "Capital [A-G], used at most once each, in alphabetical order\n\n")
                
                
                # Check day preferences
                day_pref = row[ColumnHeaders.DAY_PREF.value] # e.g., MWTR (R = Thursday)
                match = re.findall(r"^MWTR$|^MW$|^TR$|^$", str(day_pref))
                if not match:
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.DAY_PREF.value}:\n" +
                                            "Choose one: MW, TR, MWTR\n\n")
                
                
                # Check seats open
                seats_open = row[ColumnHeaders.SEATS_OPEN.value] # Positive integer denoting max number of students for that section
                match = re.findall(r"^\d+$|^$", str(seats_open))
                if not match:
                    format_error_count += 1
                    format_error_msg += (f"Row {row_num} in {filename} is formatted incorrectly.\n" +
                                            f"Please follow the following format for {ColumnHeaders.SEATS_OPEN.value}:\n" +
                                            "An integer value\n\n")
                
                # No need to do the rest of the row operations if a format error is found
                if format_error_count > 0:
                    continue
                
                # Creates nested dictionary with course section as the key
                course_dict = row
                course = course_dict.pop(ColumnHeaders.COURSE_SEC.value)
                
                # Appends three key-value pairs for assignments
                course_dict[ColumnHeaders.ROOM_ASS.value] = ""
                course_dict[ColumnHeaders.TIME_ASS.value] = ""
                course_dict[ColumnHeaders.DAY_ASS.value] = ""

                
                # Appends Course Section dictionary to cumulative dictionary of sections
                dict_of_course_dicts[course] = course_dict
                
            # End for loop
        # End of file reading
        
        # If errors are found, raise the exception
        if format_error_count > 0:
            raise ImportFormatError(f"{format_error_count} errors have been found:\n"
                                    + format_error_msg)
        
        
        
        # Updates the department's database tree
        department_dict = {department_abbr : dict_of_course_dicts}
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
    
    
    def exportCSV(self, department_abbr, outfile=""):
        """
        Exports a CSV from the database. This function depends on output generated from the getDB function
        
        Args:
            department_abbr (string): Data from the firebase db for a specfic department.
                EX. It could be the CS data or the ECE data depending on parameter that was given to getDB
                department_abbr = CS
                department_abbr = ECE
            outfile (string): File path and name of the output csv. Default is "Export{department_abbr}Data.csv"
                in current directory
        
        Raises:
            QueryNotFoundError: database_path doesn't return data
            PermissionError: Existing CSV file cannot be accessed (check if any programs are currently using it)
        """
        
        # Default path for outfile is in current directory, if not specified
        if not outfile: outfile = f"Export{department_abbr}Data.csv"
        
        # Get the dictionary from getDB function
        department_dict = self.getDB(f"/{DatabaseHeaders.COURSES.value}/{department_abbr}")
        
        # Column headers for output CSV
        fieldnames = [ ColumnHeaders.COURSE_SEC.value, ColumnHeaders.FAC_ASSIGN.value, ColumnHeaders.ROOM_ASS.value,
                       ColumnHeaders.DAY_ASS.value, ColumnHeaders.TIME_ASS.value, ColumnHeaders.ROOM_PREF.value,
                       ColumnHeaders.DAY_PREF.value, ColumnHeaders.TIME_PREF.value, ColumnHeaders.SEATS_OPEN.value ]
        
        # Now lets open a CSV file to write to
        with open(outfile, 'w', encoding='utf-8-sig') as csvfile:
            
            # Create a writer that has fieldnames equal to column_information. 
            # Line Terminator must be set to \n or it will skip lines in the export CSV
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames, lineterminator = '\n')
            writer.writeheader()

        
            # Iterate through the first part of the dictionary department_dict and get the section
            # Append section info to a dict with the section name and write out to CSV
            for section_name, section_info in department_dict.items():
                new_row = { ColumnHeaders.COURSE_SEC.value : section_name }
                
                # section_info already has all the dictionary info we need, so we can just append it to new_row with .update()
                # .update() takes key-value pairs from section_info and puts them into new_row, overwriting the values of any existing keys in new_row
                new_row.update(section_info)
                
                writer.writerow(new_row)
                
    # End of exportCSV
    
    
    def checkUserPass(self, username, password):
        """
        Checks username and plaintext password against database to confirm proper login.
        Password hashing will be done within this method, so only a plaintext password
        is necessary.
        Returns true only if a username and password is found.

        Args:
            username (string): Username of the account
            password (string): Plaintext password of the account

        Returns:
            Boolean: Returns True if login credentials are found, False if not
        """
        
        fetched_account = {}
        
        # Check username
        try: # Fetches account of the specified username as a dict
            fetched_account = self.getDB(f"/{DatabaseHeaders.ACCOUNTS.value}/{username}")
            
        except QueryNotFoundError: # Username not defined, return false
            return False
        
        # Username check passed
        # Split account info
        fetched_salt = fetched_account['Salt']
        fetched_password = fetched_account['Password']
        
        # Hash the plaintext password using hashlib SHA256
        import hashlib
        hashed_password = hashlib.sha256((password+fetched_salt).encode('utf-8')).hexdigest()
        
        # Check if password hash matches the one in the database
        if hashed_password != fetched_password:
            return False
        
        # All checks passed, return True
        return True
    
    # End of checkUserPass

################################################################################    
    
    ######################################
    #
    # Generate Assignment Methods
    #
    ######################################
    
    def _init_tables(self):
        """
        Initializes room tables for each room and stores them out to database.
        """
        
        # Gets all the buildings
        buildings_dict = self.getDB(f"/{DatabaseHeaders.ROOMS.value}")
        tables_dict = {}
        
        # For each building, we need to make the tables
        for building, list_of_rooms in buildings_dict.items():            
            # Creates new dictionary of rooms, each room keying a dictionary to a RoomTable 2D List
            new_building_dict = {}
            for room in list_of_rooms:
                empty_table = RoomTable()
                new_building_dict[room] = empty_table.getTable()
            tables_dict[building] = new_building_dict
        
        # Stores dictionary to database
        self.updateDB(tables_dict, f"/{DatabaseHeaders.TABLES.value}")
            
    # End of init_tables
    
    
    
    def generate_assignments(self):
        """
        Generates all the class assignments and marks conflicting assignments
        """
        
        # Generates schedule tables
        self._init_tables()
        
        # Gets all the departments
        all_departments_dict = self.getDB(f"/{DatabaseHeaders.COURSES.value}")
        
        # For each department, we need to make the assignments
        for department, courses_dict in all_departments_dict.items():
            if department == "ECE": continue # @DEBUG skips ECE
            
            # Grabs all available rooms
            ## First 3 letters of room preference will have building acronym,
            ## so we use that to determine which list of available rooms to pull.
            sample_room = courses_dict[list(courses_dict.keys())[0]][ColumnHeaders.ROOM_PREF.value] # Returns room preference of first section
            building_name = sample_room[:3] # Grabs first 3 letters
            
            # Gets room tables
            r_room_tables_dict = self.getDB(f"/{DatabaseHeaders.TABLES.value}/{building_name}")
            room_tables = {}
            
            # Creates room table objects
            for room_num, table in r_room_tables_dict.items():
                new_table = RoomTable()
                new_table.importTable(table)
                room_tables[room_num] = new_table
            
            #^ At this point, we have a dictionary of all the course sections as well
            #^ as a dictionary of all the available rooms tables for that department's building.
            
            #^ Time to make assignments.
            
            #^ 1st - Assign courses with Room Preferences
            room_tables = self._assign_with_room_pref(courses_dict, room_tables)
            
            #^ 2nd - Assign courses with Day/Time Preferences
            room_tables = self._assign_with_day_time_pref(courses_dict, room_tables)

            #^ 3rd - Assign the rest of the courses
            room_tables = self._assign_rest_of_courses(courses_dict, room_tables)
            
            
            # Now that room_tables is done, loop through tables and update the database with the new assignments
            for room_num, room_table in room_tables.items():
                
                for day, day_index in TableIndex.DAY_REF.items():
                    
                    for time, time_index in TableIndex.TIME_REF.items():
                        
                        if not room_table.isEmptyCell(day_index, time_index): # If table cell is occupied
                            course_in_cell = room_table.getCell(day_index, time_index) # Gets course name in that cell
                            
                            # Changes the course info in courses_dict accordingly
                            # Changes Day Assignment, Time Assignment, and Room Assignment
                            courses_dict[course_in_cell][ColumnHeaders.ROOM_ASS.value] = building_name + room_num
                            courses_dict[course_in_cell][ColumnHeaders.DAY_ASS.value] = day
                            courses_dict[course_in_cell][ColumnHeaders.TIME_ASS.value] = time
            
            # Update all_departments_dict
            all_departments_dict[department] = courses_dict
            
        # End department, courses_dict for loop
        
        # Update database
        self.updateDB(all_departments_dict, f"/{DatabaseHeaders.COURSES.value}")

    # End of generate_assignments
    
    
    
    
    
    ######################################
    #
    # Assignment helper functions
    #
    ######################################
    
    def _assign_rest_of_courses(self, courses_dict, room_tables):
        """
        Private method to help generate_assignments in handling
        assignments for professors without preferences.
        """
        
        for course_name, course_info in courses_dict.items():
            
            # Gets time/day fields
            c_time_pref = course_info[ColumnHeaders.TIME_PREF.value]
            c_day_pref = course_info[ColumnHeaders.DAY_PREF.value]
            
            # 4 combinations of day/time preferences:
            #     1) Day and Time, 2) Only day, 3) Only time, 4) Neither time nor day
            # Must prepare for ONLY outcome 4
            
            if not c_day_pref and not c_time_pref: # Outcome 4
                c_time_pref = "ABCDEFG" # Set to all possible time periods
                c_day_pref = "MWTR" # Set to all possible days
            
            else: # Outcomes 1-3
                continue # Outcomes 1-3 were already handled
                
            # Breaks up days into 2-character list to loop better (e.g., ['MW', 'TR'])
            c_day_pref = list(c_day_pref[i:i+2] for i in range(0, len(c_day_pref), 2))

            
            
            # Now, we need to loop through every room table to find the next available cell
            assignment_made = False    # Gets changed to True when assignment made, breaks out of loop(s)
            for room_num, table in room_tables.items():
                
                for day in c_day_pref: # Will be either 'MW' or 'TR'
                    
                    for time in c_time_pref: # Will be a letter A-G
                        
                        # Checks if cell is empty, then sets the cell with the course name
                        if table.isEmptyCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time]):
                            table.setCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time], str=course_name)
                            assignment_made = True
                            break
                        # If the cell is not empty, move on to the next preferred one
                    
                    # Checks if assignment has been made
                    if assignment_made: break
            
            # Checked if assignment was made, if not, then there was a conflict
            if not assignment_made:
            # @TODO rest_of_courses conflict handling goes here
                pass
        # End of course_dict for loop
        
        
        return room_tables
    # End of _assign_rest_of_courses
    
    
    def _assign_with_day_time_pref(self, courses_dict, room_tables):
        """
        Private method to help generate_assignments in handling
        assignments for professors with specific day/time preferences.
        """
        
        for course_name, course_info in courses_dict.items():
            
            # Gets time/day fields
            c_time_pref = course_info[ColumnHeaders.TIME_PREF.value]
            c_day_pref = course_info[ColumnHeaders.DAY_PREF.value]
            
            # 4 combinations of day/time preferences:
            #     1) Day and Time, 2) Only day, 3) Only time, 4) Neither time nor day
            # Must prepare for all but Outcome 4
            
            if c_day_pref and c_time_pref: # Outcome 1
                pass # leave as is
            
            elif c_day_pref and not c_time_pref: # Outcome 2
                c_time_pref = "ABCDEFG" # Set to all possible time periods
            
            elif c_time_pref and not c_day_pref: # Outcome 3
                c_day_pref = "MWTR" # Set to all possible days
            
            else: # Outcome 4
                continue # Prioritizing preferences right now
                
            # Breaks up days into 2-character list to loop better (e.g., ['MW', 'TR'])
            c_day_pref = list(c_day_pref[i:i+2] for i in range(0, len(c_day_pref), 2))

            
            
            # Now, we need to loop through every room table to find the next available cell
            assignment_made = False    # Gets changed to True when assignment made, breaks out of loop(s)
            for room_num, table in room_tables.items():
                
                for day in c_day_pref: # Will be either 'MW' or 'TR'
                    
                    for time in c_time_pref: # Will be a letter A-G
                        
                        # Checks if cell is empty, then sets the cell with the course name
                        if table.isEmptyCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time]):
                            table.setCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time], str=course_name)
                            assignment_made = True
                            break
                        # If the cell is not empty, move on to the next preferred one
                    
                    # Checks if assignment has been made
                    if assignment_made: break
            
            # Checked if assignment was made, if not, then there was a conflict
            # @TODO day_time_pref conflict handling goes here
            if not assignment_made:
                pass
                
        # End of course_dict for loop
        
        
        return room_tables
    # End of _assign_with_day_time_pref
    
    
    def _assign_with_room_pref(self, courses_dict, room_tables):
        """
        Private method to help generate_assignments in handling
        assignments for courses in specific rooms.
        """
        
        for course_name, course_info in courses_dict.items():
            # Checks if it has a room preference
            room_pref = course_info[ColumnHeaders.ROOM_PREF.value]
            
            if len(room_pref) > 3:      # Would be > 3 characters if room preference is specified
                # Gets room table
                room_num = room_pref[3:]
                selected_table = room_tables[room_num]
                
                # Gets time/day fields
                c_time_pref = course_info[ColumnHeaders.TIME_PREF.value]
                c_day_pref = course_info[ColumnHeaders.DAY_PREF.value]
                
                # 4 combinations of day/time preferences:
                #     1) Day and Time, 2) Only day, 3) Only time, 4) Neither time nor day
                # Must prepare for all 4 outcomes
                
                if c_day_pref and c_time_pref: # Outcome 1
                    pass # leave as is
                
                elif c_day_pref and not c_time_pref: # Outcome 2
                    c_time_pref = "ABCDEFG" # Set to all possible time periods
                
                elif c_time_pref and not c_day_pref: # Outcome 3
                    c_day_pref = "MWTR" # Set to all possible days
                
                else: # Outcome 4
                    c_time_pref = "ABCDEFG" # Set to all possible time periods
                    c_day_pref = "MWTR" # Set to all possible days
                
                
                # Breaks up days into 2-character list to loop better (e.g., ['MW', 'TR'])
                c_day_pref = list(c_day_pref[i:i+2] for i in range(0, len(c_day_pref), 2))
                
                
                # Now that table is selected, loop through room table to check for an empty PREFERRED cell.
                assignment_made = False    # Gets changed to True when assignment made, breaks out of loop(s)
                for day in c_day_pref: # Will be either 'MW' or 'TR'
                    
                    for time in c_time_pref: # Will be a letter A-G
                        
                        # Checks if cell is empty, then sets the cell with the course name
                        if selected_table.isEmptyCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time]):
                            selected_table.setCell(TableIndex.DAY_REF[day], TableIndex.TIME_REF[time], str=course_name)
                            assignment_made = True
                            break
                        # If the cell is not empty, move on to the next preferred one
                    
                    # Checks if assignment has been made
                    if assignment_made: break
                
                # Checked if assignment was made, if not, then there was a conflict
                # @TODO room_pref conflict handling goes here
                if not assignment_made:
                    pass
            # End of if len(room_pref) > 3
            
            else: # We have no interest in this course at the moment
                continue
            
        return room_tables
    # End of _assign_with_room_pref
    
    
    ######################################
    #
    # @DEBUG Methods
    # @TODO DELETE THESE METHODS BEFORE PUSHING TO PRODUCTION
    #
    ######################################
    
    def print_room_tables(self, room_tables, building):
        with open("test.txt",'a') as w:
            for room, table in room_tables.items():
                string = f"{building}{room}:{table}"
                w.write(string+"\n")
    
# End of DataOperation
