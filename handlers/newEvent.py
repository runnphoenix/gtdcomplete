#!/usr/bin/python

from handler import Handler
from models import Event
from models import Project
from models import Context
from models import TimeCategory
from google.appengine.ext import db
import accessControl
from datetime import datetime,date,time
import pytz

def events_key(name="default"):
    return db.Key.from_path("events", name)

class NewEvent(Handler):
    @accessControl.user_logged_in
    def get(self):
        self.render(
            "newEvent.html",
            projects=self.user.projects,
            contexts=self.user.contexts,
            timeCategories=self.user.timeCategories,
            repeat='0000000',
            eventTitle='',
            eventContent='',
            finished=False,
            planStartTime=datetime.now(pytz.timezone('Asia/Shanghai')),
            planEndTime=datetime.now(pytz.timezone('Asia/Shanghai')),
            exeStartTime=datetime.now(pytz.timezone('Asia/Shanghai')),
            exeEndTime=datetime.now(pytz.timezone('Asia/Shanghai'))
        )

    @accessControl.user_logged_in
    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        repeat = ""
        for i in range(7):
            rep = self.request.get("repeat"+str(i))
            if (rep != "on"):
                repeat = repeat + '0'
            else:
                repeat = repeat + '1'

        planStartTime = datetime.strptime(self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
        planEndTime = datetime.strptime(self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
        exeStartTime = datetime.strptime(self.request.get("exeStartTime"), "%Y-%m-%dT%H:%M")
        exeEndTime = datetime.strptime(self.request.get("exeEndTime"), "%Y-%m-%dT%H:%M")

        project = None
        projectName = self.request.get('projects')
        print projectName
        for pro in self.user.projects:
            print pro.name
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

        errorMessage = self.erMessage(title)

        if errorMessage:
            self.render("newEvent.html",
                        projects=self.user.projects,
                        contexts=self.user.contexts,
                        timeCategories=self.user.timeCategories,
                        errorMessage=errorMessage,
                        eventTitle=title,
                        eventContent=content,
                        repeat=repeat,
                        planStartTime=planStartTime,
                        planEndTime=planEndTime,
                        exeStartTime=exeStartTime,
                        exeEndTime=exeEndTime,
                        finished=False)
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
                time_exe_end=exeEndTime,
                finished=False)
            event.put()
            self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title):
        if not title:
            return "Field is empty."
        elif ' ' in title:
            return "No space allowed in title."
        else:
            return None
