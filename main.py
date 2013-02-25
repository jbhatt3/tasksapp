#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import re
import user
import hashlib
import hmac
import string
import utils
#Initializes templating features of Jinja2 framework
template_dir = os.path.join(os.path.dirname(__file__))
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#Base handler contains basic templating functions 
class BaseHandler(webapp2.RequestHandler):
    # Writes string  
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    #returns template from string path with string substitution parameters in mapping called params
    def render_str(self,template, **params):
        template = jinja_environment.get_template(template)
        return template.render(params)

    #takes string template path and mapping of template paramters and renders them
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class FrontPageHandler(BaseHandler):
    def get(self):
        self.render("/templates/index.html")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("/templates/login.html")
    def post(self):
        email = self.request.get('email')
        password = self.request.get('passoword')
        self.write("Welcome %s" %password)

class RegisterHandler(BaseHandler):
    def get(self):
        template_values= {'username':"",
                         'password':"",
                         'verifypass':"",
                         'email':"",
                         'error_username':"",
                         'error_password':"",
                         'error_verify':"",
                         'error_email':""}
        self.render("/templates/register.html")
    def post(self):
        username=self.request.get('username')
        password = self.request.get('passoword')
        verify_pass=self.request.get('verify_pass')
        email = self.request.get('email')
        newUser = user.User(username=username, password=password, email=email)
        newUser.put()
        self.write("Welcome %s" %username)


template_values= {'username':"",
                         'password':"",
                         'verifypass':"",
                         'email':"",
                         'error_username':"",
                         'error_password':"",
                         'error_verify':"",
                         'error_email':""}
        self.write_self(template_values)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verifypass')
        email = self.request.get('email')

        params = {'username' : username,
                      'email' : email,
                      'error_username':"",
                      'error_password' : "",
                      'error_verify' : "",
                      'error_email' : ""}
        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.write_self(params)
        else:
          user_id_hash = self.register_user(username,password,email)
          if user_id_hash:
            self.response.headers.add_header("Set-Cookie", "user_id = %s; Path = /" %user_id_hash)
            self.redirect('/welcome')
          else:
            params['error_username'] = "This User already exists"
            self.write_self(params)





app = webapp2.WSGIApplication([('/', FrontPageHandler),
                                ('/login', LoginHandler),
                                ('/register', RegisterHandler)
                                ], debug=True)

