from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from pathlib import Path
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import calendar
import datetime as dt
from pprint import pprint
from collections import OrderedDict


class WordTable():

	def __init__(self, duty_dates, total_days):
		self.duty_dates = OrderedDict(zip(list(map(self.convert_dates_to_text, duty_dates.keys())), duty_dates.values()))
		self.total_days = total_days
		
	def convert_dates_to_text(self, date_string):
		shift_start, shift_end = list(map(lambda x : dt.datetime.strptime(x, '%Y-%m-%d'), date_string.split(' - ')))
		shift_start_text = "{} {}".format(calendar.month_name[shift_start.month], shift_start.day)
		shift_end_text = "{} {}".format(calendar.month_name[shift_end.month], shift_end.day)
		text = "{} - {}".format(shift_start_text, shift_end_text)
		
		return text
		
        
	
	def write_to_table(self):

		path = Path('backend/word_files/test.docx')
		print(path.resolve)
		document = Document()

		styles = document.styles
		table = document.add_table(rows = 15, cols = 5)
		table.style = styles['Table Grid']

		header_cells = table.rows[0].cells
		headers = ['Week', 'Dates', 'RD', 'Management', 'Central Office']

		#Fill Header
		for i in range(5):
			text = headers[i]
			p = table.rows[0].cells[i].add_paragraph(text + "\n")
			p.alignment = WD_ALIGN_PARAGRAPH.CENTER
			
			#black_fill = parse_xml(r'<w:shd {} w:fill="000000"/>'.format(nsdecls('w')))
			
			#table.rows[0].cells[i]._tc.get_or_add_tcPr().append(black_fill)
		
		for i in range(len(self.duty_dates.items())):
			date_info = list(self.duty_dates.items())[i]
			row_info = ["Week %s" % (i + 1), date_info[0], date_info[1]]
			
			for j in range(len(row_info)):
				p = table.rows[i + 1].cells[j].add_paragraph(row_info[j])
				p.alignment = WD_ALIGN_PARAGRAPH.CENTER
		
		print(os.path.realpath(__file__))
		document.save(path)
		os.startfile(path) 
		'''
		shading_elm_2 = parse_xml(r'<w:shd {} w:fill="1F5C8B"/>'.format(nsdecls('w')))
		#hdr_cells[0]._tc.get_or_add_tcPr().append(shading_elm_2)
		#hdr_cells[1]._tc.get_or_add_tcPr().append(shading_elm_2)
		#hdr_cells[0].text = 'ID'
		#p = hdr_cells[1].add_paragraph('Quantity')

		#	p.alignment=WD_ALIGN_PARAGRAPH.CENTER


		for i in range(1, 10):
			row_cells = table.rows[i].cells
			row_cells[0].text = ""
			row_cells[1].text = "She"
			row_cells[2].text = "Cutie"

		row_cells = table.rows[4].cells

		row_cells[0].merge(row_cells[1])

		


		print(path)

		print(os.path.exists(path))
		'''
		
