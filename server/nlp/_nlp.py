from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import pymysql

import six

def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    return entities
    '''for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))'''

def syntax_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
    return tokens
    '''for token in tokens:
        #print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
         #                      token.text.content))
        print(token)'''

def recognize_intent_type(text):
	if "where" in text:
		conn = pymysql.connect(host='localhost', user='root', password='~Exodus<365>!',
                           db='NLG_DB', charset='utf8')
		curs = conn.cursor()

		sql = "SELECT name FROM location"

		curs. execute(sql)
		rows = curs.fetchall()
		conn.close()
		nIndex = 0
		entity_location = {}
		entities = entities_text(text)
		entity_location = {}
		
		try :
			for entity in entities:
				if entity.type == 2: # LOCATION = 2
					entity_location['location'] = entity.name
				if entity.type == 7: # OTHER = 7
					if entity.name == 'library':
						entity_location['location'] = 'Sanghuh Memorial Library'
					if entity.name == 'center':
						entity_location['location'] = 'Konkuk University Medical Center'
				if entity.type == 3: # ORGANIZATION = 3
					if 'school' in entity.name:
						entity_location['location'] = entity.name
					if 'center' in entity.name:
						entity_location['location'] = entity.name
					if 'institute' in entity.name:
						entity_location['location'] = entity.name

			if not 'location' in entity_location or ('location' in entity_location and entity_location['location'] == 'hall'):
				tokens = syntax_text(text)
				nown_set = []
				for token in tokens:
					if token.part_of_speech.tag == 6:
						nown_set.append(token.text.content)
				for i in range(len(rows)):
					if nown_set[0] in rows[i][0].lower():
						nIndex = i
						break

				if nIndex == 0:
					if not 'admin' in text:
						entity_location['location'] = None


				entity_location['location'] = rows[nIndex][0]
				if 'new engineering' in text:
					entity_location['location'] = rows[nIndex + 1][0]
		except Exception as e:
			return e

		return {'LOCATION' : entity_location}
	elif "what" in text:

		if "weather" in text:
			entities = entities_text(text)
			entity_weather = {}
			for entity in entities:
				if entity.type == 2: # LOCATION = 2
					entity_weather['location'] = entity.name
			tokens = syntax_text(text)
			for token in tokens:
				if token.dependency_edge.label == 57: # TOMD = 57
					entity_weather['time'] = token.text.content
			return {'WEATHER' : entity_weather }

		elif  "menu" in text:
			entity_menu = {'location' : None, 'time' : 'today'}
			tokens = syntax_text(text)
			entities = entities_text(text)

			for entity in entities:
				if entity.type == 2: # LOCATION = 2
					entity_menu['location'] = entity.name
				if entity.type == 7: # OTHER = 7
					if entity.name == 'library':
						entity_menu['location'] = entity.name

			for i in range(len(tokens)):
				if tokens[i].dependency_edge.label == 57: # TOMD = 57
					entity_menu['time'] = tokens[i].text.content
				elif tokens[i].dependency_edge.label == 43: #PREP = 43
					if tokens[i].lemma == 'for':
						entity_menu['time'] = tokens[i+1].text.content

			return {"MENU" : entity_menu}

		elif ( "telephone number" in text or 
				"contact number" in text or
				"phone number" in text or
				"digits" in text ):
			tokens = syntax_text(text)
			entity_phone_number = {}
			nIndex = 0
			for token in tokens:
				if token.dependency_edge.label == 36: #POBJ = 36
					entity_phone_number['location'] = token.text.content
			return {"PHONE_NUMBER" : entity_phone_number}

	elif ("hi" in text or
        	"hello" in text or
        	"good morning" in text or
        	"good afternoon" in text or
        	"good evening" in text or
        	"how are you" in text):
		return {'GREETING' : text}

	elif "qt" in text:
		entity_qt = {'time' : 'today'}
		tokens = syntax_text(text)

		for token in tokens:
				if token.dependency_edge.label == 57: # TOMD = 57
					entity_qt['time'] = token.text.content
		return {"QT" : entity_qt}

	elif ("read" in text or
                "chatper" in text or
                  "verse" in text):
		entity_bible = {}
		tokens = syntax_text(text)
		for token in tokens:
			if token.part_of_speech.tag == 6:
				if token.text.content == 'chapter' or token.text.content == 'verse':
					continue
				entity_bible['book'] = token.text.content
			if token.part_of_speech.tag == 7 and not 'chapter' in entity_bible:
				entity_bible['chapter'] = token.text.content
			if token.part_of_speech.tag == 7 and 'chapter' in entity_bible:
				entity_bible['verse'] = token.text.content
		return {"READ_BIBLE" : entity_bible}

	else:
		return {'CANTUNDERSTAND' : "sorry, I don't understand what you are saying"}




