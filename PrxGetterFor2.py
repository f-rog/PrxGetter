# -*- coding: utf-8 -*-
import requests as r
import re
from bs4 import BeautifulSoup
from random import randint
import urllib2
import socket

def putfile(filename, content):
    file_ = open(filename, 'a')
    file_.write(content)
    file_.close()

url = "http://www.httptunnel.ge/ProxyListForFree.aspx"
rx  = r.get(url)
data = rx.text
soup = BeautifulSoup(data)
goodprxs = []
for link in soup.find_all('a'):
    a = link.get('href')
    if "ProxyChecker" in a:
        b = a.split("?p=")
        if len(b) > 1:
            goodprxs.append(b[1])

def is_bad_proxy(pip):    
    try:
        proxy_handler = urllib2.ProxyHandler({'http': pip})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(opener)
        req=urllib2.Request('http://www.google.com')
        sock=urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        return e.code
    except Exception, detail:
        return True
    return False

outname = "output"+str(randint(1,199999))+".txt"

def main():
    socket.setdefaulttimeout(1)
    proxyList = goodprxs

    for currentProxy in proxyList:
        if is_bad_proxy(currentProxy) == False:
            dab = "LIVE / %s" % (currentProxy)+"\n"
            putfile(outname,dab)

if __name__ == '__main__':
    main()
