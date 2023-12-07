import argparse
import sys
import re
from datetime import datetime
from datetime import datetime, timedelta
from icalendar import Calendar, Event






def get_day_of_week(date):
    day_of_week = date.weekday() + 1  # Add 1 to align with Monday as 1
    return day_of_week


def create_event(course, start_date, end_date):
    event = Event()
    event.add('summary', course['code'])
    event.add('description', course['type'])
    event.add('location', course['location'])

    # Set constant start and end times
    #start_date = datetime.strptime('09/28/23', '%m/%d/%y')
    #end_date = datetime.strptime('12/16/23', '%m/%d/%y')

    ###print(end_date) debug purpose

    #if specific date specified then use it instead(this is for midterm and final)
    if course.get('specDate'):
        temp = course['specDate'].split(' ')[1]
        specDate = temp[0:6]+temp[8:10]
        ##print(specDate)  #for debug purpose
        start_date = datetime.strptime(specDate, '%m/%d/%y')


    
    # Parse start and end times
    time_range = re.search(r'(\d{1,2}:\d{2}[ap])-(\d{1,2}:\d{2}[ap])', course['time'])

    if time_range:
        start_time, end_time = time_range.groups()

        start_time+="m"
        end_time+="m"

  

        start_time = datetime.strptime(start_time, '%I:%M%p').time()
        end_time = datetime.strptime(end_time, '%I:%M%p').time()


        #class start differenly depending on the days of the week.
        diff = 0
        if course.get('diff'):
            diff = course['diff']
        


        event.add('dtstart', datetime.combine(start_date+timedelta(days= diff), start_time))
        event.add('dtend', datetime.combine(start_date+timedelta(days=diff), end_time))
    
    # Set recurrence rule if applicable
    if course.get('recurrence') and course ['recurrence']['days']!= None:
        rule = {
            'freq': 'weekly',
            'until': end_date,
            'byday': course['recurrence']['days']
        }
        event.add('rrule', rule)
    
    return event

def generate_ics(course_list):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//Apple Inc.//Mac OS X 10.15.6//EN')
    cal.add('calscale', 'GREGORIAN')
    
    for course in course_list:
        event = create_event(course,start_date,end_date)
        cal.add_component(event)
    
    return cal.to_ical()


#Main 

# Extract command-line arguments

parser = argparse.ArgumentParser()
parser.add_argument('course_data', type=str, help="Course data as a string")
parser.add_argument('semester', choices=['ss1', 'ss2', 'fall', 'winter', 'spring'], help="Semester (ss1, ss2, fall, winter, spring)")
args = parser.parse_args()

course_data = args.course_data.strip()
semester = args.semester

semester_dates = {
    'ss1': {'start': '07/01/24', 'end': '08/03/24'},
    'ss2': {'start': '08/05/24', 'end': '09/07/24'},
    'fall': {'start': '09/28/23', 'end': '12/16/23'},
    'winter': {'start': '01/08/24', 'end': '03/23/24'},
    'spring': {'start': '03/27/24', 'end': '06/16/24'}
}


course_list = []
course_matches = re.findall(r'([^\t\n]+)', course_data)
course_matches = [match for match in course_matches if match.strip() != '']

start_date = datetime.strptime(semester_dates[semester]['start'], '%m/%d/%y')
end_date = datetime.strptime(semester_dates[semester]['end'], '%m/%d/%y')
start_date_DOW = get_day_of_week(start_date)
##print("start date is integer:" +str(start_date_DOW))




i = 0
while i in range(len(course_matches)):
    ##print(course_matches[i]) #debug
    courseCode = course_matches[i]
    #for lec
    course_info = {
        'code': courseCode,
        'type': course_matches[i+3],
        'location': course_matches[i+9]+course_matches[i+10],
        'time': course_matches[i+8]
    }

    course_info['recurrence'] = {
        'days': None,  # Placeholder for the 'days' value
    }
    
    if course_matches[i+7] == "MWF":
        course_info['recurrence']['days'] = ["MO", "WE", "FR"]
        
        a = course_info['diff']  = (1-start_date_DOW) %7
        b = course_info['diff']  = (3-start_date_DOW) %7
        c = course_info['diff']  = (5-start_date_DOW) %7
        course_info['diff']  = min(a,b,c)
        #print("MWF detect diff is: "+ str(course_info['diff']))

    elif course_matches[i+7] == "TuTh":
        
        course_info['recurrence']['days'] = ["TU", "TH"]
        a = course_info['diff']  = (2-start_date_DOW) %7
        b = course_info['diff']  = (4-start_date_DOW) %7
        course_info['diff']  = min(a,b)
        #print("TuTh detect diff is: "+ str(course_info['diff']))

    elif course_matches[i+7] == "MTuWTh":
        
        course_info['recurrence']['days'] = ["MO", "TU", "WE", "TH"]
        a = course_info['diff']  = (1-start_date_DOW) %7
        b = course_info['diff']  = (3-start_date_DOW) %7
        c = course_info['diff']  = (2-start_date_DOW) %7
        d = course_info['diff']  = (4-start_date_DOW) %7
        course_info['diff']  = min(a,b,c,d)
        #print("MTUWTH detect diff is: "+ str(course_info['diff']))
    course_list.append(course_info)



    if not (course_matches[i + 12] == "Midterm" or course_matches[i + 12] == "Final Exam"):

        #for di or st
        course_info2 = {
        'code': courseCode,
        'type': course_matches[i+13]+course_matches[i+12],
        'location': course_matches[i+17] + course_matches[i+16],
        'time': course_matches[i+15]
        }


        course_info2['recurrence'] = {
            'days': None,  # Placeholder for the 'days' value
        }
        ##print(course_matches[i+14])
        if course_matches[i+14] == "M":
            course_info2['recurrence']['days'] = ["MO"]
            course_info2['diff']  = (1-start_date_DOW) %7
        elif course_matches[i+14] == "Tu":
            course_info2['recurrence']['days'] = ["TU"]
            course_info2['diff']  = (2-start_date_DOW) %7
        elif course_matches[i+14] == "W":
            course_info2['recurrence']['days'] = ["WE"]
            course_info2['diff']  = (3-start_date_DOW) %7
        elif course_matches[i+14] == "Th":
            course_info2['recurrence']['days'] = ["TH"]
            course_info2['diff']  = (4-start_date_DOW) %7
        elif course_matches[i+14] == "F":
            course_info2['recurrence']['days'] = ["FR"]
            course_info2['diff']  = (5-start_date_DOW) %7
        elif course_matches[i+14] == "Sa":
            course_info2['recurrence']['days'] = ["SA"]
            course_info2['diff']  = (6-start_date_DOW) %7
        elif course_matches[i+14] == "Su":
            course_info2['recurrence']['days'] = ["SU"]
            course_info2['diff']  = (7-start_date_DOW) %7
        elif course_matches[i+14] == "MWF":
            course_info2['recurrence']['days'] = ["MO", "WE", "FR"]
            a = course_info2['diff']  = (1-start_date_DOW) %7
            b = course_info2['diff']  = (3-start_date_DOW) %7
            c = course_info2['diff']  = (5-start_date_DOW) %7
            course_info2['diff']  = min(a,b,c)
        elif course_matches[i+14] == "TuTh":
            course_info2['recurrence']['days'] = ["TU", "TH"]
            a = course_info2['diff']  = (2-start_date_DOW) %7
            b = course_info2['diff']  = (4-start_date_DOW) %7
            course_info2['diff']  = min(a,b)

        course_list.append(course_info2)
        i+=6

    #for midterm and final
    i += 12
    while i < len(course_matches) and (course_matches[i] == "Midterm" or course_matches[i] == "Final Exam"):
        # Perform operations for the "midterm" equivalent
        # ...
        course_info3 = {

        'code': courseCode+course_matches[i],
        'type': course_matches[i]+course_matches[i+1],
        'location': course_matches[i+4] + course_matches[i+5],
        'time': course_matches[i+3],
        'specDate': course_matches[i+2]
        }


        course_list.append(course_info3)
        i += 6  # Skip to the next relevant position

    # Continue with the rest of the code outside the loop
    # ...




    
# Generate the iCalendar file
ics_data = generate_ics(course_list)


# Write the iCalendar data to a file on the desktop
output_file_path = "/Users/primepi/Desktop/course_schedule.ics"
# Write the iCalendar data to a file
with open('/Users/primepi/Desktop/course_schedule.ics', 'wb') as f:
    f.write(ics_data)

