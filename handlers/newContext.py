#!/usr/bin/python

from handler import Handler
from models import Context
from google.appengine.ext import db
import accessControl

class NewContext(Handler):

	@accessControl.user_logged_in
	def get(self):
		self.render("newContext.html")

	@accessControl.user_logged_in
	def post(self):
		name = self.request.get('name')
		if not name:
			errorMessage = 'name can not be empty'
			self.render('newContext.html', errorMessage=errorMessage)
		else:
			context = Context(name=name, user=self.user)
			context.put()
			self.redirect('/context/%s' % str(context.key().id()))
