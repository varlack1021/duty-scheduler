import time
from pathlib import Path
from datetime import datetime, date

def record_time_spent():
	start =  time.time()

	file = open('timespent.txt')
	total_time = float(file.read())
	
	file = open('timespent.txt', 'w+')
	
	total_time += time.time() - start
	file.write(str(total_time))

def remove_excel_files_from_downloads():
	path = Path('C:/Users/Varla/Downloads')
	todays_date = date.today()
	
	for file in path.iterdir():
		
		if file.suffix == '.xlsx':
			if 'Duty' in file:
				file.unlink()

while True:
	record_time_spent()
	remove_excel_files_from_downloads()
	
	
