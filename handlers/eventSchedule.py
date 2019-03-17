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
        # Collect information
        title, content, repeat, planStartTime, planEndTime, project, context = self.get_page_info()

        # Process requests
        if "Delete" in self.request.params:
            event.delete()
            self.redirect("/collection")
        elif "Change" in self.request.params: # only change title and content
            errorMessage = self.errMessage_1st_part(title, content)
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
                    planStartTime=planStartTime,
                    planEndTime=planEndTime,
                    errorMessage=errorMessage)
            else:
                event.title = title
                event.content = content
                event.put()
                self.render(
                    "eventSchedule.html",
                    projects=self.projects_without_inbox(),
                    contexts=self.user.contexts,
                    timeCategories=self.user.timeCategories,
                    repeat=repeat,
                    eventTitle=title,
                    eventContent=content,
                    finished=False,
                    planStartTime=planStartTime,
                    planEndTime=planEndTime,
                    errorMessage=errorMessage)
        else: #Update
            errorMessage = self.errMessage_2nd_part(planStartTime, planEndTime, project, context)
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
                    planStartTime=planStartTime,
                    planEndTime=planEndTime,
                    errorMessage=errorMessage)
            else:
                event.title = title
                event.content = content
                event.repeat = repeat
                event.time_plan_start = planStartTime
                event.time_plan_end = planEndTime
                event.project = project
                event.context = context

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
                event.put()

                #self.redirect("/event/schedule/%s" % str(event.key().id()))
                self.redirect("/collection")

    def projects_without_inbox(self):
        projects = []
        for project in self.user.projects:
            if not project.name == 'inbox':
                projects.append(project)
        return projects

    def errMessage_1st_part(self, title, content):
        if title == '':
            return 'Title can not be empty.'
        if content == '':
            return 'Content can not be empty.'
        return None

    def errMessage_2nd_part(self, planStartTime, planEndTime, project, context):
        if planStartTime == '':
            return "Start time can not be empty."
        if planEndTime == '':
            return "End time can not be empty."
        if planStartTime >= planEndTime:
            return "Time range is invalid."
        if not project:
            return "Must choose a project type."
        if not context:
            return "Must choose a context type."
        return None

    def get_page_info(self):
        title = self.request.get("title")
        content = self.request.get("content")

        repeat = ""
        for i in range(7):
            rep = self.request.get("repeat"+str(i))
            if (rep != "on"):
                repeat = repeat + '0'
            else:
                repeat = repeat + '1'

        if self.request.get('planStartTimeText'):
            planStartTime = datetime.strptime(self.request.get("planStartTimeText"), "%Y%m%d%H%M")
        elif self.request.get('planStartTime'):
            planStartTime = datetime.strptime(self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
        else:
            planStartTime = ''

        if self.request.get('planEndTimeText'):
            planEndTime = datetime.strptime(self.request.get("planEndTimeText"), "%Y%m%d%H%M")
        elif self.request.get('planEndTime'):
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
        return (title, content, repeat, planStartTime, planEndTime, project, context)
