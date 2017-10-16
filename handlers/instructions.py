#!/usr/bin/python

from .handler import Handler


class Instructions(Handler):

    def get(self):
        self.render("instructions.html")
