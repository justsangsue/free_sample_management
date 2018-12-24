# Website classes
from bs4 import BeautifulSoup
import requests
import sys
import re

class Compound(object):
	def __init__(self):
		self.cas_no = ''
		self.name = ''
		self.synonym = ''
		self.description = ''
		self.link = ''
		self.catalog_no = ''

	def print_compound(self):
		print("Name: %s\nSynonym: %s\nCAS No.: %s\nCatalog No.: %s\nDescription: %s\nLink: %s\n"\
		%(self.name, self.synonym, self.cas_no, self.catalog_no, self.description, self.link))

	def get_cas_no(self):
		return self.cas_no

	def get_name(self):
		return self.name

	def get_synonym(self):
		return self.synonym

	def get_description(self):
		return self.description

	def get_link(self):
		return self.link

	def get_catalog_no(self):
		return self.catalog_no

class ChemieTek(Compound):
	def __init__(self):
		Compound.__init__(self)

	def get_product_link(self, keyword):
		# Search the keyword and get the url for search results
		# Then catch product link
		keyword = keyword.lower()
		search_result = "http://www.chemietek.com/advancedsearchresult.aspx?type=any&categoryids=168+170+171+185+193+194+195+204+205+208+217+222+223+237+240+244+253+254+257+261+31+32+33+38+39+43+46+47+50+52+53+55+56+58+59+62+63+64+74+77+78+79+80+82+85+88+92+97+98+99+100+101+102+103+104+106+113+115+120+121+154+172+173+174+175+179+181+183+189+198+201+203+207+211+214+216+219+220+226+234+235+238+245+260+61+40+41+42+84+65+93+110+112+118+163+164+167+177+178+180+182+215+218+231+236+239+255+259+51+44+45+54+60+67+68+83+196+202+230+242+262+263+264+30+35+57+69+70+72+34+109+48+49+90+96+105+155+75+187+188+233+76+116+117+81+36+37+107+186+210+213+224+225+227+86+87+91+66+71+73+114+153+190+29+191+192+197+206+209+212+221+241+94+122+184+95+111+89+108+119+152+161+159+160+162+258+166+200+229+243+247+248+249+250+251+252+&keyword="+keyword+"&price1=&price2=&contentmenuitemids=&departmentids=&manufacturerid=&searchtype=&quick=true&isnewsearch=false"
		page = requests.get(search_result)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch search result!")
			return

		soup = BeautifulSoup(page.content, "html.parser")
		#print("class=\"ProductLink\"" in soup.prettify())
		try:
			result = soup('a', class_="ProductLink")[0].get("href")
		except IndexError:
			return ''
		return "http://www.chemietek.com/" + result

	
	def fill_info(self, keyword):
		# Fill all inforamtion
		product_link = self.get_product_link(keyword)
		if product_link == '' or product_link == None:
			print("Compound not found!")
			self.name = keyword
			return
		# Get link
		self.link = product_link
		page = requests.get(product_link)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch product website!")
			return

		soup = BeautifulSoup(page.content, "html.parser")

		# Get description
		result = soup.find("div", class_="ProductQuickInfoShortDescription")
		self.description = result.get_text().strip()

		# Get name
		result = soup.find("div", class_="ProductQuickInfoName")
		name_raw = result.get_text().strip()
		syn = []
		if '(' in name_raw and len(name_raw[name_raw.find('(') + 1 : name_raw.find(')')]) != 1:
			name_cleaned = name_raw[:name_raw.find('(')].strip()
			syn = name_raw[name_raw.find('(') + 1 : name_raw.find(')')].split(',')
		else:
			name_cleaned = name_raw
		self.name = name_cleaned

		# Get synonym, cas number and catalog number
		result = soup.find("div", class_="pdetail-sec-three columns")
		tags = [tag for tag in result.find_all("td")]
		for i in range(len(tags)):
			if tags[i].contents[0].strip() == "Catalog NO:":
				self.catalog_no = tags[i+1].get_text().strip()
				#print(self.catalog_no)
			if tags[i].contents[0].strip() == "Synonym:":
				self.synonym = ','.join(set(tags[i+1].get_text().strip().split(',') + syn)).strip()

			if tags[i].contents[0].strip() == "CAS NO:":
				self.cas_no = tags[i+1].get_text().strip() 


class SelleckChem(Compound):
	def __init__(self):
		Compound.__init__(self)

	def get_product_link(self, keyword):
		search_result = "https://www.selleckchem.com/search.html?searchDTO.searchParam=" + keyword
		page = requests.get(search_result)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch search result!")
			return ''

		soup = BeautifulSoup(page.content, "html.parser")
		result = soup.find("table", class_="data_sheet_noframe")
		try:
			tag = result.find('a')
		except AttributeError:
			return ''
		return "http://www.selleckchem.com" + tag.get("href")

	def fill_info(self, keyword):
		# Fill all information
		product_link = self.get_product_link(keyword)
		if product_link == '' or product_link == None:
			print("Compound not found!")
			self.name = keyword
			return
		# Get link
		self.link = product_link
		page = requests.get(product_link)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch product website!")
			return

		soup = BeautifulSoup(page.content, "html.parser")

		# Get name
		result = soup.find("h1", class_="fl")
		name_raw = result.get_text().strip()
		name_cleaned = name_raw
		syn = []
		if '(' in name_raw and len(name_raw[name_raw.find('(') + 1 : name_raw.find(')')]) != 1:
			name_cleaned = name_raw[:name_raw.find('(')].strip()
			syn = name_raw[name_raw.find('(') + 1 : name_raw.find(')')].split(',')
		self.name = name_cleaned

		# Get description
		result = soup.find('p', class_="clear mt5")
		self.description = result.get_text().strip()

		# Get synonym, cas number and catalog number
		result = soup.find('p', class_="fl mlmt25")
		self.catalog_no = ''.join(re.findall("Catalog No\.(.*)", result.get_text()))

		result = soup.find("span", class_="mlmt25")
		synonym = []
		if result:
			synonym = ''.join(re.findall("Synonyms\:(.*)", result.get_text())).strip().split(',') + syn
		self.synonym = ', '.join(set(synonym)).strip()

		tags = soup.find_all("td")
		for tag in tags:
			if len(tag.contents) > 0 and re.match("[0-9]+\-[0-9]+\-[0-9]", tag.get_text()):
				self.cas_no = tag.contents[0].strip()


class MCE(Compound):
	def __init__(self):
		Compound.__init__(self)

	def get_product_link(self, keyword):
		search_result = "https://www.medchemexpress.com/search.html?q=" + keyword + "&ft=&fa=&fp="
		page = requests.get(search_result)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch search result!")
			return

		soup = BeautifulSoup(page.content, "html.parser")
		result = soup.find("dt", class_="s_pro_list_cat")
		try:
			tag = result.find('a')
		except AttributeError:
			return ''
		return "https://www.medchemexpress.com/" + tag.get("href")

	def fill_info(self, keyword):
		# Fill all information
		product_link = self.get_product_link(keyword)
		if product_link == '' or product_link == None:
			print("Compound not found!")
			self.name = keyword
			return
		# Get link
		self.link = product_link
		page = requests.get(product_link)
		if page.status_code != 200:
			print(keyword + ": Fail to fetch product website!")
			return

		soup = BeautifulSoup(page.content, "html.parser")

		# Get name
		result = soup.find("h1", itemprop="name")
		name_raw = result.get_text().strip()
		name_cleaned = name_raw
		syn = []
		if '(' in name_raw and len(name_raw[name_raw.find('(') + 1 : name_raw.find(')')]) != 1:
			name_cleaned = name_raw[:name_raw.find('(')].strip()
			syn = name_raw[name_raw.find("(Synonyms: ") + 11:name_raw.find(')')]
		self.name = name_cleaned

		# Get description
		result = soup.find('p', itemprop="description")
		self.description = result.get_text().strip()

		# Get synonym, cas number and catalog number
		result = soup.find('div', class_="detail_hd")
		self.catalog_no = ''.join(re.findall("(HY\-.*)", result.get_text()))

		self.synonym = ', '.join(syn.split(';'))

		tags = soup.find_all("span")
		for tag in tags:
			if len(tag.contents) > 0 and re.match("[0-9]+\-[0-9]+\-[0-9]", tag.get_text()):
				self.cas_no = tag.contents[0].strip()


# Test
def test_chemietek():
	testCT = ChemieTek()
	keyword = "Serabelisib (MLN1117, INK1117, TAK-117)"
	#product_link = testCT.get_product_link(keyword)
	testCT.fill_info(keyword)
	testCT.print_compound()

def test_selleckChem():
	testSC = SelleckChem()
	keyword = "Linifanib (ABT-869)"
	product_link = testSC.fill_info(keyword)
	testSC.print_compound()

def test_mce():
	testMCE = MCE()
	keyword = "Lorlatinib"
	testMCE.fill_info(keyword)
	testMCE.print_compound()

if __name__ == "__main__":
	#test_chemietek()
	#test_selleckChem()
	test_mce()





















