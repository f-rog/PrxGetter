# -*- coding: utf-8 -*-
"""
Usage (in case you didn't read the GitHub README):
    MODES:
        * 1: Scrapes and checks proxies from HTTPTunnel.ge.
        * 2: Tries to scrape and check proxies from a given source.
        * 3: Checks proxies from a given file.
    ARGUMENTS:
        * -1 (Sets the mode to 1) -- Mode 1 does not require additional arguments.
        * -2 (Sets the mode to 2)
            Additional arguments:
                The source URL to scrape the proxies from. (No '-' required)
        * -3 (Sets the mode to 3)
            Additional arguments:
                The source file to check the proxies from. (No '-' required)
        * -p (Prints the progress of the proxie checking) -- OPTIONAL
    EXAMPLES OF USE:
        ex1.-
            >>> python PrxGetter.py -1
        Doing this will only scrape and check the proxies from the original URL (HTTPTunnel.ge)
        ex2.-
            >>> python PrxGetter.py -2 http://pagefullofproxies.com -p
        Doing this will try to scrape the proxies from <<pagefullofproxies.com>> and print the progress.

"""
import requests as r
import re
from bs4 import BeautifulSoup
from random import randint
import urllib2
import socket
import sys

# ---- START OF BASE FUNCTIONS ----
def put_file(filename, content): # This functions purpose is to write (not overwrite) some given content into a given file
    file_ = open(filename, 'a')
    file_.write(content)
    file_.close()

def read_file(filename): # This functions purpose is to read and split the file by the end of every line and return it as an array.
    file_ = open(filename, 'r').read().split('\n')
    return file_

def CheckProxies(list_,output_name): # Checks a whole list and uses the given output name
    def CheckProxie(proxy_ip): # Just checks an individual proxie. 
        try: # Tries to open google.com with the given proxie.
            proxy_handler = urllib2.ProxyHandler({'http': proxy_ip})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req=urllib2.Request('http://www.google.com')
            sock=urllib2.urlopen(req)
        # -- START OF ERROR CASES --
        except urllib2.HTTPError, e:
            return e.code
        except Exception, detail:
            return True
        # -- END OF ERROR CASES --
        return False # If opening google succeeds, the proxie is live and the function will return False.

    def main(): # Main function to start the proxie checking
        socket.setdefaulttimeout(1) # Timeout for the proxie test.
        proxyList = list_
        for currentProxy in proxyList:
            if "-p" in sys.argv[1:]:
                if CheckProxie(currentProxy) == False:
                    result = "[*] LIVE / %s" % (currentProxy)+"\n"
                    print result
                    put_file(output_name, result)
                else:
                    print("[*] DEAD /"+str(currentProxy)+"\n")
            else:
                if CheckProxie(currentProxy) == False:
                    result = "LIVE / %s" % (currentProxy)+"\n"
                    put_file(output_name, result)
    if __name__ == '__main__':
        main()
# ---- END OF BASE FUNCTIONS ----

print("""
   ___          _____    __  __            
  / _ \_____ __/ ______ / /_/ /____ ____   
 / ___/ __\ \ / (_ / -_/ __/ __/ -_/ __/   
/_/  /_/ /_\_\\___/\__/\__/\__/\__/_/      

""")

def mode1():
    try:
        site  = r.get("http://www.httptunnel.ge/ProxyListForFree.aspx")
    except:
        print("Is HTTPTunnel.ge offline?")
    else:
        data = site.text
        # -- START OF BEAUTIFUL SOUP CONSTRUCTOR --
        features="html.parser"
        soup = BeautifulSoup(data,features)
        # -- END OF BEAUTIFUL SOUP CONSTRUCTOR --
        proxy_list = []
        for link in soup.find_all('a'):
            all_hrefs = link.get('href')
            if "ProxyChecker" in all_hrefs:
                good_line = all_hrefs.split("?p=")
                if len(good_line) > 1:
                    proxy_list.append(good_line[1])
        output_name = "output"+str(randint(1,199999))+".txt"
        print("This might take a while . . .")
        CheckProxies(proxy_list,output_name)
        print("Output saved on "+output_name)

def mode2(source_url):
    if "://" not in source_url:
        source_url = "http://"+source_url
    try:
        site = r.get(source_url)
    except:
        print("An error has been encountered.")
    else:
        data = site.text
        proxie_expression = ur"((?:\d{1,3}\.){3}\d{1,3}):(\d+)" # RegEx to match any proxie.
        matches = re.findall(proxie_expression,data)
        good_list = []
        if len(matches) > 1:
            for match in matches:
                proxy_ip = str(match[0])+":"+str(match[1])
                good_list.append(proxy_ip)
            output_name = "output-"+str(randint(1,199999))+".txt"
            print("This might take a while . . .")
            CheckProxies(good_list,output_name) 
            print("Output saved on "+output_name)
        else:
            print("No proxies found in the source.")

def mode3(source_file):
    list_ = read_file(source_file)
    if len(list_) == 0:
        print("No proxies")
    else:
        output_name = "output"+str(randint(1,199999))+".txt"
        try:
            CheckProxies(list_,output_name) 
        except:
            print("Invalid proxies / Fatal error")
        else:
            print("Output saved on "+output_name)


if sys.argv[1] == "-1":
    mode1()
elif sys.argv[1] == "-2":
    mode2(sys.argv[2])
elif sys.argv[1] == "-3":
    mode3(sys.argv[2])
else:
    print("Error.")