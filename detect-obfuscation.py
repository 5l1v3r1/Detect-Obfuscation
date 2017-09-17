import sys
import math

unknown_transition_prob = 0.000001
BASE = float(2)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class table:
	def __init__(self):
		self.body = {}

	def get_keys(self):
		return self.body.keys()

	def merge_letters(self,ngram,letters):
		letters_keys = letters.get_keys()
		for key in letters_keys:
			self.body[ngram].update(key,letters.get(key))

	def add(self,ngram,letters):
		keys = self.get_keys()
		if ngram in keys:
			self.merge_letters(ngram,letters)
		else:
			self.body[ngram] = letters

	def calculate(self):
		for key in self.get_keys():
			self.body[key].calculate()

	def get_probability(self,ngram,letter):
		try:
			return self.body[ngram].get(letter)
		except Exception as e:
			return unknown_transition_prob

	def print_table(self):
		for key in self.get_keys():
			print key
			self.body[key].print_letters()

class letters:
	def __init__(self):
		self.body = {}

	def get(self,key):
		return self.body[key]

	def get_keys(self):
		return self.body.keys()

	def update(self,letter,num):
		keys = self.get_keys()
		if letter in keys:
			self.body[letter] += num
		else:
			self.body[letter] = 1

	def add(self,letter):
		keys = self.get_keys()
		if letter in keys:
			self.body[letter] += 1
		else:
			self.body[letter] = 1

	def calculate(self):
		acc = 0
		keys = self.get_keys()
		for key in keys:
			acc += self.body[key]

		for key in keys:
			self.body[key] = (float(self.body[key]) / float(acc))

	def print_letters(self):
		print self.body

def read_text(filename):

	with open(filename) as f: lines = [line.rstrip('\n') for line in f]
	words = set()
	for line in lines:
		words.add(line)
	return words

def build_model(filename,t):
	words = read_text(filename)
	create_table(words,t)

def create_ngram(n,string):
	size = len(string)
	step = n - 1
	ngrams = []
	ngrams_ = {}
	for i in range(0,size-step):
		ngram = ""
		for j in range(i,i+n):
			ngram += string[j]
		ngrams.append(ngram)
	for i in range(len(ngrams)-1):
		ngrams_[ngrams[i]] = ngrams[i+1][n-1]
	return ngrams_

def create_table(words,t):
	N = 2
	for word in words:
		ngrams = create_ngram(N,word)
		for key in ngrams.keys():
			l = letters()
			l.add(ngrams[key])
			t.add(key,l)

def calculate_probability(word,t):
	N=2
	sum_prob = 0
	ngrams = create_ngram(N,word)
	for key in ngrams.keys():
		ngram = key
		letter = ngrams[key]
		prob = t.get_probability(key,ngrams[key])
		sum_prob += math.log(prob,BASE)
	if get_evaluation_factor(word) >= sum_prob:
		return {"status":False,"eval":get_evaluation_factor(word),"prob":sum_prob,"text":word}
	else:
		return {"status":True,"eval":get_evaluation_factor(word),"prob":sum_prob,"text":word}

def get_evaluation_factor(word):
	if len(word) > 2000:
		return (len(word) / 2) * (math.log(unknown_transition_prob,BASE) / 8)
	else:	
		return len(word) * (math.log(unknown_transition_prob,BASE) / 8)

t = table()
build_model("corpus",t)
t.calculate()

file = open("test","r")
for line in file:
	line = line.replace("\n","")
	line = " ".join(line.split())
	result = calculate_probability(line,t)
	if result["status"]:
		print bcolors.WARNING + result["text"] + bcolors.ENDC + bcolors.BOLD + bcolors.OKBLUE + " seems legit" + bcolors.ENDC
	else:
		print bcolors.WARNING + result["text"] + bcolors.ENDC + bcolors.BOLD + bcolors.FAIL + " seems obfuscated" + bcolors.ENDC
	print "String length: " + str(len(line))
	print "Probability: " + str(result["prob"]) 
	print "Evaluation Value: " + str(result["eval"])
	print "-------------------------------------------------"
file.close()
