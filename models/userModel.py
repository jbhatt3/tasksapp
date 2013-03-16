from google.appengine.ext import db

class User(db.Model):
	email = db.StringProperty()
	username = db.StringProperty()
	passHashed = db.StringProperty()
