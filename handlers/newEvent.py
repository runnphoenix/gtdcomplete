#!/usr/bin/python

from handler import Handler
from models import Event
from google.appengine.ext import db
import accessControl

def events_key(name="default"):
	return db.Key.from_path("events", name)

class NewEvent(Handler):
	@accessControl.user_logged_in
	def get(self):
		self.render("newEvent.html")

	@accessControl.user_logged_in
	def post(self):
		title = self.request.get("title")
		content = self.request.get("content")
		repeat = self.request.get("repeat")
		planStartTime = self.request.get("planStartTime")
		planEndTime = self.request.get("planEndTime")
		exeStartTime = self.request.get("exeStartTime")
		exeEndTime = self.request.get("exeEndTime")

		# List all existing projects

		# List all existing contexts && select one from them (/Projects /Contexts)

		errorMessage = self.erMessage(title, content, repeat, planStartTime, planEndTime, exeStartTime, exeEndTime)

		if errorMessage:
			self.render("newEvent.html", 
				errorMessage=errorMessage, 
				eventTitle=eventTitle, 
				content=content, 
				repeat=repeat, 
				planStartTime=planStartTime, 
				planEndTime=planEndTime, 
				exeStartTime=exeStartTime, 
				exeEndTime=exeEndTime)
		else:
			event = Event(
				project = project,
				context = context,
				user = self.user,
				parent = events_key,
				title = title,
				content = content,
				repeat = repeat,
				time_plan_start = planStartTime,
				time_plan_end = planEndTime,
				time_exe_start = exeStartTime,
				time_exe_end = exeEndTime)
			event.put()
			self.redirect("/event/%s" % str(event.key().id()))

	def erMessage(self, title, content, repeat, planStartTime, planEndTime, exeStartTime, exeEndTime):
		if not title or not content or not repeat or not planStartTime or not planEndTime or not exeStartTime or not exeEndTime:
			return "Field is empty."
		else:
			return None

