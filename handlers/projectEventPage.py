#!/usr/bin/python

from .handler import Handler
from models import Event
from . import accessControl
from datetime import datetime, date, time, timedelta
from models import Oauth2Service
from google.appengine.ext import db
from urllib2 import HTTPError

import pytz
shanghai_tz_str='Asia/Shanghai'
rome_tz_str='Europe/Rome'
shanghai = pytz.timezone(shanghai_tz_str)
rome = pytz.timezone(rome_tz_str)

def events_key(name="default"):
    return db.Key.from_path("events", name)

class ProjectEventPage(Handler):

    @accessControl.user_logged_in
    @accessControl.event_exist_and_belong_Project
    def get(self, project_id, project, event_id, event):rome
        (finished_events, unfinished_events) = self.eventsInContainer(project)
        self.render("projectEventPage.html",
            projects = self.projects_without_inbox(),
            project = project,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            event=event,
            startDate=datetime.now(rome),
            endDate=datetime.now(rome),
            exeStartTime=datetime.now(rome),
            exeEndTime=datetime.now(rome)

    def projects_without_inbox(self):
        projects = []
        for project in self.user.projects:
            if not project.name == 'inbox':
                projects.append(project)
        return projects

    @accessControl.user_logged_in
    @accessControl.event_exist
    @accessControl.user_own_event
    @Oauth2Service.decorator.oauth_required
    def post(self, project_id, project, event_id, event):
        if "Delete" in self.request.params:
            event.delete()
            # add delete sync to gcalendar
            try:
                request = Oauth2Service.service.events().delete(
                    calendarId='primary', eventId=event.google_calendar_plan_id)
                response = request.execute(http=Oauth2Service.decorator.http())
            except HTTPError, e:
                self.redirect("/projects/project_id")
            except TypeError, e:
                self.redirect("/projects/project_id")
            else:
                self.redirect("/projects/project_id")

            # TODO: delete Execution calendar events
            # have to judge first: wether added to calendar, which calendars?
        else:
            title = self.request.get("title")
            content = self.request.get("content")
            repeat = ""
            for i in range(7):
                rep = self.request.get("repeat" + str(i))
                if (rep != "on"):
                    repeat = repeat + '0'
                else:
                    repeat = repeat + '1'

            if self.request.get('planStartTime'):
                planStartTime = datetime.strptime(
                    self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
            else:
                planStartTime = ''
            if self.request.get('planEndTime'):
                planEndTime = datetime.strptime(
                    self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
            else:
                planEndTime = ''
            if self.request.get('exeStartTime'):
                exeStartTime = datetime.strptime(
                    self.request.get("exeStartTime"), "%Y-%m-%dT%H:%M")
            else:
                exeStartTime = ''
            if self.request.get('exeEndTime'):
                exeEndTime = datetime.strptime(
                    self.request.get("exeEndTime"), "%Y-%m-%dT%H:%M")
            else:
                exeEndTime = ''

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

            errorMessage = self.errMessage(title, planStartTime,
                planEndTime, exeStartTime, exeEndTime, project,
                context, timeCategory)

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
                    finished=False)
                self.render("projecteventPage.html",
                    projects=self.user.projects,
                    project=project,
                    event=event,
                    errorMessage=errorMessage)
            else:
                exe_calendar_id = ''
                request = Oauth2Service.service.calendarList().list()
                calendars = request.execute(
                    http=Oauth2Service.decorator.http())
                for calendar in calendars['items']:
                    if calendar['summary'] == 'Execution':
                        exe_calendar_id = calendar['id']

                if finished and (not event.finished):
                    if event.repeat != "0000000":
                        # find date of next event
                        weekDayth = event.time_plan_start.date().weekday()
                        nextDayCount = -1
                        doubleRepeat = repeat + repeat
                        for i in range(weekDayth + 1, 14):
                            if doubleRepeat[i] == '1':
                                nextDayCount = i - weekDayth
                                break
                        # Create new Event
                        newEvent = Event(
                            project=event.project,
                            timeCategory=event.timeCategory,
                            context=event.context,
                            user=self.user,
                            title=event.title,
                            parent=events_key(),
                            content=event.content,
                            repeat=event.repeat,
                            time_plan_start=event.time_plan_start +
                            timedelta(days=nextDayCount),
                            time_plan_end=event.time_plan_end +
                            timedelta(days=nextDayCount),
                            time_exe_start=event.time_exe_start +
                            timedelta(days=nextDayCount),
                            time_exe_end=event.time_exe_end +
                            timedelta(days=nextDayCount),
                            finished=False)
                        # add new recurrent event to gcalendar
                        gEvent = {
                            'summary': newEvent.title,
                            'location': '',
                            'description': newEvent.content,
                            'start': {
                                'dateTime': newEvent.time_plan_start.strftime("%Y-%m-%dT%H:%M:%S"),
                                'timeZone': rome_tz_str,
                            },
                            'end': {
                                'dateTime': newEvent.time_plan_end.strftime("%Y-%m-%dT%H:%M:%S"),
                                'timeZone': rome_tz_str,
                            },
                        }
                        request = Oauth2Service.service.events().insert(
                            calendarId='primary', body=gEvent)
                        response = request.execute(
                            http=Oauth2Service.decorator.http())
                        # Add to Database
                        newEvent.google_calendar_plan_id = response['id']
                        newEvent.put()

                    # The first time an event marked finished, add it to
                    # Execution Calendar
                    gEvent = {
                        'summary': event.title,
                        'location': '',
                        'description': event.content,
                        'start': {
                            'dateTime':
                            exeStartTime.strftime(
                                    "%Y-%m-%dT%H:%M:%S"),
                            'timeZone': rome_tz_str,
                        },
                        'end': {
                            'dateTime':
                            exeEndTime.strftime(
                                "%Y-%m-%dT%H:%M:%S"),
                            'timeZone': rome_tz_str,
                        },
                    }
                    request = Oauth2Service.service.events().insert(
                        calendarId=exe_calendar_id, body=gEvent)
                    response = request.execute(
                        http=Oauth2Service.decorator.http())
                    event.google_calendar_exec_id = response['id']
                    # update primary calendar(At last)
                elif finished and event.finished:
                    # update Primary calendar(At last)
                    # update Execution calendar
                    gEventRequest1 = Oauth2Service.service.events().get(
                        calendarId=exe_calendar_id, eventId=event.google_calendar_exec_id)
                    gEvent1 = gEventRequest1.execute(
                        http=Oauth2Service.decorator.http())
                    gEvent1['summary'] = event.title
                    gEvent1['description'] = event.content
                    gEvent1['start']['dateTime'] = event.time_exe_start.strftime(
                        "%Y-%m-%dT%H:%M:%S")
                    gEvent1['end']['dateTime'] = event.time_exe_end.strftime(
                        "%Y-%m-%dT%H:%M:%S")
                    request = Oauth2Service.service.events().update(
                        calendarId=exe_calendar_id, eventId=event.google_calendar_exec_id, body=gEvent1)
                    response = request.execute(
                        http=Oauth2Service.decorator.http())
                elif (not finished) and (not event.finished):
                    # update primary calendar
                    pass
                else:  # (not finished) and event.finished
                    # delete event from Execution calendar
                    # update primary calendar
                    pass

                event.project = project
                event.timeCategory = timeCategory
                event.context = context
                event.user = self.user
                event.title = title
                event.content = content
                event.repeat = repeat
                event.time_plan_start = planStartTime
                event.time_plan_end = planEndTime
                event.time_exe_start = exeStartTime
                event.time_exe_end = exeEndTime
                event.finished = finished

                # update event to primary calendar
                if event.time_plan_start and event.time_plan_end:
                    gEventRequest = Oauth2Service.service.events().get(
                        calendarId='primary', eventId=event.google_calendar_plan_id)
                    gEvent = gEventRequest.execute(
                        http=Oauth2Service.decorator.http())
                    gEvent['summary'] = event.title
                    gEvent['description'] = event.content
                    gEvent['start']['dateTime'] = event.time_plan_start.strftime(
                        "%Y-%m-%dT%H:%M:%S")
                    gEvent['end']['dateTime'] = event.time_plan_end.strftime(
                        "%Y-%m-%dT%H:%M:%S")
                    request = Oauth2Service.service.events().update(
                        calendarId='primary', eventId=event.google_calendar_plan_id, body=gEvent)
                    response = request.execute(
                        http=Oauth2Service.decorator.http())

                # Add event to database
                event.put()
                self.redirect("/projects/%s/%s" % str(project_id),str(event.key().id()))

    def errMessage(self, title, planStartTime, planEndTime, exeStartTime, exeEndTime, project, context, category):
        if title == '':
            return 'Title can not be empty.'
        if planStartTime == '':
            return 'Plan Start time can not be empty.'
        if planEndTime == '':
            return "Plan end time can not be empty."
        if planStartTime >= planEndTime:
            return "Plan time range is invalid."
        if exeStartTime == '':
            return 'Execution start time can not be empty.'
        if exeEndTime == '':
            return "Execution end time can not be empty."
        if exeStartTime >= exeEndTime:
            return "Execution time range is invalid."
        if not project:
            return "Must choose a project type."
        if not context:
            return "Must choose a context type."
        if not category:
            return "Must choose a category type."
        return None

    def eventsInContainer(self, container, lookupDates=[]):
        finished_events = {}
        unfinished_events = {}
        for event in container.events:
            if event.finished:
                if event.time_exe_start.date() in lookupDates:
                    if not finished_events.get(str(event.time_exe_start.date())):
                        finished_events[str(event.time_exe_start.date())] = [event]
                    else:
                        finished_events[str(event.time_exe_start.date())].append(event)
            else:
                if not unfinished_events.get(str(event.time_plan_start.date())):
                    unfinished_events[str(event.time_plan_start.date())] = [event]
                else:
                    unfinished_events[str(event.time_plan_start.date())].append(event)
        return (finished_events, unfinished_events)
