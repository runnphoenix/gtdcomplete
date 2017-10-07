#/usr/bin/python

from handler import Handler
from models import Oauth2Service

class Calendar(Handler):
	def get(self):
		self.render('calendar.html')

	@Oauth2Service.decorator.oauth_required
	def post(self):
		request = Oauth2Service.service.events().list(calendarId='primary')
		response = request.execute(http=Oauth2Service.decorator.http())
		events = []
		for event in response['items']:
			conciseEvent = {}
			conciseEvent['start'] = event['start']
			conciseEvent['end'] = event['end']
			conciseEvent['summary'] = event['summary']
			conciseEvent['updated'] = event['updated']
			events.append(conciseEvent)
		self.render('calendar.html', events=events)
