#!/usr/bin/python

from google.appengine.ext import db
from user import User

class Event(db.Model):
	project = db.StringProperty(required=True)
	context = db.TextProperty(required=False)
	time_plan_start = db.DateTimeProperty(auto_now_add=False)
	time_plan_end = db.DateTimeProperty(auto_now_add=False)
	time_exe_start = db.DateTimeProperty(auto_now_add=False)
	time_ext_end = db.DateTimeProperty(auto_now_add=False)
	title = db.StringProperty(required=True)
	content = db.TextProperty(required=False)
	repeat = db.StringProperty(required=False)

	user = db.ReferenceProperty(User, collection_name = 'events')
