from DataOperation import DataOperation
from DataOperationEnums import *
from DataOperationException import * # Custom exceptions

import time

def main():

    data_operation = DataOperation() # Runs constructor to authenticate credentials
    
    """
    # Test addUserPass
    data_operation.addUserPass(username="CSChair", password="CSChair", department="CS")
    data_operation.addUserPass(username="ECEChair", password="ECEChair", department="ECE")
    
    # Test checkUserPass
    print(data_operation.checkUserPass(username="CSChair", password="CSChair")) # Correct pass: CSChair
    print(data_operation.checkUserPass(username="ECEChair", password="ECEChair")) # Correct pass: ECEChair
    """
    
    # Test getEmptyRooms
    #empty_cells = data_operation.getEmptyRooms("CS")
    #for room, list_of_cells in empty_cells.items():
    #    print(f"{room}: {list_of_cells}")
    
    
    
    # Test try-catch block for import CSV methods
    try:
        # CS Department and OKT
        course_csv_file = "../ClassData/Dept1ClassDataConflicts.csv"
        department_abbr = "CS"
        data_operation.importCSV(course_csv_file, "ClassData/Dept1Rooms.csv", department_abbr)
        
        # ECE Department and ENG
        course_csv_file = "../ClassData/Dept2ClassData.csv"
        department_abbr = "ECE"
        data_operation.importCSV(course_csv_file, "ClassData/Dept2Rooms.csv", department_abbr)
    
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
        return
        
    except ImproperDBPathError as idpe: # Raised by updateDB
        print(idpe)
        return
    """
    
    # Testing generate_assignment
    data_operation.generate_assignments(user_department="CS")
    data_operation.generate_assignments(user_department="ECE")
    
    
    # Test exportCSV
    #data_operation.exportCSV("CS", "ClassData/ExportCSData.csv")
    
    # Test updateSolutionAssignment
    #data_operation.updateSolutionAssignments()


if __name__ == "__main__":
    start_time = time.time() # Used to measure execution time
    
    main()
    
    # Prints execution time
    print(f"\n\n---Execution Time: {time.time()-start_time:.3f} seconds---")