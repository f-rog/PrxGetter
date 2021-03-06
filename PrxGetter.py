# -*- coding: utf-8 -*-
import requests as r
import re
import socket, sys, os, time, datetime, argparse, colorama
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup

#initialize colorama
colorama.init()
white = Fore.WHITE
green = Fore.GREEN
red = Fore.RED
yellow = Fore.YELLOW
end = Style.RESET_ALL
info = Fore.YELLOW + '[!]' + Style.RESET_ALL
prog = Fore.MAGENTA + '[&]' + Style.RESET_ALL
que = Fore.BLUE + '[*]' + Style.RESET_ALL
bad = Fore.RED + '[-]' + Style.RESET_ALL
good = Fore.GREEN + '[+]' + Style.RESET_ALL
run = Fore.WHITE + '[~]' + Style.RESET_ALL

# ---- START OF BASE FUNCTIONS ----
def put_file(filename, content): # This functions purpose is to write (not overwrite) some given content into a given file
	file_ = open(filename, 'a')
	file_.write(content)
	file_.close()

def read_file(filename): # This functions purpose is to read and split the file by the end of every line and return it as an array.
	file_ = open(filename, 'r').read()
	return file_

def find_proxies(file_content):
	proxie_expression = r"((?:\d{1,3}\.){3}\d{1,3}):(\d+)"
	matches = re.findall(proxie_expression,file_content)
	good_list = []
	if len(matches) > 1:
		for match in matches:
			proxy_ip = str(match[0])+":"+str(match[1])
			good_list.append(proxy_ip)
	return good_list

def CheckProxies(list_,output_name): # Checks a whole list and uses the given output name
	def CheckProxie(proxy_ip): # Just checks an individual proxie. 
		try: # Tries to open google.com with the given proxie.
			header = {'User-Agent': 'Mozilla/5.0'}
			req= r.get('http://www.google.com', headers=header, proxies={'http' : proxy_ip}, timeout=1)
			if req.status_code == 200:
				return False
		# -- START OF ERROR CASES --
			else:
				return True
		except Exception:
			return True
		# -- END OF ERROR CASES --

	def main(): # Main function to start the proxie checking
		proxyList = list_
		progress = 1
		output_stream = sys.stdout
		for currentProxy in proxyList:
			if CheckProxie(currentProxy) == False:
				progress += 1 
				result = good + currentProxy + " - Working"
				print (result)
				put_file(output_name, currentProxy + " - Working"+"\n")				
			else:
				progress += 1
				print (bad + currentProxy + " - Not working")
			if float(progress*100) / len(proxyList) - 0.5 >= 100:
				output_stream.write(prog+' Progress: '+str(100)+" %"+'\r')
				output_stream.flush()
			else:
				output_stream.write(prog+' Progress: '+str(float(progress*100) / len(proxyList) - 0.5)+" %"+'\r')
				output_stream.flush()	
		output_stream.write('\n')
	if __name__ == '__main__':
		main()
# ---- END OF BASE FUNCTIONS ----

logo = ("""
   ___          _____    __  __            
  / _ \_____ __/ ______ / /_/ /____ ____   
 / ___/ __\ \ / (_ / -_/ __/ __/ -_/ __/   
/_/  /_/ /_\_\\\___/\__/\__/\__/\__/_/      

""")

def parse_error(errmsg):
	print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
	print(bad + "[-] " + errmsg)
	sys.exit(1)

def parse_args():
	print (logo)
	parser = argparse.ArgumentParser(epilog="\tExample: \r\npython " + sys.argv[0] + " -t/-s http://proxysource.com/-i file.txt")
	parser.error = parse_error
	parser._optionals.title = "OPTIONS"
	parser.add_argument("-t", "--tunnel", help="check proxies from httptunnel.ge", action="store_true", default=False)
	parser.add_argument("-s", "--source", help="check proxies from other source", action='store', dest='source_url', default=None)
	parser.add_argument("-i", "--input", help="check proxies from local file", action="store", dest="source_file", default=None)
	parser.add_argument("-l", "--limit",required=False, type=int, help="limit of proxies to scrape", default=100)
	return parser.parse_args()

def mode1():
	try:
		site  = r.get("http://www.httptunnel.ge/ProxyListForFree.aspx")
		data = site.text
		# -- START OF BEAUTIFUL SOUP CONSTRUCTOR --
		features="html.parser"
		soup = BeautifulSoup(data,features)
		# -- END OF BEAUTIFUL SOUP CONSTRUCTOR --
		proxy_list = []
		print("\n" + info + "Proxies loaded.")
		for link in soup.find_all('a'):
			all_hrefs = link.get('href')
			if "ProxyChecker" in all_hrefs:
				good_line = all_hrefs.split("?p=")
				if len(good_line) > 1:
					try:
						if len(proxy_list) == args.limit:
							output_name = "output "+(DT.strftime("%Y-%m-%d %H%M"))+".txt"
							CheckProxies(proxy_list,output_name)
							break
						else:
							proxy_list.append(good_line[1])
							continue
					except KeyboardInterrupt:
						if sys.version_info[0] == 3:
							answer = input(info + ' are you sure you want to exit? y/n: ').strip().lower()
						else:
							answer = raw_input(info + ' are you sure you want to exit? y/n: ').strip().lower()
							
						if answer == "yes" or answer == "y":
							sys.exit(0)
						elif answer == "no" or answer == "n":
							continue

	except r.exceptions.RequestException as e:
		print(bad + e + "Is HTTPTunnel.ge offline?")
	


def mode2(source_url):
	if "://" not in source_url:
		source_url = "http://"+source_url
	try:
		site = r.get(source_url)
		data = site.text
	except:
		print(bad + " An error has been encountered.")
	else:
		proxie_expression = r"((?:\d{1,3}\.){3}\d{1,3}):(\d+)" # RegEx to match any proxie.
		matches = re.findall(proxie_expression,data)
		good_list = []
		if len(matches) > 1:
			for match in matches:
				proxy_ip = str(match[0])+":"+str(match[1])
				good_list.append(proxy_ip)
			output_name = "output"+(DT.strftime("%Y-%m-%d-%H%M"))+".txt"
			print("\n" + info + "Proxies loaded.")
			print(good + " Output saved on "+output_name+"\n" + que + " Checking proxies. This might take a while . . .")
			CheckProxies(good_list,output_name)
		else:
			ip_expression = r"((?:\d{1,3}\.){3}\d{1,3})"
			matches2 = re.findall(ip_expression,data)
			if len(matches2) > 1:
				for match in matches2:
					proxy_ip1 = str(match)+":"+"8080"
					proxy_ip2 = str(match)+":"+"3128"
					proxy_ip3 = str(match)+":"+"80"
					good_list.append(proxy_ip1)
					good_list.append(proxy_ip2)
					good_list.append(proxy_ip3)
				output_name = "output"+(DT.strftime("%Y-%m-%d-%H%M"))+".txt"
				print(good + " Output saved on "+output_name+"\n" + que + " Checking proxies. This might take a while . . .")
				CheckProxies(good_list,output_name)
			else:
				print(bad + " No proxies found in the source.")

def mode3(source_file):
	try:
		file_content = read_file(source_file)
		list_ = find_proxies(file_content)
		if len(list_) == 0:
			print(bad + " No proxies")
		else:
			output_name = "output"+(DT.strftime("%Y-%m-%d-%H%M"))+".txt"
			print(info + " Proxies loaded")
			CheckProxies(list_,output_name) 
	except IOError:
			print(bad + "File not found. Please verify the file name")

				

if __name__=="__main__":
	DT = datetime.datetime.now()
	try:
		args = parse_args()
		if args.tunnel == True:
			mode1()
		elif args.source_url != None:
			mode2(args.source_url)
		elif args.source_file != None:
			mode3(args.source_file)
		else:
			print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
			print (bad + " too few arguments")
			exit(0)
	except KeyboardInterrupt:
		print ("\n" * 80)
		if 'win' in sys.platform:
			os.system('cls')
		else:
			os.system('clear')
		print (logo)
		print(yellow + " ~ Successful Exit")
		exit(0)
