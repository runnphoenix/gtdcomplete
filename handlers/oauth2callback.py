#/usr/bin/python

from handler import Handler

class Oauth2Callback(Handler):

	def get(self):
		print self.request.body
