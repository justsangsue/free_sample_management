import gspread
from oauth2client.service_account import ServiceAccountCredentials

__author__ = "James Wang"

def access_gsheet():
	# Clarify APIs needed in this project
	scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

	# Credential files
	credentials = ServiceAccountCredentials.from_json_keyfile_name("Free Sample Management-c25f044c25be.json", scope)

	# Authorization
	return gspread.authorize(credentials)


# Data cleaning methods for free sample list
def format_date(date):
	""" 
	input: month/day/year
	return: MM/DD/YYYY
	"""
	if date.strip() == '':
		return ''

	if date.count('/') != 2:
		print("Invalid date format!")
		return ''

	month, day, year = date.split('/')[0], date.split('/')[1], date.split('/')[2]

	if len(month) != 2:
		month = '0' + month

	if len(day) != 2:
		day = '0' + day

	if len(year) == 2:
		year = "20" + year

	return month + '/' + day + '/' + year

def fill_row_values(row_values, length):
	# Fill row_values to length using ''
	if len(row_values) < length:
		need = length - len(row_values)
	for i in range(need):
		row_values.append('')

