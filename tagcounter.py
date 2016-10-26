import pycurl, sys, getopt, os, time, yaml
from io import BytesIO
from bs4 import BeautifulSoup as BS
from tabulate import tabulate as tb

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
        print('Inspected URL: {}'.format(self.url))
    def encoding(self, value):
        self.enc = value
    def get(self):
        print('Encoding: {}'.format(self.enc))
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.WRITEDATA, self.buffer)
        c.perform()
        c.close()
        self.body = self.buffer.getvalue()
        #print(self.body.decode(self.enc))

def usage():
    print("""Example of usage:
          tagcounter tagcounter --help
          tagcounter --get 'google.com'
          tagcounter --view 'google.com'
          """)

def counter(html):
    tags = []
    res = {}
    soup = BS(html, 'html.parser')
    for tag in soup.findAll():
        tags.append(tag.name)
    uniq = list(set(tags))
    for tag in uniq:
        res[tag] = tags.count(tag)
    sort=sorted(res.items(), key=lambda x:(x[1],x[0]))
    print(tb(sort, headers=['Tags', 'Numbers'], tablefmt='psql'))

def log(url, lpath='logs'):
    if not os.path.exists(lpath):
        os.makedirs(lpath)
    with open('{}/{}'.format(lpath, 'access.log'), 'a+') as file:
        file.write('{} {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))

def check_syn(yfile, syn):
    with open(yfile, 'r') as stream:
        allsyn = yaml.load(stream)
    try:
        synurl = allsyn[syn]
        print('Synonym {} found!'.format(syn))
        return synurl
    except BaseException as bexc:
        return syn

try:
    opts, args = getopt.getopt(sys.argv[1:], 'g:v:e:s:h',
                               ['get=', 'view=', 'enc=', 'synfile=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

url = None
enc = None
synfile = 'synonyms.yaml'
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
    elif opt in ('-s', '--synfile'):
        synfile = arg
    else:
        usage()
        sys.exit(2)

if __name__ == '__main__':
    if url:
        link = check_syn(synfile, url)
        response = GetResponse(link)
        if enc:
            response.encoding(enc)
        response.get()
        counter(response.body)
        log(link)
