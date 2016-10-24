import pycurl
from io import BytesIO

class GetResponse:
  """
  This class help you to get source code of any Web-page
     Use:
       GetResponse.encoding(value) - to change encoding for decoding HTML page
       GetResponse.get() - to get source code of Web-page
  """
  def __init__(self, value):
    self.url = value
    self.buffer = BytesIO()
    self.enc = 'utf-8'
    print("Inspected URL: {}".format(self.url))
  def encoding(self, value):
    self.enc = value
    print("Encoding has been changed to {}".format(self.enc))
  def get(self):
    c = pycurl.Curl()
    c.setopt(c.URL, self.url)
    c.setopt(c.WRITEDATA, self.buffer)
    c.perform()
    c.close()
    body = self.buffer.getvalue()
    print(body.decode(self.enc))

url = input("Please specify URL for inspecting [pycurl.io]: ")
url = url or 'pycurl.io'
response = GetResponse(url)
body = response.get()
