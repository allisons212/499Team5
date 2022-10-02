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
            if department == "ECE": continue # DEBUG
            
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
            # TODO: Conflict handling goes here
            if not assignment_made:
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
            # TODO: Conflict handling goes here
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
                # TODO: Conflict handling goes here
                if not assignment_made:
                    pass
            # End of if len(room_pref) > 3
            
            else: # We have no interest in this course at the moment
                continue
            
        return room_tables
    # End of _assign_with_room_pref
    
    
    ######################################
    #
    # DEBUG Methods
    # TODO: DELETE THESE METHODS BEFORE PUSHING TO PRODUCTION
    #
    ######################################
    
    def print_room_tables(self, room_tables, building):
        with open("test.txt",'a') as w:
            for room, table in room_tables.items():
                string = f"{building}{room}:{table}"
                w.write(string+"\n")
    
# End of DataOperation
