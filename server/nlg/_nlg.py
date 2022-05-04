import random
import time
import pymysql
from . import weather as Weather
from . import menu as Menu

def location(intent):

	_location = intent['location']
	if _location == None:
		content = "sorry, I don't understand what you are saying"
		return content
	_address = ''
	_phone_number = '02-450-3114'

	conn = pymysql.connect(host='localhost', user='root', password='~Exodus<365>!',
                           db='NLG_DB', charset='utf8')
	curs = conn.cursor()

	sql = ("SELECT * FROM location WHERE" +
			" name LIKE '%" + _location + "%'")

	curs. execute(sql)
	rows = curs.fetchall()
	conn.close()

	_address = rows[0][0]
	content =( "The " + _location +" is the building number " + str(_address) + ". " +
		"If you want some more information for finding it, please call this number " + _phone_number + ".")

	return content

def weather(intent):

	sky = (None,'clear', 'a little cloudy', 'cloudy' , 'most cloudy')
	pty = (None, 'rain', 'rain & snow', 'snow')
	_temp = 0
	_skytype = 0
	_ptyCode = 0

	items = Weather.getWeather()

	for item in items:
		if item.get('category') == 'T1H':
			_temp = item.get('obsrValue')
		if item.get('category') == 'SKY':
			_skytype = item.get('obsrValue')
		if item.get('category') == 'PTY':
			_ptyCode = item.get('obsrValue')
	if _ptyCode == 0:
		content = "Today of seoul, it's {tempreature} degree of Celsius and {sky}".format(
					tempreature = _temp, sky = sky[_skytype])
	else:
		content = "Today of seoul, it's {pty}y day and {tempreature} degree of Celsius".format(
					tempreature = _temp, pty = pty[_ptyCode])
	return content

def phone_number(intent):
	content= ""
	_location = intent['location']
	if _location == None:
		content = "sorry, I don't understand what you are saying"
		return content

	conn = pymysql.connect(host='localhost', user='root', password='~Exodus<365>!',db='NLG_DB', charset='utf8')

	curs = conn.cursor()
	sql = "SELECT number.number, number.name FROM number WHERE number.name LIKE '%" + _location + "%'"
	curs.execute(sql)

	rows = curs.fetchall()

	number = rows[0][0]
	location = rows[0][1]

	content = "The number of "+ location + "is " + number

	return content

def menu_q(intent):
	content = ("Which cafeteria would you like to know? " +
				"number one.  cafeteria at the basement of student union hall." + 
				" number two. cafteria at the groundfloor of student union hall." + 
				" number three. cafeteria at the library." +
				" number four. cafeteria at the dormitory." + 
				" number five. cafeteria at new millennium hall.")

	return content

def menu_a(content):
	menutable = None

	if 'one' in content or '1' in content or content == 'student union hall':
		menutable = Menu.getMenu(1)

	elif 'two' in content or '2' in content or content == 'dorm' or content == 'dormitory':
		menutable = Menu.getMenu(2)

	elif 'three' in content or '3' in content or content == 'library':
		menutable = Menu.getMenu(3)

	elif 'four' in content or '4' in content:
		menutable = Menu.getMenu(4)

	elif 'five' in content or '5' in content or content == 'new millennium hall':
		menutable = Menu.getMenu(5)
	else:
		menutable = "sorry, I don't understand what you are saying"

	return menutable

def greeting(intent):
	text = intent
	if "hi" or "hello" in text:
		content = "hi, there. I'm Kate."
	if "good" in text:
		if "morning" in text:
			content = "Good morning. How are you feeling today?"
		if "afternoon" in text:
			content = "Good afternoon. Is there anything fun going on?"
		if "evening" in text:
			content = "Good evening. What's up?"
	if "how are you" in text:
		how_ans = ["I'm pretty good.and you?", "Never better.and you?", "I'm doing great.and you?"]
		content = how_ans[random.randint(0, 2)]

	return content

def read_bible(intent):
	content = "Implementing"
	conn = pymysql.connect(host='localhost', user='root', password='~Exodus<365>!',
                           db='NIV', charset='utf8')
	curs = conn.cursor()

	sql = ("SELECT verse.text FROM verse, bookmapping Where verse.book_id=bookmapping.id"+
			" and bookmapping.book='" + intent['book'] +"'" +
			" and verse.chapter=" + intent['chapter'] +
			" and verse.verse=" + intent['verse'])

	curs. execute(sql)
	rows = curs.fetchall()
	conn.close()

	content = rows[0][0]

	return content

def qt(intent):
	content = "Implementing"

	return content
