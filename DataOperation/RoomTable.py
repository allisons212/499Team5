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
# Filename:     RoomTable.py
# Purpose:      To establish a Data Structure to organize schedule data
#
# Editors of this file:     Devin Patel
#                           Harrison Matthews
# 
# NOTES:
#
#   Lookup Table Implementation
#     Each room is assigned a 2D list which represents a table as follows:
#     ROOM: OKT123
#     -------------------------------
#             |  MW (0)  |  TR (1)  |
#     -------------------------------
#     | (0) A | <COURSE> | <COURSE> |
#     | (1) B | <COURSE> | <COURSE> |
#     | (2) C | <COURSE> | <COURSE> |
#     | (3) D | <COURSE> | <COURSE> |
#     | (4) E | <COURSE> | <COURSE> |
#     | (5) F | <COURSE> | <COURSE> |
#     | (6) G | <COURSE> | <COURSE> |
#
#     So C block on MW would be: list[0][2]
#     Each cell will contain the course name as a string
#       or just an empty string.
#
########################################################################

from enum import Enum

class RoomTable:
    """
    Data structure to organize time periods for every classroom
    """
    
    ##########################################
    #
    # Variables
    #
    ##########################################
    
    table = [] # list of lists
    
    
    ##########################################
    #
    # Methods
    #
    ##########################################
    
    def __init__(self):
        """
        Initializes table as a list with 2 sublists, each representing a day period MW or TR
        """
        self.table = [ ["", "", "", "", "", "", ""], # MW, each "" is a course at time A-G
                       ["", "", "", "", "", "", ""]  # TR, each "" is a course at time A-G
                    ]
    
    
    def isEmptyCell(self, day, time):
        """
        Checks if contents of a cell in the table is empty.
        day can be either 0 (MW) or 1 (TR)
        time can be 
        0 (A),
        1 (B),
        2 (C),
        3 (D),
        4 (E),
        5 (F),
        6 (G)

        Args:
            day (int): Integer 0 or 1
            time (int): Integer 0-6

        Returns:
            boolean: Returns True if cell is empty, False if cell is occupied
        """
        if self.table[day][time]: return False
        else: return True
    
    
    def getDay(self, day):
        """
        Returns list of time periods on specified day.
        day can be either 0 (MW) or 1 (TR)

        Args:
            day (int): Integer 0 or 1

        Returns:
            list: Returns list of time periods on specified day
        """
    
    
    # Getters
    def getCell(self, day, time):
        """
        Returns contents of a cell in the table.
        day can be either 0 (MW) or 1 (TR)
        time can be 
        0 (A),
        1 (B),
        2 (C),
        3 (D),
        4 (E),
        5 (F),
        6 (G)

        Args:
            day (int): Integer 0 or 1
            time (int): Integer 0-6

        Returns:
            string: Returns course name if contained in cell, empty string if not occupied.
        """
        return self.table[day][time]
    
    
    def getDay(self, day):
        """
        Returns list of time periods on specified day.
        day can be either 0 (MW) or 1 (TR)

        Args:
            day (int): Integer 0 or 1

        Returns:
            list: Returns list of time periods on specified day
        """
        return self.table[day]
    
    
    def getTable(self):
        """
        Returns entire table as a 2D list.
        The intended use is for storing out to database.
        
        Returns:
            list: Returns table as a 2D list
        """
        return self.table
    
    # Setters
    def setCell(self, day, time, str):
        """
        Sets contents of a cell in the table.
        day can be either 0 (MW) or 1 (TR)
        time can be 
        0 (A),
        1 (B),
        2 (C),
        3 (D),
        4 (E),
        5 (F),
        6 (G)

        Args:
            day (int): Integer 0 or 1
            time (int): Integer 0-6
            str (string): Course to set the cell to
        """
        self.table[day][time] = str
    
    
    def importTable(self, table):
        """
        Sets current table with another 2D list

        Args:
            table (list): 2D list
        """
        self.table = table
    

# End of RoomTable

class RoomTableEnum(Enum):
    """
    Reference dictionaries for indexing the table
    """
    DAY_REF = { "MW": 0, "TR": 1 }
    TIME_REF = { "A": 0,
                 "B": 1,
                 "C": 2,
                 "D": 3,
                 "E": 4,
                 "F": 5,
                 "G": 6 }
