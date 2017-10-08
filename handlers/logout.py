#!/usr/bin/python

from .handler import Handler


class Logout(Handler):

    def get(self):
        self.reset_cookie()
        self.redirect('/login')
