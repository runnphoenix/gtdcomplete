#!/usr/bin/python

import functools
from google.appengine.ext import db

def events_key(name='default'):
	return db.Key.from_path("events", name)

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
