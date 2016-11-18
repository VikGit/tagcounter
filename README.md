# Tagcounter

Tagcounter - is a program for counting HTML tags on web pages. It's written on Python 3, so please ensure that you have required version of Python before using.

**Note**: Probably you'll have to install 'libcurl-devel' package for installing the app. For Centos, it looks like:

```sh
$ sudo yum install libcurl-devel
```

# Installation 
Install existed package:

```sh
$ git clone https://github.com/VikGit/tagcounter.git
$ cd tagcounter/dist 
$ sudo pip3 install tagcounter-1.0.0.tar.gz
```

Install by source:

```sh
$ git clone https://github.com/VikGit/tagcounter.git
$ cd tagcounter
$ sudo python3 setup.py sdist
$ cd dist
$ sudo pip3 install tagcounter-1.0.0.tar.gz
```

# Usage

Common options:

```sh
usage: tagcounter.py [-h] [-g URL] [-v VURL] [-e ENC] [-s SYNFILE]
                     [--home HOME] [--version]
This program inspect a Web-page and returt the number of tags
optional arguments:
  -h, --help            show this help message and exit
  -g URL, --get URL     URL for inspecting
  -v VURL, --view VURL  URL for extracting information from DB
  -e ENC, --enc ENC     Encoding for inspecting URL
  -s SYNFILE, --synfile SYNFILE
                        Path for file with synonyms
  --home HOME           Define the place for storing all tachnical info
  --version             show program's version number and exit
```

Tagcounter has two modes:
  - visual
  - console

Example or running in visual mode:

```sh
$ tagcounter
$ tagcounter --home 'tmp/myhome'
$ tagcounter --enc 'utf8' --synfile 'myfavoritesites.yaml'
```

Example of running in console mode:

```sh
$ tagcounter --get 'google.com'
$ tagcounter --view 'yandex.com'
$ tagounter --get 'google.com' --enc 'utf8' --synfile 'myfavoritesites.yaml'
```
