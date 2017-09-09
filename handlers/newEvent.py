#!/usr/bin/python

from handler import Handler
from models import Event
from models import Project
from models import Context
from models import TimeCategory
from google.appengine.ext import db
import accessControl
from datetime import datetime,date,time

def events_key(name="default"):
    return db.Key.from_path("events", name)

class NewEvent(Handler):

    # List all existing projects
    projects = db.GqlQuery("select * from Project order by created desc")
    # List all existing contexts && select one from them (/Projects /Contexts)
    contexts = db.GqlQuery("select * from Context order by created desc")
    timeCategories = db.GqlQuery("select * from TimeCategory order by created desc")

    @accessControl.user_logged_in
    def get(self):
        self.render(
            "newEvent.html", projects=self.user.projects, contexts=self.user.contexts, timeCategories=self.user.timeCategories)

    @accessControl.user_logged_in
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        repeat = self.request.get("repeat")
        planStartTime = datetime.strptime(self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
        planEndTime = datetime.strptime(self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
        exeStartTime = datetime.strptime(self.request.get("exeStartTime"), "%Y-%m-%dT%H:%M")
        exeEndTime = datetime.strptime(self.request.get("exeEndTime"), "%Y-%m-%dT%H:%M")

        project = None
        projectName = self.request.get("projects")
        for pro in self.user.projects:
            if pro.name == projectName:
                project = pro

        timeCategory = None
        timeCategoryName = self.request.get("timeCategories")
        for category in self.user.timeCategories:
            if category.name == timeCategoryName:
                timeCategory = category

        context = None
        contextName = self.request.get("contexts")
        for con in self.user.contexts:
            if con.name == contextName:
                context = con

        errorMessage = self.erMessage(title, content, repeat)

        if errorMessage:
            self.render("newEvent.html",
                        projects=self.projects,
                        contexts=self.contexts,
                        timeCategories=self.timeCategories,
                        errorMessage=errorMessage,
                        eventTitle=title,
                        content=content,
                        repeat=repeat,
                        planStartTime=planStartTime,
                        planEndTime=planEndTime,
                        exeStartTime=exeStartTime,
                        exeEndTime=exeEndTime)
        else:
            event = Event(
                project=project,
                timeCategory=timeCategory,
                context=context,
                user=self.user,
                parent=events_key(),
                title=title,
                content=content,
                repeat=repeat,
                time_plan_start=planStartTime,
                time_plan_end=planEndTime,
                time_exe_start=exeStartTime,
                time_exe_end=exeEndTime)
            event.put()
            self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title, timeCategory, content, repeat):
        if not title or not timeCategory or not content or not repeat:
            return "Field is empty."
        else:
            return None
