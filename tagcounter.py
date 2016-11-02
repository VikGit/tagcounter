import pycurl, sys, os, time, yaml, argparse, sqlite3, pickle
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
    def __init__(self, url):
        self.url = url
        self.buffer = BytesIO()
        self.enc = 'iso-8859-1'
        print('Inspected URL: {}'.format(self.url))
    def encoding(self, enc):
        self.enc = enc
    def get(self):
        print('Encoding: {}'.format(self.enc))
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.FOLLOWLOCATION, True)
        c.setopt(c.WRITEDATA, self.buffer)
        c.perform()
        c.close()
        self.body = self.buffer.getvalue()

class DB:
    """
    This class uses for operations with sqlite3 database
        Use:
            DB.insert(site, url, tags) - to add the records to DB
            DB.select(site) - to get info about site from DB
    """
    def __init__(self, dbname='db'):
        self.dbname = dbname
        self.table = 'taginfo'
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()
    def insert(self, site, url, tags):
        self.cur.execute(
                """
                create table if not exists {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site CHAR,
                url TEXT,
                tags TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                """.format(self.table)
                )
        ptags = pickle.dumps(tags)
        v = (site, url, ptags,)
        self.cur.execute(
                """
                insert into {} (site, url, tags) values (?, ?, ?)
                """.format(self.table), v
                )
        self.con.commit()
        return self.cur
    def select(self, site):
        self.cur.execute(
                      """
                      select site,url,tags, timestamp from {} where site=?
                      """.format(self.table), (site,)
                      )
        res = self.cur.fetchall()
        if res:
            for row in res:
                l = list(row)
                l[2] = pickle.loads(l[2])
                print(l)
        else:
            print("Sorry, but record for {} site is absent in the database".format(site))
    def close(self):
        self.cur.close()
        self.con.close()

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
    return res

def log(url, lpath='logs'):
    if not os.path.exists(lpath):
        os.makedirs(lpath)
    with open('{}/{}'.format(lpath, 'access.log'), 'a+') as file:
        file.write('{} {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))

def check_syn(yfile, syn):
    try:
        with open(yfile, 'r') as stream:
            allsyn = yaml.load(stream)
        try:
            synurl = allsyn[syn]
            return synurl, syn
        except BaseException:
            return syn, None
    except:
        print("File {} doesn't exist!".format(yfile))

def main():
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
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.url:
        url, orig_syn = check_syn(args.synfile, args.url)
        response = GetResponse(url)
        if args.enc:
            response.encoding(args.enc)
        response.get()
        tags = counter(response.body)
        log(url)
        db = DB()
        if orig_syn:
            db.insert(orig_syn, url, tags)
        else:
            db.insert(url, url, tags)
        db.close()
    elif args.vurl:
        url, orig_syn = check_syn(args.synfile, args.vurl)
        db = DB()
        if orig_syn:
            db.select(orig_syn)
        else:
            db.select(url)
        db.close()
    else:
        root=Tk()
        root.mainloop()

if __name__ == '__main__':
    main()
