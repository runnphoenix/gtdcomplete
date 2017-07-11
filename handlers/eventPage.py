#!/usr/bin/python

from handler import Handler
from models import Event
import accessControl

class EventPage(Handler):
	@accessControl.user_logged_in
	@accessControl.event_exist
	def get(self, event_id, event):
		self.render("eventPage.html", event=event)

	@accessControl.user_logged_in
	def post(self):
		pass

