#/usr/bin/python

from . import accessControl
from .handler import Handler


class Projects(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("projects.html", projects=self.projects_without_inbox())

    @accessControl.user_logged_in
    def post(self):
        pass

    def projects_without_inbox(self):
        projects = []
        for project in self.user.projects:
            if not project.name == 'inbox':
                projects.append(project)
        return projects
