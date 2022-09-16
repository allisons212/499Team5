import csv

"""

Method to read CSV file with schedule data and checks for formatting.
Afterwards, it creates database entries for each class section.

"""
def importCSV(filename):

    f = filename
    with open(f, mode='r', encoding='utf-8-sig') as read_obj:
        csv_dict_reader = csv.DictReader(read_obj)
        
        # Reads in each row of csv file, 'row' is a dictionary keyed by the column headers
        for row in csv_dict_reader:            
            # Initializes row dict info
            course = row['Course']                              # e.g., CS103-01
            faculty_assignment = row['Faculty Assignment']      # e.g., Dr. Goober
            classroom_pref = row['Classroom Preferences']       # e.g., OKT203, SST123, MOR
            time_pref = row['Time Block Preferences']           # e.g., A, B, C, D, E, F, G; designating class time blocks throughout the day
            day_pref = row['Day Preferences']                   # e.g., M, T, W, R, F (R = Thursday)
            seats_open = row['Seats Open']                      # Positive integer denoting max number of students for that section

            # Update database fields here
            
            


# File path of csv file
filename = ""

if len(filename) == 0:
    print("Specify a filename or file path in main")
else:
    # Runs procedure
    importCSV(filename)

