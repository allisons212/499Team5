from DataOperation import DataOperation
from DataOperationEnums import *
from DataOperationException import * # Custom exceptions

def main():

    data_operation = DataOperation() # Runs constructor to authenticate credentials
    
    # Test checkUserPass
    #print(data_operation.checkUserPass(username="CSChair", password="CSChair")) # Correct pass: CSChair
    #print(data_operation.checkUserPass(username="ECEChair", password="ECEChair")) # Correct pass: ECEChair

    
    # Test try-catch block for import CSV methods
    try:
        # CS Department and OKT
        course_csv_file = "ClassData/Dept1ClassDataConflicts.csv" # This is provided from GUI
        department_abbr = "CS"                          # This is provided from GUI
        data_operation.importCSV(course_csv_file, "ClassData/Dept1Rooms.csv", department_abbr )
        
        # ECE Department and ENG
        course_csv_file = "ClassData/Dept2ClassData.csv"
        department_abbr = "ECE"
        data_operation.importCSV(course_csv_file, "ClassData/Dept2Rooms.csv", department_abbr )
    
    except FileNotFoundError as fnfe:
        print(f"{fnfe}\n")
        return
        
    except ImportFormatError as ife:
        print(f"{ife}\n")
        return
    
    

    """
    # Test try-catch block for getDB and updateDB
    try:
        r = data_operation.getDB(f"{DatabaseHeaders.COURSES.value}/CS/CS100-01")
        
        # Changes the entry by removing Faculty Assignment and appending "Test header"
        r.pop(ColumnHeaders.FAC_ASSIGN.value)
        r["Test Header"] = "Test Value"
        
        data_operation.updateDB(r, f"{DatabaseHeaders.COURSES.value}/CS/CS100-01")
        
    except QueryNotFoundError as qnfe: # Raised by getDB
        print(qnfe)
        
    except ImproperDBPathError as idpe: # Raised by updateDB
        print(idpe)
    """

    """
    # Updating Database to store other fields of data
    try:
        r = { "TestAccount" : "Test Password. This needs to be a hash when in production."
            , "CSDeptChair" : "<SHA256 Hash>"
            }
        
        data_operation.updateDB(r, DatabaseHeaders.ACCOUNTS.value)
        
        r = data_operation.getDB(DatabaseHeaders.ROOMS.value + "/OKT")
        print(f"Room numbers are of type: {type(r)}")
        
    except QueryNotFoundError as qnfe: # Raised by getDB
        print(qnfe)    
    
    except ImproperDBPathError as idpe: # Raised by updateDB
        print(idpe)
    """
    
    # Testing generate_assignment
    data_operation.generate_assignments(user_department="CS")
    data_operation.generate_assignments(user_department="ECE")
    
    
    # Test exportCSV
    data_operation.exportCSV("CS", "ClassData/ExportCSData.csv")


if __name__ == "__main__":
    main()