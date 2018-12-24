import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("Free Sample Management-c25f044c25be.json", scope)
gc = gspread.authorize(credentials)

wks = gc.open("Free Sample").sheet1

# CAS No.
cas_values = wks.col_values(5)

all_cas = set()
for value in cas_values:
	if value != '':
		if (value not in all_cas):
			all_cas.add(value)
		else:
			print("Found duplicate! CAS: %s" %value)
