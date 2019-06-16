'''Schedule CSV Creactor for Google Calendar Import

This script takes a csv of a teacher's schedule exported from Aspen
and creates a csv for import into Google Calendar. Set the
dates definition file and any schedule information in the settings 
section. 

The script requires python3 and the pandas library.
'''

import argparse
from os import listdir, makedirs, path
import csv
import re
import datetime as dt

import pandas

#### Settings that you might need to change ####

# school year definition file
dates_file = '2019-2020 dates.csv'

# semester 2 begins
semester_cutoff = dt.date(2019,1,20)
# Use these since Google seems to want separate date and time strings
periods = [[],
           ["7:50","8:55"],
           ["9:00","9:53"],
           ["9:58","11:03"],
           ["11:08","12:31"],
           ["12:36","13:41"],
           ["13:46","14:39"]]

# Each day code has a corresponding number, starting with 1
daynum_list = ['', 'bM', 'bT', 'bW', 'bR', 'bF', 'wM', 'wT', 'wW', 'wR', 'wF']

# basic regular expression for pulling the period from a day
# append the daynum string, e.g., bM or wW to complete the pattern
# ex schedule line from Aspen: 1(bM,bR,wT,wF) 2(bT,bF,wR) 4(wM)
perex = '(\d)\([^\(]*'

# read in dates file and convert the dates to actual date objects
dates_frame = pandas.read_csv(dates_file)
dates_frame['Date'] = pandas.to_datetime(dates_frame['Date'],
                              format='%m/%d/%Y')
dates_frame['Date'] = dates_frame['Date'].dt.date


def create_csv_for_file(infile, outdir=None):

    infile_naked = infile.rsplit('.', 1)[0]
    outfile = infile_naked + '_gcal.csv'
    if outdir:
        basename = path.basename(outfile)
        outfile = path.join(outdir, basename)
        print(outfile)

    # individual teacher file
    teacher_frame = pandas.read_csv(infile, dtype={'SecNo': str})

    with open(outfile, mode='w') as f:
        
        # Google wants these header names exactly for import into Calendar
        sched_writer = csv.writer(f, delimiter=',')
        sched_writer.writerow(['Subject','Start Date','Start Time','End Date', 'End Time'])
        
        for i, day in dates_frame.iterrows():
            daynum = day.DayNum
            
            # skip days without regular schedule
            if daynum == 0:
              continue

            # Set the semester for the current day
            semester = 'S1' if day.Date < semester_cutoff else 'S2'

            for j, klass in teacher_frame.iterrows():

                # skip classes that don't meet on the given day
                if klass.Schedule != klass.Schedule or daynum_list[daynum] not in klass['Schedule']:
                    continue
                
                # skip if wrong semester
                if klass.Term != semester:
                    continue

                # skip classes that don't have a normal section number
                if klass.SecNo not in ['01', '02', '03', '04', '05', '06', '07']:
                    continue 

                # Get the period for the block on this day, and from that the start/end strings
                pattern = perex + daynum_list[daynum]
                match = re.search(pattern, klass['Schedule'])
                if not match:
                    continue

                period = int(match.group(1)) 
                start = periods[period][0]
                end = periods[period][1]

                # Manually set the lunch start/end
                if period == 4 and klass['Lunch Group'] == '1.0':
                    start = "11:08"
                    end = "12:01"
                elif period == 4 and klass['Lunch Group'] == '3.0':
                    start = "11:38"
                    end = "12:31"
                    
                # Write the row of information - represents one event on calendar / one class meeting
                sched_writer.writerow([klass['Description'], day.Date, start, day.Date, end])

def main():
    '''Read in arguments and act appropriately.'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="process all files in a directory")
    parser.add_argument("-f", "--file", type=str, help="process a single file")
    parser.add_argument("-o", "--output", type=str, help="output directory")
    args = parser.parse_args()

    # create output directory if specified and doesn't already exist
    output_dir = None
    if args.output:
        if not path.exists(args.output):
            makedirs(args.output)
        output_dir = args.output

    if args.directory:
        allfiles = [path.join(args.directory, f) for f in listdir(args.directory) if path.isfile(path.join(args.directory, f))]
        print(allfiles)
        for infile in allfiles:
            create_csv_for_file(infile, outdir=output_dir)
    elif args.file:
        create_csv_for_file(args.file, outdir=output_dir)
    else:
        print("Must include either a single csv file or a directory of csv files")


if __name__ == "__main__":
    main()