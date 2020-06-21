import urllib.request
import chardet
import os


from imp_lexer import *
from prsr import *

encoding = [
'utf-8',
'windows-1251',
]

def parserHTML(filename):
	characters = None
	if filename:
		if 'http' in filename:
			try:
				f = urllib.request.urlopen(filename, timeout=10)

				characters = f.read()
				result_code = chardet.detect(characters)
				characters = characters.decode(result_code['encoding'])
			except (TimeoutError, urllib.error.URLError):
				print("\n\033[41m{}\033[40m\n".format("Parsed not completed! Invalid URL!"))
				return None
		else:
			for enc in encoding:
				try:
					file = open(filename, encoding=enc)
					characters = file.read()
					file.close()
				except (UnicodeDecodeError, LookupError):
					print("\n\033[41m{}\033[40m\n".format("Parsed not completed! Invalid Encoding!"))
					return None
				else:
					break
	document = ""
	if characters:
		tokens = imp_lex(characters) #лексируем файл
		if tokens:
			document = parser(tokens) #парсируем файл
	# for token in tokens:
		# print (token)
	if document != "":
		return document
	print("\n\033[41m{}\033[40m\n".format("Parsed not completed! Invalid File!"))
	return None
