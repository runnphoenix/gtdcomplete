#/usr/bin/python

from . import accessControl
from .handler import Handler

class TimeCategories(Handler):

    #@accessControl.user_logged_in
    def get(self):
        self.render(
            "timeCategories.html",
            timeCategories=self.user.timeCategories)

    @accessControl.user_logged_in
    def post(self):
        pass
