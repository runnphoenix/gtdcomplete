#/usr/bin/python

from . import accessControl
from .handler import Handler

from datetime import datetime, timedelta
import pytz
shanghai = pytz.timezone('Asia/Shanghai')
rome = pytz.timezone('Europe/Rome')

class ProjectPage(Handler):

    @accessControl.user_logged_in
    @accessControl.project_exist
    def get(self, project_id, project):
        (finished_events, unfinished_events) = self.eventsInContainer(project)
        self.render("projectPage.html",
            projects=self.projects_without_inbox(),
            project_name=project.name,
            finished_events=finished_events,
            unfinished_events=unfinished_events,
            startDate=datetime.now(rome),
            endDate=datetime.now(rome))

    @accessControl.user_logged_in
    @accessControl.project_exist
    def post(self, project_id, project):
        if 'Delete' in self.request.params:
            for event in project.events:
                event.delete()
            project.delete()
            self.redirect("/projects")
        elif "Update" in self.request.params:
            project_name = self.request.get('project_name')
            project.name = project_name
            project.put()
            (finished_events, unfinished_events) = self.eventsInContainer(project)
            self.render("projectPage.html",
                projects=self.projects_without_inbox(),
                project_name=project.name,
                finished_events=finished_events,
                unfinished_events=unfinished_events,
                startDate=datetime.now(rome),
                endDate=datetime.now(rome))
        else: #Look up throught date
            startDate = datetime.strptime(self.request.get("startDate"),"%Y-%m-%d")
            endDate = datetime.strptime(self.request.get("endDate"), "%Y-%m-%d")
            if startDate > endDate:
                errMessage = "End date MUST be bigger than start date."
                self.render("projectPage.html",
                    projects=self.projects_without_inbox(),
                    project_name=project.name,
                    finished_events=[],
                    unfinished_events=[],
                    startDate=datetime.now(rome),
                    endDate=datetime.now(rome),
                    errMessage=errMessage)
            else:  # with duration
                days = (endDate - startDate).days + 1
                dates = [(startDate + timedelta(i)).date() for i in range(days)]
                (finished_events, unfinished_events) = self.eventsInContainer(project, dates)
                self.render("projectPage.html",
                    projects=self.projects_without_inbox(),
                    project_name=project.name,
                    finished_events=finished_events,
                    unfinished_events=unfinished_events,
                    startDate=datetime.now(rome),
                    endDate=datetime.now(rome))

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
                if event.time_plan_start:
                    if not unfinished_events.get(str(event.time_plan_start.date())):
                        unfinished_events[str(event.time_plan_start.date())] = [event]
                    else:
                        unfinished_events[str(event.time_plan_start.date())].append(event)
        return (finished_events, unfinished_events)
