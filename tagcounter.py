import pycurl
import sys
import getopt
from io import BytesIO
from bs4 import BeautifulSoup as BS

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
        self.enc = 'iso-8859-1'
        print("Inspected URL: {}".format(self.url))
    def encoding(self, value):
        self.enc = value
    def get(self):
        print("Encoding: {}".format(self.enc))
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.WRITEDATA, self.buffer)
        c.perform()
        c.close()
        self.body = self.buffer.getvalue()
        print(self.body.decode(self.enc))

def usage():
    print("""Example of usage:
          tagcounter tagcounter --help
          tagcounter --get 'google.com'
          tagcounter --view 'google.com'
          """)

def counter(html):
    soup = BS(html)
    for tag in soup.findAll():
        print(tag.name)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'g:v:e:h',
                               ['get=', 'view=', 'enc=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

url = None
enc = None
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-g', '--get'):
        url = arg
    elif opt in ('-v', '--view'):
        site = arg
    elif opt in ('-e', '--enc'):
        enc = arg
    else:
        usage()
        sys.exit(2)

if __name__ == '__main__':
    if url:
        response = GetResponse(url)
        if enc:
            response.encoding(enc)
        response.get()
        counter(response.body)
