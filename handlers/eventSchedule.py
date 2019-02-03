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

class EventSchedule(Handler):
    @accessControl.user_logged_in
    @accessControl.event_exist
    def get(self, event_id, event):
        self.render(
            "eventSchedule.html",
            projects=self.projects_without_inbox(),
            contexts=self.user.contexts,
            timeCategories=self.user.timeCategories,
            repeat='0000000',
            eventTitle=event.title,
            eventContent=event.content,
            finished=False,
            planStartTime=datetime.now(pytz.timezone('Asia/Shanghai')),
            planEndTime=datetime.now(pytz.timezone('Asia/Shanghai'))
        )

    @accessControl.user_logged_in
    @accessControl.event_exist
    @Oauth2Service.decorator.oauth_required
    def post(self, event_id, event):
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

        project = None
        projectName = self.request.get('projects')
        for pro in self.user.projects:
            if pro.name == projectName:
                project = pro

        context = None
        contextName = self.request.get("contexts")
        for con in self.user.contexts:
            if con.name == contextName:
                context = con

        errorMessage = self.errMessage(title, planStartTime, planEndTime, project, context)
        if errorMessage:
            self.render(
                "eventSchedule.html",
                projects=self.projects_without_inbox(),
                contexts=self.user.contexts,
                timeCategories=self.user.timeCategories,
                repeat=repeat,
                eventTitle=title,
                eventContent=content,
                finished=False,
                errorMessage=errorMessage,
                planStartTime=planStartTime,
                planEndTime=planEndTime)
        else:
            event.title = title
            event.content = content
            event.repeat = repeat
            event.time_plan_start = planStartTime
            event.time_plan_end = planEndTime
            event.project = project
            event.context = context
            event.put()

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

            self.redirect("/event/%s" % str(event.key().id()))

    def projects_without_inbox(self):
        projects = []
        for project in self.user.projects:
            if not project.name == 'inbox':
                projects.append(project)
        return projects

    def errMessage(self, title, planStartTime, planEndTime, project, context):
        if title == '':
            return 'Title can not be empty.'
        if planStartTime == '':
            return 'Start time can not be empty.'
        if planEndTime == '':
            return "End time can not be empty."
        if planStartTime >= planEndTime:
            return "Time range is invalid."
        if not project:
            return "Must choose a project type."
        if not context:
            return "Must choose a context type."
        return None