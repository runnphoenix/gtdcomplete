#/usr/bin/python

import accessControl
from handler import Handler

class Projects(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("projects.html")

    @accessControl.user_logged_in
    def post(self):
        pass
