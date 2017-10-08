#!/usr/bin/python

from .handler import Handler
from models import Project
from google.appengine.ext import db
from . import accessControl


class NewProject(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("newProject.html")

    @accessControl.user_logged_in
    def post(self):
        name = self.request.get('name')
        if not name:
            errorMessage = 'name can not be empty'
            self.render('newProject.html', errorMessage=errorMessage)
        elif ' ' in name:
            errorMessage = 'No space allowed.'
            self.render('newProject.html', errorMessage=errorMessage)
        else:
            # find project names already exist
            project_exist = False
            for project in self.user.projects:
                if project.name == name:
                    project_exist = True
                    errorMessage = 'project already exist, find another name.'
                    self.render('newProject.html', errorMessage=errorMessage)

            if project_exist == False:
                project = Project(name=name, user=self.user)
                project.put()
                self.redirect('/project/%s' % str(project.key().id()))
