import re

#Signin Verification Functions
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return EMAIL_RE.match(email)


#Hashing Functions

def make_salt():
      return ''.join(random.choice(string.letters) for x in xrange(5))

def make_hash(pw,salt=None):
  if not salt:
    salt = make_salt()
  tohash = salt + SECRET + str(pw)  
  #h = hashlib.sha256(tohash).hexdigest()
  h= hmac.new(str(salt+SECRET),str(pw),hashlib.sha256).hexdigest()
  return '%s|%s' % (salt,h)

def valid_hash(pw, h):
      salt = h.split("|")[0]
      hashed = make_hash(pw,salt)
      if h == hashed:
          return True