#!/usr/bin/python

from handler import Handler
from models import Context
import accessControl


class ContextPage(Handler):
	@accessControl.user_logged_in
	@accessControl.context_exist
	def get(self, context_id, context):
		self.render("contextPage.html", context=context)

	@accessControl.user_logged_in
	@accessControl.context_exist
	def post(self, context_id, context):
		for event in context.events:
			event.delete()
		context.delete()
		self.redirect("/contexts")

