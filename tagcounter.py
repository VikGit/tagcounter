import pycurl, sys, getopt, os, time, yaml, argparse
from tkinter import *
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
    except BaseException:
        return syn

parser = argparse.ArgumentParser(description='This program inspect a Web-page \
                                              and returt the number of tags')
parser.add_argument('-g', '--get', dest='url', default=None, type=str,
                    help='URL for inspecting')
parser.add_argument('-v', '--view', dest='vurl', type=str,
                    help='URL for extracting information from DB')
parser.add_argument('-e', '--enc', default=None, type=str,
                    help='Encoding for inspecting URL')
parser.add_argument('-s', '--synfile', default='synonyms.yaml', type=str,
                    help='Path for file with synonyms')
args = parser.parse_args()

if __name__ == '__main__':
    if args.url:
        url = check_syn(args.synfile, args.url)
        response = GetResponse(url)
        if args.enc:
            response.encoding(args.enc)
        response.get()
        counter(response.body)
        log(url)
    else:
        root=Tk()
        root.mainloop()
