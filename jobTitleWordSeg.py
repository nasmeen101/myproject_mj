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
collectionJobTitleWord = db["jobTitleWord"]

# get rows number
allRowsNum = collectionJobList.count_documents({})

custom_words_list = set(thai_words())
## add multiple words
custom_words_list.update(customWords)
## add word
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)
#custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm')

# travel through all rows
jobPerLoop  = 50
jobNum      = 1
for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
    jobs = collectionJobList.find({},None,currSet*jobPerLoop,jobPerLoop)
    for job in jobs:
        #print( job["jobTitle"],"\n")
        #print("no whitespace:", word_tokenize(job["jobTitle"], keep_whitespace=False))
        #print("custom :", custom_tokenizer.word_tokenize(job["jobTitle"], keep_whitespace=False))
        wordSeq = 1
        jobTitleWords = custom_tokenizer.word_tokenize(job["jobTitle"])
        for jobTitleWord in jobTitleWords:
            #print(wordSeq," ", jobTitleWord)
            # skip duplicate word
            if collectionJobTitleWord.count_documents({"jobId":job["jobId"],"word":jobTitleWord})!=0:
                continue
            # add only new word found
            wordSeq = wordSeq+1
            word = {
                "jobId"     : job["jobId"],
                "word"      : jobTitleWord,
                "seqNum"    : wordSeq,
                "timestamp" : datetime.today().replace(microsecond=0)
            }
            collectionJobTitleWord.insert_one(word)
        if(jobNum%100)==0:
            print(jobNum, end =" ")
            print(" segmented and added to db")
            #print(jobTitleWords, " segmented and added to db")
        jobNum = jobNum+1
        #print("custom :", custom_tokenizer.word_tokenize(job["jobTitle"]))
    # print("\n")
    # if currSet==25:
    #     break
# text = "???????????????????????????????????????????????????????????????????????????????????????????????????????????????    i am a book    ???????????????????????????????????????????????????????????????????????????????????????????????????????????????"
# print("sent_tokenize:", sent_tokenize(text))
# print("word_tokenize:", word_tokenize(text))
# print("no whitespace:", word_tokenize(text, keep_whitespace=False))
