# PrxGetter

This project was built with the purpose of saving time when searching for proxies. Using this tool you can scrape and check proxies easily. 

Here's what PrxGetter looks in action.

```
$ python PrxGetter.py --tunnel

   ___          _____    __  __
  / _ \_____ __/ ______ / /_/ /____ ____
 / ___/ __\ \ / (_ / -_/ __/ __/ -_/ __/
/_/  /_/ /_\_\\___/\__/\__/\__/\__/_/


[+]Output saved on output 2019-06-07 1451.txt
[*]Checking proxies. This might take a while . . .
[+]222.110.147.50:3128 - Working
[+]157.230.212.164:80 - Working
[+]62.33.207.202:80 - Working
[+]35.158.114.186:3128 - Not Working
[+]203.246.112.133:3128 - Working
[+]185.62.190.60:8080 - Working
[+]116.202.43.228:3128 - Working
[+]94.242.59.135:10010 - Working
[+]13.56.2.56:8090 - Working
[+]62.33.207.201:80 - Working
[+]142.4.204.85:8080 - Working
[+]80.211.36.44:3128 - Not Working

```

## Setup

1) Clone the repository

```
$ git clone https://github.com/hohohoesmad/PrxGetter.git
```

2) Install the dependencies

```
$ cd PrxGetter
$ pip install -r requirements.txt
```

3) Run PrxGetter (see [Usage](#usage) below for more detail)

```
$ python PrxGetter.py -t
```

## Usage

```
$ python PrxGetter.py --help

   ___          _____    __  __
  / _ \_____ __/ ______ / /_/ /____ ____
 / ___/ __\ \ / (_ / -_/ __/ __/ -_/ __/
/_/  /_/ /_\_\\___/\__/\__/\__/\__/_/


usage: PrxGetter.py [-h] [-t] [-s SOURCE_URL] [-i SOURCE_FILE]

OPTIONS:
  -h, --help            show this help message and exit
  -t, --tunnel          check proxies from httptunnel.ge
  -s SOURCE_URL, --source SOURCE_URL
                        check proxies from other source
  -i SOURCE_FILE, --input SOURCE_FILE
                        check proxies from local file

Example: python PrxGetter.py -t/-s http://proxysource.com/-i file.txt

```

## Compatibility

Tested on Python 2.7 on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

[open an issue]: https://github.com/hohohoesmad/PrxGetter/issues/new