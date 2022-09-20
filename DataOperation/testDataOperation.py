from DataOperation import DataOperation
from DataOperationException import * # Custom exceptions


def main():

    data_operation = DataOperation() # Runs constructor to authenticate credentials
    
    # Sample try-catch block for importCSV()
    try:
        csv_file = "ClassData/Dept2ClassData.csv" # This is provided from GUI
        department_abbr = "ECE"                   # This is provided from GUI
        data_operation.importCSV(csv_file, department_abbr) # Test a csv file
    
    except FileNotFoundError as fnfe:
        print(f"{fnfe}\n")
        
    except ImportFormatError as ife:
        print(f"{ife}\n")





if __name__ == "__main__":
    main()