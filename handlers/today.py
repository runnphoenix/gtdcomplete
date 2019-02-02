#/usr/bin/python

from . import accessControl
from .handler import Handler


class Today(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("today.html", projects=self.user.projects)

    @accessControl.user_logged_in
    def post(self):
        pass
