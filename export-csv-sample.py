import csv


def doCSV(filename):
    # Opens output csv file
    csvfile = open("output.csv", 'w', newline='')

    # Column headers for output CSV
    fieldnames = ['Course Section', 'Faculty Assignment', 'Classroom Preferences', 'Time Block Preferences', 'Day Preferences',
                    'Seats Open']
    

    # Writes out the 1st row header
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    f = filename
    with open(f, mode='r', encoding='utf-8-sig') as read_obj:
        csv_dict_reader = csv.DictReader(read_obj)
        
        
        # Reads in each row of csv file, 'row' is a dictionary keyed by the column headers
        for row in csv_dict_reader:
            
            # Initializes row dict info
            
            course = row['Course Section']                      # e.g., CS103-01
            faculty_assignment = row['Faculty Assignment']      # e.g., Dr. Goober
            classroom_pref = row['Classroom Preferences']       # e.g., OKT203, SST123, MOR
            time_pref = row['Time Block Preferences']           # e.g., A, B, C, D, E, F, G; designating class time blocks throughout the day
            day_pref = row['Day Preferences']                   # e.g., M, T, W, R, F (R = Thursday)
            seats_open = row['Seats Open']                      # Positive integer denoting max number of students for that section            
            
            

            # Outputs row
            writer.writerow({'Course Section':course, 'Faculty Assignment':faculty_assignment,
                                'Classroom Preferences':classroom_pref, 'Time Block Preferences':time_pref,
                                'Day Preferences':day_pref, 'Seats Open':seats_open})
            
    csvfile.close()



# File path of csv file
filename = "path/to/file.csv"
doCSV(filename)

