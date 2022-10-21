from DataOperation import DataOperation
from DataOperationEnums import *
from DataOperationException import * # Custom exceptions


def restoreDB(data_operation, willRestore):
    if willRestore:
        try:
            # CS Department and Available Rooms
            course_csv_file = "ClassData/Dept1ClassDataConflicts.csv" # This is provided from GUI
            department_abbr = "CS"                          # This is provided from GUI
            data_operation.importCourseCSV(course_csv_file, department_abbr) # Test a course csv file
            data_operation.importRoomCSV("ClassData/AvailableRooms.csv") # Test a room csv file
            
            # ECE Department
            course_csv_file = "ClassData/Dept2ClassData.csv"
            department_abbr = "ECE"
            data_operation.importCourseCSV(course_csv_file, department_abbr)
        
        except FileNotFoundError as fnfe:
            print(f"{fnfe}\n")
            
        except ImportFormatError as ife:
            print(f"{ife}\n")
        finally:
            return willRestore
    
    else: return willRestore

def main():

    data_operation = DataOperation() # Runs constructor to authenticate credentials
    
    # Test exportCSV
    #data_operation.exportCSV("CS", "ClassData/ExportCSData.csv")
    
    
    # Test checkUserPass
    #print(data_operation.checkUserPass(username="CSChair", password="ComputerScienceDepartmentChair")) # Correct pass: ComputerScienceDepartmentChair
    #print(data_operation.checkUserPass(username="ECEChair", password="ElectricalComputerEngineeringDepartmentChair")) # Correct pass: ElectricalComputerEngineeringDepartmentChair
    
    
    
    
    
    #willRestore = True
    willRestore = False
    if restoreDB(data_operation, willRestore): return
    
    
    
    
    
    
    # Test try-catch block for import CSV methods
    try:
        # CS Department and OKT
        course_csv_file = "ClassData/Dept1ClassDataConflicts.csv" # This is provided from GUI
        department_abbr = "CS"                          # This is provided from GUI
        data_operation.importCourseCSV(course_csv_file, department_abbr) # Test a course csv file
        data_operation.importRoomCSV("ClassData/Dept1Rooms.csv", department_abbr) # Test a room csv file
        
        # ECE Department and ENG
        course_csv_file = "ClassData/Dept2ClassData.csv"
        department_abbr = "ECE"
        data_operation.importCourseCSV(course_csv_file, department_abbr)
        data_operation.importRoomCSV("ClassData/Dept2Rooms.csv", department_abbr)
    
    except FileNotFoundError as fnfe:
        print(f"{fnfe}\n")
        
    except ImportFormatError as ife:
        print(f"{ife}\n")
    
    

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


if __name__ == "__main__":
    main()