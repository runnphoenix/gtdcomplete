#!/usr/bin/python

from handler import Handler

class Welcome(Handler):
	
	def get(self):
		self.render("welcome.html", username=self.user.name)
