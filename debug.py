# jobDetail word segmentation
from pythainlp import sent_tokenize
from pythainlp import word_tokenize, Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words
from connectMongo import get_database
from customWords import customWords
import math
from datetime import datetime

# connect db
db = get_database()
collectionJobList = db["jobList"]
collectionJobDetailWord = db["jobDetailWord"]

print( collectionJobDetailWord.find_one( {"jobId":'1201758'},{'seqNum':1,'_id':0} ) is None )
