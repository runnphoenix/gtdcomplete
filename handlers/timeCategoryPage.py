#!/usr/bin/python

from .handler import Handler
from models import TimeCategory
from . import accessControl


class TimeCategoryPage(Handler):

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def get(self, timeCategory_id, timeCategory):
        self.render("timeCategoryPage.html", timeCategory=timeCategory)

    @accessControl.user_logged_in
    @accessControl.timeCategory_exist
    def post(self, timeCategory_id, timeCategory):
        for event in timeCategory.events:
            event.delete()
        timeCategory.delete()
        self.redirect("/timeCategories")
