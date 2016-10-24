import pycurl
from io import BytesIO

class GetResponse:
  buffer = BytesIO()
  def __init__(self, value):
    self.url = value
    print(self.url)
  def setbuf(self, value):
    self.buffer = value
    print(self.buffer)
  def request(self):
    c = pycurl.Curl()
    c.setopt(c.URL, self.url)
    c.setopt(c.WRITEDATA, self.buffer)
    c.perform()
    c.close()
    print(c)
  def get(self):
    self.body = self.buffer.getvalue()
    # Body is a string in some encoding.
    # In Python 2, we can print it without knowing what the encoding is.
    print(self.body.decode('iso-8859-1'))

body = GetResponse('http://pycurl.io/')
body.request()
body.get()
