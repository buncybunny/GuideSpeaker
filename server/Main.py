##-- import library --##
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import urllib.parse
import sys

##-- import custom module -- ##
from nlp import _nlp as NLP
from nlg import _nlg as NLG




# MySQL 연결
mysql = MySQL()

app = Flask(__name__)
api = Api(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '~Exodus<365>!'
app.config['MYSQL_DATABASE_DB'] = 'user_data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class Request(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('serviceKey', type=str)
            parser.add_argument('content', type=str)
            args = parser.parse_args()

            _serviceKey = args['serviceKey']
            _content = urllib.parse.quote(args['content'])

            if _serviceKey == 'hiseungmin':
                if _content != '':

                    
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO request_data (content) VALUES ('" + _content +"')")
                    conn.commit()
                    conn.close()
                    

                    _intent = NLP.recognize_intent_type(args['content'].lower())
                    print(str({'Content': args['content'], 'IntentDict' : _intent}), file=sys.stdout)

                    ## --- Controller ----##
                    if 'LOCATION' in _intent:
                        ''' LOCATION Intent '''
                        content = NLG.location(_intent['LOCATION'])
                        return {'status_code' : '200', 'content' : content}

                    if 'WEATHER' in _intent:
                        ''' WEATHER Intent '''
                        content = NLG.weather(_intent['WEATHER'])
                        return {'status_code' : '200', 'content' : content}
                        
                    elif 'PHONE_NUMBER' in _intent:
                        ''' PHONE NUMBER Intent '''
                        content = NLG.phone_number(_intent['PHONE_NUMBER'])
                        return {'status_code' : '200', 'content' : content}
                        
                    elif 'MENU' in _intent:
                        ''' MENU Intent '''
                        if _intent['MENU']['location'] == None:
                            content = NLG.menu_q(_intent['MENU'])
                            ## 클라이언트가 메뉴 질문 코드 789
                            return {'status_code' : '789', 'content' : content}
                        else:
                            content = NLG.menu_a(_intent['MENU']['location'])
                            return {'status_code' : '780', 'content' : content}
                        
                    elif 'GREETING' in _intent:
                        ''' GREETING Intent '''
                        content = NLG.greeting(_intent['GREETING'])
                        return {'status_code' : '200', 'content' : content}

                    elif 'CANTUNDERSTAND' in _intent:
                        ''' CANTUNDERSTAND Intent '''
                        return {'status_code' : '200', 'content' : _intent['CANTUNDERSTAND']}

                    elif 'READ_BIBLE' in _intent:
                        ''' Read bible intent'''
                        content = NLG.read_bible(_intent['READ_BIBLE'])
                        return {'status_code' : '200', 'content' : content}

                    elif 'QT' in _intent:
                        '''Read QT intent'''
                        content = NLG.qt(_intent['QT'])
                        return {'status_code' : '200', 'content' : content}

                    else:
                        return {'StatusCode': '200', 'content': args['content'], 'IntentDict' : _intent}
                else:
                    return {'StatusCode' : '400', 'resultMsg' : 'NULL Content'}
            else :
                return {'StatusCode': '401', 'resultMsg': 'SERVICE KEY IS NOT REGISTERED ERROR.'}

        except Exception as e:
            return {'error': str(e)}

class Answer(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)
            parser.add_argument('content', type=str)
            args = parser.parse_args()

            _type = args['type']
            _content = args['content']

            if _type == "menu":
                content = NLG.menu_a(_content)
                return {'StatusCode' : '200', 'content' : content}

        except Exception as e:
            return {'error': str(e)}

                

api.add_resource(Request, '/request')
api.add_resource(Answer, '/answer')

if __name__ == '__main__':
    app.run(host = '127.0.0.1', debug=True)
