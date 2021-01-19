from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

start_date = '//*[@id="root"]/div/div/form/div[2]/div[1]/input'
end_date = '//*[@id="root"]/div/div/form/div[2]/div[2]/div/input'
hall_name = '//*[@id="root"]/div/div/form/div[3]/div[1]/input'

name = '//*[@id="root"]/div/div/form/div[{}]/div[1]/input'
add_staff = '//*[@id="root"]/div/div/form/div[{}]/div[2]/div/button'


class TestBot():

	def __init__(self, url, formData):
		options = Options()
		options.add_argument('--headless')
		d_path = 'chromedriver_win32/chromedriver.exe'
		self.driver = webdriver.Chrome(d_path, options=options)
		self.url = url
		self.formData = formData


	def fill_out_ra_form(self):
		d = self.driver
		d.get(self.url)
		d.find_element_by_xpath(start_date).send_keys('01152021')
		d.find_element_by_xpath(end_date).send_keys('05142021')
		d.find_element_by_xpath(hall_name).send_keys('RA Test')
		div_num = 4

		for i, person in enumerate(formData['staffData']):
			path = name.format(div_num) 
			div_num += 3

			d.find_element_by_xpath(path).send_keys(person['name'])

			if i == len(formData['staffData']) - 1:
				break
			
			d.find_element_by_xpath(add_staff.format(div_num)).click()

		d.find_element_by_class_name('btn.btn-primary').click()
	
	def fill_out_rd_form(self):
		pass

	def check_file_downloaded(self):
		path = Path('C:/Users/Varla/Downloads')
		filename = 'RA Test Duty Calendar.xlsx' if True else 'RD Test Duty Calendar.docx'
		path = path / filename

		if path.exists():
			print(True)
			path.unlink()
		else:
			print(False)
	
	def start(self):
		d = self.driver
		self.fill_out_ra_form()
		self.check_file_downloaded()
		d.close()

url = 'http://www.npautoscheduler.com/'
formData = {
	'startDate': '01152021',
	'endDate': '05142021', 
	'staffData': [
	{'name': 'test1', 'prefDayOff': ['01152021']},
	{'name': 'test2', 'prefDayOff': ['01152021']},
	{'name': 'test3', 'prefDayOff': ['01152021']},
	{'name': 'test4', 'prefDayOff': ['01152021']},
	{'name': 'test5', 'prefDayOff': ['01152021']}

	]

}
test_bot = TestBot(url, formData)
test_bot.start()