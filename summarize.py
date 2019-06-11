from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import youtube_dl
import os
import glob
from sys import argv
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import speech_recognition as sr

LANGUAGE = "english"
SENTENCES_COUNT = 10

download_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'nocheckcertificate': True,
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'wav',
	}],
}

with youtube_dl.YoutubeDL(download_options) as dl:
	dl.download([argv[1]])

r = sr.Recognizer()
print('\nTranscribing audio...')
myFiles = glob.glob("./*.wav")
with sr.AudioFile(myFiles[0]) as source:
	audio = r.record(source)
	print('\nRecognized text:\n' + r.recognize_sphinx(audio))
	with open("transcript.txt", "w") as text_file:
		text_file.write(r.recognize_sphinx(audio))

print('\nSummarizing from transcript...')
parser = PlaintextParser.from_file("./transcript.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

with open("./result.txt", "w") as text_file:
	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		print(sentence)
		# text_file.write(sentence)

print('\nDone.')