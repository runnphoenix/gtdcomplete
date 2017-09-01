#!/usr/bin/python

import functools
from google.appengine.ext import db

def events_key(name="default"):
	return db.Key.from_path("events", name)

def projects_key(name="default"):
	return db.Key.from_path("projects", name)

def contexts_key(name="default"):
	return db.Key.from_path("contexts", name)

def user_logged_in(function):
	@functools.wraps(function)
	def wrapper(self, *a):
		if self.user:
			return function(self, *a)
		else:
			print("------- User not logged in.")
			self.redirect('/login')
			return
	return wrapper

def project_exist(function):
	@functools.wraps(function)
	def wrapper(self, project_id):
		key = db.Key.from_path("Project", int(project_id), parent=projects_key())
		projects = db.GqlQuery("select * from Project")
		project = None
		for pro in projects:
			if pro.key().id() == key.id():
				project = pro
		if project:
			return function(self, project_id, project)
		else:
			print("------- Project does not exist.")
			self.error(404)
			return
	return wrapper

def context_exist(function):
	@functools.wraps(function)
	def wrapper(self, context_id):
		key = db.Key.from_path("Context", int(context_id), parent=contexts_key())
		#context = db.get(key)
		contexts = db.GqlQuery("select * from Context")
		context = None
		for con in contexts:
			if con.key().id() == key.id():
				context = con
		if context:
			return function(self, context_id, context)
		else:
			print("------- Context does not exist.")
			self.error(404)
			return
	return wrapper

def event_exist(function):
	@functools.wraps(function)
	def wrapper(self, event_id):
		key = db.Key.from_path("Event", int(event_id), parent=events_key())
		event = db.get(key)
		if event:
			return function(self, event_id, event)
		else:
			print("------- Event not exist.")
			self.error(404)
			return
	return wrapper

def user_own_event(function):
	@functools.wraps(function)
	def wrapper(self, event_id, event):
		if self.user.name == event.project.user.name:
			return function(self, event_id, event)
		else:
			print("------- User does not own event.")
			self.redirect('/event/%s' % str(event_id))
			return
	return wrapper


