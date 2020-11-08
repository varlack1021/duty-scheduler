import openpyxl
import calendar
import xlsxwriter

#list of cell fill in colors for different months
month_styles = {1: '0099ff', 2: '66c2ff', 3: '8cd98c', 4: '339933', 5: '00802b', 6: 'ffdd99',
				7: 'ffbb33', 8: 'ff9933', 9: 'e65c00', 10: 'cc0000', 11: '990000', 12: '0066cc'}

# Set the first day as Sunday
def create_excel_calendar(year, filename):
	calendar.setfirstweekday(firstweekday=6)

	workbook = xlsxwriter.Workbook('%s.xlsx' % (filename))

	# Traveling for 12 months

	for i in range(1, 13):
		# Add worksheets
		month_name = calendar.month_name[i]
		worksheet = workbook.add_worksheet(month_name)
		worksheet.set_column('A:H',20)
		worksheet.set_row(1, 20)
		worksheet.set_row(0, 55)
		worksheet.hide_gridlines(2)
		step = 0

		# Add cell styles
		date_format = workbook.add_format()
		day_format = workbook.add_format()
		title_format = workbook.add_format()
		gray_fill = workbook.add_format()

		gray_fill.set_bg_color('e6e6e6')
		gray_fill.set_align('left')
		
		#day number
		date_format.set_align('left')
		date_format.set_align('top')
		
		#day of the week
		day_format.set_font_name('Rockwell')
		day_format.set_font_size(11)
		day_format.set_bottom()
		day_format.set_align('vcenter')
		day_format.set_align('center')
		
		title_format.set_font_size(35)
		title_format.set_bg_color(month_styles[i])
		title_format.set_font_name('Rockwell')
		title_format.set_align('vcenter')

		# Get the exact date and time
		fill_in = False

		for j in range(len(calendar.monthcalendar(year, i))):
			

			worksheet.set_row(j + 3 + step, 45)

			for k in range(len(calendar.monthcalendar(year, i)[j])):

				value = calendar.monthcalendar(year, i)[j][k]
				
				if value != 0:
					worksheet.write(j + 2 + step, k, value, date_format)

					if fill_in:
						worksheet.write(j + 2 + step, k, value, gray_fill)
						worksheet.write(j + 3 + step, k, '', gray_fill)

			fill_in = True if not fill_in else False

			step += 1		

		# Add Weekly Information Line
		
		days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
		
		for k3 in range(7):

			worksheet.write(1, k3, days[k3], day_format)
			worksheet.write(0, k3, '', title_format)
		
		month_name = calendar.month_name[i]
		worksheet.write(0, 0, "{}  {}".format(month_name, year), title_format)
		
	# Save Documents
	workbook.close()