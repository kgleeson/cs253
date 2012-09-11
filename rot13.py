import webapp2
import cgi

html="""
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, text=''):
        self.response.write(html % text)
    def rot13(self, text):
        return text.encode('rot13')

    def get(self):
        self.write_form()
    def post(self):
        text = cgi.escape(self.request.get('text'))
        self.write_form(self.rot13(text))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)
