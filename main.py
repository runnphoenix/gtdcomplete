
import webapp2

from models import User
from models import Event
from models import Project
from models import Context

from handlers import Signup
from handlers import Login
from handlers import Logout
from handlers import Welcome
from handlers import NewEvent
from handlers import NewProject
from handlers import NewContext
from handlers import ProjectPage
from handlers import ContextPage
#from handlers import EditEvent
#from handlers import DeleteEvent
from handlers import EventPage
#from handlers import Events
from handlers import MainPage


app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/signup', Signup),
	('/welcome', Welcome),
	('/login', Login),
	('/logout', Logout),
	('/project/new', NewProject),
	('/contex/new', NewContext),
	('/event/new', NewEvent),
	('/project/([0-9]+)', ProjectPage),
	('/context/([0-9]+)', ContextPage),
    ('/event/([0-9]+)', EventPage)
], debug=True)
