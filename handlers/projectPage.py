#!/usr/bin/python

from handler import Handler
from models import Project
import accessControl
from google.appengine.ext import db


class ProjectPage(Handler):
	def projects_key(name='default'):
		return db.Key.from_path('projects', name)

	def get(self):
		print self.projects_key()

	#@accessControl.user_logged_in
	#@accessControl.project_exist
	#def get(self, project_id, project):
		#self.render("projectPage.html", project=project)

	@accessControl.user_logged_in
	def post(self):
		pass

