#!/usr/bin/python3
import pycurl, sys, os, time, yaml, argparse, sqlite3, pickle
from tkinter import *
from tkinter.ttk import *
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
        return self.enc
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
    def insert(self, site, url, tags):
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
                      select site,url,tags, timestamp from {} where site=? limit 1
                      """.format(self.table), (site,)
                      )
        res = self.cur.fetchall()
        if res:
            for row in res:
                l = list(row)
                l[2] = pickle.loads(l[2])
                print(l)
            info=l
        else:
            message = "Sorry, but record for {} site is absent in the database".format(site)
            print(message)
            info = message
        return info
    def last(self, number):
        last = self.cur.execute(
                              """
                              select site from {} order by id desc limit {}
                              """.format(self.table, number)
                              )
        res = []
        for row in last:
            res.append(row[0])
        return res
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
    restb=tb(sort, headers=['Tags', 'Numbers'], tablefmt='psql')
    print(restb)
    return res, restb

def log(url, lpath='logs'):
    if not os.path.exists(lpath):
        os.makedirs(lpath)
    with open('{}/{}'.format(lpath, 'access.log'), 'a+') as file:
        file.write('{} {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S'), url))

def check_syn(yfile, syn):
    if not os.path.isfile(yfile):
        def_syn = {'ggl': 'google.com', 'ydx': 'yandex.ru'}
        with open(yfile, 'w') as syn_file:
            yaml.dump(def_syn, syn_file, default_flow_style=False)
    try:
        with open(yfile, 'r') as stream:
            allsyn = yaml.load(stream)
        try:
            synurl = allsyn[syn]
            return synurl, syn
        except:
            return syn, None
    except IOError:
        print("File {} doesn't exist! \nUse --synfile option to specify other synonyms file".format(yfile))
        sys.exit(1)


def download(url, synfile, enc, tktext=None, st=None, visual=False):
    try:
        url, orig_syn = check_syn(synfile, url)
        response = GetResponse(url)
        if enc:
            response.encoding(enc)
        encod = response.enc
        response.get()
        tags, tagstb = counter(response.body)
        log(url)
        db = DB()
        if orig_syn:
            db.insert(orig_syn, url, tags)
        else:
            db.insert(url, url, tags)
            db.close()
    except BaseException as error:
        tagstb = error
    if visual:
        tktext.delete('1.0', END)
        tktext.insert(END, tagstb)
        st["text"] = "Enc: " + encod

def view(vurl, synfile, tktext=None, visual=False):
    try:
        url, orig_syn = check_syn(synfile, vurl)
        db = DB()
        if orig_syn:
            res = db.select(orig_syn)
            db.close()
        else:
            res = db.select(url)
            db.close()
    except BaseException as error:
        res = error
    if visual:
       tktext.delete('1.0', END)
       tktext.insert(END, res)

def visual(title, synfile, enc):
    text = 'None'
    win = Tk()
    win.title(title)
    # "Enter the website" section
    textFrame = Frame(win)
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Enter the website:"
    entryLabel.grid(row=0, column=0, padx=2, pady=2)
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 21
    entryWidget.grid(row=0, column=1, padx=2, pady=2)
    textFrame.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)

    #Scrollbar and test field
    scroll = Scrollbar(win)
    text = Text(win, height=20, width=40)
    scroll.grid(row=3, column=3, sticky=N+S+E+W)
    text.grid(row=3, column=0, columnspan=2)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    # Status bar
    stLabel = Label(win)
    stLabel["text"] = "Krasheninnikov, 2016"
    stLabel.grid(row=4, column=0, columnspan=2)

    # Buttons for dowloads and shows from db
    down = Button(win, text="Download")
    down.grid(row=1, column=0, padx=2, pady=2, sticky=N+S+E+W)
    down["command"] = lambda: download(entryWidget.get(), synfile, enc, text, stLabel, True)
    showfromdb = Button(win, text="Show from DB")
    showfromdb.grid(row=1, column=1, padx=2, pady=2, sticky=N+S+E+W)
    showfromdb["command"] = lambda: view(entryWidget.get(), synfile, text, True)

    #Combobox
    db = DB()
    list1 = db.last(5)
    db.close()
    if not list1:
        list1 = ['google.com', 'yandex.ru']
    combobox = Combobox(win, values = list1, state='readonly', style='TButton', justify='center')
    combobox.set(list1[0])
    combobox.grid(row=2, column=1, padx=2, pady=2, sticky=N+S+E+W)
    choice = Button(win, text="Select")
    choice["command"] = lambda: download(combobox.get(), synfile, enc, text, stLabel, True)
    choice.grid(row=2, column=0, padx=2, pady=2, sticky=N+S+E+W)

    win.mainloop()

def ch_pwd(path):
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

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
    parser.add_argument('--home', default=os.path.expanduser('~') + '/__tagcache__', type=str,
                        help='Define the place for storing all tachnical info')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    ch_pwd(args.home)

    if args.url:
        download(args.url, args.synfile, args.enc)
    elif args.vurl:
        view(args.vurl, args.synfile)
    else:
        visual('TagCounter v1.0', args.synfile, args.enc)

if __name__ == '__main__':
    main()
