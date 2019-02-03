#/usr/bin/python

from . import accessControl
from .handler import Handler
from datetime import date

class Today(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("today.html", events=self.events_today())

    def events_today(self):
        events_today = {}
        events_today['finished'] = []
        events_today['unfinished'] = []
        today = date.today()
        for project in self.user.projects:
            events = project.events
            if events is not None:
                for event in events:
                    if event.time_plan_start and event.time_plan_end:
                        if event.time_plan_start.date() == today or event.time_exe_end.date() == today:
                            if event.finished == True:
                                timeD = self.times_diff(event.time_exe_end, event.time_exe_start)
                                self.insert_event_by_time(events_today['finished'], event, timeD, 'exe')
                            else:
                                timeD = self.times_diff(event.time_plan_end, event.time_plan_start)
                                self.insert_event_by_time(events_today['unfinished'], event, timeD, 'plan')
        return events_today

    # Calculate time diff in minutes
    def times_diff(self, time1, time2):
        if time1 < time2:
            return
        else:
            return (time1 - time2).seconds / 60

    # Sort events by time when adding new event
    def insert_event_by_time(self, events, event, duration, phase):
        if len(events) == 0:
            events.append([event,duration])
        else:
            if phase == 'plan':
                i = 0
                while events[i][0].time_plan_start < event.time_plan_start:
                    i += 1
                events.insert(i, [event, duration])
            elif phase == 'exe':
                i = 0
                while events[i][0].time_exe_start < event.time_exe_start:
                    i += 1
                events.insert(i, [event, duration])
            else:
                return

    @accessControl.user_logged_in
    def post(self):
        pass
