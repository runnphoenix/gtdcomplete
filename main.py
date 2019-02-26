import webapp2

from models import User
from models import Event
from models import Project
from models import Context
from models import TimeCategory
from models import Oauth2Service

from handlers import Signup
from handlers import Login
from handlers import Logout
from handlers import Projects
from handlers import UnfinishedEvents
from handlers import TimeCategories
from handlers import TimeCategoryPage
from handlers import Contexts
from handlers import ProjectsJson
from handlers import EventSchedule
from handlers import NewProject
from handlers import NewTimeCategory
from handlers import NewContext
from handlers import ProjectPage
from handlers import ProjectPageJson
from handlers import ContextPage
from handlers import EventPage
from handlers import MainPage
from handlers import TimeStatistics
from handlers import Instructions
from handlers import LoginJson
from handlers import Today
from handlers import Collection

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/instructions', Instructions),
    ('/signup', Signup),
    ('/login', Login),
    ('/login.json', LoginJson),
    ('/logout', Logout),
    ('/project/new', NewProject),
    ('/timeCategory/new', NewTimeCategory),
    ('/context/new', NewContext),
    ('/event/schedule/([0-9]+)', EventSchedule),
    ('/projects/([0-9]+)', ProjectPage),
    ('/contexts/([0-9]+)', ContextPage),
    ('/event/([0-9]+)', EventPage),
    ('/projects', Projects),
    ('/unfinishedEvents', UnfinishedEvents),
    ('/timeCategories', TimeCategories),
    ('/timeCategories/([0-9]+)', TimeCategoryPage),
    ('/contexts', Contexts),
    ('/statistics', TimeStatistics),
    ('/projects.json', ProjectsJson),
    ('/today', Today),
    ('/collection', Collection),
    (Oauth2Service.decorator.callback_path, Oauth2Service.decorator.callback_handler()),
    ], debug=True)
