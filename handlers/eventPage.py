#!/usr/bin/python

from .handler import Handler
from models import Event
from . import accessControl
from datetime import datetime, date, time, timedelta
from models import Oauth2Service
from google.appengine.ext import db


def events_key(name="default"):
    return db.Key.from_path("events", name)


class EventPage(Handler):

    @accessControl.user_logged_in
    @accessControl.event_exist
    def get(self, event_id, event):
        self.render("eventPage.html", event=event)

    @accessControl.user_logged_in
    @accessControl.event_exist
    @accessControl.user_own_event
    @Oauth2Service.decorator.oauth_required
    def post(self, event_id, event):
        if "Delete" in self.request.params:
            # add delete sync to gcalendar
            request = Oauth2Service.service.events().delete(calendarId='primary', eventId=event.google_calendar_plan_id)
            response = request.execute(http=Oauth2Service.decorator.http())
            # Delete event from database
            event.delete()
            self.redirect("/projects")
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
                planStartTime = datetime.strptime(self.request.get("planStartTime"), "%Y-%m-%dT%H:%M")
            else:
                planStartTime = ''
            if self.request.get('planEndTime'):
                planEndTime = datetime.strptime(self.request.get("planEndTime"), "%Y-%m-%dT%H:%M")
            else:
                planEndTime = ''
            exeStartTime = datetime.strptime(
                self.request.get("exeStartTime"),
                "%Y-%m-%dT%H:%M")
            exeEndTime = datetime.strptime(
                self.request.get("exeEndTime"),
                "%Y-%m-%dT%H:%M")

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
                    finished=False)
                self.render("eventPage.html", event=event)
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
                                'dateTime':
                                    newEvent.time_plan_start.strftime("%Y-%m-%dT%H:%M:%S"),
                                'timeZone': 'Asia/Shanghai',
                            },
                            'end': {
                                'dateTime':
                                    newEvent.time_plan_end.strftime("%Y-%m-%dT%H:%M:%S"),
                                'timeZone': 'Asia/Shanghai',
                            },
                        }
                        request = Oauth2Service.service.events().insert(
                            calendarId='primary', body=gEvent)
                        response = request.execute(http=Oauth2Service.decorator.http())
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
                            'timeZone': 'Asia/Shanghai',
                        },
                        'end': {
                            'dateTime':
                            exeEndTime.strftime(
                                "%Y-%m-%dT%H:%M:%S"),
                            'timeZone': 'Asia/Shanghai',
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
                    gEventRequest = Oauth2Service.service.events().get(calendarId=exe_calendar_id, eventId=event.google_calendar_exec_id)
                    gEvent = gEventRequest.execute(http=Oauth2Service.decorator.http())
                    gEvent['summary'] = event.title
                    gEvent['description'] = event.content
                    gEvent['start']['dateTime'] = event.time_exe_start.strftime("%Y-%m-%dT%H:%M:%S")
                    gEvent['end']['dateTime'] = event.time_exe_end.strftime("%Y-%m-%dT%H:%M:%S")
                    request = Oauth2Service.service.events().update(calendarId=exe_calendar_id, eventId=event.google_calendar_plan_id, body=gEvent)
                    response = request.execute(http=Oauth2Service.decorator.http())
                elif (not finished) and (not event.finished):
                    # update primary calendar
                    pass
                else: # (not finished) and event.finished
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
                gEventRequest = Oauth2Service.service.events().get(calendarId='primary', eventId=event.google_calendar_plan_id)
                gEvent = gEventRequest.execute(http=Oauth2Service.decorator.http())
                gEvent['summary'] = event.title
                gEvent['description'] = event.content
                gEvent['start']['dateTime'] = event.time_plan_start.strftime("%Y-%m-%dT%H:%M:%S")
                gEvent['end']['dateTime'] = event.time_plan_end.strftime("%Y-%m-%dT%H:%M:%S")
                request = Oauth2Service.service.events().update(calendarId='primary', eventId=event.google_calendar_plan_id, body=gEvent)
                response = request.execute(http=Oauth2Service.decorator.http())

                # Add event to database
                event.put()
                self.redirect("/event/%s" % str(event.key().id()))

    def erMessage(self, title):
        if not title:
            return "Field is empty."
        else:
            return None
