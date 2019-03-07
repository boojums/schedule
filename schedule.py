# Generate a csv schedule for importing into Google Calendar
import datetime as dt
import csv

# Customize start and end dates
start = dt.date(2019,3,4)
end = dt.date(2019,6,13)

# Default block names
block_names = ['Block 1', 'Block 2', 'Block 3', 'Block 4',
               'Block 5', 'Block 6', 'Block 7']

# Customize what to call each block ("Subject" in a GCal item)
# and set the days it meets (Monday=1)
block_info = [None,
              {'name': 'Game Prog (2)', 'blue': [2,3,5], 'white': [1,3], 'lunch':'early'},
              None,
              {'name': 'Intro (4)', 'blue': [2,4], 'white': [1,2,4], 'lunch':'early'},
              {'name': 'Intro (5)', 'blue': [3,5], 'white': [2,3,5], 'lunch':'early'},
              None, None]

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

        # days with no classes
        if d in specials:
            continue

        # weekend
        if dow > 5:
            continue

        if week in blue_weeks:
            blocks = blue_blocks[dow - 1]
            color = 'blue'
        elif week in white_weeks:
            blocks = white_blocks[dow - 1]
            color = 'white'
        else:
            continue

        for i in range(len(blocks)):
            period = periods[i]
            info = block_info[blocks[i] - 1]
            if not info:
                continue
            if dow not in info[color]:
                continue

            start = period[0]
            end = period[1]

            if i == 3 and info['lunch'] == 'early':
                start = "11:08"
                end = "12:01"
            elif i==3 and info['lunch'] == 'late':
                start = "11:38"
                end = "12:31"
                
            sched_writer.writerow([info['name'], d, start, d, end])
