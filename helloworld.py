import webapp2

form='''
<label>
<form method='post'>
    <label>
        What is your name?
        <input name='name'>
    </label>
    <br>
    <input type='SUBMIT'>
</form>
</label>
'''
page='''
<p>Hello, %s!</p>
'''

def valid_name(name):
    if name:
        return name

class MainPage(webapp2.RequestHandler):
    def write_form(self, error='', name=''):
        self.response.write(form % {'error': error})

    def get(self):
        self.write_form()
    def post(self):
        name = valid_name(self.request.get('name'))
        if name:
          self.response.write(page % name)
        else:
            self.write_form('Thats not right')

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
