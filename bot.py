import json
import requests
import random
import string
import logging

class Api:
    aRegister = '/api/register/'
    aLogin = '/api/login/'
    aPost = '/api/post/'
    aUser = '/api/user/'
    aLike = '/api/like/'


class Const:
    aFile_config = 'config.json'
    aUrl_api = 'http://127.0.0.1'
    nPort = 8000


class User_actions():
    def __init__(self):
        self.aToken = None

    # def post_list(self):
    #     #aToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImphaiIsImV4cCI6MTU4NzA3MTk0MywiZW1haWwiOiIifQ.D4Voe089pJXsiudhyBNHwJYpqM0DVE-zzmpd8JXOP5I'
    #     aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aPost}'
    #     oHeaders = {
    #         'Authorization': f'JWT {self.aToken}'
    #     }
    #     return requests.get(aUrl, headers=oHeaders)

    def post(self, aText):
        #aToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImphaiIsImV4cCI6MTU4NzA3MTk0MywiZW1haWwiOiIifQ.D4Voe089pJXsiudhyBNHwJYpqM0DVE-zzmpd8JXOP5I'
        aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aPost}'
        oHeaders = {
            'Authorization': f'JWT {self.aToken}'
        }
        oData = {
            'post': aText
        }
        return requests.post(aUrl, headers=oHeaders, data=oData)

    def user(self):
        #aToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImphaiIsImV4cCI6MTU4NzA3MTk0MywiZW1haWwiOiIifQ.D4Voe089pJXsiudhyBNHwJYpqM0DVE-zzmpd8JXOP5I'
        aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aUser}'
        oHeaders = {
            'Authorization': f'JWT {self.aToken}'
        }
        return requests.get(aUrl, headers=oHeaders)

    def like_post(self, nPost_id):
        #aToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImphaiIsImV4cCI6MTU4NzA3MTk0MywiZW1haWwiOiIifQ.D4Voe089pJXsiudhyBNHwJYpqM0DVE-zzmpd8JXOP5I'
        aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aLike}'
        oHeaders = {
            'Authorization': f'JWT {self.aToken}'
        }
        oData = {
            'postid': nPost_id,
            'action': 'like'
        }
        return requests.post(aUrl, headers=oHeaders, data=oData)


def config_load():
    oFile = open(Const.aFile_config, 'r')
    oConfig = json.load(oFile)
    return oConfig

def post_list():
    aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aPost}'
    return requests.get(aUrl).json()

def create_user(aUser, aPassword):
    aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aRegister}'
    oData = {
        "username": aUser,
        "password1": aPassword,
        "password2": aPassword
    }
    oRespond = requests.post(aUrl, data=oData)
    return oRespond

def login(aUser, aPassword):
    aUrl = f'{Const.aUrl_api}:{Const.nPort}{Api.aLogin}'
    oData = {
        "username": aUser,
        "password": aPassword
    }
    oRespond = requests.post(aUrl, data=oData)
    return oRespond

def random_string(nLen_string):
    xLetters = string.ascii_lowercase
    aString = ''
    for i in range(nLen_string):
        aString = aString + random.choice(xLetters)
    return aString


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Starting bot..')
logging.info('Reading config file [%s]', Const.aFile_config)
oConfig = config_load()
logging.info('Config was read')

xUsers = []
logging.info('Signup users..')
for nCounter, nUser in enumerate(range(oConfig['number_of_users'])):
    aUsername = random_string(6)
    aPassword = random_string(6)
    xUsers.append(create_user(aUsername, aPassword).json())
    logging.info('Signup user [%s] with password [%s]', aUsername, aPassword)
logging.info('Signup [%s] users is finshed.', nCounter+1)

logging.info('Start creating posts..')
for oUser in xUsers:
    for nPost_count in range(random.randint(0, oConfig['max_posts_per_user'])):
        oUser_action = User_actions()
        oUser_action.aToken = oUser['token']
        aPost = random_string(10)
        oUser_action.post(aText=aPost)
        logging.info('Created post [%s] by user [%s]', aPost, oUser['user']['username'])
logging.info('Creating posts is finshed ')

xPosts = post_list()

logging.info('Start creating likes..')
for oUser in xUsers:
    oUser_action = User_actions()
    oUser_action.aToken = oUser['token']
    for nPost_counter in range(random.randint(0, oConfig['max_likes_per_user'])):
        oPost = xPosts[random.randint(1, len(xPosts)-1)]
        nPost_id = oPost['postid']
        oLike = oUser_action.like_post(nPost_id)
        logging.info('Like from user [%s] to post with id [%s]', oUser['user']['username'], nPost_id)
logging.info('Creating likes is finished.')



