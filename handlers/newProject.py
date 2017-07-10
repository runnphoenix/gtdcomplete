#!/usr/bin/python

from handler import Handler
from models import Project
from google.appengine.ext import db
import accessControl

class NewProject(Handler):

	@accessControl.user_logged_in
	def get(self):
		self.render("newProject.html")


	@accessControl.user_logged_in
	def post(self):
		name = self.request.get('name')
		if not name:
			errorMessage = 'name can not be empty'
			self.render('newProject.html', errorMessage=errorMessage)
		else:
			project = Project(name=name, user=self.user)
			project.put()
			self.redirect('/project/%s' % str(project.key().id()))
