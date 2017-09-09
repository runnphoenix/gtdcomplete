
import webapp2

from models import User
from models import Event
from models import Project
from models import Context
from models import TimeCategory

from handlers import Signup
from handlers import Login
from handlers import Logout
from handlers import Projects
from handlers import TimeCategories
from handlers import ProjectsJson
from handlers import NewEvent
from handlers import NewProject
from handlers import NewTimeCategory
from handlers import NewContext
from handlers import ProjectPage
from handlers import TimeCategoryPage
from handlers import ContextPage
#from handlers import EditEvent
#from handlers import DeleteEvent
from handlers import EventPage
#from handlers import Events
from handlers import MainPage

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/signup', Signup),
	('/login', Login),
	('/logout', Logout),
	('/project/new', NewProject),
	('/timeCategory/new', NewTimeCategory),
	('/context/new', NewContext),
	('/event/new', NewEvent),
	('/project/([0-9]+)', ProjectPage),
	('/timeCategory/([0-9]+)', TimeCategoryPage),
	('/context/([0-9]+)', ContextPage),
	('/event/([0-9]+)', EventPage),
	('/projects', Projects),
	('/timeCategories', TimeCategories),
	('/projects.json', ProjectsJson)
], debug=True)
