#!/usr/bin/python

from handler import Handler
from models import Project
import accessControl

class ProjectPage(Handler):
	@accessControl.user_logged_in
	@accessControl.project_exist
	def get(self, project_id, project):
		self.render("projectPage.html")

	@accessControl.user_logged_in
	def post(self):
		pass

