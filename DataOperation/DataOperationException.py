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
# Filename:     DataOperationExceptions.py
# Purpose:      To establish a set of exceptions to be raised
#               in DataOperation.py to warn against improper inputs.
#
# Editors of this file:     Devin Patel
# 
# NOTES:
#   1) Ensure each exception class has a default message
#
########################################################################


class ImportFormatError(Exception):
    """
    Import CSV file is not the right format.
    """
    
    def __init__(self, msg="Incorrect input formatting. Please check import CSV guidelines."):
        super().__init__(msg)


class QueryNotFoundError(Exception):
    """
    Database query returned no data or findings.
    """
    
    def __init__(self, msg="Database query returned no data."):
        super().__init__(msg)
