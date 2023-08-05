"""
dload - Download Library

A python library to simplify your download tasks.
~~~~~~~~~~~~~~~~~~~~~
"""

import os, sys, time
from contextlib import closing
from shutil import copyfileobj
import urllib.request as request
import zipfile

def check_installation(rv):
	"""
	checks if current python version is correct to run this module
	:param rv: string - python version, i.e. check_installation(36)
	:return: boolean
	"""
	current_version = sys.version_info
	if current_version.major == int(rv[0]) and current_version.minor >= int(rv[1]):
		return True
	else:
		sys.stderr.write( "[%s] - Error: Your Python interpreter must be %s.%s or greater (within major version %s)\n" % (sys.argv[0], rv[0], rv[1], rv[0]) )
		sys.exit(-1)
	return False


check_installation("36")

import traceback, io
from urllib.parse import urlparse

try:
	import requests
except Exception:
	print ("'requests' is required.")

def bytes(url):
	"""
	Returns the remote file as a byte obj
	:param url: str - url to download
	:return: bytes
	"""
	try:
		return requests.get(url).content
	except:
		pass
		print(traceback.print_exc())
		return b""

def rand_fn():
	"""
	provides a random filename when it's impossible to determine the filename, i.e.: http://site.tld/dir/
	:return: str
	"""
	return str(int(time.time()))[:5]

def save(url, path=""):
	"""
	Download and save a remote file
	:param url: str - file url to download
	:param path: str - Full path to save the file, ex: c:/test.txt or /home/test.txt.
	Defaults to script location and url filename. http, https and ftp schemes supported
	:return: str - The full path of the downloaded file
	"""

	try:
		namespace = sys._getframe(1).f_globals  # caller's globals
		c_path = os.path.dirname(namespace['__file__'])
		fn = os.path.basename(urlparse(url).path)
		fn = fn if fn else f"dload{rand_fn()}"
		r = requests.get(url)
		path = path if path.strip() else c_path+os.path.sep+fn
		with open(path, 'wb') as f:
			f.write(r.content)
		return path
	except:
		pass
		print(traceback.print_exc())
		return ""

def text(url, encoding=""):
	"""
	Returns the remote file as a string
	:param url: str - url to retrieve the text content
	:param encoding: str - character encoding
	:return: str
	"""
	try:
		r = requests.get(url)
		if encoding:
			r.encoding = encoding
		return r.text
	except:
		print(traceback.print_exc())
		pass
		return ""

def json(url):
	"""
	Returns the remote file as a dict
	:param url: str - url to retrieve the json
	:return: dict
	"""
	try:
		return requests.get(url).json()
	except:
		print(traceback.print_exc())
		pass
		return {}


def headers(url, redirect=True):
	"""
	Returns the reply headers as a dict
	:param url: str - url to retrieve the reply headers
	:param redirect: boolean - should we follow redirects?
	:return: dict
	"""
	try:
		return dict(requests.head(url, allow_redirects=redirect).headers)
	except:
		print(traceback.print_exc())
		pass
		return {}


def ftp(ftp_url, localpath=""):
	"""
	Download and save an FTP file
	:param url: str - ftp://ftp.server.tld/path/to/file.ext or ftp://username:password@ftp.server.tld/path/to/file.ext
	:param localpath: str - local path to save the file, i.e.: /home/myfile.ext or c:/myfile.ext
	:return: str - local path of the downloaded file
	"""

	try:
		namespace = sys._getframe(1).f_globals  # caller's globals
		c_path = os.path.dirname(namespace['__file__'])
		fn = os.path.basename(urlparse(ftp_url).path)
		fn = fn if fn else f"dload{rand_fn()}"
		localpath = localpath if localpath.strip() else c_path+os.path.sep+fn
		with closing(request.urlopen(ftp_url)) as r:
			with open(localpath, 'wb') as f:
				copyfileobj(r, f)
				return localpath
	except:
		print(traceback.print_exc())
		pass
		return ""



def save_multi(url_list, dir="", max_threads=1, tsleep=0.05):
	"""
	Multi threaded file downloader
	:param url_list: str or list - A python list or a path to a text file containing the urls to be downloaded
	:param dir: str - Directory to save the files, will be created if it doesn't exist
	:param max_threads: int - Max number of parallel downloads
	:param tsleep: int - time to sleep in seconds when the max_threads value is reached
	:return: boolean
	"""
	import threading
	from time import sleep
	try:
		if not isinstance(url_list, list):
			with open(url_list) as f:
				url_list = [x.rstrip() for x in f if x]

		if dir:
			if not os.path.exists(dir):
				from pathlib import Path
				Path(dir).mkdir(parents=True, exist_ok=True)

		for url in url_list:
			if dir:
				fn = os.path.basename(urlparse(url).path)
				fp = f"{dir}/{fn}"
				args = [url, fp]
			else:
				args = [url]


			threading.Thread(target=save, args=args, name="dload" ).start()
			dload_threads = [x.getName() for x in threading.enumerate() if "dload" == x.getName()]
			while len(dload_threads) >= max_threads:
				dload_threads = [x.getName() for x in threading.enumerate() if "dload" == x.getName()]
				sleep(tsleep)

		while dload_threads:
			dload_threads = [x.getName() for x in threading.enumerate() if "dload" == x.getName()]
			sleep(tsleep)
		return True
	except:
		pass
		print(traceback.print_exc())
		return False


def down_speed(size=5, ipv="ipv4", port=80):
	"""
	Measures the download speed
	:param size: int -  5, 10, 20, 50, 100, 200, 512, 1024 Mb
	:param ipv: str - ipv4, ipv6
	:param port: int - 80, 81, 8080
	:return: boolean
	"""

	if size == 1024:
		size = "1GB"
	else:
		size = f"{size}MB"

	url = f"http://{ipv}.download.thinkbroadband.com:{port}/{size}.zip"

	with io.BytesIO() as f:
		start = time.clock()
		r = requests.get(url, stream=True)
		total_length = r.headers.get('content-length')
		dl = 0
		if total_length is None: # no content length header
			f.write(r.content)
		else:
			for chunk in r.iter_content(1024):
				dl += len(chunk)
				f.write(chunk)
				done = int(30 * dl / int(total_length))
				sys.stdout.write("\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30-done), dl//(time.clock() - start) / 100000))

	print( f"\n{size} = {(time.clock() - start):.2f} seconds")


def save_unzip(zip_url, extract_path="", delete_after=False):
	"""
	Save and Extract a remote zip
	:param zip_url: the zip file url to download
	:param extract_path: the path to extract the zip file, defaults to local dir
	:param delete_after: if the zip file should be deleted after, defaults to False
	:return: str the extract path or an empty string
	"""
	try:
		namespace = sys._getframe(1).f_globals  # caller's globals
		c_path = os.path.dirname(namespace['__file__'])
		fn = os.path.basename(urlparse(zip_url).path)
		fn = fn if fn.strip() else f"dload{rand_fn()}"
		zip_path = save(zip_url, f"{c_path}/{fn}")
		folder = os.path.splitext(fn)[0]
		extract_path = extract_path if extract_path.strip() else c_path+os.path.sep+folder
		with zipfile.ZipFile(zip_path, 'r') as zip_ref:
			zip_ref.extractall(extract_path)
		if delete_after and os.path.isfile(zip_path):
			os.remove(zip_path)
		return extract_path
	except:
		pass
		print(traceback.print_exc())
	return ""
