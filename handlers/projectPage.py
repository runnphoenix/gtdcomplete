#!/usr/bin/python

from .handler import Handler
from models import Project
from . import accessControl
from datetime import datetime,timedelta
import pytz

class ProjectPage(Handler):

    @accessControl.user_logged_in
    @accessControl.project_exist
    def get(self, project_id, project):
        (finished_events, unfinished_events) = self.eventsInContainer(project)
        self.render("projectPage.html",
            project_name=project.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            endDate=datetime.now(pytz.timezone('Asia/Shanghai')),
            xxx=self.request.params)


    @accessControl.user_logged_in
    @accessControl.project_exist
    def post(self, project_id, project):
        if 'Delete Project' in self.request.params:
            for event in project.events:
                event.delete()
            project.delete()
            self.redirect("/projects")
        elif 'Update Name' in self.request.params: #Update
            project_name = self.request.get('project_name')
            project.name = project_name
            project.put()

            (finished_events, unfinished_events) = self.eventsInContainer(project)
            self.render("projectPage.html",
                project_name=project.name,
                finished_events=finished_events,
                unfinished_events=unfinished_events,
                startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                endDate=datetime.now(pytz.timezone('Asia/Shanghai')))
        else: #Look up throught date
            startDate = datetime.strptime(self.request.get("startDate"),"%Y-%m-%d")
            endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
            if startDate > endDate:
                errMessage = "End date MUST be bigger than start date."
                self.render("projectPage.html",
                    project_name=project.name,
                    finished_events=[],
                    unfinished_events=[],
                    startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    endDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    errMessage=errMessage)
            else:  # with duration
                days = (endDate - startDate).days + 1
                dates = (startDate + timedelta(i) for i in range(days))
                (finished_events, unfinished_events) = self.eventsInContainer(project, dates)
                self.render("projectPage.html",
                    project_name=project.name,
                    finished_events=finished_events,
                    unfinished_events=unfinished_events,
                    startDate=datetime.now(pytz.timezone('Asia/Shanghai')),
                    endDate=datetime.now(pytz.timezone('Asia/Shanghai')))

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
                if not unfinished_events.get(str(event.time_exe_start.date())):
                    unfinished_events[str(event.time_exe_start.date())] = [event]
                else:
                    unfinished_events[str(event.time_exe_start.date())].append(event)
        return (finished_events, unfinished_events)
