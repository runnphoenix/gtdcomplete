#!/usr/bin/python

from handler import Handler
from models import Context
import accessControl


class ContextPage(Handler):

	# find all events @ this project

	@accessControl.user_logged_in
	@accessControl.context_exist
	def get(self, context_id, context):
		self.render("contextPage.html", context=context)

	@accessControl.user_logged_in
	@accessControl.context_exist
	def post(self):
		pass

