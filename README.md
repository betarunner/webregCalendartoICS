# webregCalendartoICS
convert webreg Calendar to ics file.

before run:
install dependencies:
pip install icalendar
please change file path in line 248 and line 250
use by copy the calendar to clip board and run (Notice the course list is enclosed in "" mark where as the added argument for semester[winter, speing, etc.] is not)
sample:
python  generate_calendar_beta1.py "COGS 108  	Data Science in Practice	A00	LE	Ellis, Shannon Elizabeth	L	4.00	MWF	9:00a-9:50a	CTL	0125	Enrolled	
 		A05	LA		 	 	F	5:00p-5:50p	DIB	121	 	 
 	Final Exam	 	FI		 	 	W 03/20/2024	8:00a-10:59a	TBA	TBA	 	 
COGS 150  	Large Language Models/CogSci	A00	LE	Trott, Sean Thomas	L	4.00	MWF	3:00p-3:50p	DIB	121	Enrolled	
 		A01	LA		 	 	M	4:00p-4:50p	DIB	121	 	 
 	Final Exam	 	FI		 	 	W 03/20/2024	3:00p-5:59p	TBA	TBA	 	 
ENG 100L 	Design for Development Lab	H00	LA	Bratton, Maryann	L	2.00	W	12:00p-1:50p	CMRR	1H	Enrolled	
COGS 107B 	Systems Neuroscience	A00	LE	Mooshagian, Eric Frederick	L	4.00	TuTh	9:30a-10:50a	CTL	0125	Waitlist (7)	
 		A01	DI		 	 	W	4:00p-4:50p	CSB	005	 	 
 	Final Exam	 	FI		 	 	Tu 03/19/2024	8:00a-10:59a	TBA	TBA	 	 
COGS 118B 	Intro to Machine Learning	A00	LE	Fleischer, Jason G	L	4.00	MWF	2:00p-2:50p	PCYNH	109	Waitlist (3)	
 		A02	DI		 	 	F	10:00a-10:50a	CSB	115	 	 
 	Final Exam	 	FI		 	 	M 03/18/2024	3:00p-5:59p	TBA	TBA	 	 
COGS 101B 	Learning, Memory and Attention	A00	LE	Allen, Michael Gordon	L	4.00	MWF	1:00p-1:50p	CENTR	115	Planned	
 		A03	DI		 	 	W	2:00p-2:50p	PCYNH	121	 	 
 	Final Exam	 	FI		 	 	F 03/22/2024	11:30a-2:29p	TBA	TBA	 	 
JAPN  10B 	First Year Japanese II	F00	LE	Iwamoto, Naoki	L	5.00	TuTh	11:00a-12:20p	CENTR	218	Planned	
 		F02	TU		 	 	MWF	11:00a-11:50a	HSS	1138	 	 
 	Final Exam	 	FI		 	 	Th 03/21/2024	11:30a-2:29p	TBA	TBA	 	 " winter




currently the semester are set as following:

semester_dates = {
    'ss1': {'start': '07/03/23', 'end': '08/05/23'},
    'ss2': {'start': '08/07/23', 'end': '09/09/23'},
    'fall': {'start': '09/28/23', 'end': '12/16/23'},
    'winter': {'start': '01/08/24', 'end': '03/23/24'},
    'spring': {'start': '03/27/24', 'end': '06/16/24'}
}
