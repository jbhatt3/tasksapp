from google.appengine.ext import db

def taskListAncestorKey(userId):
	return db.Key.from_path('User',userId)


class TaskList(db.Model):
	userId = int()
	dateCreated = db.DateTimeProperty(auto_now_add=True)