#!/usr/bin/python

from google.appengine.ext import db
from .user import User


class TimeCategory(db.Model):
    name = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, collection_name='timeCategories')
