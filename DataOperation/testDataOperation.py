import DataOperation
from DataOperationEnums import ColumnHeaders
from DataOperationException import * # Custom exceptions


def main():

    data_operation = DataOperation.DataOperation() # Runs constructor to authenticate credentials
    
    
    # Test try-catch block for importCSV()
    #"""
    try:
        csv_file = "ClassData/Dept1ClassData.csv" # This is provided from GUI
        department_abbr = "CS"                   # This is provided from GUI
        data_operation.importCSV(csv_file, department_abbr) # Test a csv file
    
    except FileNotFoundError as fnfe:
        print(f"{fnfe}\n")
        
    except ImportFormatError as ife:
        print(f"{ife}\n")
    #"""

    # Test try-catch block for getDB and updateDB
    try:
        r = data_operation.getDB("CS/CS100-01")
        
        # Changes the entry by removing Faculty Assignment and appending "Test header"
        r.pop(ColumnHeaders.FAC_ASSIGN.value)
        r["Test Header"] = "Test Value"
        
        data_operation.updateDB(r, "CS/CS100-01")
        
    except QueryNotFoundError as qnfe: # Raised by getDB
        print(qnfe)
        
    except ImproperDictionaryError as ide: # Raised by updateDB
        print(ide)









if __name__ == "__main__":
    main()