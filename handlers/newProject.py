#!/usr/bin/python

from handler import Handler
from models import Project
from google.appengine.ext import db
import accessControl

calss NewProject(Handler):

	@accessControl.user_logged_in
	def get(self):
		self.render("newProject.html")


	@accessControl.user_logged_in
	def post(self):
		name = self.reqeuset.get('name')
		if not name:
			erMessage = 'name can not be empty'
			self.render('newProject.html', erMessage=erMessage)
		else:
			project = Project(name=name, user=self.user)
			project.put()
			self.redirect('/project/%s' %s str(project.key().id()))
