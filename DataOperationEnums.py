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
# Filename:     DataOperationEnums.py
# Purpose:      To establish a set of enums for DataOperation.py
#
# Editors of this file:     Devin Patel
#                           Harrison Matthews
# 
# NOTES:
#   1) To access a value of an enum, do <EnumClass>.<EnumName>.value
#
########################################################################

from enum import Enum

class ColumnHeaders(Enum):
    """
    Used for importing CSV column headers.
    
    Access by typing "ColumnHeaders.<EnumName>.value"
    """
    COURSE_SEC = 'Course Section'
    FAC_ASSIGN = 'Faculty Assignment'
    ROOM_PREF = 'Room Preferences'
    TIME_PREF = 'Time Block Preferences'
    DAY_PREF = 'Day Preferences'
    SEATS_OPEN = 'Seats Open'
    ROOM_ASS = 'Classroom Assignment'
    TIME_ASS = 'Time Assignment'
    DAY_ASS = 'Day Assignment'
    BUILD = 'Building'
    ROOM_NUM = 'Room Number'
    
    
class DatabaseHeaders(Enum):
    """
    Selects which section of the database to move the reference to.
    Used for generating a database path.
    e.g., /[Accounts]/CSDeptChair
    
    Access by typing "DatabaseHeaders.<EnumName>.value"
    """
    ACCOUNTS = 'Accounts'
    COURSES = 'Department Courses'
    ROOMS = 'Available Classrooms'
    TABLES = 'Room Tables'
    FACULTYTABLES = 'Faculty Tables'
    
class AccountHeaders(Enum):
    """
    Accesses Database tree branches containing account information
    """
    DEPARTMENT = 'Department'
    PASSWORD = 'Password'
    SALT = 'Salt'
    SALT_LEN = 10