import webapp2
import jinja2
import os
import re
import hashlib
import hmac
import string
import utils
import main
from models import user
from models import task

#Initializes templating features of Jinja2 framework
template_dir = os.path.join(os.path.dirname(__file__))
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class BaseTaskHandler(main.BaseHandler)

class HomePageHandler(BaseTaskHandler):
    def renderStart(self,template, errors = {}, fields = {}):
        template_values = self.createTemplate_values(errors,fields)
        self.render(template,**template_values)
    def get(self):
        user = self.getUserFromCookie()
        fields = {"username":user.username
                  }
        self.renderStart("/templates/homepage.html",fields=fields)



class NewTaskHandler(BaseTaskHandler):
    def post(self):
        title = self.request.get("title")
        description = self.request.get("description")
        dueDate = self.request.get("dueDate")
        priority = self.request.get("priority")
        newTask = task.Task(title = title,description = description, dueDate = dueDate, priority = priority, parent=task.taskKey())
        newTask.put()
        self.redirect('/homepage')                  




app = webapp2.WSGIApplication([('/homepage',HomePageHandler),
                                ("/homepage/newtask",NewTaskHandler)
                                ], debug=True)