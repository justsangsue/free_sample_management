from utilities import *
from websites import *
from time import sleep

wks = access_gsheet().open("Free Sample").sheet1

#print(wks.get_all_records())
#wks.append_row([''])
#wks.delete_row(2)
#cell = wks.acell("E2").value

"""
# Format date
date_cell_list = wks.range("E2:E270")

for date_cell in date_cell_list:
	date_cell.value = format_date(date_cell.value)

wks.update_cells(date_cell_list)
"""

# Update synonym, CAS No., description and link

column_content = {"name" : 0, 
				  "synonym" : 1,
				  "catalog no" : 2,
				  "requester" : 3,
				  "cas no" : 4,
				  "description" : 5,
				  "company" : 6,
				  "date" : 7,
				  "link" : 8}

row_num = 4
row_values = wks.row_values(row_num)
if len(row_values) < 9:
	need = 9 - len(row_values)
	for i in range(need):
		row_values.append('')

#print(row_values)
# row_values is a list of values only
while(len([ele for ele in row_values if ele != '']) != 0):
	keyword = row_values[column_content.get("name")]
	try:
		company = row_values[column_content.get("company")]
	except IndexError:
		print("No company name!")
		row_num += 1
		row_values = wks.row_values(row_num)
		continue
	cas = row_values[column_content["cas no"]]
	if len(cas) > 2:
		print("Row %s has been updated, CAS No. is %s." %(str(row_num), cas))
		row_num += 1
		row_values = wks.row_values(row_num)
		sleep(1)
		continue

	if len(row_values) < 9:
		need = 9 - len(row_values)
		for i in range(need):
			row_values.append('')

	if company == "ChemieTek":
		new_CT = ChemieTek()
		new_CT.fill_info(keyword)
		row_values[column_content.get("name")] = new_CT.get_name()
		row_values[column_content.get("synonym")] = new_CT.get_synonym()
		row_values[column_content.get("catalog no")] = new_CT.get_catalog_no()
		row_values[column_content.get("cas no")] = new_CT.get_cas_no()
		row_values[column_content.get("description")] = new_CT.get_description()
		row_values[column_content.get("link")] = new_CT.get_link()

		# Update row
		cells = []
		col_num = 1
		for value in row_values:
			cells.append(gspread.Cell(row_num, col_num, value))
			col_num += 1

		if cells[0].value != '':
			wks.update_cells(cells)
		else:
			print("Empty new row!")

		print("Updated No. " + str(row_num-1) + "\n")
		new_CT.print_compound()
		sleep(1)

	if company == "SelleckChem":
		new_SC = SelleckChem()
		new_SC.fill_info(keyword)
		row_values[column_content.get("name")] = new_SC.get_name()
		row_values[column_content.get("synonym")] = new_SC.get_synonym()
		row_values[column_content.get("catalog no")] = new_SC.get_catalog_no()
		row_values[column_content.get("cas no")] = new_SC.get_cas_no()
		row_values[column_content.get("description")] = new_SC.get_description()
		row_values[column_content.get("link")] = new_SC.get_link()
		# Update row
		cells = []
		col_num = 1
		for value in row_values:
			cells.append(gspread.Cell(row_num, col_num, value))
			col_num += 1

		if cells[0].value != '':
			wks.update_cells(cells)
		else:
			print("Empty new row!")

		print("Updated No. " + str(row_num-1) + "\n")
		new_SC.print_compound()
		sleep(1)

	if company == "MCE":
		new_MCE = MCE()
		new_MCE.fill_info(keyword)
		row_values[column_content.get("name")] = new_MCE.get_name()
		row_values[column_content.get("synonym")] = new_MCE.get_synonym()
		row_values[column_content.get("catalog no")] = new_MCE.get_catalog_no()
		row_values[column_content.get("cas no")] = new_MCE.get_cas_no()
		row_values[column_content.get("description")] = new_MCE.get_description()
		row_values[column_content.get("link")] = new_MCE.get_link()
		# Update row
		cells = []
		col_num = 1
		for value in row_values:
			cells.append(gspread.Cell(row_num, col_num, value))
			col_num += 1

		if cells[0].value != '':
			wks.update_cells(cells)
		else:
			print("Empty new row!")

		print("Updated No. " + str(row_num-1) + "\n")
		new_MCE.print_compound()
		sleep(1)

	row_num += 1
	row_values = wks.row_values(row_num)
