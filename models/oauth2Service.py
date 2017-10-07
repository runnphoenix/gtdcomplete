#!/usr/bin/python

from apiclient import discovery
from oauth2client.contrib.appengine import OAuth2Decorator

class Oauth2Service():
    decorator = OAuth2Decorator(
        client_id='616429551496-5pq095a8rujmih0l0alfrl8jgadqtaaj.apps.googleusercontent.com',
        client_secret='7kOx9i9yDJriYbJbpFvDaizI',
        scope='https://www.googleapis.com/auth/calendar')

    service = discovery.build('calendar', 'v3')
