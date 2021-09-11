from pythainlp import sent_tokenize
from pythainlp import word_tokenize, Tokenizer
from pythainlp.util import dict_trie
from pythainlp.corpus.common import thai_words
from connectMongo import get_database
from customWords import customWords
import math

# connect db
db = get_database()
collectionJobList = db["jobList"]
collectionJobDetailWord = db["jobDetailWord"]

# get rows number
allRowsNum = collectionJobList.count_documents({})


custom_words_list = set(thai_words())
## add multiple technical words
custom_words_list.update(customWords)
## add technical words
trie = dict_trie(dict_source=custom_words_list)
custom_tokenizer = Tokenizer(custom_dict=trie, engine='newmm', keep_whitespace=False)

# travel through all rows
jobPerLoop  = 50    # 50 rows per loop
jobNum      = 1
for currSet in range( math.ceil(allRowsNum/jobPerLoop) ):
    # find find(
    #           {}->select all ,
    #           None, 
    #           currSet*jobPerLoop->skip from first ,
    #           jobPerLoopall->limit per query 
    jobs = collectionJobList.find({},None,currSet*jobPerLoop,jobPerLoop)
    for job in jobs:
        wordSeq = 1
        jobDetailWords = custom_tokenizer.word_tokenize(job["jobDetail"])
        for jobDetailWord in jobDetailWords:
            wordSeq = wordSeq+1
            word = {
                "jobId" : job["jobId"],
                "wordJobDetail"  : jobDetailWord,
                "seqNum": wordSeq
            }
            collectionJobDetailWord.insert_one(word)
        print(jobNum,  "added")
        #print(jobTitleWords, " segmented and added to db")
        jobNum = jobNum+1
