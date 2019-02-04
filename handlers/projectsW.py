#/usr/bin/python

from . import accessControl
from .handler import Handler

from datetime import datetime, timedelta
import pytz

class ProjectsW(Handler):

    @accessControl.user_logged_in
    @accessControl.project_exist
    def get(self, project_id, project):
        (finished_events, unfinished_events) = self.eventsInContainer(project)
        self.render("projectsW.html",
            projects=self.projects_without_inbox(),
            project_name=project.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')))

    @accessControl.user_logged_in
    def post(self):
        pass

    def projects_without_inbox(self):
        projects = []
        for project in self.user.projects:
            if not project.name == 'inbox':
                projects.append(project)
        return projects

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
