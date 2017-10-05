#/usr/bin/python

from apiclient import discovery
from handler import Handler
from httplib2 import Http
from oauth2client.contrib.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
  client_id='616429551496-5pq095a8rujmih0l0alfrl8jgadqtaaj.apps.googleusercontent.com',
  client_secret='7kOx9i9yDJriYbJbpFvDaizI',
  scope='https://www.googleapis.com/auth/calendar')

service = discovery.build('calendar', 'v3')

class Calendar(Handler):
	def get(self):
		self.render('calendar.html')

	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		request = service.events().list(calendarId='primary')
		response = request.execute(http=http)
		events = []
		for event in response['items']:
			conciseEvent = {}
			conciseEvent['start'] = event['start']
			conciseEvent['end'] = event['end']
			conciseEvent['summary'] = event['summary']
			conciseEvent['updated'] = event['updated']
			events.append(conciseEvent)
		self.render('calendar.html', events=events)
