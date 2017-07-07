#!/usr/bin/python

from google.appengine.ext import db
from project import Project
from user import User
from context import Context

class Event(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty(required=False)
	repeat = db.StringProperty(required=False)
	time_plan_start = db.DateTimeProperty(auto_now_add=False)
	time_plan_end = db.DateTimeProperty(auto_now_add=False)
	time_exe_start = db.DateTimeProperty(auto_now_add=False)
	time_ext_end = db.DateTimeProperty(auto_now_add=False)

	context = db.ReferenceProperty(Context, collection_name = 'events')
	user = db.ReferenceProperty(User, collection_name = 'events')
	project = db.ReferenceProperty(Project, collection_name = 'events')
