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
rome
class EventPage(Handler):
    @accessControl.user_logged_in
    @accessControl.event_exist
    def get(self, event_id, event):
        self.render("eventPage.html",
            event = event,
            exeStartTime=datetime.now(rome),
            exeEndTime=datetime.now(rome))

    @accessControl.user_logged_in
    @accessControl.event_exist
    @accessControl.user_own_event
    @Oauth2Service.decorator.oauth_required
    def post(self, event_id, event):
        title, content, repeat, planStartTime, planEndTime, exeStartTime, exeEndTime, project, context, timeCategory, ChangeFinishState, ChangeScheduleState = self.get_page_info()

        if "Delete" in self.request.params:
            try:
                self.processCalendar(event, 'primary', 'delete')
                if event.finished:
                    self.processCalendar(event, self.get_execution_calendar_id(), 'delete')
            except HTTPError, e:
                self.redirect("/today")
            except TypeError, e:
                self.redirect("/today")
            else:
                self.redirect("/today")

            event.delete()
        elif "Change" in self.request.params:
            errorMessage = self.errMessage_1st_part(title, planStartTime, planEndTime, project, context)
            if errorMessage: # render errorMessage
                self.render("eventPage.html", event=event, exeStartTime=datetime.now(rome),exeEndTime=datetime.now(rome), errorMessage=errorMessage)
            else: # An event must be already scheduled(otherwise it remains in schedule page)
                # 1. set new event status locally
                event.title = title
                event.content = content
                event.repeat = repeat
                event.project = project
                event.context = context
                event.time_plan_start = planStartTime
                event.time_plan_end = planEndTime
                # 2. process calendar and event locally
                if not ChangeScheduleState and event.scheduled:
                    # update calendar and update event locally
                    self.processCalendar(event, 'primary', 'update')
                    event.put()
                    self.redirect("/event/%s" % str(event.key().id()))
                elif ChangeScheduleState and event.scheduled:
                    print"Here to retreat!"
                    # delete calendar event
                    self.processCalendar(event, 'primary', 'delete')
                    if event.finished:
                        self.processCalendar(event, self.get_execution_calendar_id(), 'delete')
                    # set event to unscheduled(to collection)
                    event.scheduled = False
                    if event.finished:
                        event.finished = False
                    event.repeat = '0000000'
                    event.project = self.get_inbox_project()
                    event.context = None
                    event.time_plan_start = None
                    event.time_plan_end = None
                    # update database and redirect
                    event.put()
                    self.redirect("/event/schedule/%s" % str(event.key().id()))
        else: # update exec calendar
            errorMessage_1st_part = self.errMessage_1st_part(title, planStartTime, planEndTime, project, context)
            errorMessage_2nd_part = self.errMessage_2nd_part(exeStartTime, exeEndTime, timeCategory)

            if errorMessage_1st_part or errorMessage_2nd_part:
                errorMessage = ''
                if errorMessage_1st_part:
                    errorMessage = errorMessage_1st_part
                else:
                    errorMessage = errorMessage_2nd_part
                self.render("eventPage.html", event=event, exeStartTime=datetime.now(rome),exeEndTime=datetime.now(rome), errorMessage=errorMessage)
            else: # no error, begin update exec calendar
                exe_calendar_id = self.get_execution_calendar_id()

                event.project = project
                event.context = context
                event.title = title
                event.content = content
                event.repeat = repeat
                event.time_plan_start = planStartTime
                event.time_plan_end = planEndTime
                #event.scheduled = ChangeScheduleState
                event.time_exe_start = exeStartTime
                event.time_exe_end = exeEndTime
                event.timeCategory = timeCategory
                #event.finished = ChangeFinishState

                if ChangeFinishState and (not event.finished):
                    # Create a new event according to the repeat settings when finish a repeat event
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
                            time_plan_start=event.time_plan_start + timedelta(days=nextDayCount),
                            time_plan_end=event.time_plan_end + timedelta(days=nextDayCount),
                            time_exe_start=event.time_exe_start + timedelta(days=nextDayCount),
                            time_exe_end=event.time_exe_end + timedelta(days=nextDayCount),
                            finished=ChangeFinishState,
                            scheduled=ChangeScheduleState)
                        # add new recurrent event to gcalendar
                        response = self.processCalendar(newEvent, 'primary', 'insert')
                        # Add to Database
                        newEvent.google_calendar_plan_id = response['id']
                        newEvent.put()
                    # The first time an event marked finished, add it to Execution Calendar
                    response = self.processCalendar(event, exe_calendar_id, 'insert')
                    event.google_calendar_exec_id = response['id']
                    event.finished = True
                    event.put()
                    self.redirect("/event/%s" % str(event.key().id()))
                elif not ChangeFinishState and event.finished: # update Execution calendar
                    response = self.processCalendar(event, exe_calendar_id, 'update')
                    event.put()
                    self.redirect("/event/%s" % str(event.key().id()))
                elif ChangeFinishState and event.finished:
                    #delete from calendar and unfinish event
                    self.processCalendar(event, exe_calendar_id, 'delete')
                    event.finished = False
                    event.put()
                    self.redirect("/event/%s" % str(event.key().id()))
                else: #shouldn't do aynthing
                    self.redirect("/event/%s" % str(event.key().id()))

    def processCalendar(self, event, calendarName, operationType):
        if calendarName == 'primary':
            eventStartTime = event.time_plan_start
            eventEndTime = event.time_plan_end
            eventCalendarId = event.google_calendar_plan_id
        elif calendarName == self.get_execution_calendar_id():
            eventStartTime = event.time_exe_start
            eventEndTime = event.time_exe_end
            eventCalendarId = event.google_calendar_exec_id
        else:
            return None

        request = None
        response = None

        if operationType == 'update':
            gEventRequest = Oauth2Service.service.events().get(calendarId=calendarName, eventId=eventCalendarId)
            gEvent = gEventRequest.execute(http=Oauth2Service.decorator.http())
            gEvent['summary'] = event.title
            gEvent['description'] = event.content
            gEvent['start']['dateTime'] = eventStartTime.strftime("%Y-%m-%dT%H:%M:%S")
            gEvent['end']['dateTime'] = eventEndTime.strftime("%Y-%m-%dT%H:%M:%S")
            request = Oauth2Service.service.events().update(calendarId=calendarName, eventId=eventCalendarId, body=gEvent)
            response = request.execute(http=Oauth2Service.decorator.http())
        elif operationType == 'insert':
            gEvent = {
                'summary': event.title,
                'location': '',
                'description': event.content,
                'start': {
                    'dateTime': eventStartTime.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': rome_tz_str,
                },
                'end': {
                    'dateTime': eventEndTime.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': rome_tz_str,
                },
            }
            request = Oauth2Service.service.events().insert(calendarId=calendarName, body=gEvent)
            response = request.execute(http=Oauth2Service.decorator.http())
        elif operationType == 'delete':
            request = Oauth2Service.service.events().delete(calendarId=calendarName, eventId=eventCalendarId)
            response = request.execute(http=Oauth2Service.decorator.http())
        return response

    def errMessage_1st_part(self, title, planStartTime, planEndTime, project, context):
        if title == '':
            return 'Title can not be empty.'
        if planStartTime == '':
            return 'Plan Start time can not be empty.'
        if planEndTime == '':
            return "Plan end time can not be empty."
        if planStartTime >= planEndTime:
            return "Plan time range is invalid."
        if not project:
            return "Must choose a project type."
        if not context:
            return "Must choose a context type."
        return None

    def errMessage_2nd_part(self, exeStartTime, exeEndTime, category):
        if exeStartTime == '':
            return 'Execution start time can not be empty.'
        if exeEndTime == '':
            return "Execution end time can not be empty."
        if exeStartTime >= exeEndTime:
            return "Execution time range is invalid."
        if not category:
            return "Must choose a category type."
        return None

    def get_execution_calendar_id(self):
        exe_calendar_id = ''
        request = Oauth2Service.service.calendarList().list()
        calendars = request.execute(
            http=Oauth2Service.decorator.http())
        for calendar in calendars['items']:
            if calendar['summary'] == 'Execution':
                exe_calendar_id = calendar['id']
        return exe_calendar_id

    def get_page_info(self):
        title = self.request.get("title")
        content = self.request.get("content")
        repeat = ""
        for i in range(7):
            rep = self.request.get("repeat" + str(i))
            if (rep != "on"):
                repeat = repeat + '0'
            else:
                repeat = repeat + '1'

        if self.request.get('planStartTimeText'):
            planStartTime = datetime.strptime(
                self.request.get("planStartTimeText"), "%Y%m%d%H%M")
        elif self.request.get('planStartTime'):
            planStartTime = datetime.strptime(
                self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
        else:
            planStartTime = ''

        if self.request.get('planEndTimeText'):
            planEndTime = datetime.strptime(
                self.request.get("planEndTimeText"), "%Y%m%d%H%M")
        elif self.request.get('planEndTime'):
            planEndTime = datetime.strptime(
                self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
        else:
            planEndTime = ''

        if self.request.get('exeStartTimeText'):
            exeStartTime = datetime.strptime(
                self.request.get("exeStartTimeText"), "%Y%m%d%H%M")
        elif self.request.get('exeStartTime'):
            exeStartTime = datetime.strptime(
                self.request.get("exeStartTime"), "%Y-%m-%dT%H:%M")
        else:
            exeStartTime = ''

        if self.request.get('exeEndTimeText'):
            exeEndTime = datetime.strptime(
                self.request.get("exeEndTimeText"), "%Y%m%d%H%M")
        elif self.request.get('exeEndTime'):
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

        if self.request.get("FinishMent") == 'on':
            ChangeFinishState = True
        else:
            ChangeFinishState = False

        if self.request.get("Schedulement") == 'on':
            ChangeScheduleState = True
        else:
            ChangeScheduleState = False

        return (title, content, repeat, planStartTime, planEndTime, exeStartTime, exeEndTime, project, context, timeCategory, ChangeFinishState, ChangeScheduleState)

    def get_inbox_project(self):
        pro = None
        for project in self.user.projects:
            if project.name == 'inbox':
                pro = project
        return pro
