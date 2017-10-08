#/usr/bin/python

from . import accessControl
from .handler import Handler


class Contexts(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("contexts.html", contexts=self.user.contexts)

    @accessControl.user_logged_in
    def post(self):
        pass
