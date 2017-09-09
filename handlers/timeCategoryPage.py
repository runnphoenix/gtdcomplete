#!/usr/bin/python

from handler import Handler
from models import TimeCategory
import accessControl

class TimeCategoryPage(Handler):
	@accessControl.user_logged_in
	@accessControl.timeCategory_exist
	def get(self, timeCategory_id, timeCategory):
		self.render("timeCategoryPage.html", timeCategory=timeCategory)

	@accessControl.user_logged_in
	def post(self):
		pass

