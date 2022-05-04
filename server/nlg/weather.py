from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json

import time

def getWeather():

	now = time.gmtime(time.time())

	SERVICE_KEY ='27YXieXftvTJvrPjDwCXtCKWB4i9ITxG9n1Lu4R0aa0iWlM3%2BCgfx9uOyvFDdZsqTw2meXq0TBGY90F29e%2FXZw%3D%3D'
	BASE_DATE = ('%04d%02d%02d' % (now.tm_year, now.tm_mon, now.tm_mday))
	BASE_TIME = ('%02d00' % (now.tm_hour))
	
	NX = '62'
	NY = '126'


	url = ('http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib'+
	       '?serviceKey=' + SERVICE_KEY +
    	    '&base_date=' + BASE_DATE +
        	'&base_time=' + BASE_TIME +
    	    '&nx=' + NX +
    	    '&ny=' + NY +
    	    '&numOfRows=10'+
    	    '&_type=json')
        

	request = Request(url)
	request.get_method = lambda: 'GET'
	#print(request.get_method)

	response_body = urlopen(request)

	data = json.load(response_body)

	items = data.get('response').get('body').get('items').get('item')

	return items

	#pprint(data)

	#pprint(data.get('response').get('body').get('items').get('item'))
	'''
	for item in data.get('response').get('body').get('items').get('item'):
    	if item.get('category') == 'T1H':
        	print('기온: {}℃'.format(item.get('obsrValue')))
    '''
if __name__ == '__main__':
	from pprint import pprint
	items = getWeather()
	pprint(items)
	for item in items:
		if item.get('category') == 'PTY':
			print(item.get('obsrValue'))

