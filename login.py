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
    return not email or emailRE.match(email)

def verify_passwords(pass1, pass2):
    if pass1 == pass2:
        return True

class ThanksPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Thanks, %s!' % self.request.get('username'))

class MainPage(webapp2.RequestHandler):
    with open('login.html', 'rU') as f:
        html = f.read()

    def write_form(self, **kwargs):
        if not kwargs:
            kwargs_list = 'username|password|verify|email|usererror|'\
                        'passerror|verifyerror|emailerror'.split('|')
            kwargs = dict([(i, '') for i in kwargs_list])
        self.response.write(self.html % kwargs)

    def get(self):
        self.write_form()

    def post(self):
        data = {'username':'',
                'password':'',
                'verify':'',
                'email':'',
                'usererror':'',
                'passerror':'',
                'verifyerror':'',
                'emailerror':''}

        username = self.request.get('username')
        user_check = check_user(username)
        password = check_password(self.request.get('password'))
        verify = verify_passwords(password, self.request.get('verify'))
        email = self.request.get('email')
        email_check = check_email(email)
        if(user_check and password and verify and email_check):
            self.redirect('/thanks?username=%s' % username)
        else:
            if not user_check:
                data['usererror'] = "Username is not correct"
            if not password:
                data['passerror'] = "Password is not 3-20 chars long"
            if not verify:
                data['verifyerror'] = "Passwords do not match"
            if not email_check:
                data['emailerror'] = "Email address is not user@domain.tld"
            data['username'] = username
            data['email'] = email
            self.write_form(**data)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThanksPage)],
                              debug=True)
