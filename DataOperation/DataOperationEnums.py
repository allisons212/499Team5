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
    Used for importing CSV column headers
    """
    COURSE_SEC = 'Course Section'
    FAC_ASSIGN = 'Faculty Assignment'
    ROOM_PREF = 'Classroom Preferences'
    TIME_PREF = 'Time Block Preferences'
    DAY_PREF = 'Day Preferences'
    SEATS_OPEN = 'Seats Open'
    ROOM_ASS = 'Classroom Assignment'
    TIME_ASS = 'Time Assignment'
    DAY_ASS = 'Day Assignment'
    
    
class DepartmentAbbreviations(Enum):
    """
    Abbreviations for subject departments like CS = Computer Science,
    PY = Physics, etc. will be here.
    """
    CS = 'Computer Science'
    ECE = 'Electrical and Computer Engineering'

