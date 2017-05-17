import sys
import threading
import queue
import urllib.request,urllib.parse

threads = 10

# wordlist_file = "/home/yang/url.txt"
resume = None
headers = {}
exten_d = [".php",".bak",".zip",".inc"]
try:
	target_url = sys.argv[1]
	wordlist_file= sys.argv[2]
except:
	print("please check the syntax ! like:\n python bruteurl.py http://www.xxx.com /root/filename.txt")
	exit()
try:
	extensions = [sys.argv[3]]+exten_d
	# print(extensions)
except:
	extensions = exten_d
	pass


def build_wordlist(wordlist_file):
	fd = open(wordlist_file,"r")
	raw_words = fd.readlines()
	fd.close()

	found_resume = False
	words = queue.Queue()
	for word in raw_words:
		word = word.strip()
		if resume is not None:
			if found_resume:
				words.put(word)
			else:
				if word == resume:
					found_resume = True 
					print ("resuming wordlist from %s"%resume)
		else:
			words.put(word)
	return words

def dir_bruter(word_queue,extensions=None):
	while not word_queue.empty():
		attemt = word_queue.get()
		attemt_list = []
		if "." not in attemt:
			attemt_list.append("/%s/"%attemt)
			if extensions:
				for extension in extensions:
					attemt_list.append("/%s%s"%(attemt,extension))
		else:
			attemt_list.append("/%s"%attemt)
		# print(attemt_list)
		for brute in attemt_list:
			url = "%s%s"%(target_url,urllib.parse.quote(brute))
			try:
				request = urllib.request.Request(url,headers=headers)
				res=urllib.request.urlopen(request)

				print("found===>"+url)
			except urllib.error.HTTPError as error:
				if error.code>404:
					print(error.code,url)
				# print(error.code,url)
				pass



word_queue = build_wordlist(wordlist_file)


for i in range(threads):
	t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
	t.start()
