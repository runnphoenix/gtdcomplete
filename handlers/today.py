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
                    if event.time_plan_start.date() == today or event.time_exe_end.date() == today:
                        if event.finished == True:
                            timeD = self.times_diff(event.time_exe_end, event.time_exe_start)
                            self.insert_event_by_time(events_today['finished'], event, timeD, 'exe')
                        else:
                            timeD = self.times_diff(event.time_plan_end, event.time_plan_start)
                            self.insert_event_by_time(events_today['unfinished'], event, timeD, 'plan')
                            #if len(events_today['unfinished']) == 0:
                                #events_today['unfinished'].append([event, timeD])
                            #3else:
                                #for i in range(len(events_today['unfinished'])):
                                    #if events_today['unfinished'][i][0].time_plan_start <= event.time_plan_start:
                                        #i += 1
                                    #else:
                                        #events_today['unfinished'].insert(i, [event, timeD])
        return events_today

    def times_diff(self, time1, time2):
        if time1 < time2:
            return
        else:
            return (time1 - time2).seconds / 60

    def insert_event_by_time(self, events, event, duration, phase):
        if len(events) == 0:
            events.append([event,duration])
        else:
            if phase == 'plan':
                for i in range(len(events)):
                    if events[i][0].time_plan_start < event.time_plan_start:
                        i += 1
                    else:
                        print "plan add"
                        events.insert(i,[event, duration])
                        break
            elif phase == 'exe':
                for i in range(len(events)):
                    if events[i][0].time_exe_start <= event.time_exe_start:
                        i += 1
                    else:
                        print 'exe add'
                        events.insert(i, [event, duration])
                        break
            else:
                return

    @accessControl.user_logged_in
    def post(self):
        pass
