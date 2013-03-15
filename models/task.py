from google.appengine.ext import db

def taskKey(name = "default"):
	return db.Key.from_path('Tasks',name)


class Task(db.Model):
	title = db.StringProperty()
	dateCreated = db.DateTimeProperty(auto_now_add=True)	
	description = db.StringProperty()
	priority = db.StringProperty()