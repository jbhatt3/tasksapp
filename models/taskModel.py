from google.appengine.ext import db

def taskAncestorKey(userId, listName = "default"):
	return db.Key.from_path('User',userId, 'List',listName)


class Task(db.Model):
	title = db.StringProperty()
	description = db.TextProperty()
	dueDate = db.StringProperty()
	fixedDueDate = db.StringProperty()
	priority = db.StringProperty()
	userId = int()
	dateCreated = db.DateTimeProperty(auto_now_add=True)