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
				   "request_date" : 3,
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

all_rows_num = len(wks_main_table.col_values(1))
all_cas_no = wks_main_table.col_values(5)

add_new_row_num = 5
add_new_row_values = wks_add_new.row_values(add_new_row_num)
fill_row_values(add_new_row_values, 10)

cells = []

while(len([ele for ele in add_new_row_values if ele != '']) != 0):

	keyword = add_new_row_values[add_new_columns.get("name")]
	try:
		company = add_new_row_values[add_new_columns.get("company")]
	except IndexError:
		print("No company name!")
		add_new_row_num += 1
		add_new_row_values = wks_add_new.row_values(add_new_row_num)
		fill_row_values(add_new_row_values, 10)

		# Change cell background color
		format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':', cellFormat(backgroundColor=color(0.8, 0.8, 0.8)))
		continue

	new_requester = add_new_row_values[add_new_columns.get("requester")]
	new_date = add_new_row_values[add_new_columns.get("request_date")]
	new_pgp = add_new_row_values[add_new_columns.get("pgp")]
	new_bcrp = add_new_row_values[add_new_columns.get("bcrp")]
	new_mrp1 = add_new_row_values[add_new_columns.get("mrp1")]
	new_mrp7 = add_new_row_values[add_new_columns.get("mrp7")]
	new_note = add_new_row_values[add_new_columns.get("note")]

	if new_date == '':
		print(keyword + " doesn't have request date!")
		add_new_row_num += 1
		add_new_row_values = wks_add_new.row_values(add_new_row_num)
		fill_row_values(add_new_row_values, 10)
		continue

	values = []
	fill_row_values(values, 14)

	if company == "ChemieTek":
		new_CT = ChemieTek()
		new_CT.fill_info(keyword)
		values[main_columns.get("name")] = new_CT.get_name()
		values[main_columns.get("synonym")] = new_CT.get_synonym()
		values[main_columns.get("catalog no")] = new_CT.get_catalog_no()
		values[main_columns.get("requester")] = new_requester
		values[main_columns.get("cas no")] = new_CT.get_cas_no()
		values[main_columns.get("description")] = new_CT.get_description()
		values[main_columns.get("company")] = company
		values[main_columns.get("date")] = new_date
		values[main_columns.get("link")] = new_CT.get_link()
		values[main_columns.get("pgp")] = new_pgp
		values[main_columns.get("bcrp")] = new_bcrp
		values[main_columns.get("mrp1")] = new_mrp1
		values[main_columns.get("mrp7")] = new_mrp7
		values[main_columns.get("note")] = new_note

		# Update row
		if new_CT.get_cas_no() in all_cas_no:
			# Repeat compound
			format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':J'+str(add_new_row_num), cellFormat(backgroundColor=color(1, 0, 0)))
			print(new_CT.get_name() + " duplicated!")
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

		print("Updated row No. " + str(all_rows_num) + "\n")
		new_CT.print_compound()
		sleep(1)

	if company == "SelleckChem":
		new_SC = SelleckChem()
		new_SC.fill_info(keyword)
		values[main_columns.get("name")] = new_SC.get_name()
		values[main_columns.get("synonym")] = new_SC.get_synonym()
		values[main_columns.get("catalog no")] = new_SC.get_catalog_no()
		values[main_columns.get("requester")] = new_requester
		values[main_columns.get("cas no")] = new_SC.get_cas_no()
		values[main_columns.get("description")] = new_SC.get_description()
		values[main_columns.get("company")] = company
		values[main_columns.get("date")] = new_date
		values[main_columns.get("link")] = new_SC.get_link()
		values[main_columns.get("pgp")] = new_pgp
		values[main_columns.get("bcrp")] = new_bcrp
		values[main_columns.get("mrp1")] = new_mrp1
		values[main_columns.get("mrp7")] = new_mrp7
		values[main_columns.get("note")] = new_note
		# Update row
		if new_SC.get_cas_no() in all_cas_no:
			# Repeat compound
			format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':J'+str(add_new_row_num), cellFormat(backgroundColor=color(1, 0, 0)))
			print(new_SC.get_name() + " duplicated!")
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

		print("Updated row No. " + str(all_rows_num) + "\n")
		new_SC.print_compound()
		sleep(1)

	if company == "MCE":
		new_MCE = MCE()
		new_MCE.fill_info(keyword)
		values[main_columns.get("name")] = new_MCE.get_name()
		values[main_columns.get("synonym")] = new_MCE.get_synonym()
		values[main_columns.get("catalog no")] = new_MCE.get_catalog_no()
		values[main_columns.get("requester")] = new_requester
		values[main_columns.get("cas no")] = new_MCE.get_cas_no()
		values[main_columns.get("description")] = new_MCE.get_description()
		values[main_columns.get("company")] = company
		values[main_columns.get("date")] = new_date
		values[main_columns.get("link")] = new_MCE.get_link()
		values[main_columns.get("pgp")] = new_pgp
		values[main_columns.get("bcrp")] = new_bcrp
		values[main_columns.get("mrp1")] = new_mrp1
		values[main_columns.get("mrp7")] = new_mrp7
		values[main_columns.get("note")] = new_note
		# Update row
		if new_MCE.get_cas_no() in all_cas_no:
			# Repeat compound
			format_cell_range(wks_add_new, 'A'+str(add_new_row_num)+':J'+str(add_new_row_num), cellFormat(backgroundColor=color(1, 0, 0)))
			print(new_MCE.get_name() + " duplicated!")
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

		print("Updated row No. " + str(all_rows_num) + "\n")
		new_MCE.print_compound()
		sleep(1)

	# Remove infomation from "Add New" after update
	col_num = 1
	empty_cells = []
	for value in values:
		empty_cells.append(gspread.Cell(add_new_row_num, col_num, ''))
		col_num += 1
		wks_add_new.update_cells(empty_cells)

	all_rows_num += 1
	add_new_row_num += 1
	add_new_row_values = wks_add_new.row_values(add_new_row_num)
	fill_row_values(add_new_row_values, 10)



















