import webapp2
import re


userRE = re.compile('^[a-zA-Z0-9_-]{3,20}$')
def check_user(user):
    if userRE.match(user):
        return user
passRE = re.compile('^.{3,20}$')
def check_password(password):
    if passRE.match(password):
        return password
emailRE = re.compile('^[\S]+@[\S]+\.[\S]+$')
def check_email(email):
    return not email or  emailRE.match(email)
def verify_passwords(pass1, pass2):
    if pass1 == pass2:
        return True

class ThanksPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Thanks, %s!' % self.request.get('username'))

class MainPage(webapp2.RequestHandler):
    data = {'username':'',
            'password':'',
            'verify':'',
            'email':'',
            'usererror':'',
            'passerror':'',
            'verifyerror':'',
            'emailerror':''}

    with open('login.html', 'rU') as f:
        html = f.read()
    def write_form(self, **kwargs):
        if not kwargs:
            kwargs = self.data
        self.response.write(self.html % kwargs)

    def get(self):
        self.write_form(**self.data)
    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        username = check_user(user_username)
        password = check_password(user_password)
        verify = verify_passwords(user_password, user_verify)
        email = check_email(user_email)

        if(username and password and verify and email):
            self.redirect('/thanks?username=%s' % username)
        else:
            if not username:
                self.data['usererror'] = "Username is not correct"
            if not password:
                self.data['passerror'] = "Password is not 3-20 chars long"
            if not verify:
                self.data['verifyerror'] = "Passwords do not match"
            if not email:
                self.data['emailerror'] = "Email address is not user@domain.tld"
            self.data['username'] = user_username
            self.data['email'] = user_email
            self.write_form(**self.data)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThanksPage)],
                              debug=True)
