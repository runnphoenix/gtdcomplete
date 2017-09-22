#!/usr/bin/python

from handler import Handler
from models import TimeCategory
from google.appengine.ext import db
import accessControl

class NewTimeCategory(Handler):

	@accessControl.user_logged_in
	def get(self):
		self.render("newTimeCategory.html")

	@accessControl.user_logged_in
	def post(self):
		name = self.request.get('name')
		if not name:
			errorMessage = 'name can not be empty'
			self.render('newTimeCategory.html', errorMessage=errorMessage)
		elif ' ' in name:
			errorMessage = 'No space allowed.'
			self.render('newTimeCategory.html', errorMessage=errorMessage)
		else:
			# find project names already exist
			timeCategory_exist = False
			for timeCategory in self.user.timeCategories:
				if timeCategory.name == name:
					timeCategory_exist = True
					errorMessage = 'TimeCategory already exist, find another name.'
					self.render('NewTimeCategory.html', errorMessage=errorMessage)

			if timeCategory_exist == False:
				timeCategory = TimeCategory(name=name, user=self.user)
				timeCategory.put()
				self.redirect('/timeCategory/%s' % str(timeCategory.key().id()))
