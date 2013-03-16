import webapp2
import jinja2
import os
import re
import hashlib
import hmac
import string
import utils
import main
from models import userModel
from models import taskModel

#Initializes templating features of Jinja2 framework
template_dir = os.path.join(os.path.dirname(__file__))
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class BaseTaskHandler(main.BaseHandler):
    def getTasks(self, userId):
        tasksQuery = taskModel.Task.all()
        tasksQuery = tasksQuery.ancestor(taskModel.taskKey(userId))
        tasksQuery = tasksQuery.order('dateCreated')
        return tasksQuery

class HomePageHandler(BaseTaskHandler):
    def renderStart(self,template, errors = {}, fields = {}):
        template_values = self.createTemplate_values(errors,fields)
        self.render(template,**template_values)
        
    def get(self):
        user = self.getUserFromCookie()
        userId = user.key().id()
        userTasks = self.getTasks(userId)
        fields = {"user":user,
                  "userTasks":userTasks
                  }
        self.renderStart("/templates/homepage.html",fields=fields)



class NewTaskHandler(BaseTaskHandler):
    def post(self):
        title = self.request.get("title")
        description = self.request.get("description")
        dueDate = self.request.get("dueDate")
        priority = self.request.get("priority")
        user = self.getUserFromCookie()
        userId = user.key().id()
        newTask = taskModel.Task(title = title,description = description, dueDate = dueDate, priority = priority, userId = userId, parent=taskModel.taskKey(userId))
        newTask.put()
        self.redirect('/homepage')                  




app = webapp2.WSGIApplication([('/homepage',HomePageHandler),
                                ("/homepage/newtask",NewTaskHandler)
                                ], debug=True)