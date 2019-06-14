from utilities import *
from websites import *
from time import sleep
from gspread_formatting import *

__author__ = "James Wang"

wks_add_new = access_gsheet().open("Free Sample").worksheet("Add New")
wks_main_table = access_gsheet().open("Free Sample").worksheet("Free Sample")

add_new_columns = {"name" : 0, 
				   "requester" : 1,
				   "company" : 2,
				   "catalog no" : 3,
				   "request_date" : 4,
				   "pgp" : 5,
				   "bcrp" : 6,
				   "mrp1" : 7,
				   "mrp7" : 8,
				   "note" : 9}

main_columns = {"name" : 0, 
			    "synonym" : 1,
			    "catalog no" : 2,
			    "requester" : 3,
			    "cas no" : 4,
			    "description" : 5,
			    "company" : 6,
			    "date" : 7,
			    "link" : 8,
			    "pgp" : 9,
			    "bcrp" : 10,
			    "mrp1" : 11,
			    "mrp7" : 12,
			    "note" : 13}

# R, G, B: [0-1], [0-1], [0-1]
# red = color(1, 0, 0)
# magenta = color(1, 0, 1)
# cyan = color(0, 1, 1)
# green = color(0, 1, 0)
# blue = color(0, 0, 1)
# gray = color(0.8, 0.8, 0.8)
# white = color(1, 1, 1)

# Number of rows in main table
all_rows_num = len(wks_main_table.col_values(1))

# All existed CAS No.
all_cas_no = wks_main_table.col_values(5)

# Start from 4th row
add_new_row_num = 4
add_new_row_values = wks_add_new.row_values(add_new_row_num)
fill_row_values(add_new_row_values, 10)

cells = []

# Read all rows, stop when reach the last row
while(len([ele for ele in add_new_row_values if ele != '']) != 0):
	# Drug name as keyword
	keyword = add_new_row_values[add_new_columns.get("name")]

	# If no company name provided, move to next row and change cell color to gray
	try:
		company = add_new_row_values[add_new_columns.get("company")]
	except IndexError:
		print("No company name!")
		add_new_row_num += 1
		add_new_row_values = wks_add_new.row_values(add_new_row_num)
		fill_row_values(add_new_row_values, 10)
		continue

	# Get information from add_new
	new_requester = add_new_row_values[add_new_columns.get("requester")]
	new_catalog_no = add_new_row_values[add_new_columns.get("catalog no")]
	new_date = add_new_row_values[add_new_columns.get("request_date")]
	new_pgp = add_new_row_values[add_new_columns.get("pgp")]
	new_bcrp = add_new_row_values[add_new_columns.get("bcrp")]
	new_mrp1 = add_new_row_values[add_new_columns.get("mrp1")]
	new_mrp7 = add_new_row_values[add_new_columns.get("mrp7")]
	new_note = add_new_row_values[add_new_columns.get("note")]

	# If request date not given, move to next row
	if new_date == '':
		print(keyword + " doesn't have request date!")
		add_new_row_num += 1
		add_new_row_values = wks_add_new.row_values(add_new_row_num)
		fill_row_values(add_new_row_values, 10)
		continue

	# Blank rows for main table, to avoid IndexError
	values = []
	fill_row_values(values, 14)

	company_obj = MCE()
	company_obj.fill_info(keyword)
	if len(company_obj.get_cas_no()) == 0:
		company_obj = SelleckChem()
		company_obj.fill_info(keyword)
	if len(company_obj.get_cas_no()) == 0:
		campany_obj = ChemieTek()
		company_obj.fill_info(keyword)
	if len(company_obj.get_cas_no()) == 0:
		format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':', cellFormat(backgroundColor=color(0.8, 0.8, 0.8)))
		continue

	# Update new row in main table using keyword and information from company website
	# Keep the information of catalog no, requester, campany, link using companies in "add_new"
	# For other information, search by the order: MCE, SelleckChem, ChemieTek
	# If the drug is not found on the website of previous company, then try the next one
	# This is to avoid repeat in names, as different companies may have different names for the same drug
	# Drug link keeps the original one
	values[main_columns.get("name")] = company_obj.get_name()
	values[main_columns.get("synonym")] = company_obj.get_synonym()
	values[main_columns.get("catalog no")] = new_catalog_no
	values[main_columns.get("requester")] = new_requester
	values[main_columns.get("cas no")] = company_obj.get_cas_no()
	values[main_columns.get("description")] = company_obj.get_description()
	values[main_columns.get("company")] = company
	values[main_columns.get("date")] = new_date
	values[main_columns.get("pgp")] = new_pgp
	values[main_columns.get("bcrp")] = new_bcrp
	values[main_columns.get("mrp1")] = new_mrp1
	values[main_columns.get("mrp7")] = new_mrp7
	values[main_columns.get("note")] = new_note

	new_company = add_new_row_values[add_new_columns.get("company")]
	if new_company:
		obj_for_link = None
		if new_company.lower() == "selleckchem":
			obj_for_link = SelleckChem()
			obj_for_link.fill_info(keyword)
		elif new_company.lower() == "chemietek":
			obj_for_link = ChemieTek()
			obj_for_link.fill_info(keyword)
		elif new_company.lower() == "mce":
			obj_for_link = MCE()
			obj_for_link.fill_info(keyword)
		values[main_columns.get("link")] = obj_for_link.get_link()


	# Update row
	if values[main_columns.get("cas no")] in all_cas_no:
		# Repeat compound
		format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':J'+str(add_new_row_num), cellFormat(backgroundColor=color(1, 0, 0)))
		print(values[main_columns.get("name")] + " duplicated!")
		add_new_row_num += 1
		add_new_row_values = wks_add_new.row_values(add_new_row_num)
		fill_row_values(add_new_row_values, 10)
		continue

	col_num = 1
	for value in values:
		cells.append(gspread.Cell(all_rows_num + 1, col_num, value))
		col_num += 1

	if cells[0].value != '':
		wks_main_table.update_cells(cells)
	else:
		print("Empty new row!")

	print("Updated row No. " + str(all_rows_num + 1) + "\n")
	print(values)
	sleep(1)

	"""
	# Remove infomation from "Add New" after update
	col_num = 1
	empty_cells = []
	for value in values:
		empty_cells.append(gspread.Cell(add_new_row_num, col_num, ''))
		col_num += 1
		wks_add_new.update_cells(empty_cells)
	"""
	all_rows_num += 1
	add_new_row_num += 1
	add_new_row_values = wks_add_new.row_values(add_new_row_num)
	fill_row_values(add_new_row_values, 10)



















