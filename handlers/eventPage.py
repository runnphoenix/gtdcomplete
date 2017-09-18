#!/usr/bin/python

from handler import Handler
from models import Event
import accessControl
from datetime import datetime,date,time

class EventPage(Handler):
    @accessControl.user_logged_in
    @accessControl.event_exist
    def get(self, event_id, event):
        self.render("eventPage.html", event=event)

    @accessControl.user_logged_in
    @accessControl.event_exist
    @accessControl.user_own_event
    def post(self, event_id, event):
        print self.request.params

        if "Delete" in self.request.params:
            event.delete()
            self.redirect("/projects")
        else:
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

            errorMessage = self.erMessage(title, timeCategory, content, repeat)

            if errorMessage:
                event = Event(
                    project=project,
                    timeCategory=timeCategory,
                    context=context,
                    user=self.user,
                    title=title,
                    content=content,
                    repeat=repeat,
                    time_plan_start=planStartTime,
                    time_plan_end=planEndTime,
                    time_exe_start=exeStartTime,
                    time_exe_end=exeEndTime)
                self.render("eventPage.html", event=event)
            else:
                event.project=project
                event.timeCategory=timeCategory
                event.context=context
                event.user=self.user
                event.title=title
                event.content=content
                event.repeat=repeat
                event.time_plan_start=planStartTime
                event.time_plan_end=planEndTime
                event.time_exe_start=exeStartTime
                event.time_exe_end=exeEndTime

                event.put()
                self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title, timeCategory, content, repeat):
        if not title or not timeCategory or not content or not repeat:
            return "Field is empty."
        else:
            return None
