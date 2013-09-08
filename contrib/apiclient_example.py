#!/usr/bin/env python2
from getpass import getpass

import slumber
from requests.auth import AuthBase


class TastypieApikeyAuth(AuthBase):
    def __init__(self, username, apikey):
        self.username = username
        self.apikey = apikey

    def __call__(self, r):
        r.headers['Authorization'] = "ApiKey {0}:{1}".format(self.username, self.apikey)
        return r

SERVER_URL = 'http://localhost:8000/api/v1/'

username = raw_input("Username: ")
apikey = getpass("APIkey: ")

api = slumber.API(SERVER_URL, format='json', auth=TastypieApikeyAuth(username, apikey))
print "Creating new todo"
new_todo = api.todo.post({'text': 'Client test', 'priority': 'A', 'due': '2014-01-01'})
print "Id ", new_todo["id"]
print "Changing"
api.todo(new_todo['id']).put({'text': 'Client test changed'})
print "Checking"
print api.todo(new_todo['id']).get()
