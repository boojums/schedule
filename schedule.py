# Generate a csv schedule for importing into Google Calendar
import datetime as dt
import csv

# Customize start and end dates
start = dt.date(2019,3,4)
end = dt.date(2019,6,13)

# Customize what to call each block ("Subject" in a GCal item)
block_names = ['Block 1', 'Game Prog (2)', 'Block 3', 'Intro (4)',
               'Intro (5)', 'Block 6', 'Block 7']

# Schedule definitions
blue_weeks = [1,3,6,9,11,13,15,18,20,22,24]
white_weeks = [2,5,7,10,12,14,17,19,21,23]
vacation_weeks = [8,16]
specials = [
    dt.date(2019,3,26), dt.date(2019,3,27), #MCAS
    dt.date(2019,5,21), dt.date(2019,5,22),
    dt.date(2019,6,4), dt.date(2019,6,5),
    dt.date(2019,5,27)] # Mem day

blue_blocks = [[1,4,3,2,6,7],
               [2,1,4,3,7,5],
               [3,2,5,6],
               [1,3,4,5,6,7],
               [2,1,5,4,7,6]]
white_blocks = [[3,4,2,1,7,6],
                [1,2,4,3,6,5],
                [2,3,5,7],
                [3,1,4,5,7,6],
                [1,2,5,4,6,7]]

# Use these to generate full datetimes (not used)
periods_dt = [[(7,50),(8,55)],
           [(9,00),(9,53)],
           [(9,58),(11,3)],
           [(11,8),(12,31)],
           [(12,36),(13,41)],
           [(13,46),(14,39)]]

# Use these since Google seems to want separate date and time strings
periods = [["7:50","8:55"],
           ["9:00","9:53"],
           ["9:58","11:03"],
           ["11:08","12:31"],
           ["12:36","13:41"],
           ["13:46","14:39"]]

datelist = [start + dt.timedelta(days=x) for x in range(0,(end-start).days)]

with open('schedule.csv', mode='w') as f:
    sched_writer = csv.writer(f, delimiter=',')
    sched_writer.writerow(['Subject','Start Date','Start Time','End Date', 'End Time'])
    for d in datelist:
        week = d.isocalendar()[1]
        dow = d.isocalendar()[2]

        if d in specials:
            continue

        if dow > 5:
            continue

        if week in blue_weeks:
            blocks = blue_blocks[dow - 1]
        elif week in white_weeks:
            blocks = white_blocks[dow - 1]
        else:
            continue

        for i in range(len(blocks)):
            period = periods[i]
            subject = block_names[blocks[i] - 1]
            sched_writer.writerow([subject, d, period[0], d, period[1]])

            #period_dt = periods_dt[i]
            #starttime = dt.datetime(d.year,d.month,d.day,period_dt[0][0],period_dt[0][1])
            #endtime = dt.datetime(d.year,d.month,d.day,period_dt[1][0],period_dt[1][1])
            #print(f"{starttime} - {endtime}: Block {blocks[i]}")
