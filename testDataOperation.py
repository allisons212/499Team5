from DataOperation import DataOperation
from DataOperationEnums import *
from DataOperationException import * # Custom exceptions



def main():
    db = DataOperation()

    # Test facultyList
    db.getFacultyList("CS")


if __name__ == "__main__":
    main()