#-*-coding: utf-8

from requests import get
from bs4 import BeautifulSoup

def getMenu(number):
	CAMPUS_ID = 'MoCQZdj1hE' 
	url = 'https://bds.bablabs.com/restaurants?campus_id=' + CAMPUS_ID

	response = get(url)
	response.raise_for_status()
	response.encoding='utf-8'
	html_soup = BeautifulSoup(response.text, 'html.parser')
	menu_table = html_soup.find_all('ul', class_="list-group list-group-flush")
	menus = []

	for menu in menu_table:
		menus.append(menu)

	return menus[number - 1].text.replace("  ", "").strip().replace("\n\n", "")
