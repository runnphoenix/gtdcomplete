#!/usr/bin/python

from handler import Handler
from models import Event
from models import Project
from models import Context
from models import TimeCategory
from models import Oauth2Service
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
    @Oauth2Service.decorator.oauth_required
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

        if self.request.get('planStartTime'):
            planStartTime = datetime.strptime(self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
        else:
            planStartTime = ''
        if self.request.get('planEndTime'):
            planEndTime = datetime.strptime(self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
        else:
            planEndTime = ''
        exeStartTime = datetime.strptime(self.request.get("exeStartTime"), "%Y-%m-%dT%H:%M")
        exeEndTime = datetime.strptime(self.request.get("exeEndTime"), "%Y-%m-%dT%H:%M")

        project = None
        projectName = self.request.get('projects')
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

        errorMessage = self.erMessage(title, exeStartTime, exeEndTime)

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

            # Add to google calendar
            if planStartTime and planEndTime:
                gEvent = {
                    'summary': event.title,
                    'location': '',
                    'description': event.content,
                    'start': {
                        'dateTime': event.time_plan_start.strftime("%Y-%m-%dT%H:%M:%S"),
                        'timeZone': 'Asia/Shanghai',
                    },
                    'end': {
                        'dateTime': event.time_plan_end.strftime("%Y-%m-%dT%H:%M:%S"),
                        'timeZone': 'Asia/Shanghai',
                    },
                    #'recurrence': [
                        #'RRULE:FREQ=DAILY;COUNT=2'
                    #],
                    #'reminders': {
                        #'useDefault': False,
                        #'overrides': [
                            #{'method': 'email', 'minutes': 24 * 60},
                            #{'method': 'popup', 'minutes': 10},
                        #],
                    #},
                }
                request = Oauth2Service.service.events().insert(calendarId='primary', body=gEvent)
                response = request.execute(http=Oauth2Service.decorator.http())
                event.google_calendar_plan_id = response['id']
            # Add to Database
            event.put()

            self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title, exeStartTime, exeEndTime):
        if not title:
            return "Field is empty."
        elif ' ' in title:
            return "No space allowed in title."
        elif (not exeStartTime) or (not exeEndTime):
            return "Execution time can not be empty."
        else:
            return None
