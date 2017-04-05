import webapp2
import cgi
import re

form1="""
<!DOCTYPE html>
<html>
  <head>
	<title>User Signup</title>
	</head>
	<body>
		<h2>Signup</h2>
		<form method="post">
            <table>
                <tr>
    			<td ><label for ="username"> Username </label> </td>
                <td><input type="text" name="username" value="%(username)s"></td>
    			<td>	<span style="color: red">%(e_name)s</span></td>
                </tr>
                <tr>
    			<td> <label for ="password">Password</label></td>
                <td><input type="password" name="password"></td>
    			<td><span style="color: red">%(e_pass)s</span></td>
                </tr>
                <tr>
    			<td><label for ="verify">Verify Password</label></td>
                <td><input type="password" name="verify"></td>
    			<td><span style="color: red">%(e_verify)s</span></td>
                </tr>

                <tr>
    			<td><label for ="email">Email (optional)</label> </td>
                <td><input type="text" name="email" value="%(email)s"></td>
    			<td><span style="color: red">%(e_email)s</span></td>
                </tr>
            </table>
			<input type="submit">
		</form>
	</body>
</html>
"""

form2="""
<!DOCTYPE html>
<html>
	<head>
		<title>UserSignup - Welcome</title>
	</head>
	<body>
		<h2>Welcome, %s!</h2>
	</body>
</html>
"""

def escape_html(s):
	return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_name(s):
	return USER_RE.match(s)

def valid_pass(s):
	return PASS_RE.match(s)

def valid_email(s):
    if s == "":
        return True
    else:
        return EMAIL_RE.match(s)

def match_pass(p1, p2):
	return p1 == p2

class Signup(webapp2.RequestHandler):
	def write_form(self, username="", email="",
		           e_name="", e_pass="", e_verify="", e_email=""):
		self.response.out.write(form1 % {"username": escape_html(username),
			                             "email": escape_html(email),
			                             "e_name": e_name,
			                             "e_pass": e_pass,
			                             "e_verify": e_verify,
			                             "e_email": e_email})

	def get(self):
		self.write_form()

	def post(self):
		user_name = self.request.get('username')
		user_pass = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')

		name = valid_name(user_name)
		password = valid_pass(user_pass)
		verify = valid_pass(user_verify)
		email = valid_email(user_email)

		e_name = ''
		e_pass = ''
		e_verify = ''
		e_email = ''


		if not name:
			e_name = 'Please enter a valid name'
		if not password:
			e_pass = 'Please enter a valid password'
		if not match_pass(user_pass, user_verify):
			e_verify = 'The two passwords do not match'
		if not email:
			e_email = 'Please enter a valid email'

		if password and (not e_verify) and name and email:
			self.redirect('/welcome?username=%s' % user_name)
		else:
			self.write_form(user_name, user_email, e_name, e_pass, e_verify, e_email)

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(form2 % username)

app = webapp2.WSGIApplication([
	('/', Signup),
	('/welcome', WelcomeHandler)
], debug=True)
