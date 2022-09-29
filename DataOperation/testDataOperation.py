from DataOperation import DataOperation
from DataOperationException import * # Custom exceptions
import pprint


def main():

    data_operation = DataOperation() # Runs constructor to authenticate credentials
    
    # Sample try-catch block for importCSV()
    try:
        csv_file = "/file/path" # This is provided from GUI
        department_abbr = "CS"                   # This is provided from GUI
        data_operation.importCSV(csv_file, department_abbr) # Test a csv file
    
    except FileNotFoundError as fnfe:
        print(f"{fnfe}\n")
        
    except ImportFormatError as ife:
        print(f"{ife}\n")
        
    
    
    try:
        # Get the CS department in database
        r = data_operation.getDB("CS")
        
        # Testing the exportCSV function by sending it the dictionary that we got from getDB
        # Export a department from database into a csv file in this case we want CS
        abbr = "CS"
        data_operation.exportCSV(abbr)
        
        
        print(f"Type: {type(r)}")
        
    except QueryNotFoundError as qnfe:
        print(f"{qnfe}")



if __name__ == "__main__":
    main()