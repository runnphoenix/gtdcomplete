#!/usr/bin/python

from handler import Handler
from models import Event
import accessControl
from datetime import datetime,date,time,timedelta

class EventPage(Handler):
    @accessControl.user_logged_in
    @accessControl.event_exist
    def get(self, event_id, event):
        self.render("eventPage.html", event=event)

    @accessControl.user_logged_in
    @accessControl.event_exist
    @accessControl.user_own_event
    def post(self, event_id, event):
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

            if self.request.get("finished") == 'on':
                finished = True
            else:
                finished = False

            errorMessage = self.erMessage(title)

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
                    time_exe_end=exeEndTime,
                    finished = False)
                self.render("eventPage.html", event=event)
            else:
                if finished == True and event.finished == False:
                    # Change event status to finished
                    # Add a new event with date+1 AT NEXT REPEAT
                    if event.repeat != "0000000":
                        # find date of next event
                        weekDayth = event.time_plan_start.date().weekday()
                        nextDayCount=-1
                        doubleRepeat = repeat+repeat
                        for i in range(weekDayth+1, 14):
                            if doubleRepeat[i]=='1':
                                nextDayCount = i-weekDayth
                                break
                        newEvent = Event(
                            project=event.project,
                            timeCategory=event.timeCategory,
                            context=event.context,
                            user=self.user,
                            title=event.title,
                            content=event.content,
                            repeat=event.repeat,
                            time_plan_start=event.time_plan_start+timedelta(days=nextDayCount),
                            time_plan_end=event.time_plan_end+timedelta(days=nextDayCount),
                            time_exe_start=event.time_exe_start+timedelta(days=nextDayCount),
                            time_exe_end=event.time_exe_end+timedelta(days=nextDayCount),
                            finished=False)

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
                event.finished=finished


                event.put()
                self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title):
        if not title:
            return "Field is empty."
        else:
            return None
