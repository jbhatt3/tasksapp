from google.appengine.ext import db

def taskKey(userId, listName = "default"):
	return db.Key.from_path('User',userId, 'List',listName)


class Task(db.Model):
	title = db.StringProperty()
	description = db.TextProperty()
	dueDate = db.StringProperty
	priority = db.StringProperty()
	userId = db.IntProperty()
	dateCreated = db.DateTimeProperty(auto_now_add=True)	
