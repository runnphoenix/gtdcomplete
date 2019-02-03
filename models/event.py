#!/usr/bin/python

from google.appengine.ext import db
from .project import Project
from .user import User
from .context import Context
from .timeCategory import TimeCategory


class Event(db.Model):
    title = db.StringProperty(required=True)
    content = db.StringProperty(required=False)
    repeat = db.StringProperty(required=False)
    finished = db.BooleanProperty(required=True)
    time_plan_start = db.DateTimeProperty(auto_now_add=False)
    time_plan_end = db.DateTimeProperty(auto_now_add=False)
    time_exe_start = db.DateTimeProperty(auto_now_add=False)
    time_exe_end = db.DateTimeProperty(auto_now_add=False)

    context = db.ReferenceProperty(Context, collection_name='events')
    user = db.ReferenceProperty(User, collection_name='events')
    project = db.ReferenceProperty(Project, collection_name='events')
    timeCategory = db.ReferenceProperty(
        TimeCategory,
        collection_name='events')

    google_calendar_plan_id = db.StringProperty()
    google_calendar_exec_id = db.StringProperty()
